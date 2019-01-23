#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
import time,os

class CreditListPage(basepage.BasePage):
    """交易流水模块"""
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #交易流水-撤销积分
    # 撤销积分链接
    undo_LinkBtn_loc = (By.XPATH,'//*[@id="giftRunWater"]/table/tbody/tr[1]/td[9]/span')
    unodo_LinkBtnText_loc = (By.LINK_TEXT,'撤销积分')
    # 确定按钮
    undo_Btn_loc = (By.ID,'cancelGift')
    # 撤销积分后,交易列表增加一条状态,撤销积分换礼
    undo_assertList_loc = (By.XPATH,'//*[@id="giftRunWater"]/table/tbody/tr[1]/td[7]/span')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    @property
    def clickUndoLink(self):
        """单击撤销积分"""
        self.clickBtn('撤销积分',*(self.undo_LinkBtn_loc))

    @property
    def clickUndoLinkText(self):
        """单击撤销积分文本"""
        self.clickBtn('撤销积分',*(self.unodo_LinkBtnText_loc))


    @property
    def clickUndoBtn(self):
        """单击撤销积分确定按钮"""
        self.clickBtn('确定',*(self.undo_Btn_loc))


    @property
    def assertUndoSuccess(self):
        """断言,撤销成功"""
        txt = self.getTagText('text',*(self.undo_assertList_loc))
        self.getImage
        return txt