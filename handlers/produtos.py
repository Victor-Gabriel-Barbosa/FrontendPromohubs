from bot_instance import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.message_handler(commands=['produtos'])
def menu_produtos(mensagem):
  markup = InlineKeyboardMarkup()
  markup.row_width = 2
  markup.add(
    InlineKeyboardButton("📱 Smartphone", callback_data="produto_smartphone"),
    InlineKeyboardButton("💻 Notebook", callback_data="produto_notebook"),
    InlineKeyboardButton("⌨️ Teclado", callback_data="produto_teclado"),
    InlineKeyboardButton("🖱️ Mouse", callback_data="produto_mouse"),
    InlineKeyboardButton("🎮 Controle", callback_data="produto_controle"),
    InlineKeyboardButton("🎧 Fone de Ouvido", callback_data="produto_fone"),
    InlineKeyboardButton("🎙️ Microfone", callback_data="produto_microfone"),
    InlineKeyboardButton("🖥️ Monitor", callback_data="produto_monitor"),
    InlineKeyboardButton("🕹️ Console", callback_data="produto_console"),
    InlineKeyboardButton("💺 Cadeira", callback_data="produto_cadeira"),
    InlineKeyboardButton("📟 Memória RAM", callback_data="produto_ram"),
    InlineKeyboardButton("💾 SSD", callback_data="produto_ssd"),
    InlineKeyboardButton("💽 HD", callback_data="produto_hd"),
    InlineKeyboardButton("🛒 Ver Todos", callback_data="produto_todos")
  )
  
  bot.send_message(
    mensagem.chat.id, 
    "Escolha uma categoria de produtos para filtrar:", 
    reply_markup=markup
  )