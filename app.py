import dash
import dash_bootstrap_components as dbc
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output
import pandas as pd
from dotenv import load_dotenv
import os
import duckdb
assert load_dotenv()

conn = duckdb.connect(f"md:?motherduck_token={os.getenv('MOTHERDUCK_TOKEN')}")
df = conn.sql('use jobhunt;select * from companies.sponsor').to_df().drop(columns='County')

df.rename(columns={'Organisation Name':'CompanyName'},inplace=True)
# Dash app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.VAPOR])

# PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Sponsorship Dashboard", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=1),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
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
                className='w-75',
                children=[
                    dbc.CardHeader(children=[
                        
                    ]),
                    dbc.CardBody(children=[
                        html.H1("Find a Sponsor"),
                        dbc.Row([dbc.Col([
                            dbc.Input(
                            id='search-box', 
                            type='text', 
                            placeholder='Enter company name')
                        ])])
                        ,
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
        filtered_df = df[df['CompanyName'].str.contains(search_term, case=False, regex=True)]
        if filtered_df.shape[0] == 0:
            return html.P('No Result Found')
        table_data = [dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            css=[{"selector": ".row", "rule": "margin: 0; display: block"}],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'FFFFFF'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'FFFFFF'
            },
            )
            ]
        
    else:
        table_data = html.P('No Input Yet')

    return table_data

# AWS deployment setup
INSTANCE_PROD = True  # Set to True for AWS deployment

if INSTANCE_PROD:
    # AWS Elastic Beanstalk configuration and deployment script
    from dash import callback_context

    from flask import Flask
    server = Flask(__name__)

    @server.route('/')
    def hello():
        return 'Hello World'

    if __name__ == '__main__':
        app.run_server(debug=True,host='0.0.0.0', port=8050)
else:
    # Local development setup
    if __name__ == '__main__':
        app.run_server(debug=True)
