import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import plotly.express as px # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go # type: ignore


st.set_page_config(page_title="CA", 
                   page_icon=":calendar:",
                   layout="wide"
                   
)
st.sidebar.title("Navigation")
st.sidebar.header("Header")
st.sidebar.success("Success message!")
st.sidebar.header("CA Analysis")
st.sidebar.info("Analyze the Chiffre d'Affaires (CA) over different periods.")
st.set_option("client.showErrorDetails", True)

st.header("Chiffre d'Affaires (CA) Analysis")


dt_ca= pd.read_excel("./Export_CA.xls")
dt_ca = dt_ca.rename(columns={'MONTANTHT_TOTAL':'CA_HT','DATEFISCALE':'Day'})


dt_ca["Day"] = pd.to_datetime(dt_ca["Day"],dayfirst=True).dt.strftime('%d/%m/%Y')

select_date = st.selectbox("Select Date", options=dt_ca["Day"].unique())
st.write("You selected:", select_date)
dt_ca[['CA_HT']].groupby(dt_ca['Day']).agg('sum')
st.dataframe(dt_ca[['CA_HT']].groupby(dt_ca['Day']).agg('sum').query("Day == @select_date"  ), use_container_width=True)

dt_ca["Day"] = pd.to_datetime(dt_ca["Day"],dayfirst=True).dt.strftime('%U')
dt_ca.rename(columns={'Day':'Semaine'}, inplace=True)
select_week = st.selectbox("Select Week", options=dt_ca["Semaine"].unique())
st.subheader("CA de la semaine " + str(select_week))
st.dataframe(dt_ca[['CA_HT']].groupby(dt_ca['Semaine']).agg('sum').query("Semaine == @select_week" ), use_container_width=True)
fig_ca = px.bar(
        dt_ca,
        x="Semaine",
        y="CA_HT",
        hover_name="Semaine",
        color="CA_HT", 
        height=600
    )

st.header("Evolution du CA par semaine")
st.plotly_chart(fig_ca)