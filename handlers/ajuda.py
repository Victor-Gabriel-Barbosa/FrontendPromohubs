from bot_instance import bot

@bot.message_handler(commands=['ajuda'])
def help(mensagem):
  texto_ajuda = (
    f'Este é o bot do PromoHubs. Como posso ajudar {mensagem.from_user.first_name}?\n\n'
    'Comandos disponíveis:\n'
    '/start - Mensagem de boas-vindas\n'
    '/ajuda - Mostra esta mensagem de ajuda\n'
    '/produtos - Filtra ofertas por categoria de produto\n'
    '/cupons - Cupons de desconto por loja (Shopee, Amazon, Mercado Livre, AliExpress)\n'
    '/kabum - Ofertas da Kabum por faixa de preço\n'
    '/steam - Promoções da Steam por faixa de preço\n'
    '/contato - Fale com suporte, vendas ou tire outras dúvidas\n\n'
    '📸 Dica: envie uma foto de nota fiscal que eu tento identificar o valor total automaticamente!'
  )
  bot.send_message(mensagem.chat.id, texto_ajuda)