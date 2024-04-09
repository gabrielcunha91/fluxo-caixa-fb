GET_LOJAS = """
SELECT tl.ID as 'ID', 
tl.NOME as 'Nome' 
FROM T_LOJAS tl 
LIMIT 5
"""