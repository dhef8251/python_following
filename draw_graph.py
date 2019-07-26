# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:06:54 2019

@author: 350044
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib as mpl
import matplotlib.font_manager as fm
from sklearn.preprocessing import MinMaxScaler

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Div
from bokeh.layouts import layout, column
from bokeh.models.glyphs import Text
from bokeh.models.markers import Circle


output_file('behaviors_2.html')

path = 'C:/Windows/Fonts/현대체Medium_3.ttf'
fontprop = fm.FontProperties(fname=path, size=10)

df_names = ['제작입고요구일', '의장재', '주요기자재', '제작품', '배관재', '밸브재', '도장재', '후행', '사급', '선행', 'HVS', 'PSI']
dfs = {}

for df_name in df_names:
        
    df = pd.read_csv('협력사 행태 분석_{}.csv'.format(df_name), engine='python')
    df.columns = ['업체명', '행태 1', '행태 2', '행태 3', '행태 4', '발주수량']
    
    df['x좌표'] = ((df['행태 2'] - df['행태 3']) / 4) * 400
    df['y좌표'] = ((df['행태 1'] - df['행태 4']) / 4) * 400
    
    df.columns = ['Company', 'Behavior_1', 'Behavior_2', 'Behavior_3', 'Behavior_4', 'Count', 'X_coordinate', 'Y_coordinate']
    df[['Behavior_1', 'Behavior_2', 'Behavior_3', 'Behavior_4']] = df[['Behavior_1', 'Behavior_2', 'Behavior_3', 'Behavior_4']] * 100
    df[['Behavior_1', 'Behavior_2', 'Behavior_3', 'Behavior_4']] = df[['Behavior_1', 'Behavior_2', 'Behavior_3', 'Behavior_4']].applymap(lambda x: str(round(x, 1)) + ' %')

    counts = df['Count']
    counts = np.array(counts)
    counts = counts.reshape((-1, 1))
    
    scaler = MinMaxScaler(feature_range=(5, 30))
    scaler.fit(counts)
    counts_norm = scaler.transform(counts)
    counts_norm
    df['count_norm'] = counts_norm
        
    dfs[df_name] = df
    
def make_dataset(choice):
    
    return ColumnDataSource(dfs[choice])
    



# bokeh




def make_plot(cds):
    
    

    
    
    
    source = cds
    
    TOOLTIPS = [
            ('Company', '@Company'),
            ('Count', '@Count'),
            ('Behavior 1', '@Behavior_1'),
            ('Behavior 2', '@Behavior_2'),
            ('Behavior 3', '@Behavior_3'),
            ('Behavior 4', '@Behavior_4')
            ]
    
    p = figure(plot_width=1000, plot_height=1000, tooltips=TOOLTIPS)
    
    p.circle('X_coordinate', 'Y_coordinate', size='count_norm', source=source)
    p.patch([0, 100, 0, -100], [100, 0, -100, 0], alpha=0.3, line_width=0)
    
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    
    source_text = ColumnDataSource(dict(x=[-2, 105, -110, -2], y=[103, -2, -2, -108], text=['B1', 'B2', 'B3', 'B4']))
    glyph_text = Text(x='x', y='y', text='text', text_font_style='bold')
    p.add_glyph(source_text, glyph_text)
    
    return p



data_selection = Select(title='선택해', value='전체', options=df_names, sizing_mode='fixed')

desc = Div(text=open("description.html").read())

l = layout([[desc], [data_selection, make_plot(make_dataset('사급'))]], sizing_mode='scale_width')
show(l)








l = layout([[desc], [p]], sizing_mode='scale_width')
show(l)



show(p)

from bokeh.models import ColumnDataSource, Div
from bokeh.layouts import layout, column

l = layout([
    [desc],
    [inputs, p]
], sizing_mode="strectch_width")
desc = Div(text=open("description.html").read())



# 품목
df_origin = pd.read_csv('scheduled_delivery.csv')
partners = list(df['제작협력사'].value_counts().index)

items = list(df_origin['품목구분'].unique())


