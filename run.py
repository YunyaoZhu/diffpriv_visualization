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


df_test = pd.read_csv(DATA_PATH.joinpath('results_output_r_5runs_35716rows_balance_action.csv.csv'))

'''Initialize Dash'''
server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, server = server, external_stylesheets=external_stylesheets)
# app = dash.Dash(name = __name__, server = server)
app.config.supress_callback_exceptions = True

'''Define colors'''
colors = {
    'background': '#F8FBF9',
    'white': '#ffffff',
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
                    'margin-bottom': 30,
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
        # Control panel
        html.Div(style={
#                         'backgroundColor': colors['white'], 
#                         'padding-left': 20, 
#                         'padding-top': 20
                       }, 
                 children=[
            
            
            html.Div([
                dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Graph settings', value='tab-1'),
                    dcc.Tab(label='Metrics', value='tab-2'),
                ]),
                html.Div(id='tabs-content')
            ]),

            
            
             


        ], className='five columns'),
        
        # AUC graph
        html.Div([
            dcc.Graph(
                id='auc',
            ),
           dcc.Graph(id='race_di'),

           dcc.Graph(id='eth_di'),

           dcc.Graph(id='sex_di'),

        ], className='seven columns'),
        
        
        
    ], className='row'),
    
    
    # DI for race, ethnicity, and sex
#     html.Div([
        
#         html.Div([
#             dcc.Graph(id='race_di')
#         ], className='four columns'),
        
#         html.Div([
#             dcc.Graph(id='eth_di',)
#         ], className='four columns'),
        
#         html.Div([
#             dcc.Graph(id='sex_di')
#         ], className='four columns'),
        
#     ], className='row'),
    
    
    
    # checklist (di metrics)
#     html.Div([
#         dcc.Checklist(
#             id = 'metric-checklist',
#             options=[
#                 {'label': 'Approval', 'value': 'approval'},
#                 {'label': 'False Negative', 'value': 'fn'},
#                 {'label': 'False Positive', 'value': 'fp'}
#             ],
#             values=['approval'],
#             labelStyle={'display': 'inline-block',
#                        'margin-top': 20,
#                         'font-family': 'Helvetica, monospace',
#                           'font-size': 20}
#         ) 
#     ], className='container-fluid'),


], className='ten columns offset-by-one')

'''Callbacks'''
# @app.callback(
#     dash.dependencies.Output('output-container', 'children'),
#     [dash.dependencies.Input('my-dropdown', 'value')])
# def update_output(value):
#     return 'You have selected "{}"'.format(value)

# callback for overall auc

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(style={'padding-top': 20, 'font-family': 'Helvetica, monospace',}, children=[
#             html.P(
#                 "Choose dataset:",
#                 style={'font-family': 'Helvetica, monospace',
#                       'font-size': 20,
#                       'font-weight': 'bold'}
#             ),
            html.H6(
                'Choose dataset(s)',
                style={'font-family': 'Helvetica, monospace',
                      'font-size': 20,
#                       'font-weight': 'bold'
                      }
                
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
#                 value='results_output_r_5runs_35716rows_balance_action.csv.csv'
                placeholder="Select dataset(s)",
            ),
            
#             html.P(
#                 "x-axis type:",
#                 style={'margin-top': 25,
#                       'font-family': 'Helvetica, monospace',
#                       'font-size': 20,
#                       'font-weight': 'bold'}
#             ),
            
            html.H6(
                'x-axis type:',
                style={'font-family': 'Helvetica, monospace',
                      'font-size': 20,
#                       'font-weight': 'bold'
                      }
                
            ),
            
            dcc.RadioItems(
                id = 'xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Log', 'Linear']],
                value='Log',
                labelStyle={'display': 'inline-block',
                           'font-family': 'Helvetica, monospace',
                          'font-size': 20}
            ),
#             html.P(
#                 "Disparte impact metric:",
#                 style={'margin-top': 25,
#                       'font-family': 'Helvetica, monospace',
#                       'font-size': 20,
#                       'font-weight': 'bold'}
#             ),
            html.H6(
                'Disparte impact metric:',
                style={'font-family': 'Helvetica, monospace',
                      'font-size': 20,
#                       'font-weight': 'bold'
                      }
                
            ),
            dcc.Checklist(
                id = 'metric-checklist',
                options=[
                    {'label': 'Approval', 'value': 'approval'},
                    {'label': 'False Negative', 'value': 'fn'},
                    {'label': 'False Positive', 'value': 'fp'}
                ],
                values=['approval'],
                labelStyle={'display': 'inline-block',
                            'font-family': 'Helvetica, monospace',
                              'font-size': 20}
            )
        ])
    elif tab == 'tab-2':
        return html.Div(style={'padding-top': 20, 'font-family': 'Helvetica, monospace',}, children=[
            html.H6(
                'AUC',
                style={'font-family': 'Helvetica, monospace',
                      'font-size': 20,
#                       'font-weight': 'bold'
                      }
                
            ),
            html.P(
                "AUC is the area under the ROC curve. \
                The ROC curve is the receiver operating characteristic curve. \
                AUC is the area between the ROC curve and the x-axis. \
                The closer AUC is to 1, the better the model utility.",
                style={'font-family': 'Helvetica, monospace',
                      'font-size': 18}
            ),
            
            html.H6(
                'Disparate Impact',
                style={'font-family': 'Helvetica, monospace',
                      'font-size': 20,
#                       'font-weight': 'bold'
                      }
                
            ),
            html.P(
                "Disparate impact is the ratio between the probability \
                of an event happening to the protected group and the probability \
                of this event happening to the unprotected group.",
                style={'font-family': 'Helvetica, monospace',
                      'font-size': 18}
            ),
            
            html.Ul([html.Li('1.this is')])
        ])
    
    
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
            'height': 500,
            'title': 'Overall AUC',
            'xaxis' : dict(
                title='Epsilons',
                titlefont=dict(
                family='Helvetica, monospace',
                size=15,
                color='#7f7f7f'
                ),
                type ='linear' if xaxis_type == 'Linear' else 'log',
                autorange='reversed'

            ),
            'yaxis' : dict(
                title='AUC',
                titlefont=dict(
                family='Helvetica, monospace',
                size=15,
                color='#7f7f7f'),
            ),
            'legend_orientation':"h",
            'legend':dict(x=-0, y=-0.8)
            
        }
    }
    return figure



# callback for race di
@app.callback(
    dash.dependencies.Output('race_di', 'figure'),
    [dash.dependencies.Input('dataset-name', 'value'),
     dash.dependencies.Input('dataset-name', 'options'),
     dash.dependencies.Input('metric-checklist', 'values'), 
     dash.dependencies.Input('xaxis-type', 'value')])
def update_image_src(dataset_filename, dataset_options, metric_checklist, xaxis_type):
    data = []
    for filename in dataset_filename:
        index = len(dataset_options)-1
        for i in range(len(dataset_options)):
            dictionary = dataset_options[i]
            if dictionary['value'] == filename:
                index = i
        labelname=dataset_options[index]['label']
        df = pd.read_csv(DATA_PATH.joinpath(filename))

        if 'approval' in metric_checklist:
            data.append({'x': df.eps.values, 'y': df['mean_di_approval_race'].values, 'type': 'line', 'name': 'Approval DI ({})'.format(labelname)})
        if 'fn' in metric_checklist:
            data.append({'x': df.eps.values, 'y': df['mean_di_fn_race'].values, 'type': 'line', 'name': 'False Negative DI ({})'.format(labelname)})
        if 'fp' in metric_checklist:
            data.append({'x': df.eps.values, 'y': df['mean_di_fp_race'].values, 'type': 'line', 'name': 'False Positive DI ({})'.format(labelname)})
            
    figure = {
        'data': data,
        'layout': {
#             'margin': dict(l=0, r=0, b=0, t=0, pad=0),
            'height': 500,
#              'margin': { l: 5, r: 5, b: 5, t: 5, pad: 10},
            'title': 'Race Disparate Impact',
            'xaxis' : dict(
                title='Epsilons',
                titlefont=dict(
                family='Helvetica, monospace',
                size=15,
                color='#7f7f7f'
                ),
                type ='linear' if xaxis_type == 'Linear' else 'log',
                autorange='reversed'
            ),
            'yaxis' : dict(
                title='DI',
                titlefont=dict(
                family='Helvetica, monospace',
                size=15,
                color='#7f7f7f'
                )
            ),
#             'shape': [{type="rect",
#                         x0=0.1,
#                         y0=0.8,
#                         x1=2,
#                         y1=1.2,
#                         line=dict(
#                             color="RoyalBlue",
#                             width=2,
#                         ),
#                         fillcolor="LightSkyBlue",
#                     }
#                 ],
            'legend_orientation':"h",
            'legend':dict(x=0, y=-0.8)
        }
    }
    return figure





# callback for ethnicity di
@app.callback(
    dash.dependencies.Output('eth_di', 'figure'),
    [dash.dependencies.Input('dataset-name', 'value'),
     dash.dependencies.Input('dataset-name', 'options'),
     dash.dependencies.Input('metric-checklist', 'values'), 
     dash.dependencies.Input('xaxis-type', 'value')])
def update_image_src(dataset_filename, dataset_options, metric_checklist, xaxis_type):
    data = []
    for filename in dataset_filename:
        index = len(dataset_options)-1
        for i in range(len(dataset_options)):
            dictionary = dataset_options[i]
            if dictionary['value'] == filename:
                index = i
        labelname=dataset_options[index]['label']
        df = pd.read_csv(DATA_PATH.joinpath(filename))

        if 'approval' in metric_checklist:
            data.append({'x': df.eps.values, 'y': df['mean_di_approval_eth'].values, 'type': 'line', 'name': 'Approval DI ({})'.format(labelname)})
        if 'fn' in metric_checklist:
            data.append({'x': df.eps.values, 'y': df['mean_di_fn_eth'].values, 'type': 'line', 'name': 'False Negative DI ({})'.format(labelname)})
        if 'fp' in metric_checklist:
            data.append({'x': df.eps.values, 'y': df['mean_di_fp_eth'].values, 'type': 'line', 'name': 'False Positive DI ({})'.format(labelname)})
            
    figure = {
        'data': data,
        'layout': {
            'height': 500,
            'title': 'Ethnicity Disparate Impact',
            'xaxis' : dict(
                title='Epsilons',
                titlefont=dict(
                family='Helvetica, monospace',
                size=15,
                color='#7f7f7f'
                ),
                type ='linear' if xaxis_type == 'Linear' else 'log',
                autorange='reversed'

            ),
            'yaxis' : dict(
                title='DI',
                titlefont=dict(
                family='Helvetica, monospace',
                size=15,
                color='#7f7f7f'
                )
            ),
            'legend_orientation':"h",
            'legend':dict(x=0, y=-0.8)
        }
    }
    return figure



# callback for gender di
@app.callback(
    dash.dependencies.Output('sex_di', 'figure'),
    [dash.dependencies.Input('dataset-name', 'value'),
     dash.dependencies.Input('dataset-name', 'options'),
     dash.dependencies.Input('metric-checklist', 'values'), 
     dash.dependencies.Input('xaxis-type', 'value')])
def update_image_src(dataset_filename, dataset_options, metric_checklist, xaxis_type):
    data = []
    for filename in dataset_filename:
        index = len(dataset_options)-1
        for i in range(len(dataset_options)):
            dictionary = dataset_options[i]
            if dictionary['value'] == filename:
                index = i
        labelname=dataset_options[index]['label']
        df = pd.read_csv(DATA_PATH.joinpath(filename))

        if 'approval' in metric_checklist:
            data.append({'x': df.eps.values, 'y': df['mean_di_approval_sex'].values, 'type': 'scatter', 'name': 'Approval DI ({})'.format(labelname)})
        if 'fn' in metric_checklist:
            data.append({'x': df.eps.values, 'y': df['mean_di_fn_sex'].values, 'type': 'line', 'name': 'False Negative DI ({})'.format(labelname)})
        if 'fp' in metric_checklist:
            data.append({'x': df.eps.values, 'y': df['mean_di_fp_sex'].values, 'type': 'line', 'name': 'False Positive DI ({})'.format(labelname)})
    figure = {
        'data': data,
        'layout': {
            'height': 500,
            'title': 'Gender Disparate Impact',
            'xaxis' : dict(
                title='Epsilons',
                titlefont=dict(
                family='Helvetica, monospace',
                size=15,
                color='#7f7f7f'),
                type ='linear' if xaxis_type == 'Linear' else 'log',
                autorange='reversed'
            ),
            'yaxis' : dict(
                title='DI',
                titlefont=dict(
                family='Helvetica, monospace',
                size=15,
                color='#7f7f7f'
                )
            ),
            'legend_orientation':"h",
            'legend':dict(x=0, y=-0.8)
        }
    }
    return figure

