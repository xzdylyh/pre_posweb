#coding=utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from pos.lib import scripts,gl
import time,os

class BjPrintPage(basepage.BasePage):
    """班结小票打印,页"""

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>定位器<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    # 首页,班结小票打印连接
    bjPrintLink_loc = (By.XPATH,'//*[@id="header-navbar-collapse"]/ul/li[3]/a')
    bjPrintLinkText_loc = (By.LINK_TEXT,'打印班结小票')
    # 打印小票,开始时间
    bjPrintStartDate_loc = (By.ID,'inputDateStart')
    # 打印班结小票,结束时间
    bjPrintEndDate_loc = (By.ID,'inputDateEnd')
    # 打印按钮
    bjPrintBtn_loc = (By.XPATH,'/html/body/div[2]/div/div/div[2]/form/div[2]/div/a[1]')
    #弹出的打印按钮
    bjPrintPopBtn_loc =(By.XPATH,'//*[@id="print-header"]/div/button[1]')
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>结束<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#

    @property
    def clickPrintLink(self):
        '''单击班结小票打印链接'''
        self.clickBtn('班结小票打印',*(self.bjPrintLink_loc))

    @property
    def clickPrintLinkText(self):
        """单击打印班结小票打印链接"""
        self.clickBtn('班结小票打印',*(self.bjPrintLinkText_loc))

    @property
    def inputStartTime(self,text):
        '''输入打印开始时间'''
        self.inputText(text,'开始时间',*(self.bjPrintStartDate_loc))

    @property
    def inputEndTime(self,text):
        '''输入打印结束时间'''
        self.inputText(text,'结束时间',*(self.bjPrintEndDate_loc))

    @property
    def clickPrintBtn(self):
        '''单击打印按钮'''
        self.clickBtn('打印',*(self.bjPrintBtn_loc))

    @property
    def clickPrintPopBtn(self):
        '''单击，弹出窗口中的打印按钮'''
        self.clickBtn('弹出打印',*(self.bjPrintPopBtn_loc))


    @property
    def assertPrint(self):
        """断言,弹出打印页面,点击打后后,页面消失_"""
        bool_var = self.isOrNoExist(*(self.bjPrintPopBtn_loc))
        self.getImage
        return bool_var

