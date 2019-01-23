#coding=utf-8
import unittest,ddt,os
from pages.cardIndexPage import CardIndexPage

from lib.scripts import getBaseUrl,\
    getRunFlag\
    ,rmDirsAndFiles,\
    select_Browser_WebDriver,\
    replayCaseFail
from lib.excel import Excel
from lib import gl,HTMLTESTRunnerCN

cardShopData = [
    {"desc": u"实体储值卡售卖", "pagetitle": u"储值卡售卖 - 微生活POS系统","assert":u"该张储值卡已经售卖","CardType":0}
]

@ddt.ddt
class TestCardIndexPage(unittest.TestCase):
    """储值售卖模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = getBaseUrl('POS_URL')+'/card/index'
        cls.excel = Excel(
            os.path.join(
                gl.dataPath, 'posChargeCard.xls'
            ).decode('utf-8')
        )


    @unittest.skipIf(
        getRunFlag('CARDINDEX', 'testCase1') == 'N',
        '验证执行配置'
    )
    @ddt.data(*cardShopData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        """储值卡售卖-实体储值卡售卖"""
        print '功能:{0}'.format(data['desc'])

        """前置初始操作"""
        #实例化CardIndexPage类
        self.card = CardIndexPage(
            self.url,self.driver,
            data['pagetitle']
        )
        # 打开浏览器并转到指定url
        self.card.open

        #从excel获取一条标记为N的卡号
        cardNo = float(
            self.excel.getCardNo(cell_col=0,cell_valueType=1)
        ).__int__().__str__()

        """储值售卖页面"""
        #选择储值卡
        self.card.selectCardSelect(data['CardType'])

        #单击储值卡类型  实体卡储值
        self.card.clickCardType

        #输入 储值卡号
        self.card.inputCardNo(cardNo)

        #单击 确定按钮
        self.card.clickConfirmBtn

        #单击 再次确定按钮
        self.card.clickSubmitBtn

        """后置断言操作"""
        self.card.wait(2000)

        #点击储值卡类型为  实体卡储值
        self.card.clickCardType
        #输入 储值卡号
        self.card.inputCardNo(cardNo)

        self.assertEqual(
            self.card.assertChareSuccess,
            data['assert']
        )#断言已售的卡不能再售,来判断售卡成功


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        #pass





if __name__=="__main__":
    rmDirsAndFiles(gl.imgPath)
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCardIndexPage)]
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