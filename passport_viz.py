# %% Interactive Python Cell
import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

con = psycopg2.connect(
    "dbname=vaccine_passport user=postgres host=localhost port=5432")


def sql_to_df(sql_query: str):
    """Get result set of sql_query as a pandas DataFrame."""
    return pd.read_sql(sql_query, con)
# %%


def viz():

    title = "Preferred Vaccine Provider by Users"
    query = '''
        SELECT providers.name, count (*) as COUNT from passports
        JOIN providers
        ON passports.provider_id1= providers.id
        GROUP BY providers.name
        '''

    dataframe = sql_to_df(query)
    fig, axes = plt.subplots(figsize=(10, 5))
    axes.set_title(title, fontsize=14)

    fig.set_facecolor('white')
    axes.pie(
        x=dataframe["count"],
        labels=dataframe["name"],
        autopct='%1.1f%%',
        colors=['lightcoral', 'skyblue', 'lavender', 'orange']
    )
    # Equal aspect ratio ensures that pie is drawn as a circle.
    axes.axis('equal')

    plt.show()


viz()

# %%
