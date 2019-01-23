#coding=utf-8
from pos.pages.chargeListPage import ChargeListPage
import unittest,ddt,os
from pos.lib.scripts import getRunFlag,\
    select_Browser_WebDriver,\
    replayCaseFail,\
    getBaseUrl
from pos.lib import gl,HTMLTESTRunnerCN


chargeData = [{"desc": u"充值撤销正常流程", "pageTitle": u"充值流水 - 微生活POS系统"}]

@ddt.ddt
class TestChargeListPage(unittest.TestCase):
    """交易流水模块-充值"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = getBaseUrl('POS_URL')+'/charge/listcharge'


    @unittest.skipIf(getRunFlag('CHARGELIST', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*chargeData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        """充值撤销"""
        print '功能:{0}'.format(data['desc'])

        """前置操作"""
        #实例化ChargeListPage类
        self.charge = ChargeListPage(self.url,self.driver,data['pageTitle'])
        # 打开目标页
        self.charge.open

        """页面操作"""
        #单击 撤值撤销链接
        self.charge.clickUndoLinkText

        #单击 确定按钮
        self.charge.clickConfirmBtn

        """断言操作"""
        #断言成功
        txt = self.charge.getChargeStatusTxt
        print '充值撤销状态:{0}'.format(txt)
        self.assertEqual(txt,u'撤销充值',msg='撤销充值记录列表中,不存在状态为<撤销充值>的记录')


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()




if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestChargeListPage)]
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
