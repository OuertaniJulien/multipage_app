import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import plotly.express as px # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go # type: ignore


st.set_page_config(page_title="Weekly Report", 
                   page_icon=":calendar:",
                   layout="wide"
                   
)
dt_week= pd.read_excel("./Export_month.xls")
dt_week = dt_week.rename(columns={'écart d\'inventaire Total':'ecart','Pertes Total':'Pertes','Période au':'Semaine','Produit':'Produit'})
# st.sidebar.title("Navigation")
# st.sidebar.header("Header")
# page_toggle = st.sidebar.toggle(label='Pertes / Ecarts')

# selected2 = st.sidebar.multiselect(
#     "Selection de prodtuit",
#     options=dt_week["Produit"].unique(),
#     key="product_selection2",
#     )
# st.sidebar.markdown("---")


dt_week= pd.read_excel("./Export_month.xls")
dt_week = dt_week.rename(columns={'écart d\'inventaire Total':'ecart','Pertes Total':'Pertes','Période au':'Semaine','Produit':'Produit'})

def top_pertes(dt):
    dt.sort_values(by='Mois', ascending=True, inplace=True)      
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
    dt.sort_values(by='Mois', ascending=True, inplace=True)      
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



# TOP ECARTS
dt_pertes = dt_week.sort_values(by='ecart', ascending=False, inplace=True)
st.subheader("Top 10 des écarts du mois")
dt_week = dt_week.where(dt_week["Marché"] == 'FOOD').dropna(subset=['Marché'])
dt_week['Mois'] = dt_week['Semaine'].dt.strftime('%m')
st.dataframe(dt_week[["Mois","Produit","Pertes","ecart"]].
            where(dt_week["Mois"] == dt_week["Mois"].
                max()).dropna().head(10), use_container_width=True)
top_ecart(dt_week[["Produit","Pertes","ecart","Mois"]].where(dt_week["Mois"] == dt_week["Mois"].max()).dropna().head(10))




