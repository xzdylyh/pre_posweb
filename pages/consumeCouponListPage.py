#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
import time,os

class ConsumeCouponListPage(basepage.BasePage):
    """交易流水模块-商品售卖"""
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 撤销链接
    coupon_undoLink_loc = (By.XPATH,'//*[@id="consumeRunWater"]/table/tbody/tr[1]/td[12]/span[1]/a')
    coupon_undoLinkText_loc = (By.LINK_TEXT,'撤销')
    # 确认
    coupon_confirmBtn_loc = (By.ID,'undo')
    # 撤销后新增一条,撤销商品售卖的记录
    coupon_assert_loc = (By.XPATH,'//*[@id="consumeRunWater"]/table/tbody/tr[1]/td[10]/span')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    """操作"""
    @property
    def clickUndoLink(self):
        """单击 撤销商品售卖 链接"""
        self.clickBtn('商品售卖撤销',*(self.coupon_undoLink_loc))

    @property
    def clickUndoLinkText(self):
        """单击 撤销商品售卖 链接"""
        self.clickBtn('商品售卖撤销',*(self.coupon_undoLinkText_loc))

    @property
    def clickUndoConfirmBtn(self):
        """单击 撤销确认按钮"""
        self.clickBtn('确定',*(self.coupon_confirmBtn_loc))


    @property
    def getContentText(self):
        """获取 商品售卖撤销后，状态"""
        txt = self.getTagText('text',*(self.coupon_assert_loc))
        return txt


    @property
    def assertSuccess(self):
        """断言,撤销消费成功"""
        print '断言:交易流水,新增一条,交易类型为撤销商品售卖的记录'
        bool_var = self.isOrNoExist(*(self.coupon_assert_loc))
        self.getImage
        return bool_var