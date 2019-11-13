from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from unicodedata import normalize
import re

texto_original = "De pé , à cabeceira da cama , com os olhos estúpidos , a boca entreaberta , a orelhas gigante"

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
 
radicalizacao = []

rslp = RSLPStemmer()
rules = []
for i in range(0, 7):
    rules.append(rslp.read_rule('step{}.pt'.format(i)))
# print(rules)
lista = []
excessoes = []
sufixos = open("sufixos.txt", "w")
arquivo = open("excessoes.txt", "w")
lista_sufixo = []
for rule in rules:
    for r in rule:
        sufixo = normalize('NFKD', r[0]).encode('ASCII', 'ignore').decode('ASCII')
        lista.append(sufixo)
        lista_sufixo.append(sufixo)
        sufixos.writelines(sufixo + '\n')
        if r[2]:
            sufixo = normalize('NFKD', r[2]).encode('ASCII', 'ignore').decode('ASCII')
            lista.append(sufixo)
            lista_sufixo.append(sufixo)
            sufixos.writelines(sufixo + '\n')
        if r[3][0] != '':
            excessoes.extend(r[3])
    # lista.append(excessao)
    lista_sufixos.append(lista)
    lista = []
excessoes = list(filter(None, excessoes))
for e in range(0, len(excessoes)):
    excessoes[e] = normalize('NFKD', excessoes[e]).encode('ASCII', 'ignore').decode('ASCII')
    arquivo.writelines(excessoes[e]+'\n')
arquivo.close()
sufixos.close()
for i in range(0,len(sem_stopwords)):
    if sem_stopwords[i][-1] == 's':
        sufixos = rules[0]  
    if sem_stopwords[i][-1] == 'a':
        sufixos = rules[1]
    for rule in sufixos:
            
        print()
for i in range(0,len(sem_stopwords)):
    for sufixo in lista_sufixo:
        resultado = re.search('{}$'.format(sufixo), sem_stopwords[i])
        if resultado: 
            if sem_stopwords[i] not in excessoes:
                if len(sem_stopwords[i]) > len(sufixo):
                    op_sw = (re.sub('{}$'.format(sufixo), '', sem_stopwords[i]))
                    if len(op_sw) >= 2:
                        sem_stopwords[i] = op_sw

print("radicalização: ", sem_stopwords)

