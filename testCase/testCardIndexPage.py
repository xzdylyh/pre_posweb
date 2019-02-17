#coding=utf-8
import unittest,ddt,os
from pages.cardIndexPage import CardIndexPage

from lib.scripts import (
    join_url,
    getRunFlag,
    rm_dirs,
    select_Browser_WebDriver,
    replayCaseFail
)
from lib.excel import Excel
from lib import gl,HTMLTESTRunnerCN

#实体卡储值售卖数据
cardShopData = [
    {
        "desc": u"储值卡售卖功能-实体储值卡售卖(支付方式现金)",  #用例描述
        "pagetitle": u"储值卡售卖 - 微生活POS系统", #测试页浏览器标题
        "assert": "self.card.assertChareSuccess()", #断言文本
        "CardType":0, #选择储值卡列表,0第1个;1第二个,依此类推
        "card_index": 2, #实体储值卡
        "h_card_index": 2, #后置卡类型
        "card_num": "%NONE%", #选择电子卡时输入的数量
        "wechat_no": "%NONE%", #微信卡号,电子卡时需输入
        "cardno_flag":"", #卡号标记如果不输入填写"%NONE%"
        "wait_off/on": "on", #等待开关
        "wait_ms": 2000, #等待时间
        "pay_type": 0 #现金

    },
    {
        "desc": u"储值卡售卖功能-电子卡售卖(支付方式银行卡)",  # 用例描述
        "pagetitle": u"储值卡售卖 - 微生活POS系统",  # 测试页浏览器标题
        "assert": "self.card.assert_dcard_success()",  # 断言文本
        "CardType": 0,  # 选择储值卡列表,0第1个;1第二个,依此类推
        "card_index": 1, # 电子卡
        "h_card_index": "%NONE%", #后置卡类型
        "card_num": 1,  # 选择电子卡时输入的数量
        "wechat_no": "1117093",  # 微信卡号,电子卡时需输入
        "cardno_flag": "%NONE%",  # 卡号标记如果不输入填写"%NONE%"
        "wait_off/on": "off",  # 等待开关
        "wait_ms": 2000,  # 等待时间
        "pay_type": 1  # 银行卡
    }
]

@ddt.ddt
class TestCardIndexPage(unittest.TestCase):
    """储值售卖模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = join_url('/card/index')
        cls.excel = Excel(
            os.path.join(
                gl.dataPath, 'posChargeCard.xls'
            )
        )
        #从excel获取一条标记为N的卡号
        cls.cardNo = float(
            cls.excel.getCardNo(cell_col=0,cell_valueType=1)
        ).__int__().__str__()

    @unittest.skipIf(
        getRunFlag('CARDINDEX', 'testCase1') == 'N',
        '验证执行配置'
    )
    @ddt.data(*cardShopData)
    @replayCaseFail(num=1)
    def testCase1(self,data):
        """储值卡售卖-实体储值卡售卖"""
        print('功能:{0}'.format(data['desc']))

        """前置初始操作"""
        #实例化CardIndexPage类
        self.card = CardIndexPage(
            self.url,self.driver,
            data['pagetitle']
        )
        # 打开浏览器并转到指定url
        self.card.open

        """储值售卖页面"""
        #选择储值卡
        self.card.selectCardSelect(data['CardType'])
        #单击储值卡类型  实体卡储值 卡类型0.电子卡;1实体储值卡
        self.card.click_card_type(data['card_index'])
        #输入 储值卡号
        self.card.inputCardNo(self.cardNo, data['cardno_flag'])
        #输入电子卡数量
        self.card.input_card_num(data['card_num'])
        #输入微信号
        self.card.input_wechat_text(data['wechat_no'])
        #选择支付类型;0现金;1银行卡;依此类推
        self.card.click_pay_type(data['pay_type'])
        #单击 确定按钮
        self.card.clickConfirmBtn
        #单击 再次确定按钮
        self.card.clickSubmitBtn

        """后置断言操作"""
        self.card.imp_wait(option=data['wait_off/on'], ms=data['wait_ms'])
        #点击储值卡类型为  实体卡储值
        self.card.click_card_type(data['h_card_index'])
        #输入 储值卡号
        self.card.inputCardNo(self.cardNo, data['cardno_flag'])

        #断言已售的卡不能再售,来判断售卡成功
        self.assertTrue(eval(data['assert']))
        #加个等待时间,增加两个用例之间截图准确性
        self.card.wait(3000)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass



if __name__=="__main__":
    rm_dirs(gl.imgPath)
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCardIndexPage)]
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