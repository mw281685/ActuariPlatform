class Reserve:
    def __init__(self, Policy=None):
        self.Policy = Policy

    def GrossMathRes(self, t):
        return 0

    
    def UnearnedRes(self, t):
        """Net level premium reserve rate"""
        if self.Policy.prem_freq == 0: 
            earned_mth = t 
            prem_term  = self.Policy.pol_term_y*12
        else: 
            earned_mth = t % (12 / self.Policy.prem_freq)
            prem_term = 12/(self.Policy.prem_freq)
        return self.Policy.prem_paybl*(prem_term - earned_mth - 1)/ prem_term