from pydantic import BaseModel
from fastapi import HTTPException, APIRouter
from connection import conexaoBanco

class Morador(BaseModel):
    Nome: str
    CPF: str
    Telefone: str
    Senha: str
    Apartamento: int

moradores_router = APIRouter(prefix='/moradores', tags=['moradores'])

@moradores_router.get("/")
def get_moradores():
    cursor = conexaoBanco.cursor(dictionary=True)
    comando_sql = 'select * from MORADOR'
    cursor.execute(comando_sql)
    resultado_consulta = cursor.fetchall()
    return resultado_consulta

@moradores_router.post("/")
def post_moradores(item: Morador):
    cursor = conexaoBanco.cursor(dictionary=True)
    comando_sql = 'INSERT INTO MORADOR (Nome, CPF, Telefone, Senha, Apartamento) VALUES (%(Nome)s, %(CPF)s, %(Telefone)s, %(Senha)s, %(Apartamento)s)'
    cursor.execute(comando_sql, item.model_dump())
    conexaoBanco.commit()
    return cursor.lastrowid

@moradores_router.patch("/{id}")
def patch_moradores(item: Morador, id: int):
    cursor = conexaoBanco.cursor(dictionary=True)
    comando_sql = 'select * from MORADOR where id = %(id)s'
    cursor.execute(comando_sql, { "id": id })
    resultado_consulta = cursor.fetchone()

    if resultado_consulta is None:
        raise HTTPException(status_code=404, detail="Morador não encontrado")
    
    comando_sql = '''
        UPDATE produtos SET Nome = %(name)s WHERE id = %(id)s
    '''
    values = item.model_dump()
    values['id'] = id
    cursor.execute(comando_sql, values)
    conexaoBanco.commit()
    return item.model_dump()

@moradores_router.delete("/{id}")
def delete_moradores(id: int):
    cursor = conexaoBanco.cursor(dictionary=True)
    comando_sql = 'select * from MORADOR where id = %(id)s'
    cursor.execute(comando_sql, { "id": id })
    resultado_consulta = cursor.fetchone()

    if resultado_consulta is None:
        raise HTTPException(status_code=404, detail="Morador não encontrado")

    comando_sql = 'DELETE FROM MORADOR WHERE id = %(id)s'
    cursor.execute(comando_sql, { "id": id })
    conexaoBanco.commit()
    return cursor.lastrowid