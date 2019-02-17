#coding=utf-8
from pages.consumeListPage import ConsumeListPage
import unittest,ddt,os
from lib.scripts import (
    getRunFlag,
    select_Browser_WebDriver,
    replayCaseFail,
    join_url
)
from lib import gl,HTMLTESTRunnerCN


#撤销消费
consumeData = [
    {
        "consumeListTitle": "消费流水 - 微生活POS系统", #标题
        "desc": "撤销消费正常流程" #用例描述
    }
]


@ddt.ddt
class TestConsumeListPage(unittest.TestCase):
    """交易流水-消费"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = join_url('/consume/list')


    @unittest.skipIf(getRunFlag('CONSUMELIST', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*consumeData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        """交易流水-撤销消费"""
        print('功能:{0}'.format(data['desc']))

        #实例化ConsumeListPage类
        self.consumeList = ConsumeListPage(self.url,self.driver,data['consumeListTitle'])
        # 打开目标地址
        self.consumeList.open

        #单击撤销消费 链接
        self.consumeList.clickUndoLinkText
        #单击 确定按钮
        self.consumeList.clickConfirmBtn

        """断言"""
        self.assertTrue(self.consumeList.assertCancelSuccess) #断言,弹出撤销成功div框

        self.assertEqual(self.consumeList.getContentText,u'撤销消费') #撤销消费,列表中增加一条撤销记录





    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass




if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestConsumeListPage)]
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
