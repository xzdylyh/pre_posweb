#coding=utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from pos.lib import scripts,gl
import time,os


class ChargePage(basepage.BasePage):
    '''储值模块'''
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 手机号或卡号
    charge_number_loc = (By.ID,'charge_number')
    # 确定按钮
    charge_confirmBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button')

    # 储值奖历规则
    charge_GZ_loc = (By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/p[2]')
    # 自定义储值规则
    charge_customGZ_loc = (By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/a')
    # 自定义输入金额
    charge_present_loc = (By.ID,'present')
    # 确定按钮
    charge_customBtn_loc = (By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/div[5]/div[1]/div/div/button')

    # 支付类型
    charge_payType_loc =(By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[4]/div/div[1]/div/label[1]')
    # 备注
    charge_Remark_loc = (By.ID,'note')
    # 储值提交确定按钮
    charge_submit_loc = (By.ID,'chargeSubmit')

    # 储值余额
    charge_RMB_loc = (By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[1]/div')
    # 储值最后确认
    charge_LastBtn_loc = (By.ID,'chargeCheckBtn')
    # 储值成功提示
    assertChargeSuccess_loc = (By.XPATH,'//*[@id="chargeSuccessModal"]/div/div/div[1]/h3')
    # 立即消费按钮
    charge_consumeBtn_loc = (By.ID,'consumeBtn')
    # 储值余额
    usSaving_loc = (By.ID,'usSaving')

    #-------------------------------------补开发票--------------------------------------
    # 补开发票
    fill_toReceipt_loc = (By.ID,"toReceipt")
    # 第一行发票金额
    fill_RMB_loc = (By.XPATH,'//*[@id="receipt"]/div[2]/div[2]/div[2]/div[1]/div[5]/input')

    # 未开发票金额
    #//*[@id="receipt"]/div[2]/div[1]/div[2]/div[1]/div[4] @变更记录，新增加补开发票年份下拉列表
    fill_not_RMB_loc = (By.XPATH,'//*[@id="receipt"]/div[2]/div[2]/div[2]/div[1]/div[4]')
    # 确定按钮
    #//*[@id="receipt"]/div[2]/div[3]/div'
    fill_Btn_loc = (By.XPATH,'//*[@id="receipt"]/div[2]/div[4]/div')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def inputPhoneOrCardNo(self,text):
        """输入手机号或卡号"""
        self.inputText(text,'储值卡号',*(self.charge_number_loc))

    @property
    def clickConfirmBtn(self):
        """单击 确定按钮，显示储值信息"""
        self.clickBtn('确定',*(self.charge_confirmBtn_loc))

    @property
    def clickChargeGZ(self):
        """单击储值奖励规则"""
        self.clickBtn('奖励规则',*(self.charge_GZ_loc))


    @property
    def clickCustomGZ(self):
        """单击 自定义规则链接"""
        self.clickBtn('自定义规则',*(self.charge_customGZ_loc))

    def inputCustomPresent(self,text):
        """输入自定义金额"""
        self.inputText(text,'自定义金额',*(self.charge_present_loc))

    @property
    def clickCustomConfirmBtn(self):
        """单击自定义规则确定按钮"""
        self.clickBtn('自定义规则确定',*(self.charge_customBtn_loc))

    @property
    def clickPayType(self):
        """单击支付类型，现金"""
        self.clickBtn('现金支付类型',*(self.charge_payType_loc))


    def inputRemark(self,text):
        """输入 备注"""
        self.inputText(text,'备注',*(self.charge_Remark_loc))

    @property
    def clickSubmitBtn(self):
        """单击 确定按钮提交"""
        self.clickBtn('确定',*(self.charge_submit_loc))



    @property
    def clickLastConfirmBtn(self):
        """单击 最后确认储值按钮"""
        self.clickBtn('确定',*(self.charge_LastBtn_loc))


    @property
    def clickConsumeBtn(self):
        """单击 立即消费按钮"""
        self.clickBtn('立即消费',*(self.charge_consumeBtn_loc))


    @property
    def clickFillReceipt(self):
        """单击 补开发票按钮"""
        self.clickBtn('补开发票',*(self.fill_toReceipt_loc))


    @property
    def clickFillConfirmBtn(self):
        """单击 发票确认按钮"""
        self.clickBtn('确定',*(self.fill_Btn_loc))


    def inputFillPresent(self,text):
        """输入 补开发票金额"""
        self.inputText(text,'补开发票金额',*(self.fill_RMB_loc))


    @property
    def assertfindRMB(self):
        """断言，储值余额是否存在"""
        bool_Var = self.isOrNoExist(*(self.charge_RMB_loc))
        return bool_Var


    @property
    def getAfterRMB(self):
        """获取储值前余额"""
        rmb = self.find_element(
            *(self.charge_RMB_loc)).text[:-1]
        return rmb

    @property
    def getLastRMB(self):
        """获取储值后余额"""
        rmb = self.find_element(
            *(self.usSaving_loc)).text
        return rmb


    def getNotFillPresent(self,txtName):
        """获取 未开发票金额"""

        # 未开票金额
        notFill = self.getTagText(
            txtName,*(self.fill_not_RMB_loc)).encode('utf-8')
        self.getImage
        return notFill


    @property
    def assertCustom(self):
        '''断言进入消费页面'''
        bool_var = self.isExist(*(self.assertPhone))
        self.getImage
        return bool_var


    @property
    def assertChargeSuccess(self):
        '''断言支付成功'''
        bool_var = self.isExist(*(self.assertChargeSuccess_loc))
        self.getImage
        return bool_var






if __name__=="__main__":
    pass