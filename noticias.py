#!/usr/bin/env python3
import time
import urllib.request
import xml.etree.ElementTree as ET
import textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from library.lcd.lcd_comm_rev_a import LcdCommRevA, Orientation

PORTA = "/dev/ttyACM0"
LARGURA = 480
ALTURA = 320
RSS = "https://g1.globo.com/rss/g1/mundo/"

# Paleta: preto puro com detalhes coloridos
PRETO = (0, 0, 0)
CARTAO = (12, 12, 16)
BORDA = (45, 45, 55)
BRANCO = (255, 255, 255)
CINZA = (170, 175, 190)
VERMELHO = (235, 0, 25)
VERMELHO_ESCURO = (105, 0, 18)
CIANO = (45, 205, 255)
VERDE = (65, 230, 145)
ROXO = (180, 100, 255)
LARANJA = (255, 165, 55)

def fonte(tamanho, negrito=False):
    caminhos = [
        "res/fonts/roboto/Roboto-Bold.ttf" if negrito else "res/fonts/roboto/Roboto-Regular.ttf",
        "res/fonts/roboto-mono/RobotoMono-Regular.ttf",
        "res/fonts/SourceHanSansCN/SourceHanSansCN-Bold.otf" if negrito else "res/fonts/SourceHanSansCN/SourceHanSansCN-Regular.otf",
    ]
    for caminho in caminhos:
        try:
            return ImageFont.truetype(caminho, tamanho)
        except OSError:
            continue
    return ImageFont.load_default()

def buscar_noticias():
    req = urllib.request.Request(
        RSS,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resposta:
        xml = ET.fromstring(resposta.read())

    noticias = []
    for item in xml.findall(".//item"):
        titulo = item.findtext("title", default="").strip()
        if titulo:
            noticias.append(titulo)
        if len(noticias) >= 5:
            break

    if not noticias:
        raise ValueError("O feed do G1 não retornou manchetes")
    return noticias

def quebrar_texto(texto, largura, f, max_linhas=2):
    palavras = texto.split()
    linhas = []
    atual = ""

    for palavra in palavras:
        teste = f"{atual} {palavra}".strip()
        if ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(teste, font=f) <= largura:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
            if len(linhas) >= max_linhas:
                break

    if atual and len(linhas) < max_linhas:
        linhas.append(atual)

    usadas = " ".join(linhas).split()
    if len(usadas) < len(palavras) and linhas:
        linhas[-1] = linhas[-1].rstrip(" .") + "..."
    return linhas

def desenhar(tela, noticias, estado):
    imagem = Image.new("RGB", (LARGURA, ALTURA), PRETO)
    d = ImageDraw.Draw(imagem)

    # Cabeçalho vermelho
    d.rounded_rectangle((8, 7, 472, 53), radius=9, fill=VERMELHO)
    d.text((19, 10), "g1", font=fonte(30, True), fill=BRANCO)
    d.line((67, 15, 67, 45), fill=(255, 170, 170), width=2)
    d.text((80, 15), "MUNDO", font=fonte(22, True), fill=BRANCO)
    d.text((365, 13), datetime.now().strftime("%H:%M"),
           font=fonte(23, True), fill=BRANCO)
    d.text((368, 37), datetime.now().strftime("%d/%m"),
           font=fonte(10), fill=BRANCO)

    # Manchete principal
    principal = noticias[0] if noticias else "Buscando notícias do G1..."
    d.rounded_rectangle((8, 61, 472, 151), radius=8,
                        fill=CARTAO, outline=VERMELHO, width=2)
    d.rounded_rectangle((17, 69, 104, 87), radius=5, fill=VERMELHO_ESCURO)
    d.text((25, 70), "DESTAQUE", font=fonte(11, True), fill=BRANCO)

    linhas = quebrar_texto(principal, 432, fonte(17, True), 3)
    y = 94
    for linha in linhas:
        d.text((18, y), linha, font=fonte(17, True), fill=BRANCO)
        y += 19

    # Outras manchetes em cartões compactos
    cores = [CIANO, ROXO, VERDE, LARANJA]
    nomes = ["EUROPA", "ÁSIA", "AMÉRICAS", "MUNDO"]
    inicio_y = 158
    altura_cartao = 32
    espacamento = 4

    for i, titulo in enumerate(noticias[1:5]):
        y = inicio_y + i * (altura_cartao + espacamento)
        cor = cores[i]
        d.rounded_rectangle(
            (8, y, 472, y + altura_cartao),
            radius=6, fill=CARTAO, outline=BORDA, width=1
        )
        d.rounded_rectangle((14, y + 6, 79, y + 25),
                            radius=5, fill=cor)
        d.text((19, y + 9), nomes[i], font=fonte(9, True), fill=PRETO)

        linhas = quebrar_texto(titulo, 370, fonte(12), 2)
        texto = linhas[0] if linhas else titulo
        if len(linhas) > 1:
            texto += " " + linhas[1]
        d.text((87, y + 8), texto, font=fonte(11), fill=BRANCO)

    # Rodapé preto com linha vermelha e estado
    d.rectangle((8, 306, 472, 309), fill=VERMELHO)
    cor_estado = VERDE if estado == "ATUALIZADO" else LARANJA
    d.text((12, 311), estado, font=fonte(10, True), fill=cor_estado)
    d.text((230, 311), "G1 MUNDO", font=fonte(10, True), fill=CINZA)
    d.text((350, 311), "ATUALIZA: 1 MIN", font=fonte(10), fill=CIANO)

    tela.DisplayPILImage(imagem)

def main():
    tela = LcdCommRevA(
        com_port=PORTA,
        display_width=320,
        display_height=480
    )
    try:
        tela.Reset()
        tela.InitializeComm()
        tela.SetBrightness(level=100)
        tela.SetOrientation(Orientation.LANDSCAPE)

        noticias = ["Conectando ao G1 Mundo..."]
        while True:
            try:
                noticias = buscar_noticias()
                estado = "ATUALIZADO"
            except Exception as erro:
                print(f"Falha ao buscar notícias: {erro}")
                estado = "SEM ATUALIZAÇÃO"

            desenhar(tela, noticias, estado)
            print(f"[{datetime.now():%H:%M:%S}] G1 Mundo: tela atualizada.")
            time.sleep(60)
    finally:
        tela.ScreenOn()

if __name__ == "__main__":
    main()
