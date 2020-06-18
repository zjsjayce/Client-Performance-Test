class Element(object):
    def __init__(self, driver, original_element):
        self.driver = driver
        self.original_element = original_element
        self.x, self.y = self.element_point()
        self.text = self.original_element.text

    def click(self):
        # self.driver.tap([(self.x, self.y)], 30)
        self.driver.tap([(self.x, self.y)])
    # def text(self):
    #     if not self.text:
    #         self.text = self.original_element.text
    #     return self.text

    def element_point(self):
        start_x = int(self.original_element.location['x'])
        start_y = int(self.original_element.location['y'])
        width = int(self.original_element.size.get('width'))
        height = int(self.original_element.size.get('height'))
        x = start_x + width / 2
        y = start_y + height / 2
        return x, y