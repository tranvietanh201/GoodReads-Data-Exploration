# import pandas
import pandas as pd

# load data
data1 = 'Bank_clean.csv'
df = pd.read_csv(data1)
# column list to choose from
column_list = ['age','duration','campaign','emp.var.rate','cons.price.idx','cons.conf.idx','euribor3m']

# import dash
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Initialise the app
app = dash.Dash(__name__)


# Callback for interactive scatterplot
@app.callback(Output('scatterplot', 'figure'),
              [Input('selector1', 'value'), Input('selector2', 'value')])
def update_scatterplot(selector1, selector2):

    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces 
    for year in list(df_sub['age'].unique()):   
        trace.append(go.Scatter(x=df_sub[df_sub['age'] == year][selector1],
                                 y=df_sub[df_sub['age'] == year][selector2],
                                 mode='markers',
                                 name=year,
                                 textposition='bottom center'))  
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  autosize=True,
                  title={'text': 'Scatter Plot base on Consumer Confidence Index and Consumer Price Index', 'font': {'color': 'white'}, 'x': 0.5},
              ),
              }
    return figure


# Define the app
app.layout = html.Div(
    children=[
        html.Div(className='row',  # Define the row element
                 children=[
                     # Define the left element
                     html.Div(className='four columns div-user-controls',
                              children = [
                                  html.H2('Marketing Dashboard'),
                                  html.P('''Visualising the relationship between CPI and CCI'''),
                                  html.P('''This scatter plot illustrate how CPI and CCI of a person interact to each other'''),
                                  # Adding option to select columns
                                  html.Div(className='div-for-dropdown',
                                           children=[
                                               dcc.Dropdown(id='selector1',
                                                            options=[
                                                                {"label": i, "value": i}
                                                                for i in column_list
                                                            ],
                                                            multi=False,
                                                            placeholder="Select x column",
                                                            value='emp.var.rate',
                                                           )
                                           ]
                                          ),
                                  html.Div(className='div-for-dropdown',
                                           children=[
                                               dcc.Dropdown(id='selector2',
                                                            options=[
                                                                {"label": i, "value": i}
                                                                for i in column_list
                                                            ],
                                                            multi=False,
                                                            placeholder="Select y column",
                                                            value='cons.price.idx',
                                                           )
                                           ]
                                          ),
                              ]
                             ),
                     # Define the right element
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children = [
                                  dcc.Graph(id='scatterplot',
                                            config={'displayModeBar': False},
                                            animate=True,
                                            figure=px.scatter(df,
                                                               x='cons.price.idx',
                                                               y='cons.conf.idx',
                                                               color='age',
                                                               template='plotly_dark').update_layout(
                                                 {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                  'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                                           )
                              ]
                             ),
                     
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children = [
                                  dcc.Graph(id='scatterplot1',
                                            config={'displayModeBar': False},
                                            animate=True,
                                            figure=px.scatter(df,
                                                               x='emp.var.rate',
                                                               y='cons.conf.idx',
                                                               color='age',
                                                               template='plotly_dark').update_layout(
                                                 {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                  'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                                           )
                              ]
                             )
                 ]
                )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=True)



