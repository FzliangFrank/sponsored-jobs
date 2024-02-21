import dash_bootstrap_components as dbc
from dash import html

## table layout
        # result = html.Div(children=[
        #         dash_table.DataTable(
        #         data=filtered_df.to_dict('records'),
        #         columns=[{"name": i, "id": i} for i in tbl.columns],
        #         page_size=10,
        #         css=[{"selector": ".row", "rule": "margin: 0; display: block"}]
        #         ),
        #         html.P(f'{additional}')
        #     ])
def parse_company_cards(filtered_df):
    cards=[]
    for i in range(filtered_df.shape[0]):
        company_name=filtered_df['company_name'][i]
        company_location=filtered_df['location'][i] + ', ' + (filtered_df['county'][i] or '?')
        rating=filtered_df['rating'][i]
        visa=[html.Li(li) for li in filtered_df['visa_type'][i]]
        card = dbc.Card([
            dbc.CardHeader([html.H5(company_name)]),
            dbc.CardBody([
                html.P([
                    html.I(className="fa-solid fa-location-dot", style={"padding-right":"5px"}),
                    company_location
                ],style={'color':'grey'}),
                html.P(rating),
                html.P(visa)
            ])
        ])
        cards += [card]
    return cards