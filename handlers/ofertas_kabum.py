from bot_instance import bot
from telebot import types

@bot.message_handler(commands=['kabum'])
def exibir_menu_kabum(mensagem):
  markup = types.InlineKeyboardMarkup(row_width=2)
  markup.add(
    types.InlineKeyboardButton("Até R$ 100", callback_data="kabum_0_100"),
    types.InlineKeyboardButton("R$ 100 a R$ 500", callback_data="kabum_100_500"),
    types.InlineKeyboardButton("Acima de R$ 500", callback_data="kabum_500_plus"),
    types.InlineKeyboardButton("🛒 Todas", callback_data="kabum_all"),
  )

  bot.send_message(
    mensagem.chat.id,
    "Selecione a faixa de preço das ofertas do Kabum:",
    reply_markup=markup
  )