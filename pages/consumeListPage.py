#coding:utf-8
import time,os
from selenium.webdriver.common.by import By
from pos.base import basepage



class ConsumeListPage(basepage.BasePage):
    """交易流水模块"""
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 撤销消费链接
    undo_deal_loc = (By.XPATH,'//*[@id="consumeRunWater"]/table/tbody/tr[1]/td[21]/span')
    undo_dealText_loc =(By.LINK_TEXT,'撤销消费')
    # 确定按钮
    undo_dealBtn_loc = (By.ID,'undo')
    # 撤销成功
    undo_assert_loc = (By.XPATH,'//*[@id="showSuccess"]/div/i')
    # 交易流水中显示撤销成功条目
    undo_assert_list_loc = (By.XPATH,'//*[@id="consumeRunWater"]/table/tbody/tr[1]/td[18]/span')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



    """操作"""

    #封装操作
    @property
    def clickUndoLinkText(self):
        """单击 撤销消费 链接文本"""
        # 单击撤销消费之前，点一下父元素，来解决决定位到，点击无效
        self.clickBtn('撤销消费',*(self.undo_dealText_loc))

    @property
    def clickUndoLink(self):
        """单击 撤消消费 链接"""
        self.clickBtn('撤销消费',*(self.undo_deal_loc))

    @property
    def clickConfirmBtn(self):
        """单击 确定按钮"""
        self.clickBtn('确定',*(self.undo_dealBtn_loc))

    @property
    def getContentText(self):
        """获取 撤销消费后的操作状态"""
        txt = self.getTagText('text',*(self.undo_assert_list_loc))
        return txt

    @property
    def assertCancelSuccess(self):
        """断言,撤销成功"""
        bool_var = self.isOrNoExist(*(self.undo_assert_loc))
        self.getImage
        return bool_var