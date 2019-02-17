#coding=utf-8
import os,time
from PIL import (Image, ImageGrab)

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    UnexpectedAlertPresentException
)
from lib.scripts import (
    getYamlfield,
    Replay,
    hightlightConfig
)
from lib import gl


'''
basepage封装所有公共方法
'''
class BasePage(object):
    """PO公共方法类"""
    def __init__(self,baseurl,driver,pagetitle):
        """
        初始化,driver对象及数据
        :param baseurl: 目标地址
        :param driver: webdriver对象
        :param pagetitle: 用来断言的目标页标题
        """
        self.base_url = baseurl
        self.driver = driver
        self.pagetitle = pagetitle

    '''
    功能描述：所有公共方法，都写在以下
    '''



    #打开浏览器
    # 打开浏览器
    def _open(self, url):
        """
        打开浏览器，并断言标题
        :param url: 目标地址
        :return: 无
        """
        self.driver.maximize_window()
        self.driver.get(url)

        self.driver.implicitly_wait(10)
        self.getImage()
        self.driver.implicitly_wait(0)





    def is_display_timeout(self, element):
        """
        在指定时间内，轮询元素是否显示
        :param element: 元素对象
        :param timeSes: 轮询时间
        :return: bool
        """

        if element.is_displayed() and element.is_enabled():
            return True
        else:
            raise ElementNotVisibleException(msg='当前元素未显示或置灰状态')


    def find_element(self, *loc):
        """
        在指定时间内，查找元素；否则抛出异常
        :param loc: 定位器
        :return: 元素 或 抛出异常
        """
        timeout = 10
        start_time = int(time.time()) #秒级时间戳
        raise_ex = ''
        while (int(time.time())-start_time) < timeout:
            try:
                element = self.driver.find_element(*loc) #如果element没有找到，到此处会开始等待
                if self.is_display_timeout(element):
                    self.hightlight(element)  #高亮显示
                    return element
            except (NoSuchElementException,ElementNotVisibleException,UnexpectedAlertPresentException) as ex:
                raise_ex = ex

        self.getImage()
        raise Exception(raise_ex)




    @hightlightConfig('HightLight')
    def hightlight(self,element):
        """
        元素高亮显示
        :param element: 元素对象
        :return: 无
        """
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                   element, "border: 2px solid red;")


    def getElementImage(self,element):
        """
        截图,指定元素图片
        :param element: 元素对象
        :return: 无
        """
        """图片路径"""
        timestrmap = time.strftime('%Y%m%d_%H.%M.%S')
        imgPath = os.path.join(gl.imgPath, '%s.png' % str(timestrmap))

        """截图，获取元素坐标"""
        self.driver.save_screenshot(imgPath)
        left = element.location['x']
        top = element.location['y']
        elementWidth = left + element.size['width']
        elementHeight = top + element.size['height']

        picture = Image.open(imgPath)
        picture = picture.crop((left, top, elementWidth, elementHeight))
        timestrmap = time.strftime('%Y%m%d_%H.%M.%S')
        imgPath = os.path.join(gl.imgPath, '%s.png' % str(timestrmap))
        picture.save(imgPath)
        print('screenshot:', timestrmap, '.png')


    def getImage(self, option=0):
        '''
        截取图片,并保存在images文件夹
        :return: 无
        '''
        if not os.path.exists(gl.imgPath):
            os.mkdir(gl.imgPath)

        timestrmap = time.strftime('%Y%m%d_%H.%M.%S')
        imgPath = os.path.join(gl.imgPath, '%s.png' % str(timestrmap))

        try:
            self.driver.save_screenshot(imgPath)
        except:
            img = ImageGrab.grab()
            img.save(imgPath)
            img.close()
        print('screenshot:', timestrmap, '.png')




    def find_elements(self,*loc):
        '''批量找标签'''
        TimeOut = 20 #智能等待时间
        raise_ex = ''
        start_time = int(time.time())
        while int(time.time()) - start_time < TimeOut:
            try:
                self.driver.implicitly_wait(TimeOut) #智能等待；此贯穿self.driver整个生命周期
                elements = self.driver.find_elements(*loc)
                #元素高亮显示
                for e in elements:
                    self.hightlight(e)

                self.driver.implicitly_wait(0) #恢复等待
                return elements

            except (NoSuchElementException, ElementNotVisibleException,UnexpectedAlertPresentException) as ex:
                raise_ex = ex
        self.getImage()
        raise Exception(ex)




    def iterClick(self, *loc):
        '''批量点击某元素'''
        element = self.find_elements(*loc)
        for e in element:
            e.click()


    def iterInput(self,text=[],*loc):
        """
        批量输入
        :param text: 输入内容
        :param loc: 定位器(By.XPATH,'//*[@id='xxxx']/input')
        :return: 无
        """
        elements = self.find_elements(*loc)
        for i,e in enumerate(elements):
            self.wait(1000)
            #e.clear()
            e.send_keys(text[i])


    #文本框输入
    def send_keys(self,content,*loc):
        '''
        :param content: 文本内容
        :param itype: 如果等1，先清空文本框再输入。否则不清空直接输入
        :param loc: 文本框location定位器
        :return:
        '''
        inputElement = self.find_element(*loc)
        #inputElement.clear()
        inputElement.send_keys(content)

    def clearInputText(self,desc ,*loc):
        '''清除文本框内容'''
        if desc != "%NONE%":
            print('清除{}:{}'.format(desc, loc))
            self.find_element(*loc).clear()



    def add_cookies(self,ck_dict):
        '''
        增加cookies到浏览器
        :param ck_dict: cookies字典对象
        :return: 无
        '''
        for key in ck_dict.keys():
            self.driver.add_cookie({"name":key,"value":ck_dict[key]})

    def isExist(self,*loc):
        #isDisable
        '''
        元素存在,判断是否显示
        :param loc: 定位器
        :return: 元素存在并显示返回True;否则返回False
        '''
        TimeOut = 20
        try:
            self.driver.implicitly_wait(TimeOut)

            element = self.driver.find_element(*loc)
            if self.is_display_timeout(element):
                self.hightlight(element)
                return True
            else:
                return False
            self.driver.implicitly_wait(0)
        except (NoSuchElementException,ElementNotVisibleException,UnexpectedAlertPresentException) as ex:
            self.getImage() #10秒还未找到显示的元素
            return False




    def isOrNoExist(self,*loc):
        """
        判断元素,是否存在
        :param loc: 定位器(By.ID,'kw')
        :return: True 或 False
        """
        TimeOut = 60
        try:
            self.driver.implicitly_wait(TimeOut)
            e = self.driver.find_element(*loc)

            """高亮显示,定位元素"""
            self.hightlight(e)

            self.driver.implicitly_wait(0)
            return True
        except NoSuchElementException as ex:
            self.getImage() #10秒还未找到元素，截图
            return False


    def isExistAndClick(self,*loc):
        '''如果元素存在则单击,不存在则忽略'''
        print('Click:{0}'.format(loc))

        TimeOut = 3 #超时 时间
        try:
            self.driver.implicitly_wait(TimeOut)

            element = self.driver.find_element(*loc)
            self.hightlight(element)
            element.click()
            self.driver.implicitly_wait(0)
        except NoSuchElementException as ex:
            pass

    def isExistAndInput(self,text,*loc):
        '''如果元素存在则输入,不存在则忽略'''
        print('Input:{0}'.format(text))

        TimeOut = 3
        try:
            self.driver.implicitly_wait(TimeOut)

            element =self.driver.find_element(*loc)
            self.hightlight(element) #高亮显示
            element.send_keys(str(text).strip())

            self.driver.implicitly_wait(0)
        except (NoSuchElementException,ElementNotVisibleException,UnexpectedAlertPresentException) as ex:
            self.getImage()


    def getTagText(self,txtName,*loc):
        """
        获取元素对象属性值
        :param propertyName: 属性名称
        :param loc: #定位器
        :return: 属性值 或 raise
        """
        element = self.find_element(*loc)
        self.hightlight(element) #高亮显示
        #获取属性
        proValue = getattr(element,str(txtName))
        return proValue






    @property
    def switch_window(self):
        """
        切换window窗口,切换一次后退出
        :return: 无
        """
        curHandle = self.driver.current_window_handle
        allHandle = self.driver.window_handles
        for h in allHandle:
            if h != curHandle:
                self.driver.switch_to.window(h)
                break


    def wait(self,ms):
        """
        线程休眼时间
        :param ms: 毫秒
        :return: 无
        """
        ses = int(ms) / 1000
        time.sleep(ses)

    @Replay
    def jsClick(self,desc,*loc):
        """通过js注入的方式去，单击元素"""
        print('Click{}:{}'.format(desc,loc))
        element = self.find_element(*loc)
        self.driver.execute_script("arguments[0].click();",element)


    @Replay
    def inputText(self, text,desc, *loc):
        """输入文本操作"""
        if str(text).upper() != "%NONE%":
            print('Input{}:{}'.format(desc,text))
            self.send_keys(text, *loc)



    @Replay
    def click_button(self, desc,*loc):
        """点击操作"""
        if str(desc).upper() != "%NONE%":
            print('Click:{}{}'.format(desc,loc))
            ele = self.find_element(*loc)
            ActionChains(self.driver).move_to_element(ele).move_by_offset(5,5).click().perform()



    @Replay
    def click_btn_index(self, desc, index, *loc):
        """
        点击操作，按索引，适用于findelemens方法
        :param desc: 描述
        :param index: 点击索引
        :param op: 如果是True则，不执行点击操作，为False则点击
        :param loc: 定位器
        :return: 无
        """
        print('Clicks:{}{}'.format(desc, loc))
        if index == '%NONE%':
            pass
        else:
            ele = self.find_elements(*loc)[int(index)]
            # 元素高亮显示
            self.hightlight(ele)
            # 元素单击
            ActionChains(self.driver).move_to_element(ele).move_by_offset(5,5).click().perform()


    @Replay
    def selectTab(self,*loc):
        '''选择tab操作'''
        print('Select:{}'.format(loc))
        ele = self.find_element(*loc)
        ActionChains(self.driver).move_to_element(ele).move_by_offset(5,5).click().perform()


    @property
    def open(self):
        """打开浏览器，写入cookies登录信息"""
        yamldict = getYamlfield(gl.configFile)
        ck_dict = yamldict['CONFIG']['Cookies']['LoginCookies']
        self._open(self.base_url)
        self.add_cookies(ck_dict)
        self._open(self.base_url)
        if self.driver.title != self.pagetitle:
            self.getImage()
        assert self.driver.title == self.pagetitle, "断言标题错误,请查检页面"


    def selectComboxList(self,**kwargs):
        """根据索引选择下拉列表"""
        if 'loc' in kwargs:
            selectEle = self.find_element(*kwargs['loc'])
        else:
            self.getImage
            print('请传入loc定位器,以便定位')

        if 'desc' in kwargs:
            print('Select:{}'.format(kwargs['desc']))

        if 'index' in kwargs:
            Select(selectEle).select_by_index(kwargs['index'])
        elif 'value' in kwargs:
            Select(selectEle).select_by_value(kwargs['value'])
        elif 'text' in kwargs:
            Select(selectEle).select_by_visible_text(kwargs['text'])
        else:
            print('请传入,正确的选择方式,index or value or text')



if __name__=="__main__":
    ck_dict = {"pos_entry_number":"13522656892",
               "pos_entry_actualcard":"1726002880387638",
               "pos_bid":"2760627865",
               "pos_mid":"1134312064",
               "pos_sid":"3704059614",
               "pos_sign":"2a6ce62800f47551fd2826dab449b6cb"}

    #addCookies(ck_dict)


