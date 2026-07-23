import requests
import base64
import io
from bot_instance import bot
from config import API_URL

@bot.callback_query_handler(func=lambda call: call.data.startswith("cupom_"))
def filtrar_cupons(call):
  # Avisa ao Telegram que o clique foi processado
  bot.answer_callback_query(call.id)
  
  # Extrai o termo de busca do callback_data (ex: 'cupom_shopee' vira 'shopee')
  termo_busca = call.data.replace("cupom_", "")
  if termo_busca == "todos":
    termo_busca = None

  try:
    response_cupons = requests.get(f"{API_URL}/cupons")
    
    if response_cupons.status_code == 200:
      cupons = response_cupons.json()
      
      # Filtra os cupons caso não seja a opção "Ver Todos"
      if termo_busca:
        cupons = [c for c in cupons if termo_busca in c.get('nome', '').lower()]

      if cupons:
        cabecalho = "🎟 *Resultados para a loja selecionada:*" if termo_busca else "🎟 *Confira todos os Cupons:*"
        bot.send_message(call.message.chat.id, cabecalho, parse_mode="Markdown")
        
        for c in cupons:
          if not c.get('publicado'):
            texto_cupom = f"*{c['nome']}*\n\n"
            if c.get('desconto'): 
              texto_cupom += f"📉 Desconto: {c['desconto']}\n"
            if c.get('codigo'): 
              texto_cupom += f"🎟 Código: `{c['codigo']}`\n"
            if c.get('limite_minimo'): 
              texto_cupom += f"🛒 Limite Mínimo: R$ {c['limite_minimo']}\n\n"
            if c.get('link'):
              texto_cupom += f"🔗 [Acessar Cupom]({c['link']})\n"
            
            # Envia com imagem se existir
            img_data = c.get('imagem')
            if img_data:
              try:
                if "base64," in img_data:
                  img_data = img_data.split("base64,")[1]
                
                img_bytes = base64.b64decode(img_data)
                bot.send_photo(call.message.chat.id, photo=io.BytesIO(img_bytes), caption=texto_cupom, parse_mode="Markdown")
              except Exception as e:
                print(f"Erro ao decodificar Base64 do cupom {c.get('nome')}: {e}")
                bot.send_message(call.message.chat.id, texto_cupom, parse_mode="Markdown")
            else:
              bot.send_message(call.message.chat.id, texto_cupom, parse_mode="Markdown")
      else:
        bot.send_message(call.message.chat.id, "Nenhum cupom encontrado para esta loja.", parse_mode="Markdown")
  except Exception as e:
    print(f"Erro ao buscar cupons: {e}")
    bot.send_message(call.message.chat.id, "Ocorreu um erro ao buscar os cupons.")