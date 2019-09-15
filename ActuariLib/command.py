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


if __name__=="__main__":
    
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