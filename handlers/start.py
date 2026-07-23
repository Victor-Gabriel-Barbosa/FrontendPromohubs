from bot_instance import bot

@bot.message_handler(commands=['start'])
def welcome(mensagem):
  texto_boas_vindas = (
    f'Bem-vindo(a) ao bot do PromoHubs, {mensagem.from_user.first_name}!'
    'Comandos disponíveis:\n'
    '/start - Mensagem de boas-vindas\n'
    '/ajuda - Mostra mensagem de ajuda\n'
    '/produtos - Filtra ofertas por categoria de produto\n'
    '/cupons - Cupons de desconto por loja (Shopee, Amazon, Mercado Livre, AliExpress)\n'
    '/kabum - Ofertas da Kabum por faixa de preço\n'
    '/steam - Promoções da Steam por faixa de preço\n'
    '/contato - Fale com suporte, vendas ou tire outras dúvidas\n\n'
    '📸 Dica: envie uma foto de nota fiscal que eu tento identificar o valor total automaticamente!'
  )
  bot.send_message(mensagem.chat.id, texto_boas_vindas)