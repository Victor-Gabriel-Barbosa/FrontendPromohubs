from bot_instance import bot
import handlers.start
import handlers.ajuda
import handlers.contato
import handlers.produtos
import handlers.cupons
import handlers.promocoes_steam
import handlers.contato_callbacks
import handlers.produtos_callbacks
import handlers.cupons_callbacks
import handlers.nota_fiscal 
import handlers.ofertas_kabum
import handlers.ofertas_kabum_callbacks
import handlers.promocoes_steam_callbacks

if __name__ == "__main__":
  print("Bot iniciado...")
  bot.infinity_polling(timeout=10, long_polling_timeout=5)