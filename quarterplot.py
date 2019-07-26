# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:19:46 2019

@author: 350044
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib as mpl
import matplotlib.font_manager as fm
%matplotlib inline

path = 'C:/Windows/Fonts/현대체Medium_3.ttf'
fontprop = fm.FontProperties(fname=path, size=50)

df = pd.read_csv('scheduled_delivery.csv')
partners = list(df['제작협력사'].value_counts().index)


df['제작입고요구일'] = pd.to_datetime(df['제작입고요구일'], errors='coerce')
df['HMD입고요구일'] = pd.to_datetime(df['HMD입고요구일'], errors='coerce')
df['배송요구일'] = pd.to_datetime(df['배송요구일'], errors='coerce')
df['최종제작입고예정일'] = pd.to_datetime(df['최종제작입고예정일'], errors='coerce')
df['제작입고일'] = pd.to_datetime(df['제작입고일'], errors='coerce')


# 제작입고요구일이라고 가정

pd.isna(df).sum()

df = df.loc[~pd.isna(df['최종제작입고예정일'])]
df = df.loc[~pd.isna(df['제작입고일'])]
df = df.loc[~pd.isna(df['제작입고요구일'])]


#df = df.loc[df['제작입고요구일'] <= df['최종제작입고예정일']]
#df = df.loc[df['제작입고요구일'] <= df['제작입고일']]
#df = df.loc[df['최종제작입고예정일'] <= df['제작입고일']]



df['입고일 정도'] = (df['제작입고요구일'] - df['제작입고일']).apply(lambda x: x.days)
df['예정일 정도'] = (df['제작입고요구일'] - df['최종제작입고예정일']).apply(lambda x: x.days)

df[['제작입고요구일', '제작입고일', '입고일 정도']].head(20)

df = df.loc[np.abs(df['입고일 정도']) <= 500]
df = df.loc[np.abs(df['예정일 정도']) <= 500]


# 예정일과 입고일이 요구일보다 빠를 수 있다. 다시 수정할 것
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] > 0) & (df['예정일 정도'] == df['입고일 정도']), 'class'] = 'A'
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] > 0) & (df['예정일 정도'] >  df['입고일 정도']), 'class'] = 'B'
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] == 0), 'class'] = 'C' 
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] <  0), 'class'] = 'D'
df.loc[(df['예정일 정도'] == 0) & (df['입고일 정도'] < 0), 'class'] = 'E' 
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] < 0) & (df['예정일 정도'] > df['입고일 정도']), 'class'] = 'F' 
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] < 0) & (df['예정일 정도'] == df['입고일 정도']), 'class'] = 'G' 
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] < 0) & (df['예정일 정도'] < df['입고일 정도']), 'class'] = 'H' 
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] == 0), 'class'] = 'I'
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] >  0), 'class'] = 'J'
df.loc[(df['예정일 정도'] == 0) & (df['입고일 정도'] > 0), 'class'] = 'K'
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] > 0) & (df['예정일 정도'] < df['입고일 정도']), 'class'] = 'L' 
df.loc[(df['예정일 정도'] == 0) & (df['입고일 정도'] == 0), 'class'] = 'M' 

class_to_group = {'A': 'G1', 'I': 'G1', 'J': 'G1', 'K': 'G1', 'L': 'G1', 'M': 'G1',
                  'B': 'G2', 'C': 'G2',
                  'G': 'G3', 'H': 'G3',
                  'D': 'G4', 'E': 'G4', 'F': 'G4'}

df['group'] = df['class'].map(class_to_group)

# 데이터 구분
items = list(df['품목구분'].unique())

passto = pd.read_csv('사급처.csv', engine='python')

df = df.merge(passto, how='left', left_on='사급처', right_on='사급처')

df['stage'] = np.nan

df.loc[df['사외협력사'] == 1, 'stage'] = '사급'
df.loc[(pd.isna(df['stage']))&(df['중일정'].apply(lambda x: x[0]) == 'Z'), 'stage'] = '사급'
df.loc[(pd.isna(df['stage']))&(df['STAGE'] == 'M/UNIT제작 공통'), 'stage'] = '사급'
df.loc[(pd.isna(df['stage']))&(df['STAGE'] == 'GROUP UNIT 제작'), 'stage'] = '사급'

df.loc[(pd.isna(df['stage']))&(df['SHIP_NO'].apply(lambda x: x[:2]) == '10'), 'stage'] = 'PSI'

df.loc[(pd.isna(df['stage']))&(df['SHIP_NO'].apply(lambda x: x[0]) == 'S'), 'stage'] = 'HVS'

df.loc[(pd.isna(df['stage']))&(df['사급처'].isin(['선체가공부', '선체조립부', '대불공장부', '온상공장부', '선행의장부', '용연공장부', '사급처미지정'])), 'stage'] = '선행'
df.loc[(pd.isna(df['stage']))&(pd.isna(df['사급처'])), 'stage'] = '선행'
df.loc[(pd.isna(df['stage']))&(df['중일정'].apply(lambda x: x[4]) == 'H'), 'stage'] = '선행'

df.loc[(pd.isna(df['stage']))&(df['사급처'].isin(['건조1부', '건조2부', '공사지원부', '기계의장부', '도장1부', '도장2부', '선실생산부', '선행도장부', '시운전부', '의장1부', '의장2부'])), 'stage'] = '후행'
df.loc[pd.isna(df['stage']), 'stage'] = '후행'

stages = list(df['stage'].unique())

#

for it in stages:
    df_new = df.loc[df['stage'] == it]
    partners = list(df_new['제작협력사'].value_counts().index)
    
    partners_list = []
    i = 0
    for i, p in enumerate(partners):
        x = df_new.loc[df_new['제작협력사'] == partners[i]].groupby(['group']).size() / len(df_new.loc[df_new['제작협력사'] == partners[i]])
        x.name = partners[i]
        x['count'] = len(df_new.loc[df_new['제작협력사'] == partners[i]])
        partners_list.append(x)
        print(i+1, 'is done / ', len(partners), ' / ', it)
        
    df2 = pd.concat(partners_list, axis=1).T
    df2.head()
    df2.fillna(0, inplace=True)

    df2.replace(0, np.nan, inplace=True)
    df2.dropna(how='all', inplace=True)
    df2.replace(np.nan, 0, inplace=True)
    df2.columns = ['업체명', '행태 1', '행태 2', '행태 3', '행태 4', '발주수량' ]
   
    df2.to_csv('협력사 행태 분석_{}.csv'.format(it), encoding='cp949')
    print('-------------------', it, 'is done')
    
    

df2.replace(0, np.nan, inplace=True)
df2.dropna(how='all', inplace=True)
df2.replace(np.nan, 0, inplace=True)


sns.scatterplot(x='예정일 정도', y='입고일 정도', data=df.loc[df['제작협력사'] == '(주)대천'], hue='group')
plt.xlim(-500, 500)
plt.ylim(-500, 500)
plt.show()

df.loc[df['제작협력사'] == '(주)대천']

# 배송요구일로 가정

pd.isna(df).sum()

df = df.loc[~pd.isna(df['최종제작입고예정일'])]
df = df.loc[~pd.isna(df['제작입고일'])]
df = df.loc[~pd.isna(df['배송요구일'])]


#df = df.loc[df['제작입고요구일'] <= df['최종제작입고예정일']]
#df = df.loc[df['제작입고요구일'] <= df['제작입고일']]
#df = df.loc[df['최종제작입고예정일'] <= df['제작입고일']]



df['입고일 정도'] = (df['배송요구일'] - df['제작입고일']).apply(lambda x: x.days)
df['예정일 정도'] = (df['배송요구일'] - df['최종제작입고예정일']).apply(lambda x: x.days)


df = df.loc[np.abs(df['입고일 정도']) <= 500]
df = df.loc[np.abs(df['예정일 정도']) <= 500]


# 예정일과 입고일이 요구일보다 빠를 수 있다. 다시 수정할 것
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] > 0) & (df['예정일 정도'] == df['입고일 정도']), 'class'] = 'A'
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] > 0) & (df['예정일 정도'] >  df['입고일 정도']), 'class'] = 'B'
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] == 0), 'class'] = 'C' 
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] <  0), 'class'] = 'D'
df.loc[(df['예정일 정도'] == 0) & (df['입고일 정도'] < 0), 'class'] = 'E' 
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] < 0) & (df['예정일 정도'] > df['입고일 정도']), 'class'] = 'F' 
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] < 0) & (df['예정일 정도'] == df['입고일 정도']), 'class'] = 'G' 
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] < 0) & (df['예정일 정도'] < df['입고일 정도']), 'class'] = 'H' 
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] == 0), 'class'] = 'I'
df.loc[(df['예정일 정도'] < 0) & (df['입고일 정도'] >  0), 'class'] = 'J'
df.loc[(df['예정일 정도'] == 0) & (df['입고일 정도'] > 0), 'class'] = 'K'
df.loc[(df['예정일 정도'] > 0) & (df['입고일 정도'] > 0) & (df['예정일 정도'] < df['입고일 정도']), 'class'] = 'L' 
df.loc[(df['예정일 정도'] == 0) & (df['입고일 정도'] == 0), 'class'] = 'M' 


class_to_group = {'A': 'G1', 'I': 'G1', 'J': 'G1', 'K': 'G1', 'L': 'G1', 'M': 'G1',
                  'B': 'G2', 'C': 'G2',
                  'G': 'G3', 'H': 'G3',
                  'D': 'G4', 'E': 'G4', 'F': 'G4'}

df['group'] = df['class'].map(class_to_group)


partners_list = []
i = 0
for i, p in enumerate(partners):
    i += 1
    x = df.loc[df['제작협력사'] == partners[i]].groupby(['group']).size() / len(df.loc[df['제작협력사'] == partners[i]])
    x.name = partners[i]
    x['count'] = len(df.loc[df['제작협력사'] == partners[i]])
    partners_list.append(x)
    print(i, 'is done')
    
df3 = pd.concat(partners_list, axis=1).T
df3.fillna(0, inplace=True)

df3.replace(0, np.nan, inplace=True)
df3.dropna(how='all', inplace=True)
df3.replace(np.nan, 0, inplace=True)

df3.to_csv('협력사 행태 분석_배송요구일.csv', encoding='cp949')
