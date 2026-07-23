from bot_instance import bot
import requests
import io
from config import API_URL

@bot.callback_query_handler(func=lambda call: call.data.startswith('promo_'))
def processar_busca_promocoes(call):
  bot.answer_callback_query(call.id, "Buscando promoções...")
  
  try:
    response_promocoes = requests.get(f"{API_URL}/promocoes")
    
    if response_promocoes.status_code == 200:
      promocoes = response_promocoes.json()

      if promocoes:
        promocoes_filtradas = []
        
        # Filtragem de preço
        for p in promocoes:
          if not p.get('publicado'):
            continue
              
          preco_final = p.get('preco_final')
          
          if call.data == "promo_all":
            promocoes_filtradas.append(p)
            continue
          
          # Converte e garante que o preço é numérico
          if preco_final is not None:
            try:
              preco = float(str(preco_final).replace(',', '.'))
              
              # Filtra conforme a opção selecionada
              if (call.data == "promo_0_20" and preco <= 20.0) or \
                (call.data == "promo_20_50" and 20.0 < preco <= 50.0) or \
                (call.data == "promo_50_plus" and preco > 50.0):
                
                promocoes_filtradas.append(p)
            except ValueError:
              pass 

        # Processa e envia as mensagens
        if promocoes_filtradas:
          cabecalho = f"🎮 *Promoções Encontradas ({len(promocoes_filtradas)}):*"
          bot.send_message(call.message.chat.id, cabecalho, parse_mode="Markdown")
          
          for p in promocoes_filtradas:
            texto_produto = f"*{p.get('nome')}*\n\n"
            
            if p.get('desconto'): 
              texto_produto += f"📉 Desconto: {p.get('desconto')}\n"
            if p.get('preco_original'): 
              texto_produto += f"💰 Preço Original: R$ {p.get('preco_original')}\n"
            if p.get('preco_final') is not None: 
              texto_produto += f"🔥 Preço Final: R$ {p.get('preco_final')}\n\n"
            if p.get('link'): 
              texto_produto += f"🔗 [Acessar na Loja]({p.get('link')})\n"
                
            img_url = p.get('imagem')
            if img_url:
              try:
                resposta_img = requests.get(img_url)
                if resposta_img.status_code == 200:
                  img_bytes = io.BytesIO(resposta_img.content)
                  bot.send_photo(call.message.chat.id, photo=img_bytes, caption=texto_produto, parse_mode="Markdown")
                else:
                  bot.send_message(call.message.chat.id, texto_produto, parse_mode="Markdown")
                          
              except Exception as e:
                print(f"Erro ao enviar foto do jogo {p.get('nome')}: {e}")
                bot.send_message(call.message.chat.id, texto_produto, parse_mode="Markdown")
            else:
              bot.send_message(call.message.chat.id, texto_produto, parse_mode="Markdown")
        else:
          bot.send_message(call.message.chat.id, "Nenhuma promoção encontrada nessa faixa de preço específica.", parse_mode="Markdown")
      else:
        bot.send_message(call.message.chat.id, "Nenhuma promoção encontrada no banco de dados.", parse_mode="Markdown")
                
  except Exception as e:
    print(f"Erro ao buscar promoções: {e}")
    bot.send_message(call.message.chat.id, "Ocorreu um erro ao conectar com a API.")