import sys
import pandas as pd
import InputVariables, Premium
import csv
import RunConfig
import Projection
import PortfolioProjection
import Reserve
import SimpleTerm
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
  portfolioPath = sys.argv[1]
  mortalityPath = sys.argv[2]
  print("portfolioPath is " + portfolioPath)

  #data = pd.DataFrame.from_csv(portfolioPath)
  data = pd.read_csv(portfolioPath)
  print(data.head())
  print(data.keys())

#  print(data.groupby('age_at_entry')['sum_assured'].describe())

  data = {'apples': 10, 'oranges': 15, 'lemons': 5, 'limes': 20}
  names = list(data.keys())
  values = list(data.values())

  fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
  axs[0].bar(names, values)
  axs[1].scatter(names, values)
  axs[2].plot(names, values)
  fig.suptitle('Categorical Plotting')
  fig.savefig('../media/plots.png')


#  y = np.vstack([data.iloc[:,10], data.iloc[:,6], data.iloc[:,9]])
#  labels = ['Pols_If', 'Annual_prem', 'Sum_assured']
#  fig, ax = plt.subplots()
