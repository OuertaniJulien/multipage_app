import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import plotly.express as px # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go # type: ignore
import pathlib
import sqlite3

# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("styles.css")
load_css(css_path)

dt_week= pd.read_excel("./Export.xls")

dt_week = dt_week.rename(columns={'écart d\'inventaire Total':'ecart','Pertes Total':'Pertes','Période au':'Semaine','Produit':'Produit'})
# st.sidebar.title("Navigation")
# st.sidebar.header("Selection de produit")
# selected2 = st.sidebar.multiselect(
#     "Selection de prodtuit",
#     options=dt_week["Produit"].unique(),
#     key="product_selection2",
#     label_visibility="collapsed",

    
#     )

# st.sidebar.markdown("---")


dt_week= pd.read_excel("./Export.xls")
dt_week = dt_week.rename(columns={'écart d\'inventaire Total':'ecart','Pertes Total':'Pertes','Période au':'Semaine','Produit':'Produit'})


def top_pertes(dt):
    dt.sort_values(by='Semaine', ascending=True, inplace=True)      
    fig_ = px.bar(
        dt,
        x="Produit",
        y="Pertes",
        hover_name="Produit",
        color="Produit",
        height=600
    )
    
    return st.plotly_chart(fig_)
def top_ecart(dt):
    dt.sort_values(by='Semaine', ascending=True, inplace=True)      
    fig_ = px.bar(
        dt,
        x="Produit",
        y="ecart",
        hover_name="Produit",
        color="Produit",
        height=600
        )
    fig_.update_xaxes(title_text="")
    fig_.update_yaxes(title_text="")
    fig_.update_traces(marker_line_width=0.5, marker_line_color="white")
    return st.plotly_chart(fig_)



dt_week["Semaine"] = pd.to_datetime(dt_week["Semaine"],dayfirst=True)


# TOP PERTES
dt_pertes = dt_week.sort_values(by='Pertes', ascending=False, inplace=True)

st.subheader("Top 10 des pertes de la semaine " + str(dt_week["Semaine"].dt.strftime('%U').max()))

st.dataframe(dt_week[["Produit","Pertes","ecart"]].where(dt_week["Semaine"] == dt_week["Semaine"].max()).dropna().head(10), use_container_width=True, hide_index=True)
top_pertes(dt_week[["Produit","Pertes","ecart","Semaine"]].where(dt_week["Semaine"] == dt_week["Semaine"].max()).dropna().head(10))
dt_week["Semaine"] = dt_week["Semaine"].dt.strftime('%U')

con = sqlite3.connect('tutorial.db')

cur = con.cursor()
table = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Weekly'").fetchall()
if table == [] :
    cur.execute("CREATE TABLE Weekly (Semaine,Produit,Pertes,ecart, UNIQUE (Semaine,Produit) ON CONFLICT REPLACE) ")

data = dt_week[['Semaine', 'Produit', 'Pertes', 'ecart']].to_records(index=False).tolist()
# con.execute("INSERT INTO Produit(Semaine,Produit,Pertes,ecart) VALUES(?,?,?,?)",data)
# st.button(
#     label= 'db',
#     on_click=cur.execute()
# )
# semaine = pd.read_sql_query('SELECT Semaine FROM Produit', con)
# cur.execute('DROP TABLE Produit')
# test = dt_week['Semaine'].isin(semaine).any()
# print(test)
# if test==False :
cur.executemany('INSERT INTO Weekly (Semaine,Produit,pertes,ecart) VALUES(?,?,?,? )',data)
con.commit()
table = pd.read_sql_query('SELECT * FROM Weekly',con)
# st.dataframe(table.query("Produit == 'HUILE DE FRITURE'"))

con.close()

# BESOIN DE TESTER AVEC UN NOUVEL EXPORT SI CA MARCHE PAS C EST CHIANT