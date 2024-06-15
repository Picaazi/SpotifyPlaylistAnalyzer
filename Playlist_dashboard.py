import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output

from utils import fetch_data_from_playlist, fetch_query_from_file, fetch_isrc_data
def plot_track_time(data):
    """Plot track time data using plotly."""
    import plotly.express as px
    fig = px.histogram(data,
                       x='track_duration_min',
                       title='Distribution of Track Duration (min)')
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=0.5
        )
    )
    return fig

def plot_track_location(data):
    """Plot track time data using plotly."""
    import plotly.express as px
    fig = px.histogram(data,
                       x='location',
                       title='Distribution of Track Location')
    return fig


# Fetch initial data
track_data = fetch_data_from_playlist('Track.sql', type='file')

track_time_data =  fetch_data_from_playlist("SELECT track_duration_ms * 1.66666667 / 100000 AS track_duration_min FROM Tracks",
                                            type = 'query')

summary_data = fetch_data_from_playlist('PlaylistSummary.sql',type='file')

track_page_size = 10

# Define options for ordering dropdown
order_options = [
    {'label': 'Track Name AESC', 'value': 'Track'},
    {'label': 'Track Name DESC', 'value': 'Track DESC'},
    {'label': 'Track Duration ASEC ', 'value': '[Track Duration (min)]'},
    {'label': 'Track Duration DESC ', 'value': '[Track Duration (min)] DESC'},
    {'label': 'Added Time ASEC', 'value': '[Added Time]'},
    {'label': 'Added Time DESC', 'value': '[Added Time] DESC'},
]

# Define options for page size dropdown
page_size_options = [
    {'label': '10', 'value': 10},
    {'label': '20', 'value': 20},
    {'label': '50', 'value': 50},
    {'label': '100', 'value': 100},
]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the Dash app
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Spotify Playlist Dashboard"), className="mb-4")),

    dbc.Row([
        dbc.Col(html.H4("Playlist Summary"), className="mb-2"),
    ]),

    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='summary-table',
            columns=[{"name": i, "id": i} for i in summary_data.columns],
            data=summary_data.to_dict('records'),
            page_size=5,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'}
        ))
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(
            id='track-time-graph',
            figure= plot_track_time(track_time_data)
        ), width=12)
    ]),

    dbc.Row([
        dbc.Col(html.H4("Tracks Table"), className="mb-2"),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Label("Page Size:"),
                    dcc.Input(
                        id='track-page-size-input',
                        type='number',
                        min=1,
                        placeholder='Enter page size',
                        value=10  # Initial page size
                    ),
                ], width='auto'),  # Adjusts the width automatically
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Label("Order:"), width='auto'),
                        dbc.Col(
                            dcc.Dropdown(
                                id='track-order-dropdown',
                                options=order_options,
                                value='[Added Time] DESC',  # Initial value
                                clearable=False,
                                style={'width': '200px'}  # Adjust width as needed
                            ), width='auto'
                        )
                    ], align="center")
                ], width='auto')
            ], align="center")  # Aligns the internal row elements vertically
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='tracks-table',
            columns=[{"name": i, "id": i} for i in track_data.columns],
            data=track_data.to_dict('records'),
            page_size= track_page_size, #Default page size
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'}
        ))
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(
            id='isrc-graph',
            figure= plot_track_location(fetch_isrc_data())
        ), width=12)
    ]),

    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='tracks-loc-table',
            columns=[{"name": i, "id": i} for i in fetch_isrc_data().columns],
            data=fetch_isrc_data().to_dict('records'),
            page_size= track_page_size, #Default page size
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'}
        ))
    ])
])

# Callback to update the ordering of tracks table
@app.callback(
    Output('tracks-table', 'data'),
    Input('track-order-dropdown', 'value'),
)
def update_tracks_table(order_by):
    # Fetch data with SQL query ordered by selected column
    query = fetch_query_from_file('Track.sql') + "ORDER BY "+order_by+";"
    updated_data = fetch_data_from_playlist(query, type='query')
    return updated_data.to_dict('records')


# Callback to update page size of tracks table
@app.callback(
    Output('tracks-table', 'page_size'),
    Input('track-page-size-input', 'value')
)
def update_page_size(page_size):
    return page_size

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
