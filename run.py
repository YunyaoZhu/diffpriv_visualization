#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''Import Calls'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
import os
import pathlib
import pandas as pd

'''Data path'''
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()


df = pd.read_csv(DATA_PATH.joinpath('results_output_r_5runs_35716rows_balance_action.csv.csv'))

'''Initialize Dash'''
server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, server = server, external_stylesheets=external_stylesheets)
# app = dash.Dash(name = __name__, server = server)
app.config.supress_callback_exceptions = True

'''Define colors'''
colors = {
    'background': '#111111',
    'title': '#02140F',
    'text': '#00A676'
}

'''App layout'''
app.layout = html.Div(children=[
    # title row
    html.Div([
        html.Div([
            html.Img(src="http://www2.cs.duke.edu/web_resources/logo/square/blue/cslogo_square_blue.SMALL.png",
                 style={
#                     'height': '90%',
#                     'width': '90%',
                     "height": "120px",
                    "width": "auto",
                    'float': 'left',
                 },
            ),
        ], className='two columns',),
        
        html.Div([
            html.H5(children='Protecting Individual Privacy', 
                style={
                    'textAlign': 'center',
                    'color': colors['title'],
                    'margin-top': 30,
                    'margin-bottom': 0, 
                    'font-family': 'Helvetica, monospace',
                    'font-size': 40
                    },
                ),
            html.H6(children='Using Differential Privacy', 
                style={
                    'textAlign': 'center',
                    'color': colors['title'],
                    'margin-top': 0,
                    'font-family': 'Helvetica, monospace',
                    'font-size': 20
                    },
                )
        ], className='eight columns'),
        
        
        html.Div([
            html.A(html.Button("Github", id="github-button"),
                   href="https://github.com/cmzou/diffpriv",
                   style={
                       'float': 'right',
                       'margin-top': 30
                   }
            ),
        ], className='two columns'),
               
        
    ], className='row'),
    
    html.Div([
        dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='NYC'
        ),
        html.Div(id='output-container')
    ], className='row')


    
    

])

'''Callbacks'''
@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

