import requests

def buscar_internet(codigo):
    url = f"https://world.openfoodfacts.org/api/v0/product/{codigo}.json"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        if dados.get('status') == 1:
            produto = dados['product']
            return {
                "nome" : produto.get("product_name", ""),
                "marca" : produto.get("brands", "")
            }
    return None