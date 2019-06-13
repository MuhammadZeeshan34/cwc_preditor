import networkx as nx
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from numpy.random import randint

import requests
from bs4 import BeautifulSoup

import pandas as pd
import os, time
import numpy as np
import base64

page = 'http://www.espncricinfo.com/ci/engine/series/1144415.html?view=records'
most_runs = 'http://stats.espncricinfo.com/ci/engine/records/batting/most_runs_career.html?id=12357;type=tournament'
points_table = 'http://www.espncricinfo.com/table/series/8039/season/2019/icc-cricket-world-cup'
fixtures = 'http://www.espncricinfo.com/scores/series/8039/season/2019/icc-cricket-world-cup'
img = 'https://images.pexels.com/photos/67636/rose-blue-flower-rose-blooms-67636.jpeg?auto=format%2Ccompress&cs=tinysrgb&dpr=2&h=750&w=1260'


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://codepen.io/chriddyp/pen/brPBPO.css',
                        'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
                        dbc.themes.BOOTSTRAP
                        ]

states = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False
          , False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

df_table = pd.DataFrame(columns=['Country', 'Matches', 'Won', 'Lost', 'Tie','Points'])

teams_table = {}
response = requests.get(points_table)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find_all('table', class_='standings has-team-logos')[0]
teams = table.find_all('tr', class_='standings-row')
count = 0
for team in teams:
    name = team.find_all('span', class_='team-names')[0].text
    matches = int(team.find_all('td')[1].text)
    won = int(team.find_all('td')[2].text)
    lost = int(team.find_all('td')[3].text)
    tie = int(team.find_all('td')[4].text)
    no_result = int(team.find_all('td')[5].text)
    point = int(team.find_all('td')[6].text)
    df_table.loc[count] = {'Country': name, 'Matches': matches, 'Won': won, 'Lost': lost, 'Tie': tie,
                     'Points': point}
    count += 1

    # Update into local dict
    teams_table[name] = {'Matches': matches, 'Won': won, 'Lost': lost, 'Tie': tie, 'Points': point}


response = requests.get(fixtures)
soup = BeautifulSoup(response.content, 'html.parser')
matches = soup.find_all('div', class_='cscore cscore--pregame cricket cscore--watchNotes')
live_matches = soup.find_all('div', class_='cscore cscore--live cricket cscore--watchNotes')
matches = live_matches + matches
matches_list = []
for match in matches:
    team1 = match.find_all('span', 'cscore_name cscore_name--long')[0].text
    team2 = match.find_all('span', 'cscore_name cscore_name--long')[1].text
    matches_list.append((team1, team2))


server = app.server


server = app.server





app.layout = dbc.Container([

    dbc.Container([

        html.Div([
            html.Div([
                html.Div([

                ], className='col-sm-6 col-md-5 col-lg-6')
            ], className='container')
        ], className='header', style={'background-color': '#D9EDF6', 'height': '110px', 'margin': '3em 0 0.0em 0'}),

        # html.Div([
        #     html.P(id='title',children='Most Runs', style={
        #         'background-color': '#355681',
        #         'color': 'white',
        #         'textAlign': 'center',
        #         'text-shadow': '0 -1px rgba(0,0,0,0.6)',
        #         'border': 'px solid #fff',
        #         'border-radius': '0 10px 0 10px',
        #         'box-shadow': 'inset 0 0 5px rgba(53,86,129, 0.5)',
        #         'line-height': '30px',
        #         'position': 'relative',
        #         'font-weight': 'normal',
        #         'font-family': 'Multi, sans-serif',
        #         'font-size': '15px',
        #         'margin': '0.8em 0 0.5em 0'
        #     }),
        #     html.Div(id='most_runs'
        #              ),
        #     html.Br(),
        # ]),



html.Div([
            html.P(id='predictions',children='Predict Semi Finalists', style={
                'background-color': '#355681',
                'color': 'white',
                'textAlign': 'center',
                'text-shadow': '0 -1px rgba(0,0,0,0.6)',
                'border': 'px solid #fff',
                'border-radius': '0 10px 0 10px',
                'box-shadow': 'inset 0 0 5px rgba(53,86,129, 0.5)',
                'line-height': '30px',
                'position': 'relative',
                'font-weight': 'normal',
                'font-family': 'Multi, sans-serif',
                'font-size': '15px',
                'margin': '0.8em 0 0.5em 0'
            }),
        ]),

        html.Div([
            html.Div(id='radiobuttons', children=[
                dcc.RadioItems(id='fixtures1',
                        options=[
                {'label': matches_list[0][0], 'value': matches_list[0][0]},
                {'label': matches_list[0][1], 'value': matches_list[0][1]},
                {'label': 'Tie or Rain', 'value': 'Tie'}
            ],
            value='Radio',
            labelStyle={'display': 'inline-block'}  ),


        dcc.RadioItems(id='fixtures2',
                        options=[
                {'label': matches_list[1][0], 'value': matches_list[1][0]},
                {'label': matches_list[1][1], 'value': matches_list[1][1]},
                {'label': 'Tie or Rain', 'value': 'tie'}
            ],
            value='Radio',
            labelStyle={'display': 'inline-block'}  ),


        dcc.RadioItems(id='fixtures3',
                        options=[
                {'label': matches_list[2][0], 'value': matches_list[2][0]},
                {'label': matches_list[2][1], 'value': matches_list[2][1]},
                {'label': 'Tie or Rain', 'value': 'tie'}
            ],
            value='Radio',
            labelStyle={'display': 'inline-block'}  ),

        dcc.RadioItems(id='fixtures4',
                       options=[
                           {'label': matches_list[3][0], 'value': matches_list[3][0]},
                           {'label': matches_list[3][1], 'value': matches_list[3][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures5',
                       options=[
                           {'label': matches_list[4][0], 'value': matches_list[4][0]},
                           {'label': matches_list[4][1], 'value': matches_list[4][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures6',
                       options=[
                           {'label': matches_list[5][0], 'value': matches_list[5][0]},
                           {'label': matches_list[5][1], 'value': matches_list[5][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures7',
                       options=[
                           {'label': matches_list[6][0], 'value': matches_list[6][0]},
                           {'label': matches_list[6][1], 'value': matches_list[6][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures8',
                       options=[
                           {'label': matches_list[7][0], 'value': matches_list[7][0]},
                           {'label': matches_list[7][1], 'value': matches_list[7][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures9',
                       options=[
                           {'label': matches_list[8][0], 'value': matches_list[8][0]},
                           {'label': matches_list[8][1], 'value': matches_list[8][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures10',
                       options=[
                           {'label': matches_list[9][0], 'value': matches_list[9][0]},
                           {'label': matches_list[9][1], 'value': matches_list[9][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures11',
                       options=[
                           {'label': matches_list[10][0], 'value': matches_list[10][0]},
                           {'label': matches_list[10][1], 'value': matches_list[10][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures12',
                       options=[
                           {'label': matches_list[11][0], 'value': matches_list[11][0]},
                           {'label': matches_list[11][1], 'value': matches_list[11][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures13',
                       options=[
                           {'label': matches_list[12][0], 'value': matches_list[12][0]},
                           {'label': matches_list[12][1], 'value': matches_list[12][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures14',
                       options=[
                           {'label': matches_list[13][0], 'value': matches_list[13][0]},
                           {'label': matches_list[13][1], 'value': matches_list[13][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures15',
                       options=[
                           {'label': matches_list[14][0], 'value': matches_list[14][0]},
                           {'label': matches_list[14][1], 'value': matches_list[14][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures16',
                       options=[
                           {'label': matches_list[15][0], 'value': matches_list[15][0]},
                           {'label': matches_list[15][1], 'value': matches_list[15][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures17',
                       options=[
                           {'label': matches_list[16][0], 'value': matches_list[16][0]},
                           {'label': matches_list[16][1], 'value': matches_list[16][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),



        dcc.RadioItems(id='fixtures18',
                       options=[
                           {'label': matches_list[17][0], 'value': matches_list[17][0]},
                           {'label': matches_list[17][1], 'value': matches_list[17][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures19',
                       options=[
                           {'label': matches_list[18][0], 'value': matches_list[18][0]},
                           {'label': matches_list[18][1], 'value': matches_list[18][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures20',
                       options=[
                           {'label': matches_list[19][0], 'value': matches_list[19][0]},
                           {'label': matches_list[19][1], 'value': matches_list[19][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures21',
                       options=[
                           {'label': matches_list[20][0], 'value': matches_list[20][0]},
                           {'label': matches_list[20][1], 'value': matches_list[20][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures22',
                               options=[
                                   {'label': matches_list[21][0], 'value': matches_list[21][0]},
                                   {'label': matches_list[21][1], 'value': matches_list[21][1]},
                                   {'label': 'Tie or Rain', 'value': 'tie'}
                               ],
                               value='Radio',
                               labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures23',
                       options=[
                           {'label': matches_list[22][0], 'value': matches_list[22][0]},
                           {'label': matches_list[22][1], 'value': matches_list[22][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures24',
                       options=[
                           {'label': matches_list[23][0], 'value': matches_list[23][0]},
                           {'label': matches_list[23][1], 'value': matches_list[23][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures25',
                       options=[
                           {'label': matches_list[24][0], 'value': matches_list[24][0]},
                           {'label': matches_list[24][1], 'value': matches_list[24][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures26',
                       options=[
                           {'label': matches_list[25][0], 'value': matches_list[25][0]},
                           {'label': matches_list[25][1], 'value': matches_list[25][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures27',
                       options=[
                           {'label': matches_list[26][0], 'value': matches_list[26][0]},
                           {'label': matches_list[26][1], 'value': matches_list[26][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

        dcc.RadioItems(id='fixtures28',
                       options=[
                           {'label': matches_list[27][0], 'value': matches_list[27][0]},
                           {'label': matches_list[27][1], 'value': matches_list[27][1]},
                           {'label': 'Tie or Rain', 'value': 'tie'}
                       ],
                       value='Radio',
                       labelStyle={'display': 'inline-block'}),

                html.Br()
            ], className='three columns'),







            html.Div([
                # dt.DataTable(id='prediction_table',
                #              columns=[{"name": i, "id": i} for i in df_table.columns],
                #
                #              data=df_table.to_dict("rows"),
                #              row_selectable=False,
                #              filtering=False,
                #              sorting=True,
                #              style_table={
                #                  'maxHeight': '350px',
                #                  'overflowY': 'auto',
                #                  'border': 'thin lightgrey solid'
                #              },
                #              style_cell={'textAlign': 'center',
                #                          'font': 10,
                #                          'width': '100px'
                #                          },
                #              style_header={
                #                  'fontWeight': 'bold'
                #              },
                #              style_cell_conditional=[
                #                  {
                #                      'if': {'row_index': 'odd'},
                #                      'backgroundColor': 'rgb(248, 248, 248)'
                #                  }],
                #              ),

        html.Br(),
        html.Br(),

        html.Br(),
            html.Div(id='prediction_table_new'),

            html.Br(),

            html.Button('Reset', id='button', style={'background-color': '#355681',
                                                    'color':'white',
                                                    'textAlign': 'center',
                                                    'text-shadow': '0 -1px rgba(0,0,0,0.6)',
                                                    'border':'px solid #fff',
                                                    'border-radius':'0 10px 0 10px',
                                                    'box-shadow':'inset 0 0 5px rgba(53,86,129, 0.5)',
                                                    'line-height':'30px',
                                                    'position':'relative',
                                                    'font-weight':'normal',
                                                    'font-family':'Multi, sans-serif',
                                                    'font-size': '15px',
                                                    'margin': '0.8em 0 0.5em 0'},
                        ),



            ], className='seven columns'),

        ])

        ])


])


# @app.callback(Output('most_runs','children'),
#               [Input('title', 'children')])
# def get_highest_Score(title):
#
#     df = pd.DataFrame(columns=['Name','Innings', 'Runs'])
#
#     response = requests.get(most_runs)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     table = soup.find_all('table', class_='engineTable')[0]
#     players = table.find_all('tr',class_='data1')
#     count = 0
#     for player in players:
#         if count <= 10:
#             name = player.find_all('td')[0].text
#             innings = player.find_all('td')[1].text
#             runs = player.find_all('td')[4].text
#             df.loc[count] =   {'Name' : name, 'Innings': innings, 'Runs' : runs}
#             count += 1
#
#
#
#     return dt.DataTable(id='table1',
#                         columns=[{"name": i, "id": i} for i in df.columns],
#
#                         data=df.to_dict("rows"),
#                              row_selectable=False,
#                              filtering=False,
#                              sorting=True,
#                              style_table={
#                                 'maxHeight': '350px',
#                                 'overflowY': 'auto',
#                                 'border': 'thin lightgrey solid'
#                             },
#                             style_cell={  'textAlign': 'center',
#                                         'font':10,
#                                           'width': '100px'
#                                           },
#                             style_header={
#                                 'fontWeight': 'bold'
#                             },
#                             style_cell_conditional = [
#                                 {
#                                     'if': {'row_index': 'odd'},
#                                     'backgroundColor': 'rgb(248, 248, 248)'
#                                 }],
#                         )






# @app.callback(Output('fixtures1','children'),
# #               [Input('title', 'children')])
# # def get_fixtures(title):
# #



    # # return dcc.RadioItems(
    # #
    # #         options=[
    # #             {'label': matches_list[0][0], 'value': matches_list[0][0]},
    # #             {'label': matches_list[0][1], 'value': matches_list[0][1]},
    # #             {'label': 'Tie or Rain', 'value': 'tie'}
    # #         ],
    # #         value='Radio',
    # #         labelStyle={'display': 'inline-block'}
    # #     )
    # radios = []
    # for match in matches_list:
    #     radio = dbc.Container([
    #      dcc.RadioItems(
    #
    #         options=[
    #             {'label': match[0], 'value': match[0]},
    #             {'label': match[1], 'value': match[1]},
    #             {'label': 'Tie or Rain', 'value': 'tie'}
    #         ],
    #         value='Radio',
    #         labelStyle={'display': 'inline-block'}
    #     )
    #         ])
    #     radios.append(radio)

    # return radios



def reset_table(n_clicks):
    df_table = pd.DataFrame(columns=['Country', 'Matches', 'Won', 'Lost', 'Tie','Points'])

    teams_table = {}
    response = requests.get(points_table)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table', class_='standings has-team-logos')[0]
    teams = table.find_all('tr', class_='standings-row')
    count = 0
    for team in teams:
        name = team.find_all('span', class_='team-names')[0].text
        matches = int(team.find_all('td')[1].text)
        won = int(team.find_all('td')[2].text)
        lost = int(team.find_all('td')[3].text)
        tie = int(team.find_all('td')[4].text)
        no_result = int(team.find_all('td')[5].text)
        point = int(team.find_all('td')[6].text)
        df_table.loc[count] = {'Country': name, 'Matches': matches, 'Won': won, 'Lost': lost, 'Tie': tie,
                         'Points': point}
        count += 1

    # Update into local dict
        teams_table[name] = {'Matches': matches, 'Won': won, 'Lost': lost, 'Tie': tie, 'Points': point}


    return dt.DataTable(
                columns=[{"name": i, "id": i} for i in df_table.columns],
                data=df_table.to_dict("rows"),
                     row_selectable=False,
                     filtering=False,
                     sorting=True,
                     style_table={
                        'maxHeight': '400px',
                         'maxWidth': 'auto',
                        'overflowY': 'auto',
                        'border': 'thin lightgrey solid'
                    },
                    style_cell={
                              'textAlign': 'center',
                                  'fontSize':15,
                                  'width': '100px',
                                  'fontWeight': 'bold'
                                  },
                    style_header={
                        'fontWeight': 'bold',
                        'fontSize':20,
                    },

                    style_cell_conditional = [
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }],
                       )






def reduce_points(teams, n):

    teams_table[teams[0]]['Matches'] = int(teams_table[teams[0]]['Matches']) - 1
    teams_table[teams[1]]['Matches'] = int(teams_table[teams[1]]['Matches']) - 1
    if states[n] == 'Tie':
        teams_table[teams[0]]['Tie'] = int(teams_table[teams[0]]['Tie']) - 1
        teams_table[teams[1]]['Tie'] = int(teams_table[teams[1]]['Tie']) - 1
        teams_table[teams[0]]['Points'] = int(teams_table[teams[0]]['Points']) - 1
        teams_table[teams[1]]['Points'] = int(teams_table[teams[1]]['Points']) - 1
    if states[n] == teams[0]:
        teams_table[teams[0]]['Points'] = int(teams_table[teams[0]]['Points']) - 2
        teams_table[teams[0]]['Won'] = int(teams_table[teams[0]]['Won']) - 1
        teams_table[teams[1]]['Lost'] = int(teams_table[teams[1]]['Lost']) - 1
    if states[n] == teams[1]:
        teams_table[teams[1]]['Points'] = int(teams_table[teams[1]]['Points']) - 2
        teams_table[teams[1]]['Won'] = int(teams_table[teams[1]]['Won']) - 1
        teams_table[teams[0]]['Lost'] = int(teams_table[teams[0]]['Lost']) - 1


def add_points(teams, n, radio_item):
    for team in teams:
        if radio_item == 'Tie':
            states[n] = radio_item
            teams_table[team]['Tie'] = int(teams_table[team]['Tie']) + 1
            teams_table[team]['Points'] = int(teams_table[team]['Points']) + 1
            teams_table[team]['Matches'] = int(teams_table[team]['Matches']) + 1

        elif team == radio_item:
            states[n] = radio_item
            teams_table[team]['Won'] = int(teams_table[team]['Won']) + 1
            teams_table[team]['Points'] = int(teams_table[team]['Points']) + 2
            teams_table[team]['Matches'] = int(teams_table[team]['Matches']) + 1
        else:
            teams_table[team]['Lost'] = int(teams_table[team]['Lost']) + 1
            teams_table[team]['Matches'] = int(teams_table[team]['Matches']) + 1


@app.callback([Output('fixtures1', 'value'), Output('fixtures2','value'), Output('fixtures3','value'),
               Output('fixtures4', 'value'), Output('fixtures5','value'), Output('fixtures6','value'),
               Output('fixtures7', 'value'), Output('fixtures8','value'), Output('fixtures9','value'),
               Output('fixtures10', 'value'), Output('fixtures11','value'), Output('fixtures12','value'),
               Output('fixtures13', 'value'), Output('fixtures14','value'), Output('fixtures15','value'),
               Output('fixtures16', 'value'), Output('fixtures17','value'), Output('fixtures18','value'),
               Output('fixtures19', 'value'), Output('fixtures20','value'), Output('fixtures21','value'),
               Output('fixtures22', 'value'), Output('fixtures23','value'), Output('fixtures24','value'),
               Output('fixtures25', 'value'), Output('fixtures26','value'), Output('fixtures27','value'),
               Output('fixtures28', 'value')],
              [Input('button','n_clicks')])
def reset_radios(n_click):
    
    return 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio', 'Radio','Radio', 'Radio', 'Radio', 'Radio','Radio', 'Radio', 'Radio', 'Radio','Radio', 'Radio', 'Radio', 'Radio','Radio'




@app.callback(Output('prediction_table_new','children'),
              [Input('button', 'n_clicks'), Input('fixtures1', 'value'),Input('fixtures2', 'value'),Input('fixtures3', 'value')
               ,Input('fixtures4', 'value'),Input('fixtures5', 'value'),Input('fixtures6', 'value')
               ,Input('fixtures7', 'value'),Input('fixtures8', 'value'),Input('fixtures9', 'value')
               ,Input('fixtures10', 'value'),Input('fixtures11', 'value'),Input('fixtures12', 'value')
               ,Input('fixtures13', 'value'),Input('fixtures14', 'value'),Input('fixtures15', 'value')
               ,Input('fixtures16', 'value'),Input('fixtures17', 'value'),Input('fixtures18', 'value'),
               Input('fixtures19', 'value'),Input('fixtures20', 'value'),Input('fixtures21', 'value'),
               Input('fixtures22', 'value'),Input('fixtures23', 'value'),Input('fixtures24', 'value'),
               Input('fixtures25', 'value'),Input('fixtures26', 'value'),Input('fixtures27', 'value'),
               Input('fixtures28', 'value')])
def get_prediction_table(n_clicks, radio_item1, radio_item2, radio_item3, radio_item4,
                         radio_item5, radio_item6, radio_item7, radio_item8,
                         radio_item9, radio_item10, radio_item11, radio_item12,
                         radio_item13, radio_item14, radio_item15, radio_item16,
                         radio_item17, radio_item18, radio_item19, radio_item20,
                         radio_item21, radio_item22, radio_item23, radio_item24,
                         radio_item25, radio_item26, radio_item27, radio_item28
                         ):
    if n_clicks:
        return reset_table(n_clicks)



    df = pd.DataFrame(columns=['Country','Matches', 'Won', 'Lost', 'Tie', 'Points'])

    teams = []
    if radio_item1 != 'Radio':
        n = 0
        radio_item = radio_item1
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)




    if radio_item2 != 'Radio':

        n = 1
        radio_item = radio_item2
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)



    if radio_item3 != 'Radio':

        n = 2
        radio_item = radio_item3
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)



    if radio_item4 != 'Radio':
        n = 3
        radio_item = radio_item4
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item5 != 'Radio':
        n = 4
        radio_item = radio_item5
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)


    if radio_item6 != 'Radio':
        n = 5
        radio_item = radio_item6
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item7 != 'Radio':
        n = 6
        radio_item = radio_item7
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item8 != 'Radio':
        n = 7
        radio_item = radio_item8
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item9 != 'Radio':
        n = 8
        radio_item = radio_item9
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item10 != 'Radio':
        n = 9
        radio_item = radio_item10
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item11 != 'Radio':
        n = 10
        radio_item = radio_item11
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item12 != 'Radio':
        n = 11
        radio_item = radio_item12
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item13 != 'Radio':
        n = 12
        radio_item = radio_item13
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item14 != 'Radio':
        n = 13
        radio_item = radio_item14
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item15 != 'Radio':
        n = 14
        radio_item = radio_item15
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item16 != 'Radio':
        n = 15
        radio_item = radio_item16
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item17 != 'Radio':
        n = 16
        radio_item = radio_item17
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item18 != 'Radio':
        n = 17
        radio_item = radio_item18
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item19 != 'Radio':
        n = 18
        radio_item = radio_item19
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item20 != 'Radio':
        n = 19
        radio_item = radio_item20
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item21 != 'Radio':
        n = 20
        radio_item = radio_item21
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item22 != 'Radio':
        n = 21
        radio_item = radio_item22
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item23 != 'Radio':
        n = 22
        radio_item = radio_item23
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item24 != 'Radio':
        n = 23
        radio_item = radio_item24
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item25 != 'Radio':
        n = 24
        radio_item = radio_item25
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item26 != 'Radio':
        n = 25
        radio_item = radio_item26
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item27 != 'Radio':
        n = 26
        radio_item = radio_item27
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)

    if radio_item28 != 'Radio':
        n = 27
        radio_item = radio_item28
        teams = matches_list[n]

        if states[n] != False:  # Reduce the amount of matches as coming again
            reduce_points(teams, n)

        add_points(teams, n, radio_item)


    count = 0
    for team in teams_table:

        df.loc[count] = {'Country': team, 'Matches': int(teams_table[team]['Matches']), 'Won': int(teams_table[team]['Won']),
                         'Lost': int(teams_table[team]['Lost']),
                               'Tie': int(teams_table[team]['Tie']),
                           'Points': int(teams_table[team]['Points'])}
        count +=1

    df = df.sort_values(by='Points', axis=0, ascending=False)


    table = dt.DataTable(
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict("rows"),
                             row_selectable=False,
                             filtering=False,
                             sorting=True,
                             style_table={
                                'maxHeight': '400px',
                                 'maxWidth': 'auto',
                                'overflowY': 'auto',
                                'border': 'thin lightgrey solid'
                            },
                            style_cell={
                                      'textAlign': 'center',
                                          'fontSize':15,
                                          'width': '100px',
                                          'fontWeight': 'bold'
                                          },
                            style_header={
                                'fontWeight': 'bold',
                                'fontSize':20,
                            },

                            style_cell_conditional = [
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                }],
                        )

    return table




if __name__ == '__main__':
    app.run_server(debug=True, host ='0.0.0.0', port = 8080)
