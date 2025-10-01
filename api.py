# api.py
import requests

def buscar_internet(codigo: str) -> dict | None:
    """
    Busca um produto na API do OpenFoodFacts pelo código de barras.
    Retorna um dicionário com 'nome' e 'marca' ou None se não encontrado.
    """
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{codigo}.json"
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados.get('status') == 1:
                produto = dados['product']
                return {
                    "nome": produto.get("product_name", ""),
                    "marca": produto.get("brands", "")
                }
    except requests.RequestException as e:
        print("Erro na requisição à API:", e)
    return None
