from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from get_data import get_data

app = Dash()

# Fetch the data initially to determine the range of dates and hours
df = get_data(1, '2min', 'speed')  # Using '2min' as an example; adjust as needed

if df is not None and not df.empty:
    first_date = df['timestamp'].min().date()
    last_date = df['timestamp'].max().date()
    min_hour = df['timestamp'].min().hour
    max_hour = df['timestamp'].max().hour
else:
    first_date = pd.to_datetime('2024-01-01').date()
    last_date = pd.to_datetime('2024-01-01').date()
    min_hour = 0
    max_hour = 23

app.layout = html.Div([
    html.H1('Time Series Data Visualization'),
    
    # Date Picker with default date range
    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=first_date,
        max_date_allowed=last_date,
        initial_visible_month=first_date,
        date=first_date,
        display_format='YYYY-MM-DD'
    ),
    
    # Hour Range Selector with default values
    html.Div(id='hour-range-container', children=[
        html.Label('Select Hour Range (Optional):'),
        dcc.RangeSlider(
            id='hour-range-slider',
            min=0,
            max=23,
            step=1,
            value=[min_hour, max_hour],
            marks={i: f'{i}:00' for i in range(24)}
        )
    ]),
    
    # Interval Dropdown
    dcc.Dropdown(
        id='interval-dropdown',
        options=[
            {'label': '5 Seconds', 'value': '5s'},
            {'label': '30 Seconds', 'value': '30s'},
            {'label': '2 Minutes', 'value': '2min'},
            {'label': '30 Minutes', 'value': '30min'},
            {'label': '2 Hours', 'value': '2hours'},
        ],
        value='2min',
        clearable=False
    ),
    
    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    [Input('date-picker', 'date'),
     Input('hour-range-slider', 'value'),
     Input('interval-dropdown', 'value')]
)
def update_graph(selected_date, hour_range, interval):
    # Fetch the data
    df = get_data(1, interval, 'speed')

    if df is not None and not df.empty:
        # Filter by the selected date
        selected_date = pd.to_datetime(selected_date)
        df = df[df['timestamp'].dt.date == selected_date.date()]

        # Filter by the selected hour range
        df = df[(df['timestamp'].dt.hour >= hour_range[0]) & (df['timestamp'].dt.hour <= hour_range[1])]

        # Determine the threshold based on the interval
        interval_map = {
            '5s': 5,
            '30s': 30,
            '2min': 120,
            '30min': 1800,
            '2hours': 7200
        }
        threshold = interval_map[interval]  # in seconds

        # Calculate time differences between consecutive points
        df['time_diff'] = df['timestamp'].diff().dt.total_seconds().fillna(0)

        # Split the data into segments based on the threshold
        segments = []
        segment = []
        for i in range(len(df)):
            if df.iloc[i]['time_diff'] <= threshold:
                segment.append((df.iloc[i]['timestamp'], df.iloc[i]['data']))
            else:
                if segment:
                    segments.append(segment)
                    segment = []
                segment.append((df.iloc[i]['timestamp'], df.iloc[i]['data']))
        if segment:
            segments.append(segment)

        # Create the figure
        fig = go.Figure()

        # Plot each segment as a separate line
        for segment in segments:
            segment_df = pd.DataFrame(segment, columns=['timestamp', 'data'])
            fig.add_trace(go.Scatter(
                x=segment_df['timestamp'],
                y=segment_df['data'],
                mode='lines+markers',
                line=dict(color='blue'),
                marker=dict(color='blue', size=6),
                name=f'{interval} Data'
            ))

        fig.update_layout(
            title=f'Speed Data for {interval} Interval on {selected_date.strftime("%Y-%m-%d")} between {hour_range[0]}:00 and {hour_range[1]}:00',
            xaxis_title='Time',
            yaxis_title='Speed',
            xaxis=dict(tickformat="%H:%M:%S")
        )
    else:
        fig = go.Figure()
        fig.update_layout(title='No data available')

    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8051)
