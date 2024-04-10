import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import os
import numpy as np
from datetime import datetime
import mysql.connector
from utils.queries import *


LOGGER = get_logger(__name__)

def mysql_connection():
  mysql_config = st.secrets["mysql"]

  conn = mysql.connector.connect(
        host=mysql_config['host'],
        port=mysql_config['port'],
        database=mysql_config['database'],
        user=mysql_config['username'],
        password=mysql_config['password']
    )    
  return conn

def execute_query(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)

    # Obter nomes das colunas
    column_names = [col[0] for col in cursor.description]
  
    # Obter resultados
    result = cursor.fetchall()
  
    cursor.close()
    return result, column_names


def run():

    ######## Config Pag ##########
    st.set_page_config(
    page_title="Fluxo_Financeiro_FB",
    page_icon="💰",
    )

    ######## Puxando Dados #########
    conn = mysql_connection()

    def lojas_teste():    
        result, column_names = execute_query(GET_LOJAS, conn)
        df_lojas_teste = pd.DataFrame(result, columns=column_names)

        return df_lojas_teste
    df_lojas_teste = lojas_teste()
    
    def saldos_bancarios():
        result, column_names = execute_query(GET_SALDOS_BANCARIOS, conn)
        df_saldos_bancarios = pd.DataFrame(result, columns=column_names)

        df_saldos_bancarios['Data'] = pd.to_datetime(df_saldos_bancarios['Data'])

        return df_saldos_bancarios
    df_saldos_bancarios = saldos_bancarios()

    def valor_liquido_recebido():
        result, column_names = execute_query(GET_VALOR_LIQUIDO_RECEBIDO, conn)
        df_valor_liquido = pd.DataFrame(result, columns=column_names)

        df_valor_liquido['Data'] = pd.to_datetime(df_valor_liquido['Data'])

        return df_valor_liquido  
    df_valor_liquido = valor_liquido_recebido()

    def projecao_zig():
        result, column_names = execute_query(GET_PROJECAO_ZIG, conn)
        df_projecao_zig = pd.DataFrame(result, columns=column_names)

        df_projecao_zig['Data'] = pd.to_datetime(df_projecao_zig['Data'])

        return df_projecao_zig
    df_projecao_zig = projecao_zig()

    def receitas_extraord():
        result, column_names = execute_query(GET_RECEITAS_EXTRAORD, conn)
        df_receitas_extraord = pd.DataFrame(result, columns=column_names)    
    
        df_receitas_extraord['Data'] = pd.to_datetime(df_receitas_extraord['Data'])

        return df_receitas_extraord
    df_receitas_extraord = receitas_extraord()

    def despesas_aprovadas_pendentes():
        result, column_names = execute_query(GET_DESPESAS_APROVADAS, conn)
        df_despesas_aprovadas = pd.DataFrame(result, columns=column_names)

        df_despesas_aprovadas['Data'] = pd.to_datetime(df_despesas_aprovadas['Data'])

        return df_despesas_aprovadas
    df_despesas_aprovadas = despesas_aprovadas_pendentes()

    def despesas_pagas():
        result, column_names = execute_query(GET_DESPESAS_PAGAS, conn)
        df_despesas_pagas = pd.DataFrame(result, columns=column_names)

        df_despesas_pagas['Data'] = pd.to_datetime(df_despesas_pagas['Data'])

        return df_despesas_pagas
    df_despesas_pagas = despesas_pagas()

    # Unindo os DataFrames usando merge
    def projecao_bares():
        merged_df = pd.merge(df_saldos_bancarios, df_valor_liquido, on=['Data', 'Empresa'], how='outer')
        merged_df = pd.merge(merged_df, df_projecao_zig, on=['Data', 'Empresa'], how='outer')
        merged_df = pd.merge(merged_df, df_receitas_extraord, on=['Data', 'Empresa'], how='outer')
        merged_df = pd.merge(merged_df, df_despesas_aprovadas, on=['Data', 'Empresa'], how='outer')
        merged_df = pd.merge(merged_df, df_despesas_pagas, on=['Data', 'Empresa'], how='outer')

        # Preencher valores NaN com 0
        merged_df = merged_df.fillna(0)

        # Renomeando colunas
        merged_df = merged_df.rename(columns={'Valor_Projetado': 'Valor_Projetado_Zig'})

        # Ordenando
        merged_df = merged_df.sort_values(by='Data')

        # Resetando o indice
        merged_df = merged_df.reset_index(drop=True)

        # Ajustando formatação
        merged_df['Saldo_Inicio_Dia'] = merged_df['Saldo_Inicio_Dia'].astype(float).round(2)
        merged_df['Valor_Liquido_Recebido'] = merged_df['Valor_Liquido_Recebido'].astype(float).round(2)
        merged_df['Valor_Projetado_Zig'] = merged_df['Valor_Projetado_Zig'].astype(float).round(2)
        merged_df['Receita_Projetada_Extraord'] = merged_df['Receita_Projetada_Extraord'].astype(float).round(2)
        merged_df['Despesas_Aprovadas_Pendentes'] = merged_df['Despesas_Aprovadas_Pendentes'].astype(float).round(2)
        merged_df['Despesas_Pagas'] = merged_df['Despesas_Pagas'].astype(float).round(2)


        merged_df['Valor_Projetado_Zig'] = merged_df.apply(lambda row: 0 if row['Valor_Liquido_Recebido'] > 0 else row['Valor_Projetado_Zig'], axis=1)

        merged_df['Saldo_Final'] = merged_df['Saldo_Inicio_Dia'] + merged_df['Valor_Liquido_Recebido'] + merged_df['Valor_Projetado_Zig'] + merged_df['Receita_Projetada_Extraord'] - merged_df['Despesas_Aprovadas_Pendentes'] - merged_df['Despesas_Pagas']

        # List of houses to group
        houses_to_group = ['Bar Brahma - Centro', 'Bar Léo - Centro', 'Bar Brasilia -  Aeroporto ', 'Bar Brasilia -  Aeroporto', 'Delivery Bar Leo Centro', 
                        'Delivery Fabrica de Bares', 'Delivery Orfeu', 'Edificio Rolim', 'Hotel Maraba', 
                        'Jacaré', 'Orfeu', 'Riviera Bar', 'Tempus', 'Escritorio Fabrica de Bares']

        # Create a new column 'Group' based on the houses
        merged_df['Group'] = merged_df['Empresa'].apply(lambda x: 'Group' if any(house in x for house in houses_to_group) else 'Other')
        return merged_df
    df_projecao_bares = projecao_bares()

    def grouped_projecao():
    # Group by 'Data', 'Group', and 'Empresa', and sum the values
        grouped_df = df_projecao_bares.groupby(['Data', 'Group']).sum().reset_index()
        grouped_df = grouped_df[grouped_df['Group'] == 'Group']
        grouped_df = grouped_df.reset_index(drop=True)
        return grouped_df
    df_projecao_grouped = grouped_projecao()


    ######## Definindo Relatorio #########

    st.write("# Fluxo Financeiro FB")
 
    st.markdown(
        """
        Utilize as abas localizadas no lado esquerdo para buscar suas análises.
    """
    )

    if "projecao_bares" not in st.session_state:
        st.session_state["projecao_bares"] = df_projecao_bares

    if "projecao_grouped" not in st.session_state:
        st.session_state["projecao_grouped"] = df_projecao_grouped    

if __name__ == "__main__":
    run()


