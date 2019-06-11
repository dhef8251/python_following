# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:23:57 2019

@author: 350044
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/R3_AEW0001A01C009.csv', engine='python')
specs = pd.read_csv('호선_선표_schedule.csv', engine='python')
tray = pd.read_csv('트레이 표준 정보.csv', engine='python')

specs['K/L일자'] = pd.to_datetime(specs['K/L일자'])
specs['L/C일자'] = pd.to_datetime(specs['L/C일자'])

df['datetime'] = pd.to_datetime(df['datetime'])
df['datetime'].describe()

# get information 
serial_no = df['deviceName'].unique()[0]
tray_name = tray.loc[tray['시리얼 번호'] == serial_no, '트레이'].iloc[0]
product_name = tray.loc[tray['시리얼 번호'] == serial_no, '품  명  및   사   양'].iloc[0]
unit_weight = tray.loc[tray['시리얼 번호'] == serial_no, '표준 단중'].iloc[0]
proper_stock = tray.loc[tray['시리얼 번호'] == serial_no, '적정 재고'].iloc[0]
    
# get date
df['date'] = df['datetime'].apply(lambda x: str(x.date()))    

# stock
df['stock'] = df['weight'] // unit_weight

# usage
df['usage'] = df['stock'].diff().fillna(0)
df.loc[df['usage'] > 0, 'usage'] = 0
df['usage'] = np.abs(df['usage'])

usage_days = df.groupby('date').sum()['usage']
usage_days = usage_days[usage_days > 0]


usage_index = usage_days.index
shiptypes = specs['선종'].unique()
shiptypes = [item.strip(' ') for item in shiptypes]
owner = specs['선주'].unique()
owner = [item.strip(' ') for item in owner]
classification = specs['선급'].unique()
classification = [item.strip(' ') for item in classification]
docks = list(specs['DOCK NO'].unique())

specs['선종'] = specs['선종'].apply(lambda x: x.strip(' '))
specs['선주'] = specs['선주'].apply(lambda x: x.strip(' '))
specs['선급'] = specs['선급'].apply(lambda x: x.strip(' '))



work_per_day = {}

# 총 부피
for idx in usage_index:
    specs_new = specs.loc[(specs['K/L일자'] <= idx) & (specs['L/C일자'] >= idx)]

    work_per_day[idx] = {
                
                'total_length': specs_new['전체길이(L.A.O)'].sum(),
                'total_width': specs_new['폭'].sum(),
                'total_depth': specs_new['깊이'].sum(),
                'total_count': len(specs_new)
                }
            
    # 선종별
    for st in shiptypes:
        tmp_df = specs_new.loc[specs_new['선종'] == st]
        tmp_dict = {
                
                '{}_length'.format(st): tmp_df['전체길이(L.A.O)'].sum(),
                '{}_width'.format(st): tmp_df['폭'].sum(),
                '{}_depth'.format(st): tmp_df['깊이'].sum(),
                '{}_count'.format(st): len(tmp_df)}
        work_per_day[idx].update(tmp_dict)
   
    # 도크별
    for do in docks:
        tmp_df = specs_new.loc[specs_new['DOCK NO'] == do]
        tmp_dict = {
                
                '{}_length'.format(do): tmp_df['전체길이(L.A.O)'].sum(),
                '{}_width'.format(do): tmp_df['폭'].sum(),
                '{}_depth'.format(do): tmp_df['깊이'].sum(),
                '{}_count'.format(do): len(tmp_df)}
        work_per_day[idx].update(tmp_dict)
        
final_df = pd.DataFrame(work_per_day).T
final_df['usage'] = usage_days

final_df.to_csv('make_tree.csv', index=False, encoding='utf-8')

def df_for_tree(datapath):
    
    df = pd.read_csv('data/R3_{}.csv'.format(datapath), engine='python')
    specs = pd.read_csv('호선_선표_schedule.csv', engine='python')
    tray = pd.read_csv('트레이 표준 정보.csv', engine='python')
    
    specs['K/L일자'] = pd.to_datetime(specs['K/L일자'])
    specs['L/C일자'] = pd.to_datetime(specs['L/C일자'])
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['datetime'].describe()
    
    # get information 
    serial_no = df['deviceName'].unique()[0]
    tray_name = tray.loc[tray['시리얼 번호'] == serial_no, '트레이'].iloc[0]
    product_name = tray.loc[tray['시리얼 번호'] == serial_no, '품  명  및   사   양'].iloc[0]
    unit_weight = tray.loc[tray['시리얼 번호'] == serial_no, '표준 단중'].iloc[0]
    proper_stock = tray.loc[tray['시리얼 번호'] == serial_no, '적정 재고'].iloc[0]
        
    # get date
    df['date'] = df['datetime'].apply(lambda x: str(x.date()))    
    
    # stock
    df['stock'] = df['weight'] // unit_weight
    
    # usage
    df['usage'] = df['stock'].diff().fillna(0)
    df.loc[df['usage'] > 0, 'usage'] = 0
    df['usage'] = np.abs(df['usage'])
    
    usage_days = df.groupby('date').sum()['usage']
    usage_days = usage_days[usage_days > 0]
    
    
    usage_index = usage_days.index
    shiptypes = specs['선종'].unique()
    shiptypes = [item.strip(' ') for item in shiptypes]
    owner = specs['선주'].unique()
    owner = [item.strip(' ') for item in owner]
    classification = specs['선급'].unique()
    classification = [item.strip(' ') for item in classification]
    docks = list(specs['DOCK NO'].unique())
    
    specs['선종'] = specs['선종'].apply(lambda x: x.strip(' '))
    specs['선주'] = specs['선주'].apply(lambda x: x.strip(' '))
    specs['선급'] = specs['선급'].apply(lambda x: x.strip(' '))
    
    
    
    work_per_day = {}
    
    # 총 부피
    for idx in usage_index:
        specs_new = specs.loc[(specs['K/L일자'] <= idx) & (specs['L/C일자'] >= idx)]
    
        work_per_day[idx] = {
                    
                    'total_length': specs_new['전체길이(L.A.O)'].sum(),
                    'total_width': specs_new['폭'].sum(),
                    'total_depth': specs_new['깊이'].sum(),
                    'total_count': len(specs_new)
                    }
                
        # 선종별
        for st in shiptypes:
            tmp_df = specs_new.loc[specs_new['선종'] == st]
            tmp_dict = {
                    
                    '{}_length'.format(st): tmp_df['전체길이(L.A.O)'].sum(),
                    '{}_width'.format(st): tmp_df['폭'].sum(),
                    '{}_depth'.format(st): tmp_df['깊이'].sum(),
                    '{}_count'.format(st): len(tmp_df)}
            work_per_day[idx].update(tmp_dict)
       
        # 도크별
        #for do in docks:
         #   tmp_df = specs_new.loc[specs_new['DOCK NO'] == do]
         #  tmp_dict = {
                    
           #         '{}_length'.format(do): tmp_df['전체길이(L.A.O)'].sum(),
           #         '{}_width'.format(do): tmp_df['폭'].sum(),
           #         '{}_depth'.format(do): tmp_df['깊이'].sum(),
           #         '{}_count'.format(do): len(tmp_df)}
           # work_per_day[idx].update(tmp_dict)
            
    final_df = pd.DataFrame(work_per_day).T
    final_df['usage'] = usage_days
    
    final_df.to_csv('make_tree_{}.csv'.format(datapath), index=False, encoding='utf-8')



serials = list(tray['시리얼 번호'])
tmp_list = []
i = 0
for no in serials:
    #path = '19_R1_{}.csv'.format(no)
    tmp_list.append(df_for_tree(no))
    i += 1
    print(i, '--------------is done')



tray[['트레이', '시리얼 번호']].to_csv('serials.csv', index=False, encoding='euc-kr')
