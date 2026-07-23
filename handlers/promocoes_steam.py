from telebot import types
from bot_instance import bot

@bot.message_handler(commands=['steam'])
def exibir_menu_promocoes(message):
  markup = types.InlineKeyboardMarkup(row_width=2)
  
  btn_ate_20 = types.InlineKeyboardButton("Até R$ 20", callback_data="promo_0_20")
  btn_20_a_50 = types.InlineKeyboardButton("R$ 20 a R$ 50", callback_data="promo_20_50")
  btn_acima_50 = types.InlineKeyboardButton("Acima de R$ 50", callback_data="promo_50_plus")
  btn_todas = types.InlineKeyboardButton("🛒 Todas", callback_data="promo_all")
  
  markup.add(btn_ate_20, btn_20_a_50, btn_acima_50, btn_todas)
  
  bot.send_message(
    message.chat.id, 
    "Selecione a faixa de preço desejada para as promoções da Steam:", 
    reply_markup=markup
  )