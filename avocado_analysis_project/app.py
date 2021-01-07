from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

# dcc for graphs, tables etc
# html for layout of the page

data = pd.read_csv("./datasets/avocadodataset/avocado.csv")
data = data.query("type == 'conventional' and region == 'Albany'")
data['Date'] = pd.to_datetime(data["Date"], format='%Y-%m-%d')
data.sort_values("Date", inplace=True)


external_stylesheet = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },

    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1",
        "crossorigin": "anonymous"
    },

    {
        "src": "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW",
        "crossorigin": "anonymous",
    }
]

app = Dash(__name__, external_stylesheets=external_stylesheet)
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(children="Region", className='menu-title'),
                dcc.Dropdown(
                    id="region-filter",
                    options=[
                        {"label": region, "value": region}
                        for region in np.sort(data["region"].unique())
                    ],
                    value='Albany',
                    clearable=False,
                    className='dropdown',
                ),

                html.Div(children="Type", className="menu-title"),
                dcc.Dropdown(
                    id="type-filter",
                    options=[
                        {"label": type, "value": type}
                        for type in data.type.unique()
                    ],
                    value="organic",
                    clearable=False,
                    searchable=False,
                    className="dropdown",
                ),

                html.Div(children="Date Range", className="menu-title"),
                dcc.DatePickerRange(
                    id="date-range",
                    start_date=data.Date.min().date(),
                    end_date=data.Date.max().date(),
                    min_date_allowed=data.Date.min().date(),
                    max_date_allowed=data.Date.max().date()
                )

            ],
            className="menu"
        ),
        dcc.Graph(
            config={"displayModeBar": False},
            figure={
                'data': [
                    {
                        "x": data['Date'],
                        "y": data["AveragePrice"],
                        "type": 'lines',
                        "hovertemplate": "$%{y:.2f}"
                        "<extra></extra>"
                    }
                ],
                "layout": {
                    "title": {
                        "text": "Average Price Of Avocados",
                        "x": 0.05,
                        "xanchor": "middle",
                    },
                    "xaxis": {
                        "fixedrange": True
                    },
                    "yaxis": {
                        "tickprefix": '$',
                        # add dolar sign to the tool tip
                        "fixedrange": True,
                    },
                    "colorway": ["#17B897"],
                }
            },
            className="card col-sm-10 col-xs-10 m-auto mt-2",
        ),
        dcc.Graph(
            figure={
                "data": [{
                    "x": data['Date'],
                    "y": data['Total Volume'],
                    "type": 'lines',
                    "hovertemplate": "$%{y:.2f}"
                    "<extra></extra>"
                }],
                "layout": {
                    "title": {
                        "text": "Avocado Sold",
                        "x": 0.05,
                        "xanchor": "left"
                    },
                    "xaxis": {
                        "fixedrange": True,
                    },
                    "yaxis": {
                        "tickprefix": '$',
                        # add dolar sign to the tool tip
                        "fixedrange": True,
                    }
                }
            },
            className="card col-sm-10 m-auto  col-xs-10 mt-4 mb-4"
        )
    ],
    className="wrapper",
)


if __name__ == "__main__":
    app.run_server(debug=True)
