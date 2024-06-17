# import streamlit as st
# import pandas as pd

# st.set_page_config(
#     page_title="Fluxo_Caixa",
#     page_icon="💰",
#     layout="wide"
# )

# ### Puxando Dados ###
# df_projecao_bares = st.session_state["projecao_bares"]

# df_projecao_grouped = st.session_state["projecao_grouped"]

# ### Filtros ###
# bares = df_projecao_bares["Empresa"].unique()
# bar = st.selectbox("Bar", bares)

# def somar_total(df):
#     colunas_numericas = df.select_dtypes(include=[int, float]).columns
#     soma_colunas = df[colunas_numericas].sum().to_frame().T
#     soma_colunas['Data'] = 'Total'  # Adiciona um rótulo 'Total' para a linha somada
#     df_com_soma = pd.concat([df, soma_colunas], ignore_index=True)
    
#     return df_com_soma

# ### Relatorio ###

# # Projeção por bar
# df_projecao_bar = df_projecao_bares[df_projecao_bares["Empresa"] == bar]

# df_projecao_bar_com_soma = somar_total(df_projecao_bar)

# columns_projecao_bar_com_soma = ['Data', 'Empresa', 'Saldo_Inicio_Dia', 'Valor_Liquido_Recebido', 'Valor_Projetado_Zig', 'Receita_Projetada_Extraord',
#            'Despesas_Aprovadas_Pendentes', 'Despesas_Pagas', 'Saldo_Final']

# st.dataframe(df_projecao_bar_com_soma[columns_projecao_bar_com_soma],
#              column_config={
#                  'Data': st.column_config.DateColumn(
#                      'Data', format="DD/MM/YYYY"
#                  ),
#                  'Empresa': st.column_config.Column(
#                      'Bar', width="medium"
#                  )
#              })


# st.divider()

# # Projeção Agrupada
# st.markdown(
#     """
#     **Projeção de bares agrupados**: *Bar Brahma, Bar Léo, Bar Brasilia, Edificio Rolim, Hotel Maraba, 
#                     Jacaré, Orfeu, Riviera, Tempus, Escritorio Fabrica de Bares*
# """
# )

# df_projecao_grouped_com_soma =  somar_total(df_projecao_grouped)

# columns_projecao_grouped = ['Data', 'Saldo_Inicio_Dia', 'Valor_Liquido_Recebido', 'Valor_Projetado_Zig', 'Receita_Projetada_Extraord',
#            'Despesas_Aprovadas_Pendentes', 'Despesas_Pagas', 'Saldo_Final']

# st.dataframe(df_projecao_grouped_com_soma[columns_projecao_grouped],
#              column_config={
#                  'Data': st.column_config.DateColumn(
#                      'Data', format="DD/MM/YYYY"
#                  )
#             })


import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fluxo_Caixa",
    page_icon="💰",
    layout="wide"
)

### Puxando Dados ###
df_projecao_bares = st.session_state["projecao_bares"]
df_projecao_grouped = st.session_state["projecao_grouped"]

### Filtros ###
bares = df_projecao_bares["Empresa"].unique()
bar = st.selectbox("Bar", bares)

def somar_total(df):
    colunas_numericas = df.select_dtypes(include=[int, float]).columns
    soma_colunas = df[colunas_numericas].sum().to_frame().T
    soma_colunas['Data'] = 'Total'  # Adiciona um rótulo 'Total' para a linha somada
    df_com_soma = pd.concat([df, soma_colunas], ignore_index=True)
    return df_com_soma

### Relatorio ###

# Projeção por bar
df_projecao_bar = df_projecao_bares[df_projecao_bares["Empresa"] == bar]
df_projecao_bar_com_soma = somar_total(df_projecao_bar)

columns_projecao_bar_com_soma = ['Data', 'Empresa', 'Saldo_Inicio_Dia', 'Valor_Liquido_Recebido', 'Valor_Projetado_Zig', 'Receita_Projetada_Extraord',
                                 'Despesas_Aprovadas_Pendentes', 'Despesas_Pagas', 'Saldo_Final']

st.dataframe(df_projecao_bar_com_soma[columns_projecao_bar_com_soma])

st.markdown('---')  # Substituindo st.divider()

# Projeção Agrupada
st.markdown(
    """
    **Projeção de bares agrupados**: *Bar Brahma, Bar Léo, Bar Brasilia, Edificio Rolim, Hotel Maraba, 
    Jacaré, Orfeu, Riviera, Tempus, Escritorio Fabrica de Bares*
    """
)

df_projecao_grouped_com_soma = somar_total(df_projecao_grouped)

columns_projecao_grouped = ['Data', 'Saldo_Inicio_Dia', 'Valor_Liquido_Recebido', 'Valor_Projetado_Zig', 'Receita_Projetada_Extraord',
                            'Despesas_Aprovadas_Pendentes', 'Despesas_Pagas', 'Saldo_Final']

st.dataframe(df_projecao_grouped_com_soma[columns_projecao_grouped])


