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
    card_Type_str = '//*[@id="cardChoose"]/label[{}]'
    # 储值卡号
    card_Numer_loc = (By.XPATH,'//*[@id="cardNum"]/div/ul/li/input')
    #电子储值卡 数量
    card_total_loc = (By.NAME, "cardTotal")
    #微信号
    card_vx_loc = (By.NAME, "vx")
    # 确定按钮
    card_ConfirmBtn_loc = (By.ID, "cardBtn")
    # 再次确定
    card_toConfirmBtn_loc = (By.XPATH,'//*[@id="myModal"]/div/div/div/div/button[1]')
    # 断言储值卡已售卖
    card_AssertSuccess_loc = (By.XPATH,'//*[@id="cardNum"]/div/ul/li/span')
    #断言电子卡成功
    card_assert_loc = (By.XPATH, "/html/body/div[4]")
    #支付方式;0现金;1银行卡,依此类推
    card_payType_locs = (By.XPATH, "//input[@name='payType']/..")

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>结束<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def imp_wait(self, option='on', ms=1000):
        if option == 'on':
            self.wait(ms)
        if option == 'off':
            None

    def click_pay_type(self, index):
        """支付类型"""
        self.click_btn_index(
            '支付类型',
            index,
            *(self.card_payType_locs)
        )


    def selectCardSelect(self,card_type):
        """选择卡储值卡"""
        self.selectComboxList(
            desc='储值卡',
            loc= self.card_Select_loc,
            index= int(card_type)
        )


    def inputCardNo(self,text, flag):
        """输入储值卡号"""
        #由于要捕捉,成功闪现提示弹层,只能在此写判断否则时间问题捕捉不到
        if flag != "%NONE%":
            self.inputText(text,'储值卡号',*(self.card_Numer_loc))


    def input_card_num(self, text):
        """输入电子卡,购买数量"""
        self.clearInputText(text, *(self.card_total_loc))
        self.inputText(
            text,
            '数量',
            *(self.card_total_loc)
        )

    def input_wechat_text(self, text):
        """微信号"""
        self.inputText(
            text,
            '微信号',
            *(self.card_vx_loc)
        )

    def click_card_type(self, index):
        """选择实体卡储值"""
        if index != "%NONE%":
            self.click_button(
                '实体卡储值',
                *(By.XPATH, self.card_Type_str.format(index))
            )


    @property
    def clickConfirmBtn(self):
        """点击确认 按钮"""
        self.click_button('确定',*(self.card_ConfirmBtn_loc))


    @property
    def clickSubmitBtn(self):
        """再次确认，提交"""
        self.click_button('再次确定',*(self.card_toConfirmBtn_loc))


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



    def assertChareSuccess(self):
        '''断言支付成功'''
        text = self.getTagText('text',*(self.card_AssertSuccess_loc))
        self.getImage()
        if not '该张储值卡已经售卖' in text:
            return False
        return True



    def assert_dcard_success(self):
        bool = self.getTagText('text', *(self.card_assert_loc))
        self.getImage()
        if not '操作成功' in bool:
            return False
        return True




if __name__=="__main__":
    pass