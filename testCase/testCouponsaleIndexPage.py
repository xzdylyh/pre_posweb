#coding=utf-8
from pos.pages.couponsaleIndexPage import CouponsaleIndexPage
import unittest,ddt,os
from pos.lib.scripts import (
    getYamlfield,
    getRunFlag,
    select_Browser_WebDriver,
    replayCaseFail,
    getBaseUrl
)
from pos.lib import gl,HTMLTESTRunnerCN

shopData = [
    {
        "phoneOrCard":"1802326514043775",
        "iterInput":[1,1],
        "desc":u"券包+次卡+直接购买",
        "title":u"商品售卖 - 微生活POS系统",
        "password": "000000"
    }
]

@ddt.ddt
class TestCouponsaleIndexPage(unittest.TestCase):
    """商品售卖模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = getBaseUrl('POS_URL') +'/couponsale/index'



    @unittest.skipIf(getRunFlag('COUPONSALEINDEX',('testCase1'))=='N','验证执行配置')
    @ddt.data(*shopData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        """商品售卖-券包+次卡+直接购买"""
        print '功能:{0}'.format(data['desc'])

        #实例化CouponsaleIndexPage类
        self.shop = CouponsaleIndexPage(self.url,self.driver,data['title'])
        # 打开目标url
        self.shop.open

        """输入会员卡号,或手机号页"""
        #输入手机号或卡号
        self.shop.inputPhoneOrCard(data['phoneOrCard'])
        #点击 确定按钮
        self.shop.clickConfirmBtn

        """商品售卖页"""
        #批量 勾选商品复选框
        self.shop.clickiterSelect
        #单击 确定按钮，提交售卖
        self.shop.clickShopConfirmBtn

        #输入交易密码
        self.shop.inputPaypwd(data['password'])
        #交易密码对话框确定
        self.shop.clickConfirmPaypwd

        """后置断言操作"""
        self.assertTrue(self.shop.assertShopSuccess)#断言售卖成功后,返回到输入卡号或手机号页面



    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass




if __name__=="__main__":

    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCouponsaleIndexPage)]
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