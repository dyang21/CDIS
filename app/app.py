from flask import Flask, render_template
from sqlite3 import connect
from sqlite3 import OperationalError, DatabaseError, ProgrammingError
from pandas import read_sql_query, DataFrame
from typing import Union
import plotly
import plotly.graph_objs as go
import os

app = Flask(__name__)

db_path = os.path.join(os.sep, 'my-pv', 'sensor_data.db')

<<<<<<< HEAD
def get_data():
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    conn = sqlite3.connect('sensor_data.db')
=======
    conn = connect(db_path)
>>>>>>> 9639a73 (Added pytest for processor and generator)
    query = "SELECT * FROM sensor_data"
    df = read_sql_query(query, conn)
    conn.close()
=======
=======
=======
def get_data() -> Union[DataFrame, None]:
>>>>>>> cc4ef0e (Added type hinting and return value.)
    """
    Fetch sensor dataframe from the SQLite database.

    This function attempts to connect to a SQLite database, and fetches all records 
    from the `sensor_data` table. 

    Returns:
        df: A pandas dataframe containing sensor data if successful. None otherwise.
                   
    Raises:
        OperationalError: Issues related to the operational aspect of the database.
        ProgrammingError: SQL related errors, e.g., syntax errors.
        DatabaseError: General class of errors for database-related issues.
    """
>>>>>>> 241748b (Finished docstrings. Fixed some indentations fro ci-cd)
    conn = None
    try:
        conn = connect(db_path)
        query = "SELECT * FROM sensor_data"
        df = read_sql_query(query, conn)
    except OperationalError as e:
        print(f"Operational error in database connection: {str(e)}")
        return None
    except ProgrammingError as e:
        print(f"Programming error in database {str(e)}")
        return None
    except DatabaseError as e:
        print(f"General database error: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
>>>>>>> 362f3b6 (added specific error handling try blocks low in scope. next is to render error page)
    return df


def create_plot():
    """
    Create a plot of sensor data.

    This function fetches the sensor data using the get_data() function, 
    and then creates a plot with temperature and humidity traces.

    Returns:
        Figure: A plotly Figure object if successful, None otherwise.
    """
    df = get_data()
    if df is None:
        print("Unable to get data.")
        return None
    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['temperature'], mode='lines', name='Temperature'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['humidity'], mode='lines', name='Humidity'))
        fig.update_layout(title='Sensor Data', xaxis_title='Timestamp', yaxis_title='Value')
    except Exception as e:
        print(f"Plotting error: {str(e)}")
        return None

@app.route('/')
def index():
    """
    Flask route to render the main page.

    This function creates a plot of sensor data and then renders the main 
    webpage with this plot.

    Returns:
        str: String containing the html content of the webpage.
    """
    fig = create_plot()
    plot_div = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div') #Return an HTML div which can be directly inserted into a webpage's HTML.
    return render_template('index.html', plot_div=plot_div) 

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=50000)




