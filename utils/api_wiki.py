import requests
from urllib.parse import urlparse, unquote

def get_wikipedia_summary(url: str, lang: str = "en") -> dict:
    """
    Retorna título, resumo e imagem principal de um artigo da Wikipédia.
    """
    # Extrai o título do artigo a partir da URL
    path = urlparse(url).path
    titulo = path.split("/")[-1]
    titulo = unquote(titulo)  # decodifica %20 etc

    # Monta URL da API
    api_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{titulo}"

    # Chama a API
    res = requests.get(api_url)

    if res.status_code == 200:
        data = res.json()
        return {
            "title": data.get("title", ""),
            "extract": data.get("extract", ""),
            "image": data.get("originalimage", {}).get("source", "") or data.get("thumbnail", {}).get("source", "")
        }
    else:
        raise Exception(f"Erro {res.status_code} ao acessar {api_url}")

