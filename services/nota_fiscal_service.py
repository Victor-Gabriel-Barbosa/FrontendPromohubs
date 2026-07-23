import requests
from config import API_URL

def salvar_nota_fiscal(user_id: int, username: str, valor_total: str, texto: str):
  dados_nota = {
    "telegram_user_id": user_id,
    "telegram_username": username,
    "valor_total": valor_total,
    "texto_extraido": texto
  }
  
  try:
    response = requests.post(f"{API_URL}/notas-fiscais", json=dados_nota)
    response.raise_for_status() 
    
    print("Nota fiscal salva com sucesso via API!")
    return response.json()
      
  except requests.exceptions.RequestException as e:
    print(f"Erro ao salvar nota fiscal na API: {e}")
    return None