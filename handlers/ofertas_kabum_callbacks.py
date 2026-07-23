import contextlib
import requests
from bot_instance import bot
from config import API_URL

@bot.callback_query_handler(func=lambda call: call.data.startswith("kabum_"))
def processar_busca_kabum(call):
  bot.answer_callback_query(call.id, "Buscando ofertas...")

  try:
    response = requests.get(f"{API_URL}/kabum")

    if response.status_code == 200:
      ofertas = response.json()
      ofertas_filtradas = []

      for o in ofertas:
        if not o.get('publicado'):
          continue

        preco = o.get('preco')

        if call.data == "kabum_all":
          ofertas_filtradas.append(o)
          continue

        if preco is not None:
          with contextlib.suppress(TypeError, ValueError):
            preco = float(preco)
            if (call.data == "kabum_0_100" and preco <= 100.0) or \
               (call.data == "kabum_100_500" and 100.0 < preco <= 500.0) or \
               (call.data == "kabum_500_plus" and preco > 500.0):
              ofertas_filtradas.append(o)
      if ofertas_filtradas:
        cabecalho = f"🛒 *Ofertas Kabum encontradas ({len(ofertas_filtradas)}):*"
        bot.send_message(call.message.chat.id, cabecalho, parse_mode="Markdown")

        for o in ofertas_filtradas:
          texto = f"*{o.get('nome')}*\n\n"
          if o.get('desconto'):
            texto += f"📉 {o.get('desconto')}\n"
          if o.get('preco') is not None:
            texto += f"💰 Preço: R$ {o.get('preco')}\n\n"
          if o.get('link'):
            texto += f"🔗 [Ver na Kabum]({o.get('link')})\n"

          if imagem := o.get('imagem'):
            try:
              bot.send_photo(call.message.chat.id, photo=imagem, caption=texto, parse_mode="Markdown")
              continue
            except Exception as e:
              print(f"Erro ao enviar imagem da oferta {o.get('nome')}: {e}")

          bot.send_message(call.message.chat.id, texto, parse_mode="Markdown")
      else:
        bot.send_message(call.message.chat.id, "Nenhuma oferta encontrada nessa faixa de preço.", parse_mode="Markdown")
    else:
      bot.send_message(call.message.chat.id, "Erro ao consultar a API do Kabum.")

  except Exception as e:
    print(f"Erro ao buscar ofertas do Kabum: {e}")
    bot.send_message(call.message.chat.id, "Ocorreu um erro ao conectar com a API.")