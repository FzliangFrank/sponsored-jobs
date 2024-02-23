import dash
import dash_bootstrap_components as dbc
# from dash_iconify import DashIconify
from dash import dcc, html,dash_table,Patch
from dash.dependencies import Input, Output
import pandas as pd
# from dotenv import load_dotenv
import ibis

from ibis import _

from tools import parse_company_cards

# assert load_dotenv()

# AWS deployment setup
INSTANCE_PROD = True  # Set to True for AWS deployment
BUYMECOFFEE={
    # 'type':"text/javascript",
    'src':"https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js",
    **{'data-name':"bmc-button", 
        'data-slug':"fzliangukr",
        'data-color':"#FF5F5F",
        'data-emoji':"" ,
        'data-font':"Bree",
        'data-text':"Buy me a coffee",
        'data-outline-color':"#000000",
        'data-font-color':"#ffffff",
        'data-coffee-color':"#FFDD00"
    }
}

# conn = duckdb.connect(f"md:?motherduck_token={os.getenv('MOTHERDUCK_TOKEN')}")# you may want a GCloud Solution Instead
if INSTANCE_PROD:
    conn=ibis.bigquery.connect(
        project_id='visa-sponsor-uk',
        dataset_id='public'
    )
    tbl=conn.table('public.registered_sponsors')
    # df = conn.sql('select * from public.registered_sponsors').to_pandas().drop(columns='county')
else: 
    df = pd.read_csv('files/2024-02-02_-_Worker_and_Temporary_Worker.csv')\
        .rename(columns={"Organisation Name":"company_name",
                         "Town/City":"location",
                         "County":"county",
                         "Type & Rating":"rating",
                         "Route":"visa_type"
                         })
    tbl=ibis.memtable(df)

tbl=tbl\
    .group_by([_.company_name,_.location,_.county,_.rating])\
    .aggregate(visa_type=_.visa_type.collect())

# df.rename(columns={'Organisation Name':'company_name'},inplace=True)
# Dash app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.ZEPHYR,dbc.icons.FONT_AWESOME])

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Find a Registered Visa Sponsor in UK", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            html.Div(
                html.Script(
                    type="text/javascript",
                    src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js",
                    **{'data-name':"bmc-button", 
                        'data-slug':"fzliangukr",
                        'data-color':"#FF5F5F",
                        'data-emoji':"" ,
                        'data-font':"Bree",
                        'data-text':"Buy me a coffee",
                        'data-outline-color':"#000000",
                        'data-font-color':"#ffffff",
                        'data-coffee-color':"#FFDD00"
                    },
                    hidden=False
                )
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=1),
        ]
    ),
    color="dark",
    dark=True,
)
# App layout
app.index_string = '''
<html>
    <head>
        {%metas%}
        <title></title>
        {%favicon%}
        {%css%}
    </head>

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-C4HD82Y0D3"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-C4HD82Y0D3');
    </script>

    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
app.layout = dbc.Container([
    dcc.Store(id='prev-searched'),
    # dbc.Col([
        navbar,
        dbc.Row(
            [dbc.Card(
                children=[
                    dbc.CardBody(children=[
                        html.H1("Find a UK Visa Sponsor"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(
                                id='search-box', 
                                type='text', 
                                debounce=True,
                                placeholder='Enter company name')
                            ]),
                        ])
                    ]),
                    dbc.CardBody(children=[
                        ## place one ##
                    ])
                ]
            )],align='center',justify='center',className="g-0"
        ),
        ## place two ##
        dbc.Row([
            html.Div([
                dbc.Spinner(html.Div(id='table',style={
                    'overflow-x':'hidden'
                })),
                dbc.Collapse(
                    [
                        html.Br(),
                        dbc.Button('More',id='fetch-more')
                    ],
                    id='button-toggler',
                    is_open=False
                )
            ])
        ],className="g-0")
])

# Callback to update the table based on search input
@app.callback(
    (
        Output('table', 'children'),
        Output('button-toggler','is_open')
    ),
    Input('search-box', 'value'),
    Input('fetch-more','n_clicks'),
    prevent_initial_call=True
)
def update_table(search_term,n_click):
    if search_term:
        # filtered_df = df[df['company_name'].str.contains(search_term, case=False, regex=True)]
        exp=tbl.filter(_.company_name.re_search(search_term))
        if n_click is None or n_click == 0:
            return init_render(exp)
        else:
            return more_render(exp,n_click)
        
    else :
        return (html.P(''), False)#no search term


def init_render(exp):
    max_results=exp.count().to_pandas()
    filtered_df = exp.limit(3).to_pandas()
    additional=f'{max_results} results' if max_results > 3 else ''
    if filtered_df.shape[0] == 0:
        return (html.P('No Result Found'), False)
    
    cards=parse_company_cards(filtered_df)
    content = [
        html.P(additional,style={'color':'grey'}),
        html.Div(cards,style={'padding-top': '10px','padding-bottom':'10px'})#cardbox
    ]
    
    result = (content, max_results > 3)
    return result

def more_render(exp,n_click):
    # # assert n_click !=0,'Not clicked'
    next_df=exp.limit(3, offset=3*n_click).to_pandas()#for now lets not track how many time it has been clicked
    # if next_df.shape[0]
    cards=parse_company_cards(next_df)
    card_box = Patch()#patch seems to have found the first output
    card_box.append(html.Div([html.Br()] + cards))

    if next_df.shape[0] == 3:
        return (card_box, True)
    else:
        return (card_box, False)


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
