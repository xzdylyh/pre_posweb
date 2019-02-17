#coding=utf-8
from pages.chargePage import ChargePage
import unittest,ddt,os
from lib.scripts import (
    getRunFlag,
    select_Browser_WebDriver,
    replayCaseFail,
    join_url
)
from lib import gl,HTMLTESTRunnerCN

#储值正常流程数据
chargeData = [
    {
        "charge_number":"1213058035164514",
        "present":2,
        "note":"自动化测试充值",
        "desc":"储值正常流程",
        "page_title": "充值 - 微生活POS系统",
        "pay_index": 0 #支付方式,0现金;1银行卡依此类推
    }
]

#储值补开发票
FillData = [
    {
        "charge_number":"1213058035164514",
        "present":2,
        "note":"自动化测试充值",
        "desc":"储值并补开发票",
        "txtName":"text",
        "page_title": "充值 - 微生活POS系统",
        "pay_index": 0  # 支付方式,0现金;1银行卡依此类推
    }

]

#储值异常流程
raise_data = [
    {   "charge_number":"1213058035164514",
        "present":1,
        "note":"自动化测试充值",
        "desc":"储值(自定义金额与储值规则金额相同)-反向",
        "page_title": "充值 - 微生活POS系统",
        "pay_index": 0 #支付方式,0现金;1银行卡依此类推
    }
]


##########################################
#储值规则:充1元送1元送1积分;送1元券一张
##########################################
@ddt.ddt
class TestChargePage(unittest.TestCase):
    '''储值模块'''

    @classmethod
    def setUpClass(cls):

        cls.driver = select_Browser_WebDriver()
        cls.url = join_url('/charge/index')


    def inChargePage(self,data):
        """输入卡号进入储值页面"""
        #实例化ChargePage类
        self.charge = ChargePage(self.url,self.driver, data['page_title'])
        # 打开目标url
        self.charge.open

        """输入卡号，确定，进入储值页面"""
        #输入 卡号
        self.charge.inputPhoneOrCardNo((data['charge_number']))
        #单击 确定
        self.charge.clickConfirmBtn

        """断言操作"""
        #储值余额
        self.assertTrue(self.charge.assertfindRMB)

        #储值前的 储值余额
        self.usChargeSaving = self.charge.getAfterRMB

        print('当前余额:{0}'.format(self.usChargeSaving))


    def chargeFunc(self,data):
        """储值功能操作"""
        print('功能:{0}'.format(data['desc']))

        """输入卡号或手机号，确定，进入储值页面"""
        self.inChargePage(data)

        """储值操作"""
        #选择储值奖励规则
        self.charge.clickChargeGZ
        #单击 自定义规则
        self.charge.clickCustomGZ
        #输入 自定义金额
        self.charge.inputCustomPresent(data['present'])
        #点击 自定义金额对话框  确定按钮
        self.charge.clickCustomConfirmBtn
        #点击 现金支付方式
        self.charge.clickPayType(data['pay_index'])
        #输入 备注
        self.charge.inputRemark(data['note'])
        #单击 确定，进入储值确认对话框
        self.charge.clickSubmitBtn
        #单击 确认，并储值
        self.charge.clickLastConfirmBtn

        """断言操作"""
        self.charge.assertChargeSuccess

        """后置操作"""
        #单击 立即消费按钮
        self.charge.clickConsumeBtn

        """断言储值余额，是否正确"""
        #获取 储值后余额
        self.usDualSaving = self.charge.getLastRMB

        print('储值后当前余额:{0}'.format(self.usDualSaving))
        self.assertTrue(
            float(data['present']) + float(self.usChargeSaving) + 1 ==float(self.usDualSaving)
        )



    @unittest.skipIf(getRunFlag('CHARGE', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*chargeData)
    @replayCaseFail(num=3)
    def testCase1(self,data):
        """正常储值功能"""
        #调用储值功能函数
        self.chargeFunc(data)


    @unittest.skipIf(getRunFlag('CHARGE', 'testCase2') == 'N', '验证执行配置')
    @ddt.data(*FillData)
    @replayCaseFail(num=3) #case执行失败后，重新执行num次
    def testCase2(self,data):
        """储值并补开发票"""

        # 调用储值功能函数
        self.chargeFunc(data)

        """补开发票"""
        #单击 补开发票按钮
        self.charge.clickFillReceipt
        #获取 未开票金额
        notFillPresent = self.charge.getNotFillPresent(data['txtName'])
        #输入 开票金额
        self.charge.inputFillPresent(str(notFillPresent))
        #单击 确定 开发票
        self.charge.clickFillConfirmBtn


        """断言补开票成功"""
        #单击 补开发票按钮
        self.charge.clickFillReceipt
        #获取 未开票金额
        notFillPresent = float(self.charge.getNotFillPresent(data['txtName']))

        print('补开发票金额剩余:{0}'.format(notFillPresent))
        #断言补开发票后，第一行补开发票为零
        self.assertEqual(notFillPresent,float('0.00'),msg='开票余额,不为零.')


    @unittest.skipIf(getRunFlag('CHARGE', 'testCase3') == 'N', '验证执行配置')
    @ddt.data(*raise_data)
    @replayCaseFail(num=3)
    def testCase3(self,data):
        """储值功能-自定义金额与储值金额相同"""
        #调用储值功能函数
        """储值功能操作"""
        print('功能:{0}'.format(data['desc']))

        """输入卡号或手机号，确定，进入储值页面"""
        self.inChargePage(data)

        """储值操作"""
        #选择储值奖励规则
        self.charge.clickChargeGZ
        #单击 自定义规则
        self.charge.clickCustomGZ
        #输入 自定义金额
        self.charge.inputCustomPresent(data['present'])
        #点击 自定义金额对话框  确定按钮
        self.charge.clickCustomConfirmBtn

        #
        #断言
        self.assertTrue(self.charge.assert_custom_error())






    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass


if __name__=="__main__":

    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestChargePage)]
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
