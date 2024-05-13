
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
WHERE (tzf.DATA >= '2024-04-01 00:00:00' AND tzf.VALOR > 0)
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

GET_VIEW_PARC_AGRUP = '''
SELECT 
ROW_NUMBER() OVER (ORDER BY te.NOME_FANTASIA ASC, vpa.DATA_VENCIMENTO ASC) AS 'Numero_Linha',
vpa.ID as 'ID_Receita',
tl.ID as 'ID_Loja',
tl.NOME as 'Loja',
trec.NOME as 'Cliente',
vpa.DATA_VENCIMENTO as 'Data_Vencimento',
vpa.DATA_RECEBIMENTO as 'Data_Recebimento',
vpa.VALOR_PARCELA as 'Valor_Parcela',
tre.DATA_OCORRENCIA as 'Data_Ocorrencia',
trec2.CONCAT_CATEGORIA_CLASSIFICACAO as 'Categoria_Class'
FROM View_Parcelas_Agrupadas vpa
INNER JOIN T_EMPRESAS te ON (vpa.FK_EMPRESA = te.ID)
INNER JOIN T_LOJAS tl ON (te.FK_LOJA = tl.ID)
LEFT JOIN T_RECEITAS_EXTRAORDINARIAS tre ON (vpa.ID = tre.ID)
LEFT JOIN T_RECEITAS_EXTRAORDINARIAS_CLIENTE trec ON (vpa.FK_CLIENTE = trec.ID)
LEFT JOIN T_RECEITAS_EXTRAORDINARIAS_CLASSIFICACAO trec2 ON (tre.FK_CLASSIFICACAO = trec2.ID)
WHERE vpa.DATA_VENCIMENTO IS NOT NULL
ORDER BY vpa.DATA_RECEBIMENTO DESC;
'''

GET_CUSTOS_BLUEME_SEM_PARCELAMENTO = '''
SELECT 
tdr.ID as 'ID_Despesa',
tdr.FK_DESPESA_TEKNISA as 'FK_Despesa_Teknisa',
tl.ID as 'ID_Loja',
te.NOME_FANTASIA as 'Casa',
tf.CORPORATE_NAME as 'Fornecedor_Razao_Social',
tdr.VALOR_LIQUIDO as 'Valor',
tdr.VENCIMENTO as 'Data_Vencimento',
tc.`DATA` as 'Previsao_Pgto',
tc2.`DATA` as 'Realizacao_Pgto',    
tdr.COMPETENCIA as 'Data_Competencia',
tdr.LANCAMENTO as 'Data_Lancamento',
tfdp.DESCRICAO as 'Forma_Pagamento',
tccg.DESCRICAO as 'Class_Cont_1',
tccg2.DESCRICAO as 'Class_Cont_2',
CONCAT(YEAR(tdr.VENCIMENTO),'-',WEEKOFYEAR(tdr.VENCIMENTO)) as 'Ano_Semana_Vencimento', 
tscd.DESCRICAO as 'Status_Conf_Document',
tsad.DESCRICAO as 'Status_Aprov_Diret',
tsac.DESCRICAO as 'Status_Aprov_Caixa',
tsp.DESCRICAO as 'Status_Pgto'
FROM T_DESPESA_RAPIDA tdr
INNER JOIN T_EMPRESAS te ON (tdr.FK_LOJA = te.ID)
LEFT JOIN T_LOJAS tl ON (te.FK_LOJA = tl.ID)
LEFT JOIN T_FORMAS_DE_PAGAMENTO tfdp ON (tdr.FK_FORMA_PAGAMENTO = tfdp.ID)
LEFT JOIN T_FORNECEDOR tf ON (tdr.FK_FORNECEDOR = tf.ID)
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 tccg ON (tdr.FK_CLASSIFICACAO_CONTABIL_GRUPO_1 = tccg.ID)
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 tccg2 ON (tdr.FK_CLASSIFICACAO_CONTABIL_GRUPO_2 = tccg2.ID)
LEFT JOIN T_STATUS_CONFERENCIA_DOCUMENTACAO tscd ON (tdr.FK_CONFERENCIA_DOCUMENTACAO = tscd.ID)
LEFT JOIN T_STATUS_APROVACAO_DIRETORIA tsad ON (tdr.FK_APROVACAO_DIRETORIA = tsad.ID)
LEFT JOIN T_STATUS_APROVACAO_CAIXA tsac ON (tdr.FK_APROVACAO_CAIXA = tsac.ID)
LEFT JOIN T_STATUS_PAGAMENTO tsp ON (tdr.FK_STATUS_PGTO = tsp.ID)
LEFT JOIN T_CALENDARIO tc ON (tdr.PREVISAO_PAGAMENTO = tc.ID)	
LEFT JOIN T_CALENDARIO tc2 ON (tdr.FK_DATA_REALIZACAO_PGTO = tc2.ID)
LEFT JOIN T_DEPESA_PARCELAS tdp ON (tdp.FK_DESPESA = tdr.ID)
WHERE 
    tl.ID IS NOT NULL
    AND tdp.FK_DESPESA IS NULL
    AND (tdr.FK_DESPESA_TEKNISA IS NULL OR tdr.BIT_DESPESA_TEKNISA_PENDENTE = 1)
    AND tsp.DESCRICAO = "Pago"
ORDER BY 
    tc2.`DATA` DESC
'''

GET_CUSTOS_BLUEME_COM_PARCELAMENTO = '''
SELECT 
tdp.ID as 'ID_Parcela',
tdr.ID as 'ID_Despesa',
te.NOME_FANTASIA as 'Empresa',
tl.ID as 'ID_Loja',
tf.CORPORATE_NAME as 'Fornecedor_Razao_Social',
CASE
    WHEN tdp.FK_DESPESA IS NOT NULL
        THEN 'True'
    ELSE 'False'
END AS 'Parcelamento',
CASE 
    WHEN tdp.FK_DESPESA IS NOT NULL
        THEN COUNT(tdp.ID) OVER (PARTITION BY tdr.ID)
    ELSE NULL 
END AS 'Qtd_Parcelas',
tdp.PARCELA as 'Num_Parcela',
tdp.VALOR as 'Valor_Parcela',
DATE_FORMAT(DATE_ADD(tdp.`DATA`, INTERVAL 30 SECOND), '%d/%m/%Y') as 'Vencimento_Parcela',
DATE_FORMAT(DATE_ADD(tc.`DATA`, INTERVAL 30 SECOND), '%d/%m/%Y') AS 'Previsao_Parcela',
DATE_FORMAT(DATE_ADD(tc2.`DATA`, INTERVAL 30 SECOND), '%d/%m/%Y') AS 'Realiz_Parcela',
tdr.VALOR_PAGAMENTO as 'Valor_Original',
tdr.VALOR_LIQUIDO as 'Valor_Liquido',
DATE_ADD(STR_TO_DATE(tdr.LANCAMENTO, '%Y-%m-%d'), INTERVAL 30 SECOND) as 'Data_Lancamento',
tfdp.DESCRICAO as 'Forma_Pagamento',
tccg.DESCRICAO as 'Class_Cont_1',
tccg2.DESCRICAO as 'Class_Cont_2',
CONCAT(YEAR(tdr.VENCIMENTO),'-',WEEKOFYEAR(tdr.VENCIMENTO)) as 'Ano_Semana_Vencimento', 
tscd.DESCRICAO as 'Status_Conf_Document',
tsad.DESCRICAO as 'Status_Aprov_Diret',
tsac.DESCRICAO as 'Status_Aprov_Caixa',
CASE
    WHEN tdp.PARCELA_PAGA = 1 
        THEN 'Parcela_Paga'
    ELSE 'Parcela_Pendente'
END as 'Status_Pgto'
FROM T_DESPESA_RAPIDA tdr
INNER JOIN T_EMPRESAS te ON (tdr.FK_LOJA = te.ID)
LEFT JOIN T_LOJAS tl ON (te.FK_LOJA = tl.ID)
LEFT JOIN T_FORMAS_DE_PAGAMENTO tfdp ON (tdr.FK_FORMA_PAGAMENTO = tfdp.ID)
LEFT JOIN T_FORNECEDOR tf ON (tdr.FK_FORNECEDOR = tf.ID)
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 tccg ON (tdr.FK_CLASSIFICACAO_CONTABIL_GRUPO_1 = tccg.ID)
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 tccg2 ON (tdr.FK_CLASSIFICACAO_CONTABIL_GRUPO_2 = tccg2.ID)
LEFT JOIN T_STATUS_CONFERENCIA_DOCUMENTACAO tscd ON (tdr.FK_CONFERENCIA_DOCUMENTACAO = tscd.ID)
LEFT JOIN T_STATUS_APROVACAO_DIRETORIA tsad ON (tdr.FK_APROVACAO_DIRETORIA = tsad.ID)
LEFT JOIN T_STATUS_APROVACAO_CAIXA tsac ON (tdr.FK_APROVACAO_CAIXA = tsac.ID)
LEFT JOIN T_STATUS_PAGAMENTO tsp ON (tdr.FK_STATUS_PGTO = tsp.ID)
LEFT JOIN T_DEPESA_PARCELAS tdp ON (tdp.FK_DESPESA = tdr.ID)
LEFT JOIN T_CALENDARIO tc ON (tdp.FK_PREVISAO_PGTO = tc.ID)
LEFT JOIN T_CALENDARIO tc2 ON (tdp.FK_DATA_REALIZACAO_PGTO = tc2.ID)
WHERE 
    tdp.FK_DESPESA IS NOT NULL
    AND (tdr.FK_DESPESA_TEKNISA IS NULL OR tdr.BIT_DESPESA_TEKNISA_PENDENTE = 1)
    AND tdp.PARCELA_PAGA = 1
ORDER BY 
    tc2.`DATA` DESC
'''

GET_EXTRATOS_BANCARIOS = '''
SELECT
teb.ID as 'ID_Extrato_Bancario',
tcb.ID as 'ID_Conta_Bancaria',
tcb.NOME_DA_CONTA as 'Nome_Conta_Bancaria',
tl.ID as 'ID_Loja',
tl.NOME as 'Loja',
teb.DATA_TRANSACAO as 'Data_Transacao',
CASE 
    WHEN teb.FK_TIPO_CREDITO_DEBITO = 100 THEN 'CREDITO'
    ELSE 'DEBITO'
END as 'Tipo_Credito_Debito',
teb.DESCRICAO_TRANSACAO as 'Descricao_Transacao',
teb.VALOR as 'Valor'
FROM T_EXTRATOS_BANCARIOS teb
INNER JOIN T_CONTAS_BANCARIAS tcb ON (teb.FK_CONTA_BANCARIA = tcb.ID)
INNER JOIN T_LOJAS tl ON (tcb.FK_LOJA = tl.ID)
ORDER BY teb.DATA_TRANSACAO DESC
'''

GET_MUTUOS = '''
SELECT
tm.ID as 'Mutuo_ID',
tm.`DATA` as 'Data_Mutuo',
tl.ID as 'ID_Loja_Saida',
tl.NOME as 'Loja_Saida',
tl2.ID as 'ID_Loja_Entrada',
tl2.NOME as 'Loja_Entrada',
tm.VALOR as 'Valor',
tm.TAG_FATURAM_ZIG as 'Tag_Faturam_Zig'
FROM T_MUTUOS tm 
LEFT JOIN T_LOJAS tl ON (tm.FK_LOJA_SAIDA = tl.ID)
LEFT JOIN T_LOJAS tl2 ON (tm.FK_LOJA_ENTRADA = tl2.ID)
ORDER BY tm.`DATA` DESC
'''

GET_TESOURARIA_TRANSACOES = '''
SELECT
ttt.ID as 'tes_ID',
tl.ID as 'ID_Loja',
tl.NOME as 'Loja',
ttt.DATA_TRANSACAO as 'Data_Transacao',
ttt.VALOR as 'Valor',
ttt.DESCRICAO as 'Descricao'
FROM T_TESOURARIA_TRANSACOES ttt 
INNER JOIN T_LOJAS tl ON (ttt.FK_LOJA = tl.ID)   
'''

