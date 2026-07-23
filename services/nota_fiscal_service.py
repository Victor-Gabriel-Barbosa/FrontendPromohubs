from database import SessionLocal
from models import NotaFiscal

def salvar_nota_fiscal(user_id: int, username: str, valor_total: str, texto: str):
  session = SessionLocal()
  try:
    nota = NotaFiscal(
      telegram_user_id=user_id,
      telegram_username=username,
      valor_total=valor_total,
      texto_extraido=texto
    )
    session.add(nota)
    session.commit()
    return nota
  finally:
    session.close()