import numpy as np
import Reserve

class ProjectionPP:

    def __init__(self, Policy = None, RunConfig = None, Global = None):
        self.Global = Global
        self.Policy = Policy
        self.RunConfig = RunConfig
        #Decrements
        self.mat_vec = np.zeros(RunConfig.proj_term)
        self.mort_vec = np.zeros(RunConfig.proj_term) 
        self.surr_vec = np.zeros(RunConfig.proj_term) 
        self.polsIF_bop = np.zeros(RunConfig.proj_term)
        self.polsIF_eop = np.zeros(RunConfig.proj_term) 
        #Premium
        self.premium_cf = None
        self.premium_cf_PV = None
        #Benefits
        self.benefit_SURR = None 
        self.benefit_SURR_PV = None
        self.benefit_Death = None
        self.benefit_Death_PV = None
        #Expenses
        self.exp_init = None
        self.exp_init_PV = None 
        self.exp_maint = None
        self.exp_maint_PV = None
        #Comission
        self.init_comm = None
        self.init_comm_PV = None
        self.ren_comm = None
        self.ren_comm_PV = None


    #populate projection vectors:
    def run(self):
        self.runDecrements()
        self.runPremiumIncome()
        self.runBenefits()
        self.runExpenses()
        self.runCommission()

    def runExpenses(self):
        self.exp_init = self.ExpInit()
        self.exp_init_PV = self.ExpInit_PV(0)
        self.exp_maint = self.ExpRen()
        self.exp_maint_PV = self.ExpRen_PV(0)

    def runCommission(self):
        self.init_comm = self.CommInit()
        self.init_comm_PV = self.CommInit_PV(0)
        self.ren_comm = self.CommRen()
        self.ren_comm_PV = self.CommRen_PV(0)

    def runPremiumIncome(self):
        self.premium_cf = self.CalculatePremiumCF()
        self.premium_cf_PV = self.PremCF_PV(0)
        self.benefit_Death = self.BenefitDeath()
        self.benefit_Death_PV = self.BenefitDeath_PV(0)

    def runBenefits(self):
        self.benefit_SURR = self.BenefitSurr()
        self.benefit_SURR_PV = self.BenefitSURR_PV(0)

    def runDecrements(self):
        self.polsIF_bop[0] = self.Policy.pols_if
        for i in range (self.RunConfig.proj_term) :
            self.mat_vec[i] = self.polsIF_bop[i]* self.PolsMaturity(i)
            self.mort_vec[i] = self.polsIF_bop[i]*self.Global.mortality_tb[int(self.AgeAt(i))][int(self.Policy.sex)]
            self.surr_vec[i] = self.polsIF_bop[i]*self.Global.SurrRate(self.PolicyYrAt(i))
            self.polsIF_eop[i] = np.max([self.polsIF_bop[i] - self.mat_vec[i] - self.mort_vec[i] - self.surr_vec[i],0])
            if(i < self.RunConfig.proj_term - 1):
                self.polsIF_bop[i+1] = self.polsIF_eop[i]

    #-------------------------------------------------------------------------
    def ProjStartToMonths(self):
        return self.RunConfig.proj_start_yr*12 +  self.RunConfig.proj_start_mth
    
    def PolicyYrAt(self, t):
        return (self.ProjStartToMonths() - self.PolicyEntryDateToMonts() + t)//12 + 1

    def AgeAt(self, t):
        """Attained age at time t  """
        return self.Policy.age_at_entry + (self.ProjStartToMonths() - self.PolicyEntryDateToMonts() + t)/12


    def SumAssuredAt(self, t):
        """Sum assured per policy at time t """
        if self.IfWithinInsurancePeriod(t): return self.Policy.sum_assured
        return 0

    def PolicyEntryDateToMonts(self):
        return self.Policy.entry_year*12 + self.Policy.entry_month

    def IfWithinInsurancePeriod(self, t):
        return t + self.ProjStartToMonths() - self.PolicyEntryDateToMonts() < self.Policy.pol_term_y*12

    def IfWithinPremiumPeriod(self, t):
        return t + self.ProjStartToMonths() - self.PolicyEntryDateToMonts() <self.Policy.pol_term_y*12

    def IfMaturityTime(self, t):
        return t + self.ProjStartToMonths() - self.PolicyEntryDateToMonts()  == self.Policy.pol_term_y*12

    def IfWithinFirstPolicyYr(self, t):
        return t + self.ProjStartToMonths() - self.PolicyEntryDateToMonts() + 1 < 12

    def IfFirstPolicyMth(self, t):
        return  t + self.ProjStartToMonths() == self.PolicyEntryDateToMonts()

#----------------------NumberOfPolicies-----------
    def PolsIFCalc(self):
        polsIF = np.ones(self.RunConfig.proj_term)*self.Policy.pols_if
        for t in range(1, self.RunConfig.proj_term):
            polsIF[t] = polsIF[t-1] - self.surr_vec[t-1] - self.mort_vec[t-1] - self.mat_vec[t-1]
        return polsIF

    def PolsSurrVector(self):
        """Number of policies: Surrender"""
        return [self.Global.SurrRate(self.PolicyYrAt(t)) for t in range(self.RunConfig.proj_term)]

    def MortalityVector(self):
        return  [self.Global.mortality_tb[int(self.AgeAt(t))][int(self.Policy.sex)] for t in range(self.RunConfig.proj_term)]

    def PolsMaturity(self, t):
        """Number of policies: Maturity"""
        if self.IfMaturityTime(t):
            return 1
        else:
            return 0

    def MaturityVector(self):
        return [self.PolsMaturity(t) for t in range(self.RunConfig.proj_term)]

# -------------------- Income ----------------
    def PremPyblAt(self, t):
        if (self.Policy.prem_freq == 0 and (t + self.ProjStartToMonths()) == self.PolicyEntryDateToMonts()): return self.Policy.prem_paybl
        elif (self.Policy.prem_freq == 0 or self.IfWithinInsurancePeriod(t) == False ): return 0
        elif( self.IfWithinInsurancePeriod(t)):
            if( (t + self.ProjStartToMonths() - self.PolicyEntryDateToMonts())%(12/self.Policy.prem_freq) == 0 ): return self.Policy.prem_paybl
        return 0

    #PremiumIncome
    def CalculatePremiumCF(self):
        prem_cf = [self.PremPyblAt(t) for t in range(self.RunConfig.proj_term)]*self.polsIF_bop
        return prem_cf

    #PremiumIncomePV
    def PremCF_PV(self, t):
        if t >= self.RunConfig.proj_term:
            return 0
        else:
            return self.PremPyblAt(t) + (self.PremCF_PV(t+1) / (1 + self.Global.DiscRate(t)))

#-------------------BENEFITS:-------------------

#------------------BenefitSurr---------------
    def SurrCharge(self):
        """Initial Surrender Charge Rate"""
        fixed_surr_charge = self.Global.SurrChargeFixed(self.Policy.product)
        term_dep_surr_charge = self.Global.SurrChargeFloating(self.Policy.product)
        if fixed_surr_charge is None or term_dep_surr_charge is None:
            raise ValueError('SurrChargeParam not found')          
        return fixed_surr_charge + term_dep_surr_charge * min(self.Policy.pol_term_y / 10, 1)

    def CashValueSurr(self, t):
        """Cash Value as Unearned Premium Reserve """
        return max(Reserve.Reserve(self.Policy).UnearnedRes(t + self.ProjStartToMonths() - self.PolicyEntryDateToMonts())*(1 - self.SurrCharge()), 0)

    def SizeBenefitSurr(self, t):
        """Surrender benefit per policy"""
        return (self.CashValueSurr(t) + self.CashValueSurr(t+1)) / 2

    def BenefitSurr(self):
        """Surrender benefits"""
        return [self.SizeBenefitSurr(t) for t in range(self.RunConfig.proj_term)]* self.surr_vec

    def BenefitSURR_PV(self, t):
        if t>= self.RunConfig.proj_term:
            return 0
        else:
            return self.benefit_SURR[t] + (self.benefit_SURR[t+1]/ (1 + self.Global.DiscRate(t)))

#------------------BenefitDeath--------------
    def SizeBenefitDeath(self, t):
        """Death benefit per policy"""
        return self.SumAssuredAt(t)

    def BenefitDeath(self):
        return [self.SizeBenefitDeath(t) for t in range(self.RunConfig.proj_term)]* self.mort_vec

    def BenefitDeath_PV(self, t):
        if t>= self.RunConfig.proj_term:
            return 0
        else:
            return self.benefit_Death[t] + (self.benefit_Death[t+1]/ (1 + self.Global.DiscRate(t)))

#----------------Expenses---------------------------------

    def ExpInit(self):
     #    """Initial expenses"""
        return self.Global.InitExpensesPP(self.Policy.product) * self.polsIF_bop *[self.IfFirstPolicyMth(t) for t in range(self.RunConfig.proj_term)]

    def ExpInit_PV(self,t):
        if t>= self.RunConfig.proj_term:
            return 0
        else:
            return self.exp_init[t] + (self.exp_init[t+1]/ (1 + self.Global.DiscRate(t)))


    def ExpRen(self):
        return self.Global.RenExpensesPP(self.Policy.product)/12 * self.polsIF_bop *[1- self.IfFirstPolicyMth(t) for t in range(self.RunConfig.proj_term)]

    def ExpRen_PV(self,t):
        if t>= self.RunConfig.proj_term:
            return 0
        else:
            return self.exp_maint[t] + (self.exp_maint[t+1]/ (1 + self.Global.DiscRate(t)))


#----------------Comission -------------------------------
    def ExpsCommInit(self, t):
        """Initial commissions"""
        if (self.IfWithinFirstPolicyYr(t)):
            return self.Policy.init_comm * float(self.polsIF_bop[t])
        else: return 0
    
    
    def CommInit_PV(self,t):
        if t>= self.RunConfig.proj_term:
            return 0
        else:
            return self.init_comm[t] + (self.init_comm[t+1]/ (1 + self.Global.DiscRate(t)))

    
    def ExpsCommRen(self, t):
      #  """Renewal commissions"""
        if (self.IfWithinFirstPolicyYr(t)):
            return 0
        else: return self.Policy.ren_comm* float(self.polsIF_bop[t])

    def CommRen_PV(self,t):
        if t>= self.RunConfig.proj_term:
            return 0
        else:
            return self.ren_comm[t] + (self.ren_comm[t+1]/ (1 + self.Global.DiscRate(t)))

    
    def ExpsCommTotal(self, t):
        """Commissions Total"""
        return self. ExpsCommInit(t) + self.ExpsCommRen(t)

    def CommInit(self):
        return  self.Policy.init_comm*self.Policy.prem_paybl * self.polsIF_bop *[self.IfWithinFirstPolicyYr(t) for t in range(self.RunConfig.proj_term)]

    def CommRen(self):
        return self.Policy.ren_comm * self.Policy.prem_paybl* self.polsIF_bop *[1- self.IfWithinFirstPolicyYr(t) for t in range(self.RunConfig.proj_term)]

#--------------End ----------------------------------------
