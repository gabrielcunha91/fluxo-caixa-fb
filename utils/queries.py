
GET_SALDOS_BANCARIOS = """
SELECT * FROM View_Saldos_Bancarios
WHERE `Data` >= CURDATE() 
AND `Data` < DATE_ADD(CURDATE(), INTERVAL 8 DAY)
AND Empresa IS NOT NULL
ORDER BY `Data` ASC
"""

GET_VALOR_LIQUIDO_RECEBIDO = '''
SELECT * FROM View_Receitas_Extratos_Manual
WHERE `Data` >= CURDATE() 
AND `Data` < DATE_ADD(CURDATE(), INTERVAL 8 DAY)
AND Empresa IS NOT NULL
ORDER BY `Data` ASC
'''

GET_PROJECAO_ZIG = '''
SELECT * FROM View_Projecao_Zig_Agrupadas
WHERE `Data` >= CURDATE() 
AND `Data` < DATE_ADD(CURDATE(), INTERVAL 8 DAY)
AND Empresa IS NOT NULL
ORDER BY `Data` ASC
'''

GET_RECEITAS_EXTRAORD = '''
SELECT * FROM View_Previsao_Receitas_Extraord
WHERE `Data` >= CURDATE() 
AND `Data` < DATE_ADD(CURDATE(), INTERVAL 8 DAY)
AND Empresa IS NOT NULL
ORDER BY `Data` ASC
'''

GET_DESPESAS_APROVADAS = '''
SELECT
vvap.Empresa as 'Empresa',
vvap.`Data` as 'Data',
SUM(vvap.Valores_Aprovados_Previsao) as 'Despesas_Aprovadas_Pendentes' 
FROM View_Valores_Aprovados_Previsao vvap
WHERE `Data` >= CURDATE() 
AND `Data` < DATE_ADD(CURDATE(), INTERVAL 8 DAY)
AND Empresa IS NOT NULL
GROUP BY `Data`, Empresa  
ORDER BY `Data` ASC
'''

GET_DESPESAS_PAGAS = '''
SELECT
vvap.Empresa as 'Empresa',
vvap.`Data` as 'Data',
SUM(vvap.Valores_Pagos) as 'Despesas_Pagas' 
FROM View_Valores_Pagos_por_Previsao vvap
WHERE `Data` >= CURDATE() 
AND `Data` < DATE_ADD(CURDATE(), INTERVAL 8 DAY)
AND Empresa IS NOT NULL
GROUP BY `Data`, Empresa  
ORDER BY `Data` ASC
'''

GET_LOJAS = '''
SELECT
tl.ID as 'ID_Loja',
tl.NOME as 'Loja'
FROM T_LOJAS tl 
'''

GET_FATURAMENTO_ZIG = '''
SELECT
tzf.ID AS 'tzf_ID',
tl.ID as 'ID_Loja',
tl.NOME AS 'Loja',
tzf.DATA AS 'Data_Faturamento',
tzf.VALOR AS 'Valor_Faturado',
tzf.TIPO_PAGAMENTO AS 'Tipo_Pagamento'
FROM T_ZIG_FATURAMENTO tzf
LEFT JOIN T_LOJAS tl ON (tzf.FK_LOJA = tl.ID)
WHERE (tzf.DATA >= '2024-01-01 00:00:00' AND tzf.VALOR > 0)
ORDER BY tl.NOME, tzf.DATA;
'''

GET_RECEITAS_EXTRAORD_CONCILIACAO = '''
SELECT
tre.ID as 'ID_receita',
tl.ID as 'ID_Loja',
tl.NOME as 'Loja',
trec3.NOME as 'Cliente',
trec.CLASSIFICACAO as 'Classificacao',
tep.ID as 'ID_Evento',
tep.NOME_EVENTO as 'Nome_Evento',
tre.VALOR as 'Valor_Total',
tfdp.DESCRICAO as 'Forma_de_Pagamento',
CAST(tre.DATA_OCORRENCIA AS DATE) as 'Data_Competencia',
tsp.DESCRICAO as 'Status_Pgto',
tre.VALOR_CATEGORIA_AB as 'Categ_AB',
tre.VALOR_CATEGORIA_ALUGUEL as 'Categ_Aluguel',
tre.VALOR_CATEGORIA_ARTISTICO as 'Categ_Artist',
tre.VALOR_CATEGORIA_COUVERT as 'Categ_Couvert',
tre.VALOR_CATEGORIA_LOCACAO as 'Categ_Locacao',
tre.VALOR_CATEGORIA_PATROCINIO as 'Categ_Patroc',
tre.VALOR_CATEGORIA_TAXA_SERVICO as 'Categ_Taxa_Serv',
tre.VALOR_PARCELA_1 as 'Valor_Parc_1',
tre.DATA_VENCIMENTO_PARCELA_1 as 'Data_Venc_Parc_1',
tre.DATA_RECEBIMENTO_PARCELA_1 as 'Data_Receb_Parc_1',
tre.VALOR_PARCELA_2 as 'Valor_Parc_2',
tre.DATA_VENCIMENTO_PARCELA_2 as 'Data_Venc_Parc_2',
tre.DATA_RECEBIMENTO_PARCELA_2 as 'Data_Receb_Parc_2',
tre.VALOR_PARCELA_3 as 'Valor_Parc_3',
tre.DATA_VENCIMENTO_PARCELA_3 as 'Data_Venc_Parc_3',
tre.DATA_RECEBIMENTO_PARCELA_3 as 'Data_Receb_Parc_3',
tre.VALOR_PARCELA_4 as 'Valor_Parc_4',
tre.DATA_VENCIMENTO_PARCELA_4 as 'Data_Venc_Parc_4',
tre.DATA_RECEBIMENTO_PARCELA_4 as 'Data_Receb_Parc_4',
tre.VALOR_PARCELA_5 as 'Valor_Parc_5',
tre.DATA_VENCIMENTO_PARCELA_5 as 'Data_Venc_Parc_5',
tre.DATA_RECEBIMENTO_PARCELA_5 as 'Data_Receb_Parc_5'
FROM T_RECEITAS_EXTRAORDINARIAS tre
INNER JOIN T_EMPRESAS te ON (tre.FK_EMPRESA = te.ID)
INNER JOIN T_LOJAS tl ON (te.FK_LOJA = tl.ID)
LEFT JOIN T_RECEITAS_EXTRAORDINARIAS_CLASSIFICACAO trec ON (tre.FK_CLASSIFICACAO = trec.ID)
LEFT JOIN T_RECEITAS_EXTRAORDINARIAS_CLIENTE trec3 ON (tre.FK_CLIENTE = trec3.ID)
LEFT JOIN T_EVENTO_PRE tep ON (tre.FK_EVENTO = tep.ID)
LEFT JOIN T_STATUS_PAGAMENTO tsp ON (tre.FK_STATUS_PGTO = tsp.ID)
LEFT JOIN T_FORMAS_DE_PAGAMENTO tfdp ON (tep.FK_FORMA_PAGAMENTO = tfdp.ID)
'''