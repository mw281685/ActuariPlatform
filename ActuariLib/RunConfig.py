import numpy as np
class RunConfig:

    def __init__(self, proj_start_yr = None, proj_start_mth = None, proj_term = None):
        self.proj_start_yr = proj_start_yr
        self.proj_start_mth = proj_start_mth
        self.proj_term = proj_term

        


class Global:
    def __init__(self, mortality_tb = None ):
        self.mortality_tb = self.loadMortalityTb(mortality_tb)

    def loadMortalityTb(self, name):
        print(name)
        return np.genfromtxt(name, delimiter=',')
    
    def DiscRate(self, t):
        return 0.05

    def MortFactor(self, t):
        return 1

    def SurrRate(self, policy_yr):
        if policy_yr == 1:
            return 0.1
        elif policy_yr <3:
            return 0.05
        else: return 0.03

    def SurrChargeFixed(self, product):
        if product == 'TRM': return 0
        elif product == 'ENDW' : return 0.01
        else: return 0

    def SurrChargeFloating(self, product):
        if product == 'TRM': return 0
        elif product == 'ENDW' : return 0.005
        else: return 0

    def InitExpensesPP(self, product):
        if product == 'TRM': return 20
        else: return 15
    
    def RenExpensesPP(self, product):
        if product == 'TRM': return 10
        else: return 3
