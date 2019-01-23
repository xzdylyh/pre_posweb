#coding=utf-8
import time,os

from selenium.webdriver.common.by import By
from pos.base import basepage




class ChargeListPage(basepage.BasePage):
    '''储值模块'''
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<定位器>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 充值撤销链接
    charge_undoLink_loc = (By.XPATH,'//*[@id="chargeRunWater"]/table/tbody/tr[1]/td[16]/span[1]/a')
    charge_undoLinkText_loc = (By.LINK_TEXT,'撤销充值')
    # 确定按钮
    charge_confirmBtn_loc = (By.ID,'confirmBtn')
    # 成功提示
    charge_undoSuccess_loc = (By.XPATH,'//*[@id="showSuccess"]/div/i')
    # 撤销充值后,流程增加一条
    charge_undoStatus_loc = (By.XPATH,'//*[@id="chargeRunWater"]/table/tbody/tr[1]/td[13]/span')
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @property
    def clickUndoLinkText(self):
        """单击 充值撤销链接"""
        self.clickBtn('撤销充值',*(self.charge_undoLinkText_loc))


    @property
    def clickUndoLink(self):
        """单击 充值撤销链接"""
        self.clickBtn('储值撤销',*(self.charge_undoLink_loc))

    @property
    def clickConfirmBtn(self):
        """单击 确定按钮"""
        self.clickBtn('确定',*(self.charge_confirmBtn_loc))


    @property
    def getChargeStatusTxt(self):
        """获取 储值状态文本"""
        txt=self.find_element(*(self.charge_undoStatus_loc)).text
        self.getImage
        return txt

    @property
    def assertCustom(self):
        '''断言进入消费页面'''
        bool_var = self.isExist(*(self.assertPhone))
        self.getImage
        return bool_var

    @property
    def assertUndoSuccess(self):
        '''断言支付成功'''
        self.getImage
        #return self.isExist(*(self.charge_undoSuccess_loc))





if __name__=="__main__":
    pass