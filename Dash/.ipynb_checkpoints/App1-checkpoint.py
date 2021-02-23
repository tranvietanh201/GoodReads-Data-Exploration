# import pandas
import pandas as pd

# load data and preprocess
df = pd.read_csv('Bank_clean.csv')
df_subset = df[['education']]
df_subset = pd.get_dummies(df_subset)
df_subset['job'] = df['job']
df_subset = df_subset.groupby('job').sum()

# list to choose from
education_list = list(df_subset.columns)
job_list = list(df_subset.index)


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
@app.callback(Output('stackedbar', 'figure'),
              [Input('selector1', 'value'), Input('selector2', 'value')])

def update_plot(selector1, selector2):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    
    # STEP 1
    trace = []  
    jobs = []
    
    # STEP 2
    # Draw and append traces for each list
    
    print(selector1)
    if type(selector1) == list:
        for job in selector1:
            print(job)
            jobs.append(job)
    else:
        jobs.append(selector1)
        
    df_selected_job = df_subset.loc[jobs,:]  
    
    if type(selector2) == list:
        for education in selector2:    
            trace.append(go.Bar(name=education,x=jobs,y=list(df_selected_job.loc[:,education])))
    else:
        trace.append(go.Bar(name=str(selector2),x=jobs,y=list(df_selected_job.loc[:,selector2])))
        
    
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
                  barmode='stack',
                  title={'text': 'Education by job', 'font': {'color': 'white'}, 'x': 0.5},
              ),
              }
    return figure


# Define the app
app.layout = html.Div(
    children=[
        html.Div(className='row',  
                 # Define the row element
                 children=[
                     # Define the left element
                     html.Div(className='four columns div-user-controls',
                              children = [
                                  html.H2('Bank Dashboard'),
                                  html.P('''Visualising the education by job'''),
                                  html.P('''Pick job and education from the dropdown below. You can select multiple'''),
                                  # Adding option to select columns
                                  html.Div(className='div-for-dropdown',
                                           children=[
                                               html.P('''Job information'''),
                                               dcc.Dropdown(id='selector1',
                                                            options=[
                                                                {"label": i, "value": i}
                                                                for i in job_list
                                                            ],
                                                            multi=True,
                                                            placeholder="Select job",
                                                            value='blue-collar',
                                                           )
                                           ]
                                          ),
                                  html.Div(className='div-for-dropdown',
                                           children=[
                                               html.P('''Education information'''),
                                               dcc.Dropdown(id='selector2',
                                                            options=[
                                                                {"label": i, "value": i}
                                                                for i in education_list
                                                            ],
                                                            multi=True,
                                                            placeholder="Select education",
                                                            value='education_basic.4y',
                                                           )
                                           ]),
                              ]),
                     
                    
                     # Define the right element
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children = [
                                  dcc.Graph(id='stackedbar',
                                            config={'displayModeBar': False},
                                            animate=True,
                                           )
                              ]),
                     
                     # Define the left element
                     html.Div(className='sixteen columns columns div-user-controls',
                              children = [
                                    html.H2('Bank Dashboard'),
                                    html.P('''Visualising the Consumer price index and the Consumer confidence index by month'''), 
                         ]),
                     
                     # Define the right element
                     html.Div(className='eight columns div-for-charts bg-black',  
                              children = [                                
                                  dcc.Graph(id='scatterplot1',                 
                                            config={'displayModeBar': False},    
                                            animate=True,                             
                                            figure=px.scatter(df,      
                                                              x='cons.price.idx',   
                                                              y='cons.conf.idx', 
                                                              color='month',
                                                              template='plotly_dark').update_layout(   
                                                {'plot_bgcolor': 'rgba(0, 0, 0, 0)',               
                                                 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})             
                                           )                             
                              ]),
                     
                     # Define the left element
                     html.Div(className='sixteen columns columns div-user-controls',
                              children = [
                                  html.H2('Bank Dashboard'),
                                  html.P('''Visualising the previous and campaign by poutcome'''), 
                         ]),
                     
                     # Define the right element
                     html.Div(className='eight columns div-for-charts bg-black',  
                              children = [                                
                                  dcc.Graph(id='bar',                 
                                            config={'displayModeBar': False},    
                                            animate=True,                             
                                            figure=px.bar(df,      
                                                              x='previous',   
                                                              y='campaign', 
                                                              color='poutcome',
                                                        
                                                              template='plotly_dark').update_layout(   
                                                {'plot_bgcolor': 'rgba(0, 0, 0, 0)',               
                                                 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})             
                                           )                             
                              ]),
                     
                         ])
                    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=True)

