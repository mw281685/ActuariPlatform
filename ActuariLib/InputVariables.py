import numpy as np

class Inputs:
    """ Class storing all inputs: MP, Assumptions, RunConfiguration """

    def __init__(self, policy_tb = None, Global = None):
        self.policy_tb = np.array(policy_tb) 
        self.portfolio_size = len(policy_tb)
        self.Global = Global



class Policy:
    """ Class specifying MP variables """
    count = 0
    def __init__(self, product = None,  age_at_entry = None, sex = None, 
                    entry_year = None, entry_month = None,
                    pol_term_y = None, annual_prem = None, 
                    prem_paybl = None, prem_freq = None, 
                    sum_assured = None, pols_if = None, 
                    init_comm = None, ren_comm = None):
        self.product = product
        self.age_at_entry = age_at_entry
        self.sex = sex
        self.entry_year = entry_year
        self.entry_month = entry_month
        self.pol_term_y = pol_term_y
        self.ann_prem = annual_prem
        self.prem_paybl = prem_paybl 
        self.prem_freq = prem_freq
        self.sum_assured = sum_assured
        self.pols_if = pols_if
        self.init_comm = init_comm
        self.ren_comm = ren_comm
        Policy.count +=1



