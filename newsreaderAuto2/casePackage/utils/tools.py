# coding= utf-8

# from InnerToken import *
import shutil
import time
import urllib
import urllib2
import os
import base64
import json

import sys
import zipfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "..")))
import Utils.logger as logger
import requests
from apptool import adb_path
#from aip import AipOcrcr
# from module import set_timeout
# reload(sys)
# sys.setdefaultencoding('utf-8')
import constants

APP_ID = '14340077'
API_KEY = 'YTFMSmkbRCKz5wfD3dA4ncRL'
SECRET_KEY = 'K4Uj7VQ8U26Su3vWA9vPC3fXo4qBwB2i '
LOGGING = logger.get_logger(__name__)

imagePath = sys.path[0] + '/image/'
if not os.path.exists(imagePath):
    os.makedirs(imagePath)

# @set_timeout(5)
def getWords(image, with_pos = False):
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    if with_pos:
        response = aipOcr.general(image)
    else:
        response = aipOcr.basicGeneral(image)
    # p = InnerToken()
    # token = p.generateToken('9338386', '1884599608', 'BVNc7UiTCnMxPSzPDOKH5bcgpIrIb0G1')
    # url = 'http://inner.openapi.baidu.com/rest/2.0/vis-ocr/v1/ocr/general?access_token=' + token
    # data = {'image': image}
    # data = urllib.urlencode(data)
    # req = urllib2.Request(url, data)
    # response = urllib2.urlopen(req, timeout=10).read()
    return response

def getScreencap(name, device):
    image = os.path.join(imagePath, device.replace(':', '.') + name)
    os.system(adb_path() + ' -s ' + device + ' shell /system/bin/screencap -p /sdcard/screenshot.png')
    os.system(adb_path() + ' -s ' + device + ' pull /sdcard/screenshot.png ' + image)
    if not os.path.exists(image):
        return False
    return image

def get_window_size(device, name="get_window_size"):
    from PIL import Image
    img = Image.open(getScreencap(name, device))
    return img.size[0], img.size[1]

def find_text(text, file_name = None):
    with open(file_name, 'rb') as file:
        query = getWords(file.read())
    if not 'words_result' in query.keys():
        LOGGING.info('no words')
        return False
    for i in range(0, len(query['words_result'])):
        index = query['words_result'][i]['words'].encode("utf-8")
        if index.find(text) > -1:
            LOGGING.info('find word:' + text + " in " + index)
            return True
    LOGGING.info("didn't find word: " + text)
    return False

def find_text_with_pos(text, file_name=None):
    image_name = file_name.replace(':', '.') + '.png'
    image = getScreencap(image_name, file_name)
    if image:
        with open(image, 'rb') as file:
            query = getWords(file.read())
            # print jsonStr
            # query = json.loads(jsonStr)
        # file = open(image, 'rb')
        # imagebase = base64.b64encode(file.read())
        # file.close()

        # print json.dumps(query)
        if not 'words_result' in query.keys():
            print 'no words'
        for i in range(0, len(query['words_result'])):
            index = query['words_result'][i]['words'].encode("utf-8")
            if index.find(text) > -1:
                print index
                x = int(query['words_result'][i]['location']['left'])
                y = int(query['words_result'][i]['location']['top'])
                width = int(query['words_result'][i]['location']['width'])
                height = int(query['words_result'][i]['location']['height'])
                # return x + (width - 10), (y + height - 10)
                return x + width/2, y + height/2
    return None, None

def get_text_from_image(image, text):
    text = text.encode('utf-8')
    file = open(image, 'rb')
    imagebase = base64.b64encode(file.read())
    file.close()
    query = json.loads(getWords(imagebase))
    # print json.dumps(query)
    if not 'words_result' in query.keys():
        print 'no words'
        return False
    for i in range(0, len(query['words_result'])):
        index = query['words_result'][i]['words'].encode("utf-8")
        if index.find(text) > -1:
            print index
            x = int(query['words_result'][i]['location']['left'])
            y = int(query['words_result'][i]['location']['top'])
            width = int(query['words_result'][i]['location']['width'])
            height = int(query['words_result'][i]['location']['height'])
            return x + (width - 10), (y + height - 10)
    return False

def get_nid_list_from_image(image, text_list):
    file = open(image, 'rb')
    imagebase = base64.b64encode(file.read())
    file.close()
    query = json.loads(getWords(imagebase))
    if not 'words_result' in query.keys():
        print 'no words'
        return False
    result = {}
    for i in range(0, len(query['words_result'])):
        index = query['words_result'][i]['words'].encode("utf-8")
        for text in text_list:
            text = text.encode('utf-8')
            if index.find(text) > -1:
                print index
                x = int(query['words_result'][i]['location']['left'])
                y = int(query['words_result'][i]['location']['top'])
                if x > 300 and len(query['words_result'][i+1]['words'].encode("utf-8")) < 4:
                    try:
                        index = index + str(int(query['words_result'][i+1]['words'].encode("utf-8")))
                    except:
                        pass
                result.update({
                    text + '_' + index.split(text)[-1]: {
                        'left': x,
                        'top': y
                    }
                })
    return result

def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

def generateZip(source_dir, output_filename):
    newZip = zipfile.ZipFile(output_filename, "w")
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            if 'mp4' not in filename:
                pathfile = os.path.join(parent, filename)
                newZip.write(pathfile, filename)
    newZip.close()

def copyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!"%(srcfile)
    else:
        fpath, fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        LOGGING.info("copy %s -> %s"%( srcfile,dstfile))

def downloadApp(apk_url, buildId):
    LOGGING.info("download apk via url: " + apk_url)
    r = requests.get(apk_url)  # create HTTP response object
    LOGGING.info("download finished: " + apk_url)
    apk_name = buildId + ".apk"
    with open(apk_name, 'wb') as f:
        f.write(r.content)
        f.flush()
        f.close()
    return str(os.path.join(os.getcwd(), apk_name))

def uploadFile(url, files, values):
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    response = s.post(url, files = files, data = values)
    return response

if __name__ == "__main__":
    # print generateZip("D:\\Users\\zhaoyuting\\auto\\XPU4C17112010268\\performance\\biz\\XPU4C17112010268_netease_shipin_shouzhen_20181104_145604", "D:\\Users\\2018_1.zip")

    # file = {'file': open("D:\\Users\\zhaoyuting\\auto\\uploads\\20181107125805_biz_0_XPU4C17112010268_toutiao_coldstart_20181107-125821.zip", 'rb')}
    # values = {'type': 'biz'}
    # response = uploadFile(constants.UPLOAD_FILE_URL, file, values)
    # print response.status_code
    # print response.text
    nums = ['20190124144147']
    for thisnum in nums:
        payload = {'type': 'biz', 'status': 'done', 'batchId': thisnum}
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        response = s.get(constants.INFORM_SUCCESS_URL, params=payload)
        print response.status_code
        LOGGING.info("a" + str(response.status_code))

