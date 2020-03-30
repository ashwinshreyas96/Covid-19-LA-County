import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import time
import re
import os
import requests
from urllib.parse import quote_plus
from urllib.request import urlopen
from random import randint
from urllib.parse import urljoin
import pandas as pd
import math
import urllib.request
import geopandas
from html.parser import HTMLParser
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import os
import sys
import csv
import reverse_geocoder as rg
from datetime import datetime
import json
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,CustomJS, CustomJSFilter, GeoJSONDataSource, HoverTool,LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure

date=datetime.today().strftime('%B %d,%Y')
day=datetime.today().strftime("%A")
plot_title = day +' '+date

df=pd.read_csv('ncovid19_regions_communities.csv')
mappings={}
population={}
for i in range(len(df)):
    list_of_sub_com=df['All Included Communities'].iloc[i].split(';')
    label=df['City/Community Label'].iloc[i]
    label=label.split('--')[0]
    population[label]=int(df['Combined_Population'].iloc[i])
    for j in list_of_sub_com:
        j=j.lstrip()
        j=j.rstrip()
        mappings[j] = label
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/538.36'}

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

if __name__ == "__main__":
    url='http://www.publichealth.lacounty.gov/media/Coronavirus/locations.htm'
    req=urllib.request.Request(url,headers=hdr)
    html_page=urlopen(req)
    soup = BeautifulSoup(html_page,'html.parser')
    table = soup.find('table', {'class': 'table table-striped table-bordered table-sm'})
    rows = table.find_all('tr')
    df=pd.DataFrame(columns=['name','count'])
    lb_pas=rows[3:5]
    rows=rows[24:]
    rows=rows+lb_pas
    count=0
    for row in rows:
        h=row.find('th')
        r=row.find('td')
        if h is not None and r is not None:
            h=h.text
            r=r.text
            if 'City of ' in h:
                h=h.replace('City of ','')
            if h.startswith('- '):
                h=h.strip('- ')
            if ' - ' in h:
                h=h.split(' - ')
                h='-'.join(h)
            if h =='Under Investigation':
                continue
            if h =='Los Angeles':
                continue
            if '***' in h:
                h=h.replace('***','')
            if '--' in r:
                r=2
            df_row=[h,r]
            df.loc[count]=df_row
            count+=1
    df.to_csv('covid-cases.csv',index=False)

    new_df_dict={}
    pop_dict={}
    #row_count=0
    for i in range(len(df)):
        if df['name'].iloc[i]=='Azuza':
            df['name'].iloc[i]='Azusa'

        if mappings[df['name'].iloc[i]]=='Mt. Washington':
            pop_dict['Mount Washington']=int(population['Mt. Washington'])
            new_df_dict['Mount Washington']=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]]=='Baldwin Hills' or mappings[df['name'].iloc[i]]=='Crenshaw District':
            if 'Baldwin Hills/Crenshaw' not in new_df_dict:
                new_df_dict['Baldwin Hills/Crenshaw']=int(df['count'].iloc[i])
                pop_dict['Baldwin Hills/Crenshaw']=population[mappings[df['name'].iloc[i]]]
            else:
                new_df_dict['Baldwin Hills/Crenshaw']+=int(df['count'].iloc[i])
                pop_dict['Baldwin Hills/Crenshaw']+=population[mappings[df['name'].iloc[i]]]

        elif mappings[df['name'].iloc[i]] == 'Silverlake':
            pop_dict['Silver Lake']=int(population['Silverlake'])
            new_df_dict['Silver Lake']=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]] == 'Vernon Central' or mappings[df['name'].iloc[i]]=='West Vernon':
            if 'Vernon' not in new_df_dict:
                pop_dict['Vernon']=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Vernon']=int(df['count'].iloc[i])
            else:
                pop_dict['Vernon']+=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Vernon']+=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]] == 'West Whittier/Los Nietos':
            pop_dict['West Whittier-Los Nietos']=population[mappings[df['name'].iloc[i]]]
            new_df_dict['West Whittier-Los Nietos']=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]] == 'Temple-Beaudry':
            if 'Temple-Beaudry' in new_df_dict:
                pop_dict['Temple City']=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Temple City']=int(df['count'].iloc[i])
            else:
                pop_dict['Temple City']+=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Temple City']+=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]]=='Melrose':
            if 'Fairfax' not in new_df_dict:
                pop_dict['Fairfax']=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Fairfax']=int(df['count'].iloc[i])
            else:
                pop_dict['Fairfax']+=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Fairfax']+=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]]=='Canyon Country':
            if 'Castaic Canyons' not in new_df_dict:
                pop_dict['Castaic Canyons']=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Castaic Canyons']=int(df['count'].iloc[i])
            else:
                pop_dict['Castaic Canyons']+=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Castaic Canyons']+=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]]=='Wholesale District' or mappings[df['name'].iloc[i]]=='Central':
            if 'Downtown' not in new_df_dict:
                pop_dict['Downtown']=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Downtown']=int(df['count'].iloc[i])
            else:
                pop_dict['Downtown']+=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Downtown']+=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]]=='Little Bangladesh':
            if 'Koreatown' not in new_df_dict:
                pop_dict['Koreatown']=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Koreatown']=int(df['count'].iloc[i])
            else:
                pop_dict['Koreatown']+=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Koreatown']+=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]]=='Crestview' or mappings[df['name'].iloc[i]]=='Miracle Mile' or mappings[df['name'].iloc[i]]=='Park La Brea' or mappings[df['name'].iloc[i]]=='Wilshire Center':
            if 'Mid-Wilshire' not in new_df_dict:
                pop_dict['Mid-Wilshire']=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Mid-Wilshire']=int(df['count'].iloc[i])
            else:
                pop_dict['Mid-Wilshire']+=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Mid-Wilshire']+=int(df['count'].iloc[i])
        elif mappings[df['name'].iloc[i]]=='Santa Monica Mountains':
            if 'Pacific Palisades' not in new_df_dict:
                pop_dict['Pacific Palisades']=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Pacific Palisades']=int(df['count'].iloc[i])
            else:
                pop_dict['Pacific Palisades']+=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Pacific Palisades']+=int(df['count'].iloc[i])

        elif mappings[df['name'].iloc[i]]=='Athens-Westmont':
            if 'Athens' not in new_df_dict:
                pop_dict['Athens']=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Athens']=int(df['count'].iloc[i])
            else:
                pop_dict['Athens']+=population[mappings[df['name'].iloc[i]]]
                new_df_dict['Athens']+=int(df['count'].iloc[i])

        else:
            if mappings[df['name'].iloc[i]] not in new_df_dict:
                pop_dict[mappings[df['name'].iloc[i]]]=population[mappings[df['name'].iloc[i]]]
                new_df_dict[mappings[df['name'].iloc[i]]] = int(df['count'].iloc[i])
            else:
                pop_dict[mappings[df['name'].iloc[i]]]+=population[mappings[df['name'].iloc[i]]]
                new_df_dict[mappings[df['name'].iloc[i]]] += int(df['count'].iloc[i])

    new_df=pd.DataFrame(new_df_dict.items(), columns=['name', 'count'])
    cases_per_10k=[]
    for i in range(len(new_df)):
        cases=(new_df['count'].iloc[i]/pop_dict[new_df['name'].iloc[i]])*10000
        cases_per_10k.append(cases)
    new_df['cases_per_10k']=cases_per_10k

    geo_data = geopandas.read_file("/Users/ashwinshreyasm/Downloads/la-county-neighborhoods-current/l.a._county_neighborhood_(current).shp",encoding='utf-8')
    geo_data.crs = {'init' :'epsg:4269'}
    res=geo_data.merge(new_df,on='name',how='left')
    for i in range(len(res)):
        if math.isnan(res['cases_per_10k'].iloc[i]):
            res['cases_per_10k'].iloc[i] = 0
    res = res.loc[~res['name'].isin(['Avalon', 'Unincorporated Catalina Island'])]
    temp_df=res[['slug','name','count','type','cases_per_10k']].copy()
    not_done_df=new_df.merge(temp_df,how='left',on='name',indicator=True)
    not_done_df=not_done_df[not_done_df['_merge']=='left_only']
    missed_df=not_done_df[['name','count_x','slug','type','cases_per_10k_x']].copy()
    missed_df=missed_df.rename(columns={"count_x":"count","cases_per_10k_x":"cases_per_10k"})
    missed_df.to_csv('missed.csv',index=False)
    for i in range(len(res['name'])):

        res['cases_per_10k'].iloc[i] = float(res['cases_per_10k'].iloc[i])
    new_df.to_csv('covid-join.csv',index=False)

    geosource = GeoJSONDataSource(geojson = res.to_json())

    palette = brewer['Reds'][256]
    palette = palette[::-1]

    color_mapper = LinearColorMapper(palette=palette,low=res['cases_per_10k'].min(),high=res['cases_per_10k'].max())
    color_bar = ColorBar(color_mapper = color_mapper,
                     width = 500, height = 20,
                     border_line_color = None,
                     location = (0,0),
                     orientation = 'horizontal')

    p = figure(title = plot_title,toolbar_location = 'below',tools ='pan, wheel_zoom, box_zoom, reset')
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    neighborhoods = p.patches('xs','ys', source = geosource,fill_color ={'field' :'cases_per_10k','transform' : color_mapper},line_color = 'gray', line_width = 0.1, fill_alpha = 1)
    p.add_tools(HoverTool(renderers = [neighborhoods],tooltips = [('Neighborhood','@name'),('Cases Per 10K','@cases_per_10k')]))
    p.add_layout(color_bar, 'below')
    show(p)
