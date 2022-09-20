from pydantic import BaseModel
from typing import List

import user

# Classe representando os dados do endereço do cliente
class Endereco(BaseModel):
    rua: str
    cep: str
    cidade: str
    estado: str

def create_address(address, id_usuario, db_usuarios, db_end, db_usuario_end):
    if id_usuario in db_usuarios:
        id_end = len(db_end) + 1
        relation = (id_usuario, id_end)
        db_usuario_end.append(relation)
        db_end[id_end] = address
        return True
    return False

def get_address(id_usuario, db_usuarios, db_usuario_end, db_end):
    if id_usuario in db_usuarios:
        lista_end = []
        for item in db_usuario_end:
            if item [0] == id_usuario:
                lista_end.append(db_end[item[1]])
        return lista_end
    return False

def remove_address(id_endereco, db_end, db_usuario_end):
    if id_endereco in db_end:
        del db_end[id_endereco]
        for item in db_usuario_end:
            if item[1] == id_endereco:
                db_usuario_end.remove(item)
        return True
    return False

# Classe representando a lista de endereços de um cliente
class ListaDeEnderecosDoUsuario(BaseModel):
    usuario: user.Usuario
    enderecos: List[Endereco] = []