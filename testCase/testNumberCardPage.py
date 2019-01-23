#coding=utf-8
from pos.pages.numbercardPage import NumberCardPage
import unittest,ddt,os
from pos.lib.excel import Excel
from pos.lib.scripts import (
    getRunFlag,
    getYamlfield,
    select_Browser_WebDriver,
    replayCaseFail,
    getBaseUrl
)
from pos.lib import gl,HTMLTESTRunnerCN
import time,json


numberCardData = [
    {
        "useNum":1,
        "phoneOrCard":"1586313101756463",
        "desc":u"次卡消费,正常流程",
        "title":u"次卡消费 - 微生活POS系统"
    }
]

@ddt.ddt
class TestNumberCardPage(unittest.TestCase):
    """次卡消费模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = getBaseUrl('POS_URL') +'/numbercard'

    @unittest.skipIf(getRunFlag('NUMBERCARD', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*numberCardData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        """次卡消费"""
        print '功能:{0}'.format(data['desc'])

        #实例化NumberCardPage类
        self.number = NumberCardPage(self.url,self.driver,data['title'])
        # 打开目标地址
        self.number.open

        """输入手机号或卡号进入次卡消费界面"""
        #输入手机号或卡号
        self.number.inputPhoneOrCard(data['phoneOrCard'])
        #单击 确定按钮
        self.number.clickNumberCardButton

        """次卡消费界面,操作"""
        #输入 次卡使用次数
        self.number.inputNumberUse(data['useNum'])
        #单击确定按钮，提交
        self.number.clickSubmitButton

        """检查断言"""
        self.assertTrue(
            self.number.assertSuccess,
            msg='检查消费后,返回到,输入手机号界面'
        )#检查消费后,返回到,输入手机号界面


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()



if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestNumberCardPage)]
    suite.addTests(tests)
    filePath = os.path.join(gl.reportPath, 'Report.html')  # 确定生成报告的路径
    print filePath

    with file(filePath, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title=u'UI自动化测试报告',
            description=u'详细测试用例结果',  # 不传默认为空
            tester=u"yhleng"  # 测试人员名字，不传默认为小强
        )
        # 运行测试用例
        runner.run(suite)
        fp.close()