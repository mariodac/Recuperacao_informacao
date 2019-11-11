from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
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
lista_sufixos = []
print("análise léxica: ", palavras)

sem_stopwords = []
for palavra in palavras:
    if palavra not in stop_words:
        sem_stopwords.append(palavra)

print('remoção stopword: ', sem_stopwords)
""" 
radicalizacao = []

rslp = RSLPStemmer()
rules = []
teste = rslp.read_rule('step2.pt')
for i in range(0, 7):
    rules.append(rslp.read_rule('step{}.pt'.format(i)))
# print(rules)
lista = []
excessao = []
for rule in rules:
    for r in rule:
        lista.append(normalize('NFKD', r[0]).encode('ASCII', 'ignore').decode('ASCII'))
        if r[2]:
            lista.append(normalize('NFKD', r[2]).encode('ASCII', 'ignore').decode('ASCII'))
        if r[3][0] != '':
            excessao.append(r[3])
    # lista.append(excessao)
    lista_sufixos.append(lista)
    lista = []

for i in range(0,len(sem_stopwords)):
    for sufixo in lista_sufixos:
        resultado = re.search('{}$'.format(sufixo), sem_stopwords[i])
        if resultado: 
            sem_stopwords[i] = (re.sub('{}$'.format(sufixo), '', sem_stopwords[i]))

print("radicalização: ", sem_stopwords)

 """