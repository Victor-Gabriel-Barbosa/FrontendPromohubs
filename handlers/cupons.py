from bot_instance import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.message_handler(commands=['cupons'])
def menu_cupons(mensagem):
  markup = InlineKeyboardMarkup()
  markup.row_width = 2
  markup.add(
    InlineKeyboardButton("🟠 Shopee", callback_data="cupom_shopee"),
    InlineKeyboardButton("🔵 Amazon", callback_data="cupom_amazon"),
    InlineKeyboardButton("🟡 Mercado Livre", callback_data="cupom_mercado"),
    InlineKeyboardButton("🔴 AliExpress", callback_data="cupom_aliexpress"),
    InlineKeyboardButton("🎟 Ver Todos", callback_data="cupom_todos")
  )
  
  bot.send_message(
    mensagem.chat.id, 
    "Escolha uma loja para ver os cupons:", 
    reply_markup=markup
  )