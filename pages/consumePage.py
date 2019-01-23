#coding:utf-8
import time,os
from pos.base import basepage
from selenium.webdriver.common.by import By




class ConsumePage(basepage.BasePage):
    '''消费功能模块'''
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    '''消费方式选择界面'''
    #会员卡号或手机号 Tab
    consume_cardOrPhoneTab_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/a[1]')
    #输入 卡号或手机号
    consume_CardorPhone_loc = (By.ID,'charge_number')
    #确定 按钮进入消费页
    consume_confirmBtn_loc = (By.XPATH,"//div[@id='ipt_box1']/div[1]/div[1]/button")
    #消费界面断言
    assertPhone = (By.XPATH,'/html/body/div[1]/div/dl/dt[2]')

    #优惠券码Tab
    '''消费界面'''
    # 消费总金额输入框
    tcTotalFee_loc = (By.ID,'tcTotalFee')
    # 储值支付输入框
    tcStoredPay_loc = (By.ID,'tcStoredPay')

    # 参加活动复选框
    tcCheckbox_activity_loc = (By.XPATH,"//div[@id='userInfo']/form[1]/div[8]/div[1]/div[1]/div[1]")
    # 备注
    tcRemark_loc = (By.ID,'note')
    # 确认按钮,进入确认销费
    tcShowSubmit_loc = (By.ID,'showSubmit')
    # 确认消费按钮
    tcConfirm_consumeBtn_loc = (By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div[2]/div/button[1]')
    #输入使用积分
    tcUseCredit_loc = (By.ID,'tcUseCredit')
    #选择使用券
    tcCouponDiv_loc = 'ticket-wrapper'
    tcTicket_loc = '//div[@class="ticket"]'
    tcUseCount = 'useCount'

    #------------------支付方式---------------------
    # 银行卡
    pay_loc = (By.XPATH,'/html/body/div[2]/div/div/div[1]/div[2]/form/div[10]/div/div/div/label[2]')
    #输入交易密码
    paypwd_loc = (By.ID,"password")
    #再次单击交易密码
    paypwd_confirm_loc = (By.XPATH,"/html/body/div[2]/div[2]/div/div/div[2]/form/div[3]/div/button[1]")

    #支付成功
    pay_success_loc = (By.XPATH, '//*[@id ="showSuccess"]/div[1]')

    #-------------------实体卡开卡-------------------
    # 单击开卡图标
    openCard_loc = (By.XPATH,'//*[@id="openCard"]/div/div/div[2]/a[1]/i')
    # 手机号
    open_phoneNo_loc = (By.ID,'inputUserNumber')
    # 姓名
    open_username_loc = (By.NAME,'username')
    # 性别
    open_sex_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/form/div[4]/div/label[1]')
    # 生日2018-05-29
    open_birthday_loc = (By.ID,'inputBirthday')
    # 交易密码
    open_password_loc = (By.NAME,'password')
    # 确定
    open_cardConfirmBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[3]/div/button')
    # 实体卡开卡成功后返回到收费界面
    open_CardSuccess_loc = (By.ID,'tcTotalFee')

    #-------------------------------绑卡--------------------------------------
    # 单击绑卡图标
    cardBindIco_loc = (By.XPATH,'//*[@id="openCard"]/div/div/div[2]/a[2]/i')
    # 输入卡号
    cardPhone_loc = (By.ID,'inputUserNumber')
    cardNumber_loc = (By.ID,'charge_number')
    # 确定按钮
    cardBindBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/form/div[2]/div/button')
    # 选择卡确认
    cardofBtn_loc =(By.XPATH,'//*[@id="associatedModal"]/div/div/div[3]/button[1]')
    # 输入验证码
    code_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/input')
    # 确定按钮
    codeBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div[2]/div[3]/div/button[1]')

    #手机验证码
    boss_code_xpath = '//*[@id="example2"]/tbody/tr[1]/td[4]'

    #次卡绑卡
    cardOfOpenBtn_loc = (By.ID,'chargeSubmit') #次卡开卡页面,确定按钮
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def inputVerCode(self,text):
        """输入手机验证码"""
        self.inputText(text,'手机验证码',*(self.code_loc))


    @property
    def clickVerCodeConfirmBtn(self):
        """单击验证码确定按钮"""
        self.clickBtn('确定',*(self.codeBtn_loc))


    @property
    def clearInputStoredPay(self):
        """清除储值支付框的值"""
        self.clearInputText(*(self.tcStoredPay_loc))


    @property
    def clickBindCardIco(self):
        """单击 绑卡图标，进入绑卡页面"""
        self.clickBtn('绑卡图标',*(self.cardBindIco_loc))


    def inputBindCardNo(self,text):
        """输入绑卡卡号"""
        self.inputText(text,'卡号',*(self.cardPhone_loc))


    @property
    def clickBindConfirmBtn(self):
        """绑卡确定按钮"""
        self.clickBtn('确定',*(self.cardBindBtn_loc))

    @property
    def clickBindSubmit(self):
        """绑卡再次确定按钮"""
        self.clickBtn('确认',*(self.cardofBtn_loc))


    @property
    def selectCardNoTab(self):
        """选择卡号或手机号tab"""
        self.clickBtn('手机号或卡号TAB',*(self.consume_cardOrPhoneTab_loc))


    def inputPhoneOrCardNo(self,text):
        """输入卡号或手机号"""
        self.inputText(text,'输入卡号或手机号',*(self.consume_CardorPhone_loc))

    @property
    def clickConfirmBtn(self):
        """单击确定按钮进入消费页"""
        self.clickBtn('确定',*(self.consume_confirmBtn_loc))


    def inputTotalFee(self,text):
        """输入消费总金额"""
        self.inputText(text,'消费总金额',*(self.tcTotalFee_loc))


    def inputStoredPay(self,text):
        """输入储值金额"""
        self.inputText(text,'储值金额',*(self.tcStoredPay_loc))


    def inputUseCredit(self,text):
        """输入积分"""
        self.inputText(text,'积分',*(self.tcUseCredit_loc))


    def inputRemark(self,text):
        """输入备注"""
        self.inputText(text,'备注',*(self.tcRemark_loc))

    @property
    def clickConsumeSubmitBtn(self):
        """单击消费确定提交"""
        self.clickBtn('确定',*(self.tcShowSubmit_loc))


    @property
    def clickConsumeConfirmBtn(self):
        """单击消费确定按钮"""
        self.clickBtn('确定',*(self.tcConfirm_consumeBtn_loc))


    @property
    def clickCardPayType(self):
        """单击 银行卡支付方式"""
        self.clickBtn('银行卡',*(self.pay_loc))


    def inputPaypwd(self,text):
        """输入交易密码"""
        self.isExistAndInput(text,*(self.paypwd_loc))

    @property
    def clickConfirmPaypwd(self):
        """再次输入交易密码"""
        self.isExistAndClick(*(self.paypwd_confirm_loc))


    @property
    def clickOpenCardIco(self):
        """单击 开卡图标，进行开卡"""
        self.clickBtn('开卡图标',*(self.openCard_loc))

    def inputOpenCardPhone(self,text):
        """输入开卡手机号"""
        self.inputText(text,'手机号',*(self.open_phoneNo_loc))

    def inputOpenCardName(self,text):
        """输入 开卡人姓名"""
        self.inputText(text,'姓名',*(self.open_username_loc))



    @property
    def clickOpenCardSex(self):
        """单击 开卡人性别"""
        self.clickBtn('性别',*(self.open_sex_loc))


    def inputOpenCardBirthday(self,text):
        """输入 开卡人生日"""
        self.inputText(text,'生日',*(self.open_birthday_loc))


    def inputOpenPwd(self,text):
        """输入交易密码"""
        self.isExistAndInput(text,*(self.open_password_loc))


    @property
    def clickOpenConfirmBtn(self):
        """单击确定按钮"""
        self.clickBtn('确定',*(self.open_cardConfirmBtn_loc))


    @property
    def clickCardOfOpenBtn(self):
        """不记名卡开卡页面确定按钮"""
        self.clickBtn('确定',*(self.cardOfOpenBtn_loc))



    @property
    def assertCustom(self):
        '''断言进入消费页面'''
        bool_var = self.isExist(*(self.assertPhone))
        self.getImage
        return bool_var

    @property
    def assertPaySuccess(self):
        '''断言支付成功'''
        bool_var = self.isExist(*(self.consume_CardorPhone_loc))
        self.getImage
        return bool_var


    @property
    def assertCardSuccess(self):
        '''断言支付成功'''
        bool_var = self.isExist(*(self.open_CardSuccess_loc))
        self.getImage
        return bool_var

    @property
    def assertOpenCardSuccess(self):
        """断言次卡开卡成功"""
        bool_var = self.isExist(*(self.cardNumber_loc))
        self.getImage
        return bool_var
