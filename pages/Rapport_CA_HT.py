import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import plotly.express as px # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go # type: ignore
from datetime import datetime, timedelta
import locale
locale.getlocale()


locale.setlocale(locale.LC_TIME, 'fr_FR') # this sets the date time formats to es_ES, there are many other options for currency, numbers etc. 


st.set_page_config(
    page_title="CA", 
                   page_icon=":calendar:",
                   layout="wide",
                   menu_items={'About':'This is a test'},
                   initial_sidebar_state='auto'
)


st.sidebar.header("Sélection de période")
date_start = st.sidebar.date_input(
    label='Période du',
    min_value='2024-01-01',
    value='2024-01-01',
    format='DD/MM/YYYY',
    key="input"
    )

date_end = st.sidebar.date_input(
    label='Au',
    format=str('DD/MM/YYYY'),
    value='2024-01-04',
    )
st.sidebar.markdown('---')

#BODY

st.header("Chiffre d'Affaires (CA) Analysis")
dt_ca= pd.read_excel("./Export_CA.xls")
dt_ca = dt_ca.rename(columns={'MONTANTHT_TOTAL':'CA_HT','DATEFISCALE':'Day'})

#DAY
dt_ca["Day"] = pd.to_datetime(dt_ca["Day"],dayfirst=True).dt.strftime('%Y-%m-%d')

date_start = str(date_start)
date_end = str(date_end)


# dt_ca= dt_ca[['CA_HT','Day']].groupby(dt_ca['Day'])
dt_ca[['CA_HT']]= dt_ca[['CA_HT']].groupby(dt_ca['Day'], as_index=False).sum('CA_HT')
# dt_ca[['Day']].groupby(dt_ca[['CA_HT']])
dt_ca = dt_ca[['Day','CA_HT']].query("Day >= @date_start & Day <= @date_end").drop_duplicates('Day')

# .agg('sum').query("Day >= @date_start & Day <= @date_end")


dt_ca["Day"] = pd.to_datetime(dt_ca['Day'],dayfirst=True,format='mixed').dt.strftime('%d-%m-%Y')
dt_ca['wd'] =  pd.to_datetime(dt_ca["Day"],dayfirst=True,format='mixed').dt.strftime('%A')
# dt_ca = dt_ca['Day'].isin(pd.date_range(date_start,date_end))
# dt_ca
# dt_ca['wd'] = pd.to_datetime(dt_ca['Day'],dayfirst=True,format='mixed').dt.strftime('%A')

st.dataframe(dt_ca, use_container_width=True) 




# SEMAINE
# dt_ca["Day"] = pd.to_datetime(dt_ca["Day"],dayfirst=True).dt.strftime('%d%m/%')

# dt_ca["Day"] = pd.to_datetime(dt_ca["Day"],dayfirst=True).dt.strftime('%U')
# dt_ca.rename(columns={'Day':'Semaine'}, inplace=True)

# select_week = st.selectbox("Select Week", options=dt_ca["Semaine"].unique())
# st.subheader("CA de la semaine " + str(select_week))
# st.dataframe(dt_ca[['CA_HT']].groupby(dt_ca['Semaine']).agg('sum').query("Semaine == @select_week" ), use_container_width=True)
# fig_ca = px.bar(
#         dt_ca,
#         x="Semaine",
#         y="CA_HT",
#         hover_name="Semaine",
#         color="CA_HT", 
#         height=600
#     )

# st.header("Evolution du CA par semaine")
# st.plotly_chart(fig_ca)