import dash
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output
import pandas as pd
# import duckdb

# CSV data
# with duckdb.connect('db/business.db', read_only=True) as con:
#     df = con.sql('''
#     select
#             *,
#             array_to_string(sic_codes,'<br>') as sic_code
#     from sponsor_info
#     ''').to_df().drop(columns='sic_codes')
df = pd.read_csv('2024-02-02_-_Worker_and_Temporary_Worker.csv')
df.rename(columns={'Organisation Name':'CompanyName'},inplace=True)
# Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Input(id='search-box', type='text', 
              placeholder='Enter search term'),
    html.Div(id='table')
])

# Callback to update the table based on search input
@app.callback(
    Output('table', 'children'),
    [Input('search-box', 'value')]
)
def update_table(search_term):
    if search_term:
        filtered_df = df[df['CompanyName'].str.contains(search_term, case=False, regex=True)]
        table_data = dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=15
            )
    else:
        table_data = html.H5('Nothing found')

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
