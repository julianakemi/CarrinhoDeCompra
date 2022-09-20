from tracemalloc import DomainFilter
from fastapi import FastAPI

import user
import address as ad
import product as pd
import cart

app = FastAPI()

OK = "OK"
FALHA = "FALHA"

db_usuarios = {}
db_produtos = {}
db_end = {}        # enderecos_dos_usuarios
db_carrinhos = {}
db_usuario_end = [] # relação do usuário e endereço

############################
### API ###
############################

# Criar um usuário,
# se tiver outro usuário com o mesmo ID retornar falha, 
# se o email não tiver o @ retornar falha, 
# senha tem que ser maior ou igual a 3 caracteres, 
# senão retornar OK
@app.post("/usuario/")
async def criar_usuário(usuario: user.Usuario):
    return OK if user.create_user(usuario, db_usuarios) else FALHA

# Se o id do usuário existir, retornar os dados do usuário
# senão retornar falha
@app.get("/usuario/")
async def retornar_usuario(id: int):
    dados_usuario = user.get_user(id, db_usuarios)
    return dados_usuario if dados_usuario else FALHA


# Se existir um usuário com exatamente o mesmo nome, retornar os dados do usuário
# senão retornar falha
@app.get("/usuario/nome/")
async def retornar_usuario_com_nome(nome: str):
    search_result = user.search_user_by_name(nome, db_usuarios)
    return search_result if search_result else FALHA


# Se o id do usuário existir, deletar o usuário e retornar OK
# senão retornar falha
# ao deletar o usuário, deletar também endereços e carrinhos vinculados a ele
@app.delete("/usuario/")
async def deletar_usuario(id: int):
    return OK if user.remove_user(id, db_usuarios, db_end, db_carrinhos) else FALHA

# Se não existir usuário com o id_usuario retornar falha, 
# senão retornar uma lista de todos os endereços vinculados ao usuário
# caso o usuário não possua nenhum endereço vinculado a ele, retornar 
# uma lista vazia
### Estudar sobre Path Params (https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/usuario/{id_usuario}/enderecos/")
async def retornar_enderecos_do_usuario(id_usuario: int):
    user_addresses = ad.get_address(id_usuario, db_usuarios, db_usuario_end, db_end)
    return user_addresses if user_addresses else FALHA


# Retornar todos os emails que possuem o mesmo domínio
# (domínio do email é tudo que vêm depois do @)
# senão retornar falha
@app.get("/usuarios/emails/")
async def retornar_emails(dominio: str):
    lista_email = user.get_same_domain(dominio, db_usuarios)
    return FALHA if not lista_email else lista_email


# Se não existir usuário com o id_usuario retornar falha, 
# senão cria um endereço, vincula ao usuário e retornar OK
@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: ad.Endereco, id_usuario: int):
    return OK if ad.create_address(endereco, id_usuario, db_usuarios, db_end, db_usuario_end) else FALHA


# Se não existir endereço com o id_endereco retornar falha, 
# senão deleta endereço correspondente ao id_endereco e retornar OK
# (lembrar de desvincular o endereço ao usuário)
@app.delete("/endereco/{id_endereco}/")
async def deletar_endereco(id_endereco: int):
    return OK if ad.remove_address(id_endereco, db_end, db_usuario_end) else FALHA

# Se tiver outro produto com o mesmo ID retornar falha, 
# senão cria um produto e retornar OK
@app.post("/produto/")
async def criar_produto(produto: pd.Produto):
    return OK if pd.create_product(produto, db_produtos) else FALHA


# Se não existir produto com o id_produto retornar falha, 
# senão deleta produto correspondente ao id_produto e retornar OK
# (lembrar de desvincular o produto dos carrinhos do usuário)
@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    return OK if pd.remove_product(id_produto, db_carrinhos, db_produtos) else FALHA


# Se não existir usuário com o id_usuario ou id_produto retornar falha, 
# se não existir um carrinho vinculado ao usuário, crie o carrinho
# e retornar OK
# senão adiciona produto ao carrinho e retornar OK
@app.post("/carrinho/{id_usuario}/{id_produto}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int):
    carrinho = cart.add_to_cart(id_usuario, id_produto, db_usuarios, db_produtos, db_carrinhos)
    db_carrinhos[id_usuario].preco_total = cart.update_total_price(id_usuario, db_carrinhos, db_produtos)
    db_carrinhos[id_usuario].quantidade_de_produtos = cart.update_quantity(id_usuario, db_carrinhos)
    return OK if carrinho else FALHA
    
# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o carrinho de compras.
@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
    user_cart = cart.get_cart(id_usuario, db_carrinhos)
    return user_cart if user_cart else FALHA


# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o número de itens e o valor total do carrinho de compras.
@app.get("/carrinho/{id_usuario}/total")
async def retornar_total_carrinho(id_usuario: int):
    total_price = cart.get_total_price(id_usuario, db_carrinhos)
    quantity = cart.get_total_products(id_usuario, db_carrinhos)
    return total_price, quantity


# Se não existir usuário com o id_usuario retornar falha, 
# senão deleta o carrinho correspondente ao id_usuario e retornar OK
@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    return OK if cart.delete_cart(id_usuario, db_carrinhos) else FALHA


@app.get("/")
async def bem_vinda():
    site = "Seja bem vinda"
    return site.replace('\n', '')