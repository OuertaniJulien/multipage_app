import pandas as pd # pyright: ignore[reportMissingModuleSource]
import streamlit as st # pyright: ignore[reportMissingImports]
import plotly.express as px # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go    # pyright: ignore[reportMissingImports]
import pathlib

st.set_page_config(page_title="Dashboard", 
                   page_icon=":bar_chart:",
                   layout="wide")


# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("styles.css")
load_css(css_path)

# if not st.user:
#     if st.button("Log in with Google"):
#         st.login()
#     st.stop()

# if st.button("Log out"):
#     st.logout()
# st.markdown(f"Welcome! {st.user.name}")
# st.header("Home")

 

# pages = {
#     "Navigation": [
#         # st.Page('Home_Page.py',title="Home"),
#         st.Page("pages/Rapport_CA_HT.py", title="CA"),
#         st.Page("pages/Rapport_Semaine_pertes.py", title="Pertes"),
#         st.Page("pages/Rapport_Semaine_ecarts.py", title="Écarts"),
#         st.Page("pages/Suivi_Produit.py", title="Suivi produits"),
#     ]
   
# }

# pg = st.navigation(pages,expanded=False)
# pg.run()
container = st.container(
    border=True,
    horizontal=True,
    horizontal_alignment='distribute',
    gap='large',
    # width= 100
    
)
container.page_link(
    'pages/Rapport_CA_HT.py',
    label='Rapport CA HT'
)
container.page_link(
    'pages/Rapport_Semaine_pertes.py',
    label='Rapport Écarts Semaine'
)
container.page_link(
    'pages/Rapport_Semaine_ecarts.py',
    label='Rapport Pertes Semaine '
)
