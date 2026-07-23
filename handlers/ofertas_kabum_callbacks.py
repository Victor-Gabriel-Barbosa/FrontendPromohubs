import requests
from bot_instance import bot
from config import API_URL

@bot.callback_query_handler(func=lambda call: call.data.startswith("kabum_"))
def filtrar_ofertas_kabum(call):
  # Avisa ao Telegram que o clique foi processado
  bot.answer_callback_query(call.id)

  # Extrai o termo de busca do callback_data (ex: 'kabum_video' vira 'video')
  termo_busca = call.data.replace("kabum_", "")
  
  # Dicionário para traduzir o sufixo do botão em uma palavra de busca real para o filtro
  mapa_buscas = {
    "video": "placa de vídeo",
    "processador": "processador",
    "notebook": "notebook",
    "periferico": "teclado",
  }
  
  # Se for 'todas', o termo_real fica como None
  termo_real = mapa_buscas.get(termo_busca)

  try:
    response_ofertas = requests.get(f"{API_URL}/ofertas-kabum")

    if response_ofertas.status_code == 200:
      ofertas = response_ofertas.json()

      # Filtra as ofertas por nome caso uma categoria específica tenha sido escolhida
      if termo_real:
        ofertas = [o for o in ofertas if termo_real in o.get('nome', '').lower()]

      if ofertas:
        cabecalho = f"🥷 *Resultados para a busca:* {termo_real.title()}" if termo_real else "🥷 *Confira todas as ofertas do dia:*"
        bot.send_message(call.message.chat.id, cabecalho, parse_mode="Markdown")

        # Limita a 10 ofertas
        for o in ofertas[:10]:
          # Verifica se a oferta está marcada como publicada
          if o.get('publicado'):
            texto_oferta = f"*{o['nome']}*\n\n"
            
            # Validações para não exibir 'N/A' caso o scraper não encontre os dados
            if o.get('preco') and o.get('preco') != 'N/A': 
              texto_oferta += f"💰 Preço: {o['preco']}\n"
            if o.get('desconto') and o.get('desconto') != 'N/A': 
              texto_oferta += f"📉 Desconto: {o['desconto']}\n\n"
            if o.get('link'):
              texto_oferta += f"🔗 [Acessar Oferta]({o['link']})\n"

            imagem_url = o.get('imagem')
            
            # Envia a imagem da oferta se disponível
            if imagem_url and imagem_url != 'N/A':
              try:
                bot.send_photo(call.message.chat.id, photo=imagem_url, caption=texto_oferta, parse_mode="Markdown")
              except Exception as e:
                print(f"Erro ao enviar imagem da oferta {o.get('nome')}: {e}")
                bot.send_message(call.message.chat.id, texto_oferta, parse_mode="Markdown")
            else:
              bot.send_message(call.message.chat.id, texto_oferta, parse_mode="Markdown")
      else:
        bot.send_message(call.message.chat.id, "Nenhuma oferta encontrada para esta categoria hoje.", parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, f"Erro na API. Código: {response_ofertas.status_code}")
  except Exception as e:
    print(f"Erro ao buscar ofertas: {e}")
    bot.send_message(call.message.chat.id, "Ocorreu um erro interno ao buscar as ofertas.")