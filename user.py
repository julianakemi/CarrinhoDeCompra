from pydantic import BaseModel

class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    senha: str

def create_user(usuario, db_usuarios):
    if not check_user(usuario, db_usuarios):
        return False
    db_usuarios[usuario.id] = usuario
    return True

def remove_user(id, db_usuarios, db_end, db_carrinhos):
    #Todo deletar carrinho e endereço vinculado ao usuario
    if id in db_usuarios:
        del db_usuarios[id]
        return True
    return False

def get_user(id, db_usuarios):
    if id in db_usuarios:
        return db_usuarios[id]
    return False

def check_user(usuario, db_usuarios):
    if usuario.id in db_usuarios:
        return False
    if '@' not in usuario.email:
        return False
    if len(usuario.senha) < 3:
        return False
    return True

def search_user_by_name(nome, db_usuarios):
    for usuario in db_usuarios.values():
        if usuario.nome == nome:
            return usuario
    return False

def get_same_domain(domain, db_usuarios):
    return [user for user in db_usuarios.values() if user.email.split("@")[1] == domain]