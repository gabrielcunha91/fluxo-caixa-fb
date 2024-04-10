GET_LOJAS = """
SELECT tl.ID as 'ID', 
tl.NOME as 'Nome' 
FROM T_LOJAS tl 
LIMIT 5
"""

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
