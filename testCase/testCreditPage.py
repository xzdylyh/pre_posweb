#coding=utf-8
from pages.creditPage import CreditPage
from lib.scripts import (
    getYamlfield,
    getRunFlag,
    select_Browser_WebDriver,
    replayCaseFail,
    join_url
)
import unittest,ddt,os
from lib import gl,HTMLTESTRunnerCN

creditData = [
    {
        "charge_number":"1213058662866084",
        "ExchangeNumber":1,
        "ExchangeDetail":"自动化测试大礼包1个",
        "desc": "正常积分兑换流程"
    }
]

@ddt.ddt
class TestCreditPage(unittest.TestCase):
    """积分兑换模块"""
    @classmethod
    def setUpClass(cls):
        """初始化webdriver"""
        cls.driver = select_Browser_WebDriver()
        cls.url = join_url('/credit')


    def creditFunc(self,data):
        '''输入卡号或手号并点击确定'''
        self.credit = CreditPage(self.url,self.driver,u"积分换礼 - 微生活POS系统")
        # 增加cookies信息,并打开积分换礼页
        self.credit.open

        #输入手机号或卡号
        self.credit.inputPhoneorCard(data['charge_number'])
        #单击 确定按钮
        self.credit.clickPhoneConfirmBtn


    @unittest.skipIf(getRunFlag('CREDIT', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*creditData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        '''积分换礼'''
        print('{0}'.format(data['desc']))

        # 输入手机号,或卡号,进入积分换礼页面
        self.creditFunc(data)
        #积分规则
        self.credit.clickIterCheckBox
        #积分数量
        self.credit.inputCreditNumber(data['ExchangeNumber'])
        #积分详情
        self.credit.inputCreditDetail(data['ExchangeDetail'])
        #确定按钮 提交
        self.credit.clickConfirmBtn

        # 成功兑换断言
        self.credit.assertPaySuccess



    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass




if __name__=="__main__":
    suite = unittest.TestSuite()
    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCreditPage)]
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
