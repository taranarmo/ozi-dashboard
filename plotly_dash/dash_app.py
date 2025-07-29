import os
import dash
from dash import html, dcc
import plotly.express as px
import sqlalchemy
import pandas as pd
import numpy as np

def fetch_data():
    db_url = (
        f"postgresql://{os.environ.get('DASH_DB_USER', 'user')}:"
        f"{os.environ.get('DASH_DB_PASSWORD', 'password')}@"
        f"{os.environ.get('DASH_DB_HOST', 'localhost')}:"
        f"{os.environ.get('DASH_DB_PORT', '5432')}/"
        f"{os.environ.get('DASH_DB_NAME', 'exampledb')}"
    )
    engine = sqlalchemy.create_engine(db_url)
    query = "SELECT id, value FROM sample_table LIMIT 10;"
    df = pd.read_sql(query, engine)
    engine.dispose()
    return df

app = dash.Dash(__name__)

# df = fetch_data()
# fig = px.bar(df, x="id", y="value", title="Sample Data from PostgreSQL")
# plot some random data instead
df = pd.DataFrame(
    data=np.random.randint(0, 100, size=(100,4)),
    columns=list('ABCD'),
)
fig = px.area(df, title="Random Data Plot")


app.layout = html.Div([
    html.H1("PostgreSQL Data Plot"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
