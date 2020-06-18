import os

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print path+' 创建成功'
        return True
    else:
        print path+' 目录已存在'
        return False
 
# 定义要创建的目录
mkpath=""
# 调用函数
mkdir(mkpath)