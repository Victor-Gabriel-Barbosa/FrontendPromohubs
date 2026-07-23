import os
import tempfile
from bot_instance import bot
from services.ocr_service import processar_nota_fiscal
from services.nota_fiscal_service import salvar_nota_fiscal

@bot.message_handler(content_types=['photo'])
def receber_nota_fiscal(mensagem):
    bot.send_message(mensagem.chat.id, "Recebi a imagem, processando a nota fiscal...")

    file_info = bot.get_file(mensagem.photo[-1].file_id)  # maior resolução
    arquivo = bot.download_file(file_info.file_path)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(arquivo)
        caminho_temp = tmp.name

    try:
        resultado = processar_nota_fiscal(caminho_temp)
    except Exception as e:
        bot.send_message(mensagem.chat.id, f"Não consegui processar a imagem: {e}")
        return
    finally:
        os.remove(caminho_temp)

    salvar_nota_fiscal(
        user_id=mensagem.from_user.id,
        username=mensagem.from_user.username,
        valor_total=resultado["valor_total"],
        texto=resultado["texto"]
    )

    if resultado["valor_total"]:
        bot.send_message(mensagem.chat.id, f"Valor total identificado: R$ {resultado['valor_total']}")
    else:
        bot.send_message(mensagem.chat.id, "Não consegui identificar o valor total nessa nota.")