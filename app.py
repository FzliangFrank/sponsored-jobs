import dash
import dash_bootstrap_components as dbc
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output
import pandas as pd
from dotenv import load_dotenv
import os
import ibis


assert load_dotenv()

# AWS deployment setup
INSTANCE_PROD = True  # Set to True for AWS deployment

# conn = duckdb.connect(f"md:?motherduck_token={os.getenv('MOTHERDUCK_TOKEN')}")# you may want a GCloud Solution Instead
if INSTANCE_PROD:
    conn=ibis.bigquery.connect(
        project_id='visa-sponsor-uk',
        dataset_id='public'
    )
    df = conn.sql('select * from public.registered_sponsors').to_pandas().drop(columns='county')
else: 
    df = pd.read_csv('files/2024-02-02_-_Worker_and_Temporary_Worker.csv')\
        .rename(columns={"Organisation Name":"company_name"})
# df.rename(columns={'Organisation Name':'company_name'},inplace=True)
# Dash app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.ZEPHYR])
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Sponsorship Dashboard", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=1),
        ]
    ),
    color="dark",
    dark=True,
)
# App layout
app.layout = html.Div([
    dbc.Col([
        navbar,
        dbc.Row(
            [dbc.Card(
                children=[
                    dbc.CardBody(children=[
                        html.H1("Find a Sponsor"),
                        dbc.Row([dbc.Col([
                            dbc.Input(
                            id='search-box', 
                            type='text', 
                            placeholder='Enter company name')
                        ])])
                    ]),
                    dbc.CardBody(children=[
                        html.Div(id='table',style={
                            'overflow-x':'hidden'
                        })
                    ])
                ]
            )]
            ,align='center',justify='center'
        )
    ])
])

# Callback to update the table based on search input
@app.callback(
    Output('table', 'children'),
    [Input('search-box', 'value')]
)
def update_table(search_term):
    if search_term:
        filtered_df = df[df['company_name'].str.contains(search_term, case=False, regex=True)]
        if filtered_df.shape[0] == 0:
            return html.P('No Result Found')
        table_data = [dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            css=[{"selector": ".row", "rule": "margin: 0; display: block"}]
            )
            ]
        
    else:
        table_data = html.P('No Input Yet')

    return table_data


if INSTANCE_PROD:
    # AWS Elastic Beanstalk configuration and deployment script
    from dash import callback_context

    from flask import Flask
    server = Flask(__name__)

    @server.route('/')
    def hello():
        return 'Hello World'

    if __name__ == '__main__':
        app.run_server(debug=False,host='0.0.0.0', port=8080)
else:
    # Local development setup
    if __name__ == '__main__':
        app.run_server(debug=True)
