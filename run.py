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
    ], className='row'),
    
    html.Div([
        # Control panel
        html.Div([
            
            html.P(
                "Choose dataset:",
            ),

            dcc.Dropdown(
                id="dataset-name",
                 options=[{'label': 'Neural Net Balanced by Action', 
                          'value': 'results_nn_4states_balanced_action_cv_output.csv.csv'},
                        {'label': 'Neural Net Balanced by Action+Race', 
                         'value': 'results_nn_4states_balanced_action_race_cv_output.csv.csv'},
                        {'label': 'Neural Net Balanced by Race', 
                         'value': 'results_nn_4states_balanced_race_cv_output.csv.csv'},
                        {'label': 'Neural Net Balanced by Ethnicity', 
                         'value': 'results_nn_4states_balanced_ethni_cv_output.csv.csv'},
                        {'label': 'Neural Net Balanced by Sex', 
                         'value': 'results_nn_4states_balanced_sex_cv_output.csv.csv'},
                        {'label': 'Regression Balanced by Action', 
                         'value': 'results_output_r_50runs_357160rows_balance_action2019-07-23_10-44-00.csv'},
                        {'label': 'Regression Balanced by Action (non-binarized)', 
                         'value': 'results_output_r_50runs_357160rows_balance_action_default_reg2019-07-26_14-51-32.csv'},
                        {'label': 'Regression Balanced by Action+Race', 
                         'value': 'results_output_r_50runs_209040rows_balance_action_race2019-07-22_17-43-09.csv'},
                        {'label': 'Regression Balanced by Race', 
                         'value': 'results_output_r_50runs_322142rows_balance_race2019-07-22_17-56-07.csv'},
                        {'label': 'Regression Balanced by Ethnicity', 
                         'value': 'results_output_r_50runs_99684rows_balance_ethni2019-07-22_17-19-46.csv'},
                        {'label': 'Regression Balanced by Sex', 
                         'value': 'results_output_r_50runs_630450rows_balance_sex2019-07-22_19-31-25.csv'},
                        {'label': 'Regression Balanced by Action (test)', 
                         'value': 'results_output_r_5runs_35716rows_balance_action.csv.csv'},],


                multi=True,
                placeholder="Select a dataset",
            ),
            
            html.P(
                "x-axis type:",
            ),
            dcc.RadioItems(
                id = 'xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Log', 'Linear']],
                value='Log',
                labelStyle={'display': 'inline-block'}
            )  


        ], className='five columns'),
        
        # AUC graph
        html.Div([
            dcc.Graph(
                id='auc',
            )], className='seven columns'),
        
        
        
    ], className='row'),
    
    dcc.Graph(
        id='example-graph',    
        figure={
            'data': [
                {'x': df.eps.values, 'y': df.auc.values, 'type': 'bar', 'name': 'SF'}
#                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
    dcc.Input(id='my-id', value='initial value', type="text"),
    html.Div(id='my-div')


])

'''Callbacks'''
@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

# callback for di vs auc
@app.callback(
    dash.dependencies.Output('auc', 'figure'),
    [dash.dependencies.Input('dataset-name', 'value'),
     dash.dependencies.Input('dataset-name', 'options'),
     dash.dependencies.Input('xaxis-type', 'value')])
def update_image_src(dataset_filename, dataset_options, xaxis_type):
    data = []
    for filename in dataset_filename:
        index = len(dataset_options)-1
        for i in range(len(dataset_options)):
            dictionary = dataset_options[i]
            if dictionary['value'] == filename:
                index = i
        labelname=dataset_options[index]['label']
        df = pd.read_csv(DATA_PATH.joinpath(filename))
        data.append({'x': df.eps.values, 'y': df.auc.values, 'type': 'scatter', 'name': labelname})
        
    figure = {
        'data': data,
        'layout': {
            'title': 'Overall AUC',
            'xaxis' : dict(
                title='Epsilons',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
                ),
                type ='linear' if xaxis_type == 'Linear' else 'log'

            ),
            'yaxis' : dict(
                title='AUC',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'),
            ),
            'legend_orientation':"h",
            'legend':dict(x=-.1, y=-0.6)
            
        }
    }
    return figure

