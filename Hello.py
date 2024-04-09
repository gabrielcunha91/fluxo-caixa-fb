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
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Teste")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Teste
    """
    )

    conn = mysql_connection()

    def lojas_teste():    
        result, column_names = execute_query(GET_LOJAS, conn)
        df_lojas_teste = pd.DataFrame(result, columns=column_names)

        return df_lojas_teste
    df_lojas_teste = lojas_teste()
    df_lojas_teste

    def saldos_bancarios():
        result, column_names = execute_query(GET_SALDOS_BANCARIOS, conn)
        df_saldos_bancarios = pd.DataFrame(result, columns=column_names)
        return df_saldos_bancarios
    df_saldos_bancarios = saldos_bancarios()
    


if __name__ == "__main__":
    run()
