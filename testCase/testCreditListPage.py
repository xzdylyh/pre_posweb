# coding=utf-8
from pos.pages.creditListPage import CreditListPage
import unittest, ddt, os

from pos.lib.scripts import (
    getRunFlag,
    getBaseUrl,
    select_Browser_WebDriver,
    replayCaseFail
)
from pos.lib import gl, HTMLTESTRunnerCN


creditData = [
    {
        "CreditListTitle":u"积分换礼流水 - 微生活POS系统",
        "desc": u"积分换礼-撤销积分"
    }
]


@ddt.ddt
class TestCreditListPage(unittest.TestCase):
    """交易流水模块-积分换礼"""

    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = getBaseUrl('POS_URL') +'/credit/list'

    @unittest.skipIf(getRunFlag('CREDITLIST', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*creditData)
    @replayCaseFail(num=3)
    def testCase1(self, data):
        """交易流水-撤销积分"""
        print '功能:{0}'.format(data['desc'])

        #实例化CreditListPage类
        self.creditList = CreditListPage(self.url,self.driver,data['CreditListTitle'])
        # 打开目标地址
        self.creditList.open

        """撤销积分页操作"""
        #单击 撤销积分
        self.creditList.clickUndoLinkText
        #单击确定 按钮
        self.creditList.clickUndoBtn

        """断言"""
        self.assertEqual(
            self.creditList.assertUndoSuccess,
            '撤销积分换礼'
        )#撤销积分后,在列表显示一条,状态为撤销积分换礼记录


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass


if __name__ == "__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCreditListPage)]
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
