import pandas as pd
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import pandas as pd
import numpy as np

app=dash.Dash(__name__)
application=app.server



data1 = pd.read_csv(r'3dScatter.csv')
data = data1.loc[data1['Year'] == 2010]
print(data.head())
x, y, z = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 400).transpose()
print(x)
Lifexp = data.loc[data['Variable'] == 'LIFEXP[0]']
EdYrs = data.loc[data['Variable'] == 'EDYRSAG15[0]']
Income = data.loc[data['Variable'] == 'GDPPCP[0]']

trace1 = go.Scatter3d(
        x=Lifexp['Value'],
        y=EdYrs['Value'],
        z=Income['Value'],
        text=(Lifexp['Country']),
        mode='markers+text',
        textposition='top center',
        textfont=dict(
            size=10
        ),
        marker=dict(
            size=8,


            opacity=0.8
            )

    )
data = [trace1]
layout = go.Layout(title='Exploring Human development using 3D scatterplots',
                       margin=dict(
                           l=0,
                           r=0,
                           b=0,
                           t=0
                       ),
                       scene=dict(yaxis=dict(
                           title='Education years'),
                           xaxis=dict(
                               title='Life expectancy'),
                           zaxis=dict(
                               title='Income'))
                       )

styles = {
    'pre': {
        'border': 'thin lightgrey solid',

    }
}
app.layout=html.Div([html.Div(
    [
        dcc.Markdown(
            '''
            ### Interactive visualization showing analysis of the elements of human development across countries in 2010.
            '''.replace('  ', ''),
            className='eight columns offset-by-three'
        )
    ], className='row',
    style={'text-align': 'center', 'margin-bottom': '10px'}
),

    html.Div([dcc.Graph(id='3dScatter',figure={'data':data,'layout':layout},style={'height':595},
              hoverData={'points': [{'text': 'Angola'}]})],style={'width': '50%', 'float': 'left', 'display': 'inline-block','font':'15','height':'60%'}),

html.Div([
        dcc.Graph(id='time-series-LifeExp')
    ], style={'display': 'inline-block', 'width': '25%','float':'right'}),

html.Div([
        dcc.Graph(id='time-series-Income'),
    ], style={'display': 'inline-block', 'width': '25%','float':'right'}),

html.Div([
        dcc.Graph(id='time-series-Education'),
    ], style={'display': 'inline-block', 'width': '25%','float':'left'}),
])

@app.callback(
    dash.dependencies.Output('3dScatter', 'figure'))

def update_3dScatter():
    data = pd.read_csv(r'3dScatter.csv')
    data = data.loc[data['Year'] == 2010]
    print(data.head())
    x, y, z = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 400).transpose()
    print(x)
    Lifexp = data.loc[data['Variable'] == 'LIFEXP[0]']
    EdYrs = data.loc[data['Variable'] == 'EDYRSAG15[0]']
    Income = data.loc[data['Variable'] == 'GDPPCP[0]']

    trace1 = go.Scatter3d(
        x=Lifexp['Value'],
        y=EdYrs['Value'],
        z=Income['Value'],
        text=(Lifexp['Country']),
        mode='markers+text',
        textposition='top center',
        textfont=dict(
            size=10
        ),
        marker=dict(
            size=8,
            color=(z + x + y) / 3,  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=0.8
            , colorbar=dict(
                title='Colorbar'
            ))

    )
    data = [trace1]
    layout = go.Layout(title='Exploring Human development using 3D scatterplots',
                       margin=dict(
                           l=0,
                           r=0,
                           b=0,
                           t=0
                       ),
                       scene=dict(yaxis=dict(
                           title='Education years'),
                           xaxis=dict(
                               title='Life expectancy'),
                           zaxis=dict(
                               title='Income'))
                       )

    return {'data': data,
            'layout': layout}

update_3dScatter()

@app.callback(
    dash.dependencies.Output('time-series-LifeExp','figure'),
    [dash.dependencies.Input('3dScatter','hoverData')])
def update_time_series(hoverData):
    print('DF Heads')
    years=['1990','1995','2000','2005','2010','2015']
    print(hoverData)
    print(hoverData['points'][0]['text'])
    df=data1[data1['Country']==hoverData['points'][0]['text']]
    df = df.loc[df['Variable'] == 'LIFEXP[0]']
    df=df[df.Year.isin(years)]
    title = '<b>{}</b><br>{}'.format('Life expectancy'," "+str(hoverData['points'][0]['text']))
    return {
        'data': [go.Scatter(
            x=df['Year'],
            y=df['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 400,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.93, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title

            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('time-series-Income','figure'),
    [dash.dependencies.Input('3dScatter','hoverData')])
def update_time_series(hoverData):
    print('DF Heads')
    years=['1990','1995','2000','2005','2010','2015']
    print(hoverData)
    print(hoverData['points'][0]['text'])
    df=data1[data1['Country']==hoverData['points'][0]['text']]
    df = df.loc[df['Variable'] == 'GDPPCP[0]']
    df=df[df.Year.isin(years)]
    title = '<b>{}</b><br>{}'.format('Income level'," "+str(hoverData['points'][0]['text']))
    return {
        'data': [go.Scatter(
            x=df['Year'],
            y=df['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 400,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.93, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title

            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('time-series-Education','figure'),
    [dash.dependencies.Input('3dScatter','hoverData')])
def update_time_series(hoverData):
    print('DF Heads')
    years=['1990','1995','2000','2005','2010','2015']
    print(hoverData)
    print(hoverData['points'][0]['text'])
    df=data1[data1['Country']==hoverData['points'][0]['text']]
    df = df.loc[df['Variable'] == 'EDYRSAG15[0]']
    df=df[df.Year.isin(years)]
    title = '<b>{}</b><br>{}'.format('Education Years'," "+str(hoverData['points'][0]['text']))
    return {
        'data': [go.Scatter(
            x=df['Year'],
            y=df['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 400,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.93, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title

            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }



if __name__ == '__main__':
    # application.run_server(debug=True)
    application.run(debug=True)
