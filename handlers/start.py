from bot_instance import bot

@bot.message_handler(commands=['start'])
def welcome(mensagem):
  texto_boas_vindas = f'Bem-vindo(a) ao bot do PromoHubs, {mensagem.from_user.first_name}!'
  bot.send_message(mensagem.chat.id, texto_boas_vindas)