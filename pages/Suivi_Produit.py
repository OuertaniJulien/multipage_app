import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import plotly.express as px # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go # type: ignore
import pathlib
import sqlite3
# from sqlalchemy import create_engine

con = sqlite3.connect('tutorial.db')

# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("styles.css")
load_css(css_path)

dt_week= pd.read_excel("./Export.xls")
dt_week = dt_week.rename(columns={'écart d\'inventaire Total':'ecart','Pertes Total':'Pertes','Période au':'Semaine','Produit':'Produit'})
st.sidebar.title("Filtres")
st.sidebar.header("Selection de produit")

dt_week["Semaine"] = pd.to_datetime(dt_week["Semaine"],dayfirst=True)



#Par produit
st.subheader("Analyse des Pertes et écarts par semaine et par produit")
dt_week["Semaine"] = dt_week["Semaine"].dt.strftime('S%U')

dt_week[['Pertes','ecart']] = dt_week[['Pertes','ecart']].fillna(0).astype(float).round(2)
dt_week.sort_values(by='Pertes', ascending=False, inplace=True)
dt_week.sort_values(by='Semaine', ascending=False, inplace=True)

selected = st.sidebar.multiselect(
    "Selection de semaine",
    options=dt_week["Semaine"].unique(),
    default=dt_week["Semaine"].drop_duplicates().head(4).values,
    key="product_selection"
)
selected2 = st.sidebar.multiselect(
    "Selection de produits",
    options=dt_week["Produit"].unique()
)
cur = con.cursor()
# cur.execute("CREATE TABLE Produit(Semaine,Produit,Pertes,ecart)")

dt_week[['Semaine','Produit','Pertes','ecart']]
dt_week[['Semaine','Produit','Pertes','ecart']].to_sql('Produit',con,if_exists="append",index=False)
con.execute("DROP TABLE Produit")

dt_week['Prix_Unitaire'] = dt_week['Pertes']/dt_week['Pertes Qté']

dt_week[["ecart","Pertes","Prix_Unitaire"]] = dt_week[["ecart","Pertes","Prix_Unitaire"]].round(2)
dt_week[["ecart","Pertes","Prix_Unitaire"]] = dt_week[["ecart","Pertes","Prix_Unitaire"]]
dt_week = dt_week[['Semaine','Produit','Pertes','ecart','Prix_Unitaire']].query("Produit == @selected2 & Semaine == @selected")
st.dataframe(dt_week, hide_index=True)

dt_week.sort_values(by='Semaine', ascending=True, inplace=True)
fig_pertes = px.histogram(
    dt_week.query("Produit == @selected2" " & Semaine == @selected"),
    x="Semaine",
    y="Pertes",
    title="Histogramme des pertes"+" "" "+"par semaine",
    labels={"Pertes":"Pertes en €"},
    template="plotly_white",
    text_auto=True,
    facet_col_wrap=2,    
    facet_col="Produit",
    color="Produit",
    height=800
 
    
    
)



dt_week.sort_values(by='Semaine', ascending=True, inplace=True)
fig_ecart = px.histogram(
    dt_week.query("Produit == @selected2" " & Semaine == @selected"),
    x="Semaine",
    y="ecart",
    title="Histogramme des écarts"+" "" "+"par semaine",
    labels={"Pertes":"Pertes en €"},
    template="plotly_white",
    text_auto=True,
    facet_col="Produit",
    facet_col_wrap=2,    
    color="Produit",
    height=800
)


left_column, right_column = st.columns(2)
total_pertes = str(int(dt_week.query("Produit == @selected2" " & Semaine == @selected")['Pertes'].sum()))
total_ecart = str(int(dt_week.query("Produit == @selected2" " & Semaine == @selected")['ecart'].sum()))

left_column.metric(label="Total des pertes", value=str(total_pertes+'€'))
right_column.metric(label="Total des écarts", value=str(total_ecart+'€'))

if len(selected2) > 5 :
    left_column.plotly_chart(fig_pertes, use_container_width=True)
    right_column.plotly_chart(fig_ecart, use_container_width=True)
else:
    st.plotly_chart(fig_pertes)
    st.plotly_chart(fig_ecart)


# st.button(
#     label= 'db',
#     on_click=cur.execute()
# )

# data = dt_week[['Semaine', 'Produit', 'Pertes', 'ecart']].to_records(index=False).tolist()
# con.execute("INSERT INTO Produit(semaine,produits,pertes,ecarts) VALUES(?,?,?,?)",data)
# cur.executemany('INSERT INTO Produit(semaine,produits,pertes,ecarts) VALUES(?,?,?,?)',dt_week[['Semaine','Produit','Pertes','ecart']])


# cur.commit()