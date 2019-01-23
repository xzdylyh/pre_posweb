#coding=utf-8
from base import basepage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from lib.scripts import Replay
import time,os


class CardIndexPage(basepage.BasePage):
    '''储值卡售卖模块'''
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>定位器<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # 选择卡
    card_Select_loc = (By.NAME,'card')
    # 储值卡类型
    card_Type_loc = (By.XPATH,'//*[@id="cardChoose"]/label[2]')
    # 储值卡号
    card_Numer_loc = (By.XPATH,'//*[@id="cardNum"]/div/ul/li/input')
    # 确定按钮
    card_ConfirmBtn_loc = (By.XPATH,'//*[@id="cardBtn"]')
    # 再次确定
    card_toConfirmBtn_loc = (By.XPATH,'//*[@id="myModal"]/div/div/div/div/button[1]')
    # 断言储值卡已售卖
    card_AssertSuccess_loc = (By.XPATH,'//*[@id="cardNum"]/div/ul/li/span')
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>结束<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    def selectCardSelect(self,card_type):
        """选择卡储值卡"""
        self.selectComboxList(
            desc='储值卡',
            loc= self.card_Select_loc,
            index= int(card_type)
        )


    def inputCardNo(self,text):
        """输入储值卡号"""
        self.inputText(text,'储值卡号',*(self.card_Numer_loc))


    @property
    def clickCardType(self):
        """选择实体卡储值"""
        self.clickBtn('实体卡储值',*(self.card_Type_loc))


    @property
    def clickConfirmBtn(self):
        """点击确认 按钮"""
        self.clickBtn('确定',*(self.card_ConfirmBtn_loc))


    @property
    def clickSubmitBtn(self):
        """再次确认，提交"""
        self.clickBtn('再次确定',*(self.card_toConfirmBtn_loc))


    @Replay
    def selectDownList(self,option=0,index=0,value=0,txt='',*loc):
        """选择下拉列表框"""
        element = self.find_element(*loc)
        ul = Select(element)
        if option==0:
            ul.select_by_index(index)
        elif option==1:
            ul.select_by_value(value)
        else:
            ul.select_by_visible_text(txt)



    @property
    def assertChareSuccess(self):
        '''断言支付成功'''
        text = self.getTagText('text',*(self.card_AssertSuccess_loc))
        self.getImage
        return text





if __name__=="__main__":
    pass