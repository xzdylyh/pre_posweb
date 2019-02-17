#_*_coding:utf-8_*_
import unittest
import os
from lib import (HTMLTESTRunnerCN,gl,scripts)
from lib.emailstmp import EmailClass
from testCase.testConsumePage import TestConsumePage
from testCase.testChargePage import TestChargePage
from testCase.testCreditPage import TestCreditPage
from testCase.testBjPrintPage import TestBjPrintPage
from testCase.testConsumeListPage import TestConsumeListPage
from testCase.testCreditListPage import TestCreditListPage
from testCase.testChargeListPage import TestChargeListPage
from testCase.testCardIndexPage import TestCardIndexPage
from testCase.testCouponsaleIndexPage import TestCouponsaleIndexPage
from testCase.testNumberCardPage import TestNumberCardPage
from testCase.testNumberCardListPage import TestNumberCardListPage
from testCase.testConsumeCouponListPage import TestConsumeCouponListPage



if __name__=="__main__":
    scripts.rm_dirs(gl.imgPath)
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestConsumePage),
             unittest.TestLoader().loadTestsFromTestCase(TestChargePage),
             unittest.TestLoader().loadTestsFromTestCase(TestCreditPage),
             unittest.TestLoader().loadTestsFromTestCase(TestBjPrintPage),
             unittest.TestLoader().loadTestsFromTestCase(TestConsumeListPage),
             unittest.TestLoader().loadTestsFromTestCase(TestCreditListPage),
             unittest.TestLoader().loadTestsFromTestCase(TestChargeListPage),
             unittest.TestLoader().loadTestsFromTestCase(TestCardIndexPage),
             unittest.TestLoader().loadTestsFromTestCase(TestCouponsaleIndexPage),
             unittest.TestLoader().loadTestsFromTestCase(TestNumberCardPage),
             unittest.TestLoader().loadTestsFromTestCase(TestNumberCardListPage),
             unittest.TestLoader().loadTestsFromTestCase(TestConsumeCouponListPage)
             ]

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

    EmailClass().send