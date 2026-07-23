from bot_instance import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.message_handler(commands=['kabum'])
def menu_kabum(mensagem):
  markup = InlineKeyboardMarkup()
  markup.row_width = 2
  
  markup.add(
    InlineKeyboardButton("🎮 Placas de Vídeo", callback_data="kabum_video"),
    InlineKeyboardButton("⚙️ Processadores", callback_data="kabum_processador"),
    InlineKeyboardButton("💻 Notebooks", callback_data="kabum_notebook"),
    InlineKeyboardButton("🎧 Periféricos", callback_data="kabum_periferico"),
    InlineKeyboardButton("🔥 Ver Todas", callback_data="kabum_todas")
  )
  
  bot.send_message(
    mensagem.chat.id, 
    "🥷 Escolha uma categoria para ver as ofertas da KaBuM!:", 
    reply_markup=markup
  )