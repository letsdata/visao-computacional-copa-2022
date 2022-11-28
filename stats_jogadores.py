# Importando OpenCV e easyOCR
import cv2
from easyocr import Reader
import pandas as pd

# Capturando vídeo em streaming! Teste 0,1,2 até achar a câmera certa
vid = cv2.VideoCapture(1)

# Atualizando os textos a serem mostrados na tela!
texto = ""
primeiro_nome = ""
ultimo_nome = ""
clube = ""
altura = ""
peso = ""
valor = ""

# Leitor OCR do easyOCR
reader = Reader(['en'])

# Lendo o arquivo com as estatísticas dos jogadores
# Disponível no Kaggle: https://www.kaggle.com/code/raphaelmarconato/fifa-23-players-and-teams-eda/data
df_fifa = pd.read_csv('./data/raw/FIFA23_official_data.csv')


# Função para buscar as estatísticas do jogador a partir do 1o e último nome
# no arquivo de estatísticas em formato CSV
def busca_stats_jogador(primeiro_nome, ultimo_nome):
    nome_busca = f'{primeiro_nome[0]}. {ultimo_nome}'
    nome_busca = nome_busca.lower()

    # Busca estatísticas no dataframe
    linha_stats_jogador = df_fifa.loc[df_fifa['Name'].str.lower() == nome_busca, ['Club', 'Height', 'Weight', 'Value']]

    # Nem todos os nomes estão no formato L. Messi. Alguns estão como Neymar Junior
    if len(linha_stats_jogador) == 0:
        nome_busca = f'{primeiro_nome} {ultimo_nome}'
        nome_busca = nome_busca.lower()
        linha_stats_jogador = \
            df_fifa.loc[df_fifa['Name'].str.lower() == nome_busca, ['Club', 'Height', 'Weight', 'Value']]

    stats_jogador = linha_stats_jogador.values[0]

    return stats_jogador


# Enquanto não apertarmos a tecla 'q' continua o streaming
while (True):

    # Captura o streaming frame por frame
    ret, frame = vid.read()

    # Se apertar 'd' faz o OCR pra detectar o nome do jogador na figurinha
    if cv2.waitKey(1) & 0xFF == ord('d'):
        # Faz o OCR!!
        resultados = reader.readtext(frame)
        texto = "TESTE"

        # "Monta" o texto para apresentação!
        for resultado in resultados:
            print(resultado[1])
            if len(resultado[1].split()) == 2:
                primeiro_nome = resultado[1].split()[0]
                ultimo_nome = resultado[1].split()[1]

                texto = resultado[1]

    # Uma vez detectado o nome correto, busca as estatísticas e
    # preenche os campos de clube, altura, peso e valor
    if cv2.waitKey(1) & 0xFF == ord('s'):
        try:
            print(f'nome {primeiro_nome} {ultimo_nome}')
            stats_str = busca_stats_jogador(primeiro_nome, ultimo_nome)
            clube = f'CLUBE: {stats_str[0]}'
            altura = f'ALTURA: {stats_str[1]}'
            peso = f'PESO: {stats_str[2]}'
            valor = f'VALOR: {stats_str[3][1:]} DE EUROS'
        except Exception as e:
            print(e)

    # Se clicarmos 'a' apaga o nome e estatísticas
    if cv2.waitKey(1) & 0xFF == ord('a'):
        clube = ''
        altura = ''
        peso = ''
        valor = ''
        texto = ''

    # Se clicarmos 'q' sai do programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # "Escreve" todos os textos na imagem
    cv2.putText(frame, texto, (200, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    cv2.putText(frame, clube, (200, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    cv2.putText(frame, altura, (200, 140), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    cv2.putText(frame, peso, (200, 160), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    cv2.putText(frame, valor, (200, 180), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    cv2.imshow('frame', frame)

# Depois do loop, fechar o objeto de streaming
vid.release()

# Fechar todas as janelas
cv2.destroyAllWindows()
