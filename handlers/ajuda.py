from bot_instance import bot

@bot.message_handler(commands=['ajuda'])
def help(mensagem):
  texto_ajuda = f'Este é o bot do PromoHubs. Como posso ajudar {mensagem.from_user.first_name}?'
  bot.send_message(mensagem.chat.id, texto_ajuda)