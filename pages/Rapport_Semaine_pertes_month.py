import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import plotly.express as px # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go # type: ignore
import pathlib


# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("styles.css")
load_css(css_path)

dt_week= pd.read_excel("./Export_month.xls")

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


dt_week= pd.read_excel("./Export_month.xls")
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
dt_week['Mois'] = dt_week['Semaine'].dt.strftime('%m')
st.subheader("Top 10 des pertes du mois")

st.dataframe(dt_week[["Mois","Produit","Pertes","ecart"]].where(dt_week["Semaine"] == dt_week["Semaine"].max()).dropna().head(10), use_container_width=True, hide_index=True)
top_pertes(dt_week[["Produit","Pertes","ecart","Semaine"]].where(dt_week["Semaine"] == dt_week["Semaine"].max()).dropna().head(10))







