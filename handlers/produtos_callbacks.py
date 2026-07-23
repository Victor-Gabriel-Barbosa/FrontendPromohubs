import requests
import base64
import io
from bot_instance import bot
from config import API_URL

@bot.callback_query_handler(func=lambda call: call.data.startswith("produto_"))
def filtrar_produtos(call):
  bot.answer_callback_query(call.id)
  
  # Extrai o termo de busca do callback_data (ex: 'produto_smartphone' vira 'smartphone')
  termo_busca = call.data.replace("produto_", "")
  if termo_busca == "todos":
    termo_busca = None

  try:
    response_produtos = requests.get(f"{API_URL}/produtos")
    
    if response_produtos.status_code == 200:
      produtos = response_produtos.json()
      
      # Filtra os produtos caso não seja a opção "Ver Todos"
      if termo_busca:
        produtos = [p for p in produtos if termo_busca in p.get('nome', '').lower()]

      if produtos:
        cabecalho = "🛒 *Resultados para a categoria selecionada:*" if termo_busca else "🛒 *Confira todas as Promoções:*"
        bot.send_message(call.message.chat.id, cabecalho, parse_mode="Markdown")
        
        for p in produtos:
          if not p.get('publicado'):
            texto_produto = f"*{p['nome']}*\n\n"
            if p.get('preco'): 
              texto_produto += f"💸 Preço: R$ {p['preco']}\n"
            if p.get('preco_parcelado'): 
              texto_produto += f"💳 Parcelado: R$ {p['preco_parcelado']}\n"
            if p.get('cupom'):
              texto_produto += f"🎟 Cupom: `{p['cupom']}`\n\n"
            if p.get('link'): 
              texto_produto += f"🔗 [Acessar Promoção]({p['link']})\n"
              
            # Envia com imagem se existir
            img_data = p.get('imagem')
            if img_data:
              try:
                if "base64," in img_data:
                  img_data = img_data.split("base64,")[1]
                
                img_bytes = base64.b64decode(img_data)
                bot.send_photo(call.message.chat.id, photo=io.BytesIO(img_bytes), caption=texto_produto, parse_mode="Markdown")
              except Exception as e:
                print(f"Erro ao decodificar Base64 do produto {p.get('nome')}: {e}")
                bot.send_message(call.message.chat.id, texto_produto, parse_mode="Markdown")
            else:
              bot.send_message(call.message.chat.id, texto_produto, parse_mode="Markdown")
      else:
        bot.send_message(call.message.chat.id, "Nenhum produto encontrado nesta categoria.", parse_mode="Markdown")
  except Exception as e:
    print(f"Erro ao buscar produtos: {e}")
    bot.send_message(call.message.chat.id, "Ocorreu um erro ao buscar os produtos.")