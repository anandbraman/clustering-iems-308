'''
Script showing my data cleansing and subsetting process.
'''

import pandas as pd
import sqlite3
import plotly.express as px

conn = sqlite3.connect("medicare.db")
c = conn.cursor()
medicare_df = pd.read_table("data/unprocessed/Medicare_Provider_Util_Payment_PUF_CY2017.txt", skiprows=[1])
medicare_df.to_sql('MEDICARE', conn, if_exists='replace', index=False)

c.execute('''select * from MEDICARE where hcpcs_drug_indicator = "Y"''')
cols = list(medicare_df.columns)
asp_drug_df = pd.DataFrame(c.fetchall(), columns=cols)
asp_drug_df.shape

asp_wi = asp_drug_df[asp_drug_df.nppes_provider_state == "WI"]

asp_wi_df = asp_wi.filter(['nppes_credentials','nppes_entity_code', 'provider_type',
              'medicare_participation_indicator', 'place_of_service', 'line_srvc_cnt', 'bene_uniq_cnt',
              'bene_day_srvc_cnt', 'average_Medicare_allowed_amt', 'average_submitted_chrg_amt', 
               'average_Medicare_payment_amt','average_Medicare_standardized_amt'])
asp_wi_hcpcs = asp_wi.filter(['hcpcs_code', 'hcpcs_description'])
asp_wi_hcpcs.to_csv('data/processed/medicare_wi_drug_labels.csv')

entity_code_dummy = pd.get_dummies(asp_wi_df.nppes_entity_code, prefix='entity_code')
medicare_participation_dummy = pd.get_dummies(asp_wi_df.medicare_participation_indicator, prefix='medicare_particip')
place_of_service_dummy = pd.get_dummies(asp_wi_df.place_of_service, prefix='place_of_service')

# nppes_credentials has too many levels to reasonably turn into a categorical var
print(asp_wi_df.groupby('nppes_credentials').size().sort_values())
# going to create a column that captures (MD,M.D.,DO, D.O.) and other. Motivating hypothesis is that perhaps doctors 
# end up resulting in higher Medicare expenditure, or generally higher costs
asp_wi_df['nppes_credentials_2cat'] = ['doctor' if i in ['M.D.', 'MD', 'D.O.', 'DO']
                                       else 'other' for i in asp_wi_df.nppes_credentials]
credential_2cat_dummy = pd.get_dummies(asp_wi_df.nppes_credentials_2cat, prefix='nppes_credentials')

provider_dict = asp_wi_df.groupby('provider_type').size().sort_values().to_dict()

thresh = 0.01*len(asp_wi_df.index)
asp_wi_df['provider_type_reduced'] = [p_type if provider_dict[p_type] >= thresh else 'Other' 
                                      for p_type in asp_wi_df['provider_type']]

provider_type_dummy = pd.get_dummies(asp_wi_df.provider_type_reduced, prefix='provider_type')

dummy_dict = {'nppes_entity_code': [entity_code_dummy], 
             'medicare_participation_indicator':[medicare_participation_dummy], 
                 'place_of_service':[place_of_service_dummy], 
             'nppes_credentials_2cat':[credential_2cat_dummy], 
             'provider_type_reduced':[provider_type_dummy]}

asp_wi_df_final = asp_wi_df
for k, v in dummy_dict.items():
    asp_wi_df_final = asp_wi_df_final.join(v)
    asp_wi_df_final = asp_wi_df_final.drop(k, axis=1)
    
asp_wi_df_final= asp_wi_df_final.drop(['nppes_credentials', 'provider_type'], axis=1)

asp_wi_df_final.to_csv('data/processed/medicare_wi_drug_pricing.csv')