from pydantic import BaseModel

# Classe representando os dados do produto
class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float

def create_product(product, db_produtos):
    if id in db_produtos:
        return False
    db_produtos[product.id] = product
    return True

def remove_product(id_produto, db_carrinhos, db_produtos):
    if id_produto in db_produtos:
        del db_produtos[id_produto]
        remove_product_cart(id_produto, db_carrinhos)
        return True
    return False

def remove_product_cart(id_produto, db_carrinhos):
    for item in db_carrinhos:
        for product in db_carrinhos[item].id_produtos:
            if product == id_produto:
                db_carrinhos[item].id_produtos.remove(product)