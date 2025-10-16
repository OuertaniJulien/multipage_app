import pandas as pd # pyright: ignore[reportMissingModuleSource]
import streamlit as st # pyright: ignore[reportMissingImports]
import plotly.express as px # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go    # pyright: ignore[reportMissingImports]


st.set_page_config(page_title="Dashboard", 
                   page_icon=":bar_chart:",
                   layout="wide")
st.sidebar.header("Header")
st.sidebar.success("Success message!")
