#coding=utf-8
from pages.numbercardListPage import NumberCardListPage
import unittest,ddt,os
from lib.scripts import (
    getRunFlag,
    select_Browser_WebDriver,
    replayCaseFail,
    join_url
)
from lib import gl,HTMLTESTRunnerCN



listCardData = [
    {
        "useNum":1,
        "phoneOrCard":"1213058035164514",
        "desc": "次卡消费撤销正常流程",
        "title":"次卡消费流水 - 微生活POS系统"
    }
]

@ddt.ddt
class TestNumberCardListPage(unittest.TestCase):
    """交易流水模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = join_url('/numbercard/list')




    @unittest.skipIf(getRunFlag('NUMBERCARDLIST', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*listCardData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        """次卡消费撤销"""
        print('功能:{0}'.format(data['desc']))

        #实例化NumberCardListPage类
        self.list = NumberCardListPage(self.url,self.driver,data['title'])
        # 打开目标地址
        self.list.open

        """撤销操作"""
        #单击撤销消费
        self.list.clickUndoLink
        #单击确定按钮
        self.list.clickConfirmButton

        """检查断言"""
        self.assertTrue(self.list.assertSuccess)#断言，撤销后，状态是否存在
        self.assertEqual(
            self.list.getUndoStatus,
            '撤销消费'
        )#断言状态是否为 撤销消费


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()



if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestNumberCardListPage)]
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