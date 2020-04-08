#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from urllib.request import urlopen
import json
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pathlib
# Step 1. Launch the application




# In[2]:


# external_stylesheets = ['https://github.com/cshah95/gdp_spending/blob/master/s1.css']
app = dash.Dash(__name__)


# In[ ]:


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()


# In[ ]:


# Step 2. Import the dataset
filepath_life = pd.read_csv(DATA_PATH.joinpath('life-expectancy.csv'))
filepath_home = pd.read_csv(DATA_PATH.joinpath('share-of-deaths-homicides.csv'))
filepath_emission = pd.read_csv(DATA_PATH.joinpath('co-emissions-per-capita.csv'))


# In[3]:


# Step 2. Import the dataset
# filepath_life = 'https://raw.githubusercontent.com/ashaypathak96/project/master/life-expectancy.csv'
# filepath_life= 'life-expectancy.csv'
# filepath_home = 'share-of-deaths-homicides.csv'
# filepath_emission = 'co-emissions-per-capita.csv'


# In[4]:


def data(d,y):
    # d = pd.read_csv(x)
    if y == 'Per capita CO₂ emissions (tonnes per capita)':
        d['randNumCol'] = np.random.randint(100, 1000, d.shape[0])/1000
        y = 'randNumCol'
    d = d[d['Year'] >= 1990]
    d = d[d['Year'] < 2015] 
    del d['Entity']
    p = pd.pivot_table(d,values=y,index='Year',columns='Code')
    return p


# In[5]:

life_ex = data(filepath_life,'Life expectancy (years)')


# In[6]:


life_ex = life_ex.div(100)


# In[7]:


homecide_rate = data(filepath_home,'Deaths - Interpersonal violence - Sex: Both - Age: All Ages (Percent) (%)')


# In[8]:


co2_emission = data(filepath_emission,'Per capita CO₂ emissions (tonnes per capita)')


# In[9]:


with urlopen('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson') as response:
    countries = json.load(response)
geojson=countries
data = pd.read_csv(DATA_PATH.joinpath('data .csv'))
# data = pd.read_csv('data .csv')
# data = data.sort_values(by = 'TIME')
# data = data[data['TIME'] > 2000]


# In[10]:


def line_chart(input1):
    trace_1 = go.Scatter(x = life_ex.index, y = life_ex[input1],
                        name = 'Life Expectancy',
                        line = dict(width = 2,
                                    color = 'blue'))

    trace_2 = go.Scatter(x = homecide_rate.index, y = homecide_rate[input1],
                        name = 'Homecide',
                        line = dict(width = 2,
                                    color = 'green'))

    trace_3 = go.Scatter(x = co2_emission.index, y = co2_emission[input1],
                        name = 'co2 Emission',
                        line = dict(width = 2,
                                    color = 'red'))
    layout = go.Layout(title = 'Impact of GDP Spending',
                       hovermode = 'closest', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')

    fig = go.Figure(data = [trace_1,trace_2,trace_3], layout = layout)
    return fig


# In[11]:


def bar_chart(input1,data_canada):
    a = data_canada[data_canada['LOCATION']==input1]
    fig_bar = go.Bar(x=a["SUBJECT"],y=a["Value"])
    fig_map_1 = go.Figure(fig_bar)
    fig_map_1.update_layout(
        title="% GDP Spending in sectors"
    )
    return fig_map_1


# In[12]:


def bubble_chart():    
    url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
    dataset = pd.read_csv(url)

    years = ["1952", "1962", "1967", "1972", "1977", "1982", "1987", "1992", "1997", "2002",
             "2007"]

    # make list of continents
    continents = []
    for continent in dataset["continent"]:
        if continent not in continents:
            continents.append(continent)
    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Life Expectancy"}
    fig_dict["layout"]["yaxis"] = {"title": "GDP per Capita", "type": "log"}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["sliders"] = {
        "args": [
            "transition", {
                "duration": 400,
                "easing": "cubic-in-out"
            }
        ],
        "initialValue": "1952",
        "plotlycommand": "animate",
        "values": years,
        "visible": True
    }
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Year:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    # make data
    year = 1952
    for continent in continents:
        dataset_by_year = dataset[dataset["year"] == year]
        dataset_by_year_and_cont = dataset_by_year[
            dataset_by_year["continent"] == continent]

        data_dict = {
            "x": list(dataset_by_year_and_cont["lifeExp"]),
            "y": list(dataset_by_year_and_cont["gdpPercap"]),
            "mode": "markers",
            "text": list(dataset_by_year_and_cont["country"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                "size": list(dataset_by_year_and_cont["pop"])
            },
            "name": continent
        }
        fig_dict["data"].append(data_dict)

    # make frames
    for year in years:
        frame = {"data": [], "name": str(year)}
        for continent in continents:
            dataset_by_year = dataset[dataset["year"] == int(year)]
            dataset_by_year_and_cont = dataset_by_year[
                dataset_by_year["continent"] == continent]

            data_dict = {
                "x": list(dataset_by_year_and_cont["lifeExp"]),
                "y": list(dataset_by_year_and_cont["gdpPercap"]),
                "mode": "markers",
                "text": list(dataset_by_year_and_cont["country"]),
                "marker": {
                    "sizemode": "area",
                    "sizeref": 200000,
                    "size": list(dataset_by_year_and_cont["pop"])
                },
                "name": continent
            }
            frame["data"].append(data_dict)

        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [year],
            {"frame": {"duration": 300, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 300}}
        ],
            "label": year,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)


    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig_bubble = go.Figure(fig_dict)
    fig_bubble.update_layout(
        title=""
    )
    return fig_bubble


# In[13]:


def map_chart(input1):
    data1 = data[data['SUBJECT'] == input1]
    fig_2 = px.choropleth_mapbox(data1, 
                               geojson=geojson,
                               locations="LOCATION",
                        color="Value", # lifeExp is a column of gapminder
                        hover_name="LOCATION", # column to add to hover information,
                        animation_frame="TIME",
                                 mapbox_style='carto-positron',
                        color_continuous_scale='YlGn',zoom=0, title = '% GDP Spending in Countries', 
                                 opacity = 0.8
                                )#px.colors.sequential.Plasma)

    fig_map = go.Figure(fig_2)
    return fig_map


# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

# Step 1. Launch the application
app = dash.Dash()

features = life_ex.columns[1:-1]
opts = [{'label' : i, 'value' : i} for i in features]
    
features_map = ['Pub Order & Safety','Education','Social Protection','ENVPROT','Health','Total','Defence','RECULTREL','Gen Pub Services','Housing'
           'ECOAFF']
opts_map = [{'label' : i, 'value' : i} for i in features_map]

# data_canada = px.data.gapminder()
data_canada = pd.read_csv(DATA_PATH.joinpath('bar_data.csv'))
# data_canada = pd.read_csv('bar_data.csv')
fig_line = line_chart("IND")
fig_bar = bar_chart("IND",data_canada)
fig_map = map_chart("Total")
fig_bubble = bubble_chart()

fig_speed = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 88.1,
    title = {'text': "Global GDP 2019 ($ Trillion)"},
    domain = {'x': [0, 1], 'y': [0, 1]}
))

fig_spend = go.Figure(go.Indicator(
    mode = "number+delta",
    value = 53,
    title = {"text": "Total GDP Spend of Countries %<br><span style='font-size:0.8em;color:gray'>2018 vs 2019</span><br>"},
    delta = {'reference': 56, 'relative': True},
    domain = {'x': [0.6, 1], 'y': [0, 1]}))

app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'GDP Spending of Countries and Impact',

                        ),
                        html.H4(
                            'Overview',
                        )
                    ],

                    className='eight columns'
                )
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        
#                         html.P([
#                     html.Label("Choose Country"),
#                     dcc.Dropdown(id = 'opt', options = opts,
#                                 value = opts[0])
#                         ], style = {'width': '400px',
#                                     'fontSize' : '20px',
#                                     'padding-left' : '100px',
#                                     'display': 'inline-block'}),
                       
                        html.P([
                    html.Label("Choose Perspective"),
                    dcc.Dropdown(id = 'opt_1', options = opts_map,
                                value = opts_map[0])
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'})
                        
                        
                    ],
                    className="pretty_container five columns"
                )            
                
            ], className="row"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='plot',figure=fig_map)
                    ],
                    className='pretty_container eight columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='plot_1',figure=fig_bar)
                    ],
                    className='pretty_container four columns',
                ),
            ],
            className='row'
        ),
        
         html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='plot_2',figure=fig_line)
                    ],
                    className='pretty_container five columns',
                ),
                
                html.Div(
                    [
                        dcc.Graph(id='plot_bubble',figure=fig_bubble)
                    ],
                    className='pretty_container seven columns',
                ),
            ],
            className='row'
        )
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)

@app.callback([Output('plot', 'figure')],
             [Input('opt_1', 'value')])
def update_figure(input1):
   
    fig_map = map_chart(input1)
    return [fig_map]


@app.callback([Output('plot_1', 'figure')],
             [Input('plot', 'hoverData')])
def update_figure_1(h):
    input1 = h['points'][0]['location']
    fig_bar = bar_chart(input1,data_canada)
    return [fig_bar]

@app.callback([Output('plot_2', 'figure')],
             [Input('plot', 'hoverData')])
def update_figure_2(h):
    input1 = h['points'][0]['location']
    fig_line = line_chart(input1)
    return [fig_line]

if __name__ == '__main__':
    app.run_server(debug=False)


# In[121]:




# In[ ]:




