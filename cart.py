from pydantic import BaseModel
from typing import List
from functools import reduce

# Classe representando o carrinho de compras de um cliente com uma lista de produtos
class CarrinhoDeCompras(BaseModel):
    id_produtos: List[int] = []
    preco_total: float = 0 
    quantidade_de_produtos: int = 0

def add_to_cart(id_usuario, id_produto, db_usuarios, db_produtos, db_carrinhos):
    if id_usuario not in db_usuarios:
        return False
    if id_produto not in db_produtos:
        return False
    if id_usuario not in db_carrinhos:
        db_carrinhos[id_usuario] = CarrinhoDeCompras()
    db_carrinhos[id_usuario].id_produtos.append(id_produto)
    return True

def update_total_price(id_usuario, db_carrinhos, db_produtos):
    total = 0
    for item in db_carrinhos[id_usuario].id_produtos:
        total += db_produtos[item].preco
    return total

def update_quantity(id_usuario, db_carrinhos):
    return len(db_carrinhos[id_usuario].id_produtos)

def get_cart(id_usuario, db_carrinhos):
    if id_usuario not in db_carrinhos:
        return False
    return db_carrinhos[id_usuario]

def get_total_price(id_usuario, db_carrinhos):
    if id_usuario not in db_carrinhos:
        return False
    return db_carrinhos[id_usuario].preco_total

def get_total_products(id_usuario, db_carrinhos):
    if id_usuario not in db_carrinhos:
        return False
    return db_carrinhos[id_usuario].quantidade_de_produtos

def delete_cart(id_usuario, db_carrinhos):
    if id_usuario not in db_carrinhos:
        return False
    del db_carrinhos[id_usuario]
    return True