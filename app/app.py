from flask import Flask, render_template, request, jsonify
from sqlite3 import connect
import plotly
import plotly.graph_objs as go
import pandas as pd
import os
import json

app = Flask(__name__)

db_path = os.path.join(os.sep, 'my-pv', 'sensor_data.db')

@app.route('/query_data', methods=['POST'])
def query_data():
    query_type = request.json['query_type']
    df = execute_query(query_type)
    graph = create_plot(df, query_type)
    return jsonify(graph=graph)

def execute_query(query_type):
    conn = connect(db_path)
    if query_type == 'Average Temp and Humidity by Location':
        query = """SELECT s.location, AVG(t.temperature) AS avg_temp, AVG(h.humidity) AS avg_humidity
                   FROM sensor s
                   INNER JOIN temperature_data t ON s.sensor_id = t.sensor_id
                   INNER JOIN humidity_data h ON s.sensor_id = h.sensor_id
                   GROUP BY s.location"""
    elif query_type == 'Latest Logs by Sensor':
        query = """SELECT s.sensor_id, s.location, s.sensor_type, MAX(l.logs_date) AS last_log_date, l.details
                   FROM sensor s
                   INNER JOIN sensor_logs l ON s.sensor_id = l.sensor_id
                   GROUP BY s.sensor_id"""
    else:
        conn.close()
        return pd.DataFrame()

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def create_plot(df, query_type):
    if query_type == 'Average Temp and Humidity by Location':
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['location'], y=df['avg_temp'], name='Avg Temperature'))
        fig.add_trace(go.Bar(x=df['location'], y=df['avg_humidity'], name='Avg Humidity'))
        fig.update_layout(title='Average Temperature and Humidity by Location')
    elif query_type == 'Latest Logs by Sensor':
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='red',
                        align='left'),
            cells=dict(values=[df[k].tolist() for k in df.columns],
                       fill_color='blue',
                       align='left'))])
        fig.update_layout(title='Latest Logs by Sensor')
    else:
        fig = go.Figure()

    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=50000)




