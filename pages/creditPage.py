#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
import time,os

class CreditPage(basepage.BasePage):
    '''积分换礼页面'''

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #－－－－－－－－－－－会员或手机号选择页面－－－－－－－－－－－

    # 积分换礼Tab
    creditTab_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[1]/ul/li[2]/a')
    # 会员卡号或手机号
    charge_number_loc =(By.ID,'charge_number')
    # 确定按钮
    creditBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button')

    #－－－－－－－－－－－换礼页面－－－－－－－－－－－－－－－－－
    # 扣减积分
    inputExchangeNumber_loc = (By.ID,'inputExchangeNumber')
    # 礼品详情
    inputExchangeDetail_loc = (By.ID,'inputExchangeDetail')
    # 确定按钮
    sendMessageBtn_loc = (By.XPATH,'//*[@id="creditInfo"]/form/div/div[2]/div/div/a[1]')
    # 返回按钮
    cancelBtn_loc = (By.XPATH,'//*[@id="creditInfo"]/form/div/div[2]/div/div/a[2]')

    #-----
    # 积分兑换规则div
    credit_checkbox_loc =(By.XPATH,"//input[@name='rules[]']")
    # 积分数量
    creditNum_loc = (By.NAME,'credit')
    # 积分详情
    detail_loc = (By.NAME,'detail')
    # 兑换成功提示消息
    success_loc = (By.XPATH, '/html/body/div[5]')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #输入手杨号或卡号
    def inputPhoneorCard(self,text):
        """输入卡号 或手机号"""
        self.inputText(text,'输入卡号或手机号',*(self.charge_number_loc))

    @property
    def clickPhoneConfirmBtn(self):
        """单击 确定按钮"""
        self.clickBtn('确定',*(self.creditBtn_loc))

    def inputExchangeNumber(self,text):
        """输入 扣减积分数"""
        self.inputText(text,'扣减积分',*(self.inputExchangeNumber_loc))

    def inputExchangeDetail(self,text):
        """输入礼品 详情"""
        self.inputText(text,'礼品详情',*(self.inputExchangeDetail_loc))

    @property
    def clickConfirmBtn(self):
        """单击积分换礼 确定按钮，提交"""
        self.clickBtn('确定',*(self.sendMessageBtn_loc))

    @property
    def clickExitButton(self):
        """单击 返回按钮"""
        self.clickBtn('返回',*(self.cancelBtn_loc))



    def inputCreditNumber(self,text):
        """输入积分数量"""
        self.inputText(text,'积分数量',*(self.creditNum_loc))

    def inputCreditDetail(self,text):
        """输入积分详情"""
        self.inputText(text,'积分详情',*(self.detail_loc))

    @property
    def clickIterCheckBox(self):
        """循环 勾选积分规则 复选框"""
        self.iterClick('积分规则复选框',*(self.credit_checkbox_loc))


    def iterClick(self,desc,*loc):
        '''批量勾选积分规则'''
        elements = self.find_elements(*loc)
        for box in elements:
            i = 1
            if not box.is_selected():
                print '勾选:{0}{1}'.format(desc,i)
                box.click()
                i+=1


    @property
    def assertPaySuccess(self):
        '''断言支付成功'''
        bool_var = self.isExist(*(self.charge_number_loc))
        self.getImage
        return bool_var