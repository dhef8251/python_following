# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:32:16 2019

@author: hmd
"""

import os
os.chdir('C:/Users/hmd/Documents/JI/bokeh/bokeh_tutorial')

# Pandas for data management
import pandas as pd

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# Each tab is drawn by one script
from scripts.histogram import histogram_tab
from scripts.density import density_tab
from scripts.table import table_tab
from scripts.draw_map import map_tab
from scripts.routes import route_tab

# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# Read data into dataframes
flights = pd.read_csv('data/flights.csv', index_col=0).dropna()

# Formatted Flight Delay Data for map
map_data = pd.read_csv('data/flights_map.csv', header=[0, 1], index_col=0)

# Create each of the tabs
tab1 = histogram_tab(flights)
tab2 = density_tab(flights)
tab3 = table_tab(flights)
tab4 = map_tab(map_data, states)
tab5 = route_tab(flights)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5])

# Put the tabs in the current document for display
curdoc().add_root(tabs)
