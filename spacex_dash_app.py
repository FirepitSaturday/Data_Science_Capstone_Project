# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.H2('Select Launch Site:', style={'margin-left':'2em'}),
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label':'All Sites', 'value':'ALL'},
                                                {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                            ],
                                            value='ALL',
                                            placeholder="Launch Site selection",
                                            searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload,max_payload],
                                                marks={0:'0', 3000:'3000', 5000:'5000',
                                                        7000:'7000', max_payload:'10000'},
                                                tooltip={"always_visible":True,"placement":"bottom"},
                                                updatemode='drag'
                                ),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
                )
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df=spacex_df[['Launch Site', 'class']]
        data=filtered_df.groupby(['Launch Site'])['class'].sum().reset_index()
        fig = px.pie(data,values='class',
        names='Launch Site',
        title='Total Successful Launches by Site')
        return fig

    else:
        filtered_df2=spacex_df[['Launch Site', 'class']]
        filtered_df3=filtered_df2[filtered_df2['Launch Site'] == entered_site]
        classdata=pd.get_dummies(filtered_df3['class'])
        classdata=classdata.astype(int)  
        classdata.columns=['Unsuccessful Launches', 'Successful Launches']
        data0=classdata['Unsuccessful Launches'].sum()
        data1=classdata['Successful Launches'].sum()
        data2={'launch': ['Unsuccesful Launches', 'Successful Launches'],
                    'rate': [data0, data1]}
        data=pd.DataFrame(data2)
        fig=px.pie(data, values=('rate'),
        names=('launch'),
        color=['#FF0000','#00FF00'],
        title=(f"Successful Launches at {entered_site}"))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
                )
def get_payload(site, payload):
        if site == 'ALL':
            payload_adf=spacex_df[['Launch Site', 'class', 'Payload Mass (kg)', 'Booster Version','Booster Version Category']]
            payload_adf1=payload_adf[payload_adf['Payload Mass (kg)'] >= payload[0]]
            payload_adf2=payload_adf1[payload_adf1['Payload Mass (kg)'] <= payload[1]]
            fig2=px.scatter(payload_adf2,x='Payload Mass (kg)',y='class', color='Booster Version Category', title='Coorelation between Payload and Success for all Sites')
            return fig2
        else:
            payload_df1=spacex_df[['Launch Site', 'class', 'Payload Mass (kg)', 'Booster Version','Booster Version Category']]
            payload_df2=payload_df1[payload_df1['Launch Site'] == site]
            payload_df3=payload_df2[payload_df2['Payload Mass (kg)'] >= payload[0]]
            payload_df4=payload_df3[payload_df3['Payload Mass (kg)'] <= payload[1]]
            fig2=px.scatter(payload_df4,x='Payload Mass (kg)',y='class', color='Booster Version Category', title=(f"Coorelation between Payload and Success for {site}"))
            return fig2

        
        
        #python3.11 spacex_dash_app.py

# Run the app
if __name__ == '__main__':
    app.run_server()
