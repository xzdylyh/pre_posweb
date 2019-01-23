#coding=utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time,os


class CouponsaleIndexPage(basepage.BasePage):
    '''商品售卖模块'''
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 卡号或手机号
    shop_phone_loc = (By.ID,'charge_number')
    # 确定按钮
    shop_phoneBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button')

    """商品售卖页面"""
    # 商口复选择框
    shop_select_loc = (By.CLASS_NAME,'checkbox-inline')
    # 数量输入框
    shop_Num_loc = (By.NAME,'num')
    # 确定按钮
    shop_confirmBtn_loc = (By.ID,'sell-submit')

    # 输入交易密码
    paypwd_loc = (By.ID, "password")
    # 再次单击交易密码
    paypwd_confirm_loc = (By.XPATH, '//*[@id="dialog_paypwd_modal"]/div/div/div[2]/form/div[3]/div/button[1]')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def inputPhoneOrCard(self,text):
        """输入 卡号或手机号"""
        self.inputText(text,'手机号或卡号',*(self.shop_phone_loc))

    @property
    def clickConfirmBtn(self):
        """单击 确定按钮，进入商品售卖页面"""
        self.clickBtn('确定',*(self.shop_phoneBtn_loc))

    @property
    def clickiterSelect(self):
        """单击 商品复选框"""
        self.iterClick(*(self.shop_select_loc))

    def inputShopNum(self,text):
        """输入 商品数量"""
        self.inputText(text,'商品数量',*(self.shop_Num_loc))

    @property
    def clickShopConfirmBtn(self):
        """点击 确定按钮，提交售卖"""
        self.clickBtn('确定',*(self.shop_confirmBtn_loc))


    def inputPaypwd(self,text):
        """输入交易密码"""
        self.isExistAndInput(text,*(self.paypwd_loc))

    @property
    def clickConfirmPaypwd(self):
        """再次输入交易密码"""
        self.isExistAndClick(*(self.paypwd_confirm_loc))

    @property
    def assertShopSuccess(self):
        '''断言售卖成功'''
        bool_var = self.isExist(*(self.shop_phone_loc))
        print '返回到输入卡号界面?{0}'.format(bool_var)
        self.getImage
        return bool_var




if __name__=="__main__":
    pass