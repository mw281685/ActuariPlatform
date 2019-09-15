import numpy as np
import pandas as pd
import InputVariables, Premium
import csv
import RunConfig
import Projection
import PortfolioProjection
import Reserve
import SimpleTerm
import matplotlib.pyplot as plt


#--------- Read Policy input from CSV File --------------------------
Portfolio = []
with open('MP.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        Portfolio.append(InputVariables.Policy(product = row[0],
                                             age_at_entry = int(row[1]),
                                             sex = int(row[2]),   # 1 male , 0 female
                                             entry_year = int(row[3]),
                                             entry_month = int(row[4]),
                                             pol_term_y = int(row[5]),
                                             annual_prem = float(row[6]),
                                             prem_paybl = int(row[7]),
                                             prem_freq = int(row[8]),
                                             sum_assured = float(row[9]),
                                             pols_if = float(row[10]), 
                                             init_comm = float(row[11]), 
                                             ren_comm = float(row[12]) ))


Global = RunConfig.Global(mortality_tb = 'MortTb1.csv')
RunConfig =  RunConfig.RunConfig(proj_start_yr = 2019, proj_start_mth = 1, proj_term = 36)

print("Mortality_tb [24][1] = ", Global.mortality_tb[24][1])
#---------Inputs class test -------------------------------------------
Inputs = InputVariables.Inputs(policy_tb = Portfolio, Global = Global)
#print("Portfolio size is : ", Inputs.portfolio_size)
#print(Inputs.policy_tb[0].product, Inputs.policy_tb[0].age_at_entry, Inputs.policy_tb[0].sex)

#---------ProjectionPP class test --------------------------------------
ProjectionPP = Projection.ProjectionPP(Policy = Portfolio[0], RunConfig = RunConfig, Global = Global)
ProjectionPP.run()


#print("mort_vec = ", ProjectionPP.mort_vec)
#print("mat_vec = ", ProjectionPP.mat_vec)
#print("surr_vec = ", ProjectionPP.surr_vec)
print("polsIF_bop = ", ProjectionPP.polsIF_bop)
#print("polsIF_eop = ", ProjectionPP.polsIF_eop)
#---------PortfolioProjection class test --------------------------------
PortfolioProjection = PortfolioProjection.PortfolioProjection(policy_tb = Portfolio, RunConfig = RunConfig, Global = Global)
PortfolioProjection.runPortfolio()

#--------------------Plot CashFlows ------------------------------------
data = {'NetCashflows': PortfolioProjection.net_insur_CF}
ax = pd.DataFrame(data).plot.line(marker='o', color='r')


fields = ['premium_cf_agg',
        'benefit_SURR_agg',
        'benefit_Death_agg', 
        'exp_init_agg', 
        'exp_maint_agg']

df = pd.DataFrame({fn: getattr(PortfolioProjection, fn) for fn in fields}, columns = fields)
print(df['premium_cf_agg'][0])
df[fields[1:]] = df[fields[1:]].mul(-1)   # Change outflows to negatives
print(df)
df.plot(kind='bar', stacked=True, ax=ax, title=' Cashflows')
plt.show()



#---------- Reserve ------------------------------------------------------
#print("Unearned res =" , [Reserve.Reserve(Portfolio[0]).UnearnedRes(t) for t in range(12)] ) 

#---------- SimpleTerm - inheritance -------------------------------------

SimpleTerm = SimpleTerm.SimpleTerm(Policy = Portfolio[0], RunConfig = RunConfig, Global = Global)
SimpleTerm.run()
#print("SimpleTerm = ", SimpleTerm)
#print("SimpleTerm.PolsIF = ", SimpleTerm.polsIF_bop)

#------------
