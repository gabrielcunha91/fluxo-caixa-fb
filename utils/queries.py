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



