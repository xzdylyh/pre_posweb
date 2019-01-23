#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
import time,os

class NumberCardPage(basepage.BasePage):
    """次卡消费模块"""
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 手机号或卡号
    number_phone_Loc = (By.ID,'charge_number')
    # 确定
    number_conrimBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button')
    # 次卡使用数
    number_usenum_loc = (By.XPATH,'//*[@id="numberCardInfo"]/div/div[1]/div/div[1]/div[2]/span[2]/input')
    # 备注
    number_remark_loc = (By.XPATH,'//*[@id="note"]')
    # 提交
    number_submit_loc = (By.ID,'numberSubmit')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def inputPhoneOrCard(self,text):
        """输入手机号 或卡号"""
        self.inputText(text,'手机号或卡号',*(self.number_phone_Loc))

    @property
    def clickNumberCardButton(self):
        """单击 确定按钮"""
        self.clickBtn('确定',*(self.number_conrimBtn_loc))


    def inputNumberUse(self,text):
        """输入次卡使用数"""
        self.inputText(text,'次卡使用数',*(self.number_usenum_loc))

    def inputRemark(self,text):
        """输入备注"""
        self.inputText(text,'备注',*(self.number_remark_loc))


    @property
    def clickSubmitButton(self):
        """单击 确定按钮，提交"""
        self.clickBtn('确定',*(self.number_submit_loc))


    @property
    def assertSuccess(self):
        """断言,消费成功"""
        print '断言:返回到次卡消费初始页'
        bool_var = self.isOrNoExist(*(self.number_phone_Loc))
        self.getImage
        return bool_var