#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
import time,os

class NumberCardListPage(basepage.BasePage):
    """交易流水模块-次卡消费撤销"""
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 撤销消费链接
    list_undoLink_loc = (By.XPATH,'//*[@id="giftRunWater"]/table/tbody/tr[1]/td[7]')
    # 确认按钮
    list_confirmBtn_loc = (By.ID,'cancelCost')
    # 新增一条交易类型为撤销消费
    list_assert_loc = (By.XPATH,'//*[@id="giftRunWater"]/table/tbody/tr[1]/td[5]/span/span')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    """操作"""
    @property
    def clickUndoLink(self):
        """单击撤销链接"""
        self.clickBtn('消费撤销',*(self.list_undoLink_loc))


    @property
    def clickConfirmButton(self):
        """单击确定按钮"""
        self.clickBtn('确定',*(self.list_confirmBtn_loc))


    @property
    def getUndoStatus(self):
        """获取撤销后，状态"""
        txt = self.getTagText('text',*(self.list_assert_loc))
        return txt

    @property
    def assertSuccess(self):
        """断言,撤销消费成功"""
        print '断言:交易流水,新增一条,交易类型为撤销消费的记录'
        bool_var =self.isOrNoExist(*(self.list_assert_loc))
        self.getImage
        return bool_var