from bot_instance import bot
from telebot import types

@bot.message_handler(commands=['contato'])
def contato(mensagem):
  markup = types.InlineKeyboardMarkup()
  markup.add(
    types.InlineKeyboardButton("Suporte", callback_data="contato_suporte"),
    types.InlineKeyboardButton("Vendas", callback_data="contato_vendas")
  )
  markup.add(
    types.InlineKeyboardButton("Outros", callback_data="contato_outros")
  )
  bot.send_message(mensagem.chat.id, "Escolha o tipo de contato:", reply_markup=markup)