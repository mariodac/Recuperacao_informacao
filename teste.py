from nltk.corpus import stopwords
from unicodedata import normalize
import re

texto_original = "De pé , à cabeceira da cama , com os olhos estúpidos , a boca entreaberta , a orelhas"

stop_words = (stopwords.words('portuguese')) #lista de stopwords
print(texto_original)
#analise léxica e remoção de stopwords
texto_original = texto_original.lower() #deixando o texto em minusculo
texto_original = normalize('NFKD', texto_original).encode('ASCII', 'ignore').decode('ASCII')
texto_original = re.sub('[^a-zA-Z0-9 \\\]', '', texto_original)
palavras = texto_original.split() #criando vetor de palavras do texto
lista_sufixos = ['']
print("análise léxica: ", palavras)
novo_palavra = []
for palavra in palavras:
    if palavra not in stop_words:
        novo_palavra.append(palavra)

print('remoção stopword: ', novo_palavra)


