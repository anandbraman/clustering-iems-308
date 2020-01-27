'''
IEMS 308 Homework 1: Clustering
Anand Raman

This file outputs the means of each column after clustering. 
I analyzed these summary statistics to provide cost saving insights to CMS.

More detailed analysis can be found in the jupyter notebook in the repo. 
'''
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import plotly.express as px
import math
import numpy as np
import matplotlib.pyplot as plt

wi_asp_df = pd.read_csv('data/processed/medicare_wi_drug_pricing.csv')
wi_asp_df = wi_asp_df.iloc[:, 1:28]

wi_df_transform = wi_asp_df.copy()

wi_df_transform['avg_Medicare_allowed_amt_log'] = np.log(wi_df_transform.average_Medicare_allowed_amt)
wi_df_transform['avg_submitted_chrg_amt_log'] = np.log(wi_df_transform.average_submitted_chrg_amt)
wi_df_transform['avg_Medicare_payment_amt_log'] = np.log(wi_df_transform.average_Medicare_payment_amt)
wi_df_transform['line_srvc_cnt_log'] = np.log(wi_df_transform.line_srvc_cnt)
wi_df_transform['bene_day_srvc_cnt_log'] = np.log(wi_df_transform.bene_day_srvc_cnt)

drop_cols = wi_df_transform.filter(regex='bene_day_srvc').columns.tolist()
drop_cols.remove('bene_day_srvc_cnt_log')
wi_df_transform = wi_df_transform.drop(drop_cols, axis=1)

drop_cols = wi_df_transform.filter(regex='line_srvc_cnt').columns.tolist()
drop_cols.remove('line_srvc_cnt_log')
wi_df_transform = wi_df_transform.drop(drop_cols, axis=1)

wi_df_transform = wi_df_transform.drop(['average_Medicare_allowed_amt', 'average_submitted_chrg_amt',
                                        'average_Medicare_payment_amt'], axis=1)

scaler = StandardScaler().fit(wi_df_transform)
wi_df_scaled = scaler.transform(wi_df_transform)

# selected optimal cluster count in clustering jupyter notebook
kmeans = KMeans(n_clusters=16, random_state=3).fit(wi_df_scaled)
finalDf = pd.concat([wi_asp_df, pd.DataFrame(kmeans.labels_, columns=['cluster'])], axis=1)
pd.options.display.max_columns = None

print(finalDf.groupby('cluster').mean())
