#coding=utf-8
from pages.consumeCouponListPage import  ConsumeCouponListPage
import unittest,ddt,os
from lib.scripts import (
    getRunFlag,
    select_Browser_WebDriver,
    replayCaseFail,
    join_url
)
from lib import gl,HTMLTESTRunnerCN

shopCancelData = [
    {
        "desc": "撤销商品售卖(券包+次卡+直接购买)",
        "title": "商品售卖流水 - 微生活POS系统"
    }
]

@ddt.ddt
class TestConsumeCouponListPage(unittest.TestCase):
    """交易流水模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = join_url('/consume/couponlist')



    @unittest.skipIf(getRunFlag('CONSUMECOUPONLIST',('testCase1'))=='N','验证执行配置')
    @ddt.data(*shopCancelData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        """交易流水-撤销商品售卖"""
        print('功能:{0}'.format(data['desc']))

        #实例化ConsumeCouponListPage类
        self.undo = ConsumeCouponListPage(self.url,self.driver,data['title'])
        # 打开目标url
        self.undo.open

        """商品售卖,撤销"""
        #单击 撤销商口售卖
        self.undo.clickUndoLinkText
        #单击 确定按钮
        self.undo.clickUndoConfirmBtn

        """后置断言操作"""
        self.assertTrue(self.undo.assertSuccess)
        self.assertEqual(self.undo.getContentText,'撤销商品售卖')



    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()




if __name__=="__main__":

    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestConsumeCouponListPage)]
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