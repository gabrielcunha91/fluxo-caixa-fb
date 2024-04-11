import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import os
import numpy as np
from datetime import datetime
import mysql.connector
from utils.queries import *
from workalendar.america import Brazil
import openpyxl


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

    ######## Parametros de Taxas ########
    
    taxa_credito_antecipado = 0.0265
    taxa_credito_padrao = 0.016
    taxa_debito = 0.0095
    taxa_app = 0.0074
    taxa_pix = 0.0074

    ######## Puxando Dados #########
    conn = mysql_connection()

    
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
        df_receitas_extraord_proj = pd.DataFrame(result, columns=column_names)    
    
        df_receitas_extraord_proj['Data'] = pd.to_datetime(df_receitas_extraord_proj['Data'])

        return df_receitas_extraord_proj
    df_receitas_extraord_proj = receitas_extraord()

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
        merged_df = pd.merge(merged_df, df_receitas_extraord_proj, on=['Data', 'Empresa'], how='outer')
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

    def lojas():
        result, column_names = execute_query(GET_LOJAS, conn)
        df_lojas = pd.DataFrame(result, columns=column_names)

        return df_lojas        
    df_lojas = lojas()

    def faturam_zig():
        result, column_names = execute_query(GET_FATURAMENTO_ZIG, conn)
        df_faturam_zig = pd.DataFrame(result, columns=column_names)       

        df_faturam_zig['Data_Faturamento'] = pd.to_datetime(df_faturam_zig['Data_Faturamento'])
        df_faturam_zig['Valor_Faturado'] = df_faturam_zig['Valor_Faturado'].astype(float).round(2)  

        return df_faturam_zig     
    df_faturam_zig = faturam_zig()

    def antecipacao_credito():
        df_faturam_zig['Antecipacao_Credito'] = 1
        df_faturam_zig['Antecipacao_Credito'] = df_faturam_zig.apply(lambda row: 0 if row['Loja'] == 'Arcos' else row['Antecipacao_Credito'], axis=1)

        return df_faturam_zig
    df_faturam_zig = antecipacao_credito()

    def calcular_taxas():
        df_faturam_zig[['Tipo_Pagamento']].drop_duplicates()

        df_faturam_zig['Taxa'] = 0.00
        df_faturam_zig['Taxa'] = df_faturam_zig.apply(lambda row: row['Valor_Faturado'] * taxa_debito if row['Tipo_Pagamento'] == 'DÉBITO' else row['Taxa'], axis=1)
        df_faturam_zig['Taxa'] = df_faturam_zig.apply(lambda row: row['Valor_Faturado'] * taxa_credito_antecipado if (row['Tipo_Pagamento'] == 'CRÉDITO' and row['Antecipacao_Credito'] == 1) else row['Taxa'], axis=1)
        df_faturam_zig['Taxa'] = df_faturam_zig.apply(lambda row: row['Valor_Faturado'] * taxa_credito_padrao if (row['Tipo_Pagamento'] == 'CRÉDITO' and row['Antecipacao_Credito'] == 0) else row['Taxa'], axis=1)
        df_faturam_zig['Taxa'] = df_faturam_zig.apply(lambda row: row['Valor_Faturado'] * taxa_app if row['Tipo_Pagamento'] == 'APP' else row['Taxa'], axis=1)
        df_faturam_zig['Taxa'] = df_faturam_zig.apply(lambda row: row['Valor_Faturado'] * taxa_pix if row['Tipo_Pagamento'] == 'PIX' else row['Taxa'], axis=1)

        df_faturam_zig['Valor_Compensado'] = df_faturam_zig['Valor_Faturado'] - df_faturam_zig['Taxa']

        # Tratando bonus
        df_faturam_zig['Valor_Compensado'] = df_faturam_zig.apply(lambda row: 0 if row['Tipo_Pagamento'] == 'BÔNUS' else row['Valor_Compensado'], axis=1)

        return df_faturam_zig
    df_faturam_zig = calcular_taxas()   

    def custos_zig(df):
        # Adicionando uma nova coluna 'Custos_Zig' ao dataframe
        df['Custos_Zig'] = 0.008 * df['Valor_Faturado']

        # Calculando o custo acumulado para cada mês
        df['Accumulated_Cost'] = df.groupby([df['Data_Faturamento'].dt.year, df['Data_Faturamento'].dt.month, df['ID_Loja']])['Custos_Zig'].cumsum()

        # Identificando as linhas onde o custo acumulado atinge ou ultrapassa 2800.00
        exceeded_limit = df['Accumulated_Cost'] >= 2800.00

        # Ajustando os valores de 'Custos_Zig' para evitar custos negativos
        df.loc[exceeded_limit, 'Custos_Zig'] = np.maximum(0, 2800.00 - (df['Accumulated_Cost'] - df['Custos_Zig']))

        # Zerando o custo acumulado para as linhas onde atingiu o limite
        df.loc[exceeded_limit, 'Accumulated_Cost'] = np.minimum(2800.00, df.loc[exceeded_limit, 'Accumulated_Cost'])

        # Removendo a coluna temporária 'Accumulated_Cost'
        df = df.drop('Accumulated_Cost', axis=1)

        return df
    df_faturam_zig = custos_zig(df_faturam_zig)

    def valores_finais_zig():

        df_faturam_zig['Valor_Final'] = df_faturam_zig['Valor_Compensado'] - df_faturam_zig['Custos_Zig']
        df_faturam_zig['Valor_Final'] = df_faturam_zig.apply(lambda row: 0 if row['Tipo_Pagamento'] == 'VOUCHER' else row['Valor_Final'], axis=1)
        df_faturam_zig['Valor_Final'] = df_faturam_zig.apply(lambda row: 0 if row['Tipo_Pagamento'] == 'DINHEIRO' else row['Valor_Final'], axis=1)

        df_faturam_zig['Taxa'] = df_faturam_zig['Taxa'].astype(float).round(2)
        df_faturam_zig['Valor_Compensado'] = df_faturam_zig['Valor_Compensado'].astype(float).round(2)
        df_faturam_zig['Custos_Zig'] = df_faturam_zig['Custos_Zig'].astype(float).round(2)
        df_faturam_zig['Valor_Final'] = df_faturam_zig['Valor_Final'].astype(float).round(2)

        return df_faturam_zig
    df_faturam_zig = valores_finais_zig()

    def feriados():
        # Criar uma instância do calendário brasileiro
        calendario_brasil = Brazil()

        # Especificar os anos para os quais você deseja obter os feriados
        anos_desejados = list(range(2023, 2031))

        # Inicializar uma lista vazia para armazenar as datas dos feriados
        datas_feriados = []

        # Iterar pelos anos e obter as datas dos feriados
        for ano in anos_desejados:
            feriados_ano = calendario_brasil.holidays(ano)
            datas_feriados.extend([feriado[0] for feriado in feriados_ano])

        # Criar uma série com as datas dos feriados
        serie_datas_feriados = pd.Series(datas_feriados, name='Data_Feriado')
        serie_datas_feriados = pd.to_datetime(serie_datas_feriados)
        
        return serie_datas_feriados
    serie_datas_feriados = feriados()

    def calcular_data_compensacao():
        df_faturam_zig[['Tipo_Pagamento']].drop_duplicates()
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig['Data_Faturamento']

        # Debito
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig.apply(lambda row: row['Data_Compensacao'] + pd.Timedelta(days=1) 
                                                                if row['Tipo_Pagamento'] == 'DÉBITO' else row['Data_Compensacao'], axis=1)

        # Credito Antecipado
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig.apply(lambda row: row['Data_Compensacao'] + pd.Timedelta(days=1) 
                                                                if (row['Tipo_Pagamento'] == 'CRÉDITO' 
                                                                    and row['Antecipacao_Credito'] == 1) else row['Data_Compensacao'], axis=1)

        # Credito Padrao
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig.apply(lambda row: row['Data_Compensacao'] + pd.Timedelta(days=30) 
                                                                if (row['Tipo_Pagamento'] == 'CRÉDITO' 
                                                                    and row['Antecipacao_Credito'] == 0) else row['Data_Compensacao'], axis=1) 

        # Pix
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig.apply(lambda row: row['Data_Compensacao'] + pd.Timedelta(days=1) 
                                                                if row['Tipo_Pagamento'] == 'PIX' else row['Data_Compensacao'], axis=1)    

        # App
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig.apply(lambda row: row['Data_Compensacao'] + pd.Timedelta(days=1) 
                                                                if row['Tipo_Pagamento'] == 'APP' else row['Data_Compensacao'], axis=1)    

        # Ajuste Feriados (round 1)
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig.apply(lambda row: row['Data_Compensacao'] + pd.Timedelta(days=1) 
                                                                if row['Data_Compensacao'] in serie_datas_feriados else row['Data_Compensacao'], axis=1)
        
        # Ajuste fds
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig.apply(lambda row: row['Data_Compensacao'] + pd.Timedelta(days=1)
                                                                if row['Data_Compensacao'].strftime('%A') == 'Sunday' else row['Data_Compensacao'], axis=1)

        df_faturam_zig['Data_Compensacao'] = df_faturam_zig.apply(lambda row: row['Data_Compensacao'] + pd.Timedelta(days=2)
                                                                if row['Data_Compensacao'].strftime('%A') == 'Saturday' else row['Data_Compensacao'], axis=1)


        # Ajuste Feriados (round 2)
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig.apply(lambda row: row['Data_Compensacao'] + pd.Timedelta(days=1) 
                                                                if row['Data_Compensacao'] in serie_datas_feriados else row['Data_Compensacao'], axis=1)    

        # Retirando os horarios das datas
        df_faturam_zig['Data_Compensacao'] = df_faturam_zig['Data_Compensacao'].dt.date
        df_faturam_zig['Data_Faturamento'] = df_faturam_zig['Data_Faturamento'].dt.date

        return df_faturam_zig
    df_faturam_zig = calcular_data_compensacao()

    def receitas_extraord_conc():
        result, column_names = execute_query(GET_RECEITAS_EXTRAORD_CONCILIACAO, conn)
        df_receitas_extraord = pd.DataFrame(result, columns=column_names)        

        df_receitas_extraord['Data_Competencia'] = pd.to_datetime(df_receitas_extraord['Data_Competencia']).dt.date

        df_receitas_extraord['Data_Venc_Parc_1'] = pd.to_datetime(df_receitas_extraord['Data_Venc_Parc_1']).dt.date
        df_receitas_extraord['Data_Receb_Parc_1'] = pd.to_datetime(df_receitas_extraord['Data_Receb_Parc_1']).dt.date
        df_receitas_extraord['Data_Venc_Parc_2'] = pd.to_datetime(df_receitas_extraord['Data_Venc_Parc_2']).dt.date
        df_receitas_extraord['Data_Receb_Parc_2'] = pd.to_datetime(df_receitas_extraord['Data_Receb_Parc_2']).dt.date
        df_receitas_extraord['Data_Venc_Parc_3'] = pd.to_datetime(df_receitas_extraord['Data_Venc_Parc_3']).dt.date
        df_receitas_extraord['Data_Receb_Parc_3'] = pd.to_datetime(df_receitas_extraord['Data_Receb_Parc_3']).dt.date
        df_receitas_extraord['Data_Venc_Parc_4'] = pd.to_datetime(df_receitas_extraord['Data_Venc_Parc_4']).dt.date
        df_receitas_extraord['Data_Receb_Parc_4'] = pd.to_datetime(df_receitas_extraord['Data_Receb_Parc_4']).dt.date
        df_receitas_extraord['Data_Venc_Parc_5'] = pd.to_datetime(df_receitas_extraord['Data_Venc_Parc_5']).dt.date
        df_receitas_extraord['Data_Receb_Parc_5'] = pd.to_datetime(df_receitas_extraord['Data_Receb_Parc_5']).dt.date


        df_receitas_extraord['Valor_Total'] = df_receitas_extraord['Valor_Total'].astype(float).round(2)
        df_receitas_extraord['Categ_AB'] = df_receitas_extraord['Categ_AB'].astype(float).round(2)
        df_receitas_extraord['Categ_Aluguel'] = df_receitas_extraord['Categ_Aluguel'].astype(float).round(2)
        df_receitas_extraord['Categ_Artist'] = df_receitas_extraord['Categ_Artist'].astype(float).round(2)
        df_receitas_extraord['Categ_Couvert'] = df_receitas_extraord['Categ_Couvert'].astype(float).round(2)
        df_receitas_extraord['Categ_Locacao'] = df_receitas_extraord['Categ_Locacao'].astype(float).round(2)
        df_receitas_extraord['Categ_Patroc'] = df_receitas_extraord['Categ_Patroc'].astype(float).round(2)
        df_receitas_extraord['Categ_Taxa_Serv'] = df_receitas_extraord['Categ_Taxa_Serv'].astype(float).round(2) 

        df_receitas_extraord['Valor_Parc_1'] = df_receitas_extraord['Valor_Parc_1'].astype(float).round(2)
        df_receitas_extraord['Valor_Parc_2'] = df_receitas_extraord['Valor_Parc_2'].astype(float).round(2) 
        df_receitas_extraord['Valor_Parc_3'] = df_receitas_extraord['Valor_Parc_3'].astype(float).round(2) 
        df_receitas_extraord['Valor_Parc_4'] = df_receitas_extraord['Valor_Parc_4'].astype(float).round(2) 
        df_receitas_extraord['Valor_Parc_5'] = df_receitas_extraord['Valor_Parc_5'].astype(float).round(2)  


        return df_receitas_extraord
    df_receitas_extraord = receitas_extraord()

    def view_parc_agrup():
        result, column_names = execute_query(GET_VIEW_PARC_AGRUP, conn)
        df_view_parc_agrup = pd.DataFrame(result, columns=column_names)        

        df_view_parc_agrup = df_view_parc_agrup.drop('Numero_Linha', axis=1)

        df_view_parc_agrup['Data_Vencimento'] = df_view_parc_agrup['Data_Vencimento'].dt.date
        df_view_parc_agrup['Data_Recebimento'] = df_view_parc_agrup['Data_Recebimento'].dt.date
        df_view_parc_agrup['Data_Ocorrencia'] = df_view_parc_agrup['Data_Ocorrencia'].dt.date

        df_view_parc_agrup['Valor_Parcela'] = df_view_parc_agrup['Valor_Parcela'].astype(float).round(2)

        return df_view_parc_agrup
    df_view_parc_agrup = view_parc_agrup()

    def custos_blueme_sem_parcelamento():
        result, column_names = execute_query(GET_CUSTOS_BLUEME_SEM_PARCELAMENTO, conn)
        df_custos_blueme_sem_parcelamento = pd.DataFrame(result, columns=column_names)   

        df_custos_blueme_sem_parcelamento['Valor'] = df_custos_blueme_sem_parcelamento['Valor'].astype(float).round(2)
        df_custos_blueme_sem_parcelamento['Data_Vencimento'] = pd.to_datetime(df_custos_blueme_sem_parcelamento['Data_Vencimento'])
        df_custos_blueme_sem_parcelamento['Data_Competencia'] = pd.to_datetime(df_custos_blueme_sem_parcelamento['Data_Competencia'])
        df_custos_blueme_sem_parcelamento['Data_Lancamento'] = pd.to_datetime(df_custos_blueme_sem_parcelamento['Data_Lancamento'])
        df_custos_blueme_sem_parcelamento['Realizacao_Pgto'] = pd.to_datetime(df_custos_blueme_sem_parcelamento['Realizacao_Pgto'])
        df_custos_blueme_sem_parcelamento['Previsao_Pgto'] = pd.to_datetime(df_custos_blueme_sem_parcelamento['Previsao_Pgto'])    

        return df_custos_blueme_sem_parcelamento
    df_custos_blueme_sem_parcelamento = custos_blueme_sem_parcelamento()

    def custos_blueme_com_parcelamento():
        result, column_names = execute_query(GET_CUSTOS_BLUEME_COM_PARCELAMENTO, conn)
        df_custos_blueme_com_parcelamento = pd.DataFrame(result, columns=column_names)           

        df_custos_blueme_com_parcelamento['Valor_Parcela'] = df_custos_blueme_com_parcelamento['Valor_Parcela'].astype(float).round(2)
        df_custos_blueme_com_parcelamento['Valor_Original'] = df_custos_blueme_com_parcelamento['Valor_Original'].astype(float).round(2)
        df_custos_blueme_com_parcelamento['Valor_Liquido'] = df_custos_blueme_com_parcelamento['Valor_Liquido'].astype(float).round(2)

        df_custos_blueme_com_parcelamento['Vencimento_Parcela'] = pd.to_datetime(df_custos_blueme_com_parcelamento['Vencimento_Parcela'], format='%d/%m/%Y')
        df_custos_blueme_com_parcelamento['Previsao_Parcela'] = pd.to_datetime(df_custos_blueme_com_parcelamento['Previsao_Parcela'], format='%d/%m/%Y')
        df_custos_blueme_com_parcelamento['Realiz_Parcela'] = pd.to_datetime(df_custos_blueme_com_parcelamento['Realiz_Parcela'], format='%d/%m/%Y')
        df_custos_blueme_com_parcelamento['Data_Lancamento'] = pd.to_datetime(df_custos_blueme_com_parcelamento['Data_Lancamento'], format='%d/%m/%Y')

        return df_custos_blueme_com_parcelamento
    df_custos_blueme_com_parcelamento = custos_blueme_com_parcelamento()


    def extratos_bancarios():
        result, column_names = execute_query(GET_EXTRATOS_BANCARIOS, conn)
        df_extratos = pd.DataFrame(result, columns=column_names)

        df_extratos['Data_Transacao'] = df_extratos['Data_Transacao'].dt.date

        df_extratos['Valor'] = df_extratos['Valor'].astype(float).round(2)

        return df_extratos
    df_extratos = extratos_bancarios()

    def mutuos():
        result, column_names = execute_query(GET_MUTUOS, conn)
        df_mutuos = pd.DataFrame(result, columns=column_names)

        df_mutuos['Data_Mutuo'] = df_mutuos['Data_Mutuo'].dt.date
        df_mutuos['Valor'] = df_mutuos['Valor'].astype(float).round(2)

        return df_mutuos
    df_mutuos = mutuos()

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

    if "lojas" not in st.session_state:
        st.session_state["lojas"] = df_lojas

    if "faturam_zig" not in st.session_state:
        st.session_state["faturam_zig"] = df_faturam_zig

    if "receitas_extraord" not in st.session_state:
        st.session_state["receitas_extraord"] = df_receitas_extraord

    if "view_parc_agrup" not in st.session_state:
        st.session_state["view_parc_agrup"] = df_view_parc_agrup

    if "custos_blueme_sem_parcelamento" not in st.session_state:
        st.session_state["custos_blueme_sem_parcelamento"] = df_custos_blueme_sem_parcelamento

    if "custos_blueme_com_parcelamento" not in st.session_state:
        st.session_state["custos_blueme_com_parcelamento"] = df_custos_blueme_com_parcelamento

    if "extratos_bancarios" not in st.session_state:
        st.session_state["extratos_bancarios"] = df_extratos

    if "mutuos" not in st.session_state:
        st.session_state["mutuos"] = df_mutuos

if __name__ == "__main__":
    run()


