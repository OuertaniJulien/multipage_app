import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import plotly.express as px # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go # type: ignore


st.set_page_config(page_title="Weekly Report", 
                   page_icon=":calendar:",
                   layout="wide"
                   
)
st.sidebar.title("Navigation")
st.sidebar.header("Header")
st.sidebar.success("Success message!")
st.set_option("client.showErrorDetails", True)

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



dt_week["Semaine"] = pd.to_datetime(dt_week["Semaine"],dayfirst=True).dt.strftime('%U')


# TOP PERTES
dt_pertes = dt_week.sort_values(by='Pertes', ascending=False, inplace=True)

st.subheader("Top 10 des pertes de la semaine " + str(dt_week["Semaine"].max()))
st.dataframe(dt_week[["Produit","Pertes","ecart"]].where(dt_week["Semaine"] == dt_week["Semaine"].max()).dropna().head(10), use_container_width=True)
top_pertes(dt_week[["Produit","Pertes","ecart","Semaine"]].where(dt_week["Semaine"] == dt_week["Semaine"].max()).dropna().head(10))
st.text_area("Commentaire Pertes", height=400)

# TOP ECARTS
dt_pertes = dt_week.sort_values(by='ecart', ascending=False, inplace=True)
st.subheader("Top 10 des écarts de la semaine " + str(dt_week["Semaine"].max()))
dt_week = dt_week.where(dt_week["Marché"] == 'FOOD').dropna(subset=['Marché'])

st.dataframe(dt_week[["Produit","Pertes","ecart"]].
             where(dt_week["Semaine"] == dt_week["Semaine"].
                   max()).dropna().head(10), use_container_width=True)
top_ecart(dt_week[["Produit","Pertes","ecart","Semaine"]].where(dt_week["Semaine"] == dt_week["Semaine"].max()).dropna().head(10))
st.text_area("Commentaire écarts", height=400)




st.subheader("Analyse des Pertes et écarts par semaine et par produit")
dt_week[['Pertes','ecart']] = dt_week[['Pertes','ecart']].fillna(0).astype(int)

dt_week.sort_values(by='Pertes', ascending=False, inplace=True)
selected = st.multiselect(
    "Selection de semaine",
    options=dt_week["Semaine"].unique(),
    default=dt_week["Semaine"].tail(1).values,
    key="product_selection"
)

selected2 = st.multiselect(
    "Selection de prodtuit",
    options=dt_week["Produit"].unique(),
    key="product_selection2"
)
st.dataframe(dt_week[["Semaine","Produit","ecart","Pertes"]].query("Produit == @selected2" " & Semaine == @selected"), use_container_width=True)

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
left_column.metric(label="Total des pertes", value=str(dt_week.query("Produit == @selected2" " & Semaine == @selected")['Pertes'].sum())+" €")
right_column.metric(label="Total des écarts", value=str(dt_week.query("Produit == @selected2" " & Semaine == @selected")['ecart'].sum())+" €")

if len(selected2) < 5 :
    left_column.plotly_chart(fig_pertes, use_container_width=True)
    right_column.plotly_chart(fig_ecart, use_container_width=True)
else:
    st.plotly_chart(fig_pertes)
    st.plotly_chart(fig_ecart)

