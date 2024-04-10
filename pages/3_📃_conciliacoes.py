import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Conciliacao",
    page_icon="📃",
    layout="wide"
)

df_lojas = st.session_state["lojas"]

lojas = df_lojas["Loja"].unique()
loja = st.selectbox("Loja", lojas)

df_faturam_zig = st.session_state["faturam_zig"]

df_faturam_zig

df_receitas_extraord = st.session_state["receitas_extraord"]

df_receitas_extraord
