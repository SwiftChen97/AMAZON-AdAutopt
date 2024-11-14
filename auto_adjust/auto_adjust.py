from .sp import SPModule
from .sb import SBModule
from .sd import SDModule

class AutomationAdjustment:
    def __init__(self,file_path):
        self.sp = SPModule(file_path)
        self.sb = SBModule()
        self.sd = SDModule()

    def adjust_all(self, sp_function=None):
        # 调用特定的SP模块函数
        if sp_function:
            self.sp.call_function(sp_function)
        else:
            self.sp.adjust_bid()  # 默认函数
        # 调整其他模块
        self.sb.adjust_sb()
        self.sd.adjust_sd()