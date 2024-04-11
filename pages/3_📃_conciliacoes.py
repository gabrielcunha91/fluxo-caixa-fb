import streamlit as st
import pandas as pd
import openpyxl
import os

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

df_view_parc_agrup = st.session_state["view_parc_agrup"]

df_view_parc_agrup

df_custos_blueme_sem_parcelamento = st.session_state["custos_blueme_sem_parcelamento"]

df_custos_blueme_sem_parcelamento

df_custos_blueme_com_parcelamento = st.session_state["custos_blueme_com_parcelamento"]

df_custos_blueme_com_parcelamento

df_extratos = st.session_state["extratos_bancarios"]

df_extratos

df_mutuos = st.session_state["mutuos"]

df_mutuos



# excel_filename = "Conciliacao_FB.xlsx"  # Nome do arquivo Excel na mesma pasta que o código

# # def excel_export():
        
# #     id_loja = 292
    
# #     # Atualizando Zig
# #     df_faturam_zig_loja = df_faturam_zig[df_faturam_zig['ID_Loja'] == id_loja]
# #     sheet_name_zig = 'df_faturam_zig'

# #     if os.path.exists(excel_filename):
# #         wb = openpyxl.load_workbook(excel_filename)
# #     else:
# #         wb = openpyxl.Workbook()

# #     if sheet_name_zig in wb.sheetnames:
# #         wb.remove(wb[sheet_name_zig])

# #     # Convertendo DataFrame para uma planilha Excel
# #     ws = wb.create_sheet(title=sheet_name_zig)
# #     for r_idx, row in enumerate(df_faturam_zig_loja.iterrows(), start=1):
# #         for c_idx, value in enumerate(row[1], start=1):
# #             ws.cell(row=r_idx, column=c_idx, value=value)

# #     # Salvando o arquivo Excel
# #     wb.save(excel_filename)        

# #     return excel_filename


# def export_to_excel(df, sheet_name, excel_filename):
#     if os.path.exists(excel_filename):
#         wb = openpyxl.load_workbook(excel_filename)
#     else:
#         wb = openpyxl.Workbook()

#     if sheet_name in wb.sheetnames:
#         wb.remove(wb[sheet_name])

#     ws = wb.create_sheet(title=sheet_name)
#     for r_idx, row in enumerate(df.iterrows(), start=1):
#         for c_idx, value in enumerate(row[1], start=1):
#             ws.cell(row=r_idx, column=c_idx, value=value)

#     wb.save(excel_filename)

# # Chama a função para exportar o arquivo Excel
# if st.button('Gerar Excel'):
#     id_loja = 292
#     df_faturam_zig_loja = df_faturam_zig[df_faturam_zig['ID_Loja'] == id_loja]
#     excel_filename = 'Conciliacao_FB.xlsx'
#     sheet_name_zig = 'df_faturam_zig'
#     export_to_excel(df_faturam_zig_loja, sheet_name_zig, excel_filename)
#     st.success('Arquivo exportado com sucesso!')
