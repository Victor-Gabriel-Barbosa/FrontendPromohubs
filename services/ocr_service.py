import cv2
import pytesseract
from pytesseract import Output
import re
from rapidfuzz import process, fuzz, utils
import platform

if platform.system() == "Windows":
  pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def _corrigir_rotacao(imagem):
  try:
    osd = pytesseract.image_to_osd(imagem, output_type=Output.DICT)
    angulo = osd['rotate']
  except Exception:
    angulo = 0

  if angulo == 90:
    return cv2.rotate(imagem, cv2.ROTATE_90_CLOCKWISE)
  if angulo == 180:
    return cv2.rotate(imagem, cv2.ROTATE_180)
  if angulo == 270:
    return cv2.rotate(imagem, cv2.ROTATE_90_COUNTERCLOCKWISE)
  return imagem

def _melhorar_imagem(imagem):
  imagem = cv2.resize(imagem, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
  imagem = cv2.convertScaleAbs(imagem, alpha=1.5, beta=70)
  cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(cinza, (3, 3), 0)
  _, binaria = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
  return binaria

def _encontrar_total(texto_extraido: str):
  opcoes_ancora = ["VALOR TOTAL À PAGAR", "VALOR À PAGAR", "TOTAL"]
  anti_ancoras = ["SUBTOTAL", "DESCONTO", "ITENS", "TRIBUTOS", "FRETE"]
  linhas = texto_extraido.split("\n")
  linha_de_baixo = ""

  for linha in reversed(linhas):
    linha_limpa = linha.upper().strip()

    resultado_anti = process.extractOne(linha_limpa, anti_ancoras, scorer=fuzz.WRatio, processor=utils.default_process)
    if resultado_anti and resultado_anti[1] >= 75:
      linha_de_baixo = linha_limpa
      continue

    resultado = process.extractOne(linha_limpa, opcoes_ancora, scorer=fuzz.WRatio, processor=utils.default_process)
    if resultado and resultado[1] >= 75:
      if numero := re.findall(r'\d+[.,\d]*', linha_limpa) or re.findall(
          r'\d+[.,\d]*', linha_de_baixo):
        return numero[-1]
  return None

def processar_nota_fiscal(caminho_imagem: str) -> dict:
  """Recebe o caminho de uma imagem e retorna texto extraído + valor total."""
  imagem = cv2.imread(caminho_imagem)
  if imagem is None:
    raise ValueError("Não foi possível carregar a imagem.")

  imagem_corrigida = _corrigir_rotacao(imagem)
  texto_extraido = pytesseract.image_to_string(
    imagem_corrigida, lang='por',
    config='--oem 3 --psm 4 -c preserve_interword_spaces=1'
  )
  valor_total = _encontrar_total(texto_extraido)

  return {"texto": texto_extraido, "valor_total": valor_total}