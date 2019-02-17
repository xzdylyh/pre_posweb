#coding=utf-8
from selenium import webdriver
from pages.consumePage import ConsumePage
import unittest,ddt,os
from lib.excel import Excel
from lib.scripts import (
    getRunFlag,
    getYamlfield,
    select_Browser_WebDriver,
    replayCaseFail,
    join_url
)
from lib import gl,HTMLTESTRunnerCN
import time,json

consumeData = [
    {
        "phoneOrCard":"1213058035164514",
        "desc": "积分消费",
        "tcTotalFee":1,
        "tcStoredPay":1,
        "credit":1,
        "dualCode":'000000'
    }
]
chargeDealData=[
    {
        "tcTotalFee":1,
        "desc": "实体卡消费",
        "phoneOrCard":"1213058035164514",
        "dualCode":"000000"
    }
]
custCouponData = [
    {
        "tcTotalFee":1,
        "desc":u"券消费",
        "phoneOrCard":"1213058035164514",
        "dualCode":'000000'
    }
]
cardData = [
    {
        "PhoneNo":"13712345676",
        "desc": "实体卡开卡",
        'username':'yhleng',
        'birthday':'1985-03-21',
        'password':'000000'
    }
]
cardBindData = [
    {
        "PhoneNo": "13712345678",
        "desc": "绑卡正常流程"
    }
]

cardofData = [
    {
        "desc": "不记名卡开卡"
    }
]


@ddt.ddt
class TestConsumePage(unittest.TestCase):
    '''消费模块'''
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = join_url('/consume')
        #实体卡-未开过卡的
        cls.excel = Excel(os.path.join(gl.dataPath, 'posCardData.xls'))
        #不记名卡-未开过卡的
        cls.toexcel = Excel(os.path.join(gl.dataPath, 'posNotNameCardData.xls'))

    def consume_func(self,data):
        '''消费->输入卡号或手机号->确定'''
        self.consume = ConsumePage(self.url, self.driver, '消费 - 微生活POS系统')

        # 打开浏览器，并转到消费页
        self.consume.open
        # 选择会员卡号/手机号
        self.consume.selectTab
        # 输入卡号或手机号
        self.consume.inputPhoneOrCardNo(data['phoneOrCard'])
        # 点击确定按钮
        self.consume.clickConfirmBtn


    """消费模块，动态选择券"""
    def iterCoupon(self):
        '''动态选择券'''
        couponDiv = self.driver.find_elements_by_class_name(self.consume.tcCouponDiv_loc) #现金券
        for e in couponDiv:
            divEle = e.find_element_by_xpath(self.consume.tcTicket_loc)
            if divEle.is_displayed():
                divEle.click()  # 单击
                useCount = self.driver.find_element_by_name(self.consume.tcUseCount)
                if useCount.is_displayed():
                    useCount.send_keys(1)
                    break


    def getCode(self,data):
        """
        从Boss获取验证码
        :param data: 参数化数据
        :return: 验证码
        """
        """参数变量url,cookies,time"""
        yamldict = getYamlfield(gl.configFile)
        cookies= yamldict['CONFIG']['Cookies']['BossLoginCookies']
        #timeStr = time.strftime('%Y-%m-%d')
        url = 'http://boss.beta.acewill.net/sms/search?phone={0}&begin={1}&end={2}'.format(
            data['PhoneNo'],
            gl.curDate,
            gl.curDate
        )

        """设置浏览器,选项,隐藏获窗口运行"""
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars') #不显示"Chrome正在受自动测试软件控制"
        option.add_argument('headless') #后台运行,不显示界面

        """启动浏览器,增加cookies"""
        driver1 = webdriver.Chrome(chrome_options=option)
        driver1.maximize_window()
        driver1.get(url)
        driver1.implicitly_wait(30)
        driver1.add_cookie(cookies)
        driver1.get(url)

        """获取验证码,并返回验证码"""
        txtcode = driver1.find_element_by_xpath(self.consume.boss_code_xpath).text
        code = json.loads(txtcode)['template']['yanzhengma']
        driver1.quit()
        return code


    @unittest.skipIf(getRunFlag('CONSUME',('testCase1'))=='N','验证执行配置')
    @ddt.data(*cardData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        '''实体卡开卡'''
        print('功能：{0}'.format(data['desc']))

        #获取卡号
        cardNo = {'phoneOrCard':str(self.excel.getCardNo())}
        print("实体卡，卡号为：{0}".format(cardNo['phoneOrCard']))

        #进入消费页面
        self.consume_func(cardNo)
        # 实体卡开卡
        self.consume.clickOpenCardIco
        # 输入手机号
        self.consume.inputOpenCardPhone(data['PhoneNo'])
        # 姓名
        self.consume.inputOpenCardName(data['username'])
        # 性别
        self.consume.clickOpenCardSex
        # 生日
        self.consume.inputOpenCardBirthday(data['birthday'])
        # 交易密码
        self.consume.inputOpenPwd(data['password'])
        # 确定
        self.consume.clickOpenConfirmBtn

        #断言
        self.assertTrue(self.consume.assertCardSuccess)



    @unittest.skipIf(getRunFlag('CONSUME',('testCase6'))=='N','验证执行配置')
    @ddt.data(*cardofData)
    @replayCaseFail(num=3)
    def testCase6(self,data):
        """不记名卡开卡"""
        print('功能：{0}'.format(data['desc']))

        # 获取磁道号
        cardNo = {'phoneOrCard':str(self.toexcel.getCardNo(cell_col=0))}
        #进入消费界面
        self.consume_func(cardNo)

        """开卡页面"""
        #单击不记名卡，确定
        self.consume.clickCardOfOpenBtn

        """断言操作"""
        self.assertTrue(self.consume.assertOpenCardSuccess)


    @unittest.skipIf(getRunFlag('CONSUME','testCase5')=='N','验证执行配置')
    @ddt.data(*cardBindData)
    @replayCaseFail(num=3)
    def testCase5(self,data):
        """实体卡绑卡"""
        print('功能：{0}'.format(data['desc']))

        # 获取卡号-字典类型
        cardNo = {'phoneOrCard': str(self.excel.getCardNo())}

        #进入绑卡绑卡图标选择页面
        self.consume_func(cardNo)

        #单击绑卡图标
        self.consume.clickBindCardIco
        #输入卡号
        self.consume.inputBindCardNo(data['PhoneNo'])
        #单击 确定
        self.consume.clickBindConfirmBtn
        #获取验证码
        code = self.getCode(data)  #获取验证码
        #输出验证码
        print('验证码:{0}'.format(code))
        #输入验证码
        self.consume.inputVerCode(code)
        #单击 验证码框 确定
        self.consume.clickVerCodeConfirmBtn

        """断言"""
        self.assertTrue(self.consume.assertCardSuccess, msg='实体卡绑定失败')



    @unittest.skipIf(getRunFlag('CONSUME','testCase2')=='N','验证执行配置')
    @ddt.data(*consumeData)
    @replayCaseFail(num=3)
    def testCase2(self,data):
        '''积分消费'''
        print('功能:{0},消费{1}元,抵扣{2}积分.'.format(data['desc'],data['tcTotalFee'],data['credit']))

        # 进入消费页
        self.consume_func(data)

        #输入金额
        self.consume.inputTotalFee(data['tcTotalFee'])
        #清除储值支付金额
        self.consume.clearInputStoredPay
        #输入积分
        self.consume.inputUseCredit(data['credit'])
        #输入备注
        self.consume.inputRemark(data['desc'])
        #单击确认消费按钮
        self.consume.clickConsumeSubmitBtn
        #单击再次确认按钮
        self.consume.clickConsumeConfirmBtn

        '''输入密码点击确认'''
        #输入交易密码
        self.consume.inputPaypwd(data['dualCode'])
        #单击交易密码 确定按钮
        self.consume.clickConfirmPaypwd

        self.consume.assertPaySuccess #支付成功断言




    @unittest.skipIf(getRunFlag('CONSUME', 'testCase3') == 'N', '验证执行配置')
    @ddt.data(*chargeDealData)
    @replayCaseFail(num=3)
    def testCase3(self,data):
        '''储值销费'''
        print('功能:{0},消费金额{1},储值抵扣{2}元.'.format(
            data['desc'],
            data['tcTotalFee'],
            data['tcTotalFee']
        ))
        # 进入消费页
        self.consume_func(data)
        # 输入金额
        self.consume.inputTotalFee(data['tcTotalFee'])
        # 输入备注
        self.consume.inputRemark(data['desc'])
        # 确认消费按钮
        self.consume.clickConsumeSubmitBtn
        # 最终确认消费
        self.consume.clickConsumeConfirmBtn

        '''输入密码点击确认'''
        #输入交易密码
        self.consume.inputPaypwd(data['dualCode'])
        #单击交易密码 确定按钮
        self.consume.clickConfirmPaypwd

        self.consume.assertPaySuccess #支付成功断言



    @unittest.skipIf(getRunFlag('CONSUME', 'testCase4') == 'N', '验证执行配置')
    @ddt.data(*custCouponData)
    @replayCaseFail(num=3)
    def testCase4(self,data):
        '''券消费'''
        print('功能:{0},消费{1}积分.'.format(
            data['desc'],
            data['tcTotalFee']
        ))
        # 进入消费页
        self.consume_func(data)
        # 输入金额
        self.consume.inputTotalFee(data['tcTotalFee'])
        # 选择现金券
        self.iterCoupon()
        # 输入备注
        self.consume.inputRemark(data['desc'])
        # 确认消费按钮
        self.consume.clickConsumeSubmitBtn
        # 最终确认消费
        self.consume.clickConsumeConfirmBtn

        '''输入密码点击确认'''
        #输入交易密码
        self.consume.inputPaypwd(data['dualCode'])
        #单击交易密码 确定按钮
        self.consume.clickConfirmPaypwd

        self.consume.assertPaySuccess #支付成功断言


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass


if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestConsumePage)]
    suite.addTests(tests)
    filePath = os.path.join(gl.reportPath, 'Report.html')  # 确定生成报告的路径
    print(filePath)

    with open(filePath, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title=u'UI自动化测试报告',
            description=u'详细测试用例结果',  # 不传默认为空
            tester=u"yhleng"  # 测试人员名字，不传默认为小强
        )
        # 运行测试用例
        runner.run(suite)
        fp.close()
