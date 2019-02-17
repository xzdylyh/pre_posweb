#coding=utf-8
import time
import os
import unittest
import ddt
from lib.scripts import (
    getRunFlag,
    select_Browser_WebDriver,
    replayCaseFail,
    join_url
)
from lib import (gl,HTMLTESTRunnerCN)
from pages.bjPrintPage import BjPrintPage

#班结小票打印数据
printData = [
    {
        "startDate": gl.curDate, #开始日期
        "endDate": gl.curDate,   #结束日期
        "desc":u"班结小票打印正常流程"
    }
]

@ddt.ddt
class TestBjPrintPage(unittest.TestCase):
    """班结小票打印"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = join_url('/consume/list')



    @unittest.skipIf(getRunFlag('PRINT', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*printData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        """班结小结打印"""
        print('功能:{0}'.format(data['desc']))

        #实例化BjPrintPage类
        self.bjPrint = BjPrintPage(self.url,self.driver,'消费流水 - 微生活POS系统')
        # 打开交易流水页面
        self.bjPrint.open
        #点击 班结小票链接
        self.bjPrint.clickPrintLinkText
        #点击 打印按钮
        self.bjPrint.clickPrintBtn
        time.sleep(5) #等待3秒
        self.bjPrint.switch_window #切换到新窗口
        """断言"""
        self.assertTrue(self.bjPrint.assertPrint)#断言弹出最后打印界面,打印按钮存在


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__=="__main__":
    suite = unittest.TestSuite()
    tests = [unittest.TestLoader().loadTestsFromTestCase(TestBjPrintPage)]
    suite.addTests(tests)
    filePath = os.path.join(gl.reportPath, 'Report.html')  # 确定生成报告的路径
    print(filePath)

    #with块化结果后自动释放
    with open(filePath, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title=u'UI自动化测试报告',
            description=u'详细测试用例结果',  # 不传默认为空
            tester=u"yhleng"  # 测试人员名字，不传默认为小强
        )
        # 运行测试用例
        runner.run(suite)

