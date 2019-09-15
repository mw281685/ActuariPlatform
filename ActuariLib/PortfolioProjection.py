# Aggregates on the portfolio level
import Projection
import numpy as np
class PortfolioProjection:

    def __init__(self, policy_tb = None, RunConfig = None, Global = None ):
        self.policy_tb = policy_tb
        self.RunConfig = RunConfig
        self.Global = Global

        self.projection_tb = [Projection.ProjectionPP(self.policy_tb[i], self.RunConfig, self.Global) for i in range(len(self.policy_tb))] #run projection for each policy in the portfolio_tb
        
        self.premium_cf_agg = None
        self.premium_cf_PV_agg = None
        
        self.benefit_SURR_agg = None
        self.benefit_SURR_PV_agg = None

        self.benefit_Death_agg = None
        self.benefit_Death_PV_agg = None
        
        self.exp_init_agg = None
        self.exp_init_PV_agg = None

        self.exp_maint_agg = None
        self.exp_maint_PV_agg = None
        
        self.net_insur_CF = None
        

    def runPortfolio(self):
        self.runProjForPortfolio()
        self.premium_cf_agg = np.nansum(np.array([self.projection_tb[i].premium_cf for i in range(len(self.projection_tb))]), axis = 0)
        self.premium_cf_PV_agg =  np.nansum(np.array([self.projection_tb[i].premium_cf_PV for i in range(len(self.projection_tb))]), axis = 0)
    
        self.benefit_SURR_agg = np.nansum(np.array([self.projection_tb[i].benefit_SURR for i in range(len(self.projection_tb))]), axis = 0)
        self.benefit_SURR_PV_agg = np.nansum(np.array([self.projection_tb[i].benefit_SURR_PV for i in range(len(self.projection_tb))]), axis = 0)

        self.benefit_Death_agg = np.nansum(np.array([self.projection_tb[i].benefit_Death for i in range(len(self.projection_tb))]), axis = 0)
        self.benefit_Death_PV_agg = np.nansum(np.array([self.projection_tb[i].benefit_Death_PV for i in range(len(self.projection_tb))]), axis = 0)

        self.exp_init_agg = np.nansum(np.array([self.projection_tb[i].exp_init for i in range(len(self.projection_tb))]), axis = 0)
        self.exp_init_PV_agg = np.nansum(np.array([self.projection_tb[i].exp_init_PV for i in range(len(self.projection_tb))]), axis = 0)

        self.exp_maint_agg = np.nansum(np.array([self.projection_tb[i].exp_maint for i in range(len(self.projection_tb))]), axis = 0)
        self.exp_maint_PV_agg = np.nansum(np.array([self.projection_tb[i].exp_maint_PV for i in range(len(self.projection_tb))]), axis = 0)

        self.net_insur_CF = self.premium_cf_agg - self.benefit_SURR_agg - self.benefit_Death_agg - self.exp_init_agg - self.exp_maint_agg

    def runProjForPortfolio(self):
        for i in range(len(self.projection_tb)):
            self.projection_tb[i].run()
    