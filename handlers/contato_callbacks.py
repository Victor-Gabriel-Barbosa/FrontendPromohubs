from bot_instance import bot

@bot.callback_query_handler(func=lambda call: call.data.startswith("contato_"))
def responder_contato(call):
  if call.data == "contato_suporte":
    bot.send_message(call.message.chat.id, "Entre em contato com suporte: victorgabrielbarbosa88@yahoo.com")
  elif call.data == "contato_vendas":
    bot.send_message(call.message.chat.id, "Fale com vendas: victorgabrielbarbosa88@yahoo.com")
  elif call.data == "contato_outros":
    bot.send_message(call.message.chat.id, "Descreva sua dúvida que iremos ajudar.")