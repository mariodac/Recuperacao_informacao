from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from unicodedata import normalize
from os import listdir
from nltk.stem import RSLPStemmer
import re

class ModeloVetorial:
    __rlsp = RSLPStemmer()
    __regras = []
    def __init__(self, texto_original):
        self.texto_original = texto_original
        self.texto_stop_words = []
        self.texto_analise_lexica = []
        self.texto_radicalizado = []

    def regras(self):
        for i in range(0, 7):
            regras = self.__rlsp.read_rule('step{}.pt'.format(i))
            for j in range (0, len(regras)):
                regras[j][0] = normalize('NFKD', regras[j][0]).encode('ASCII', 'ignore').decode('ASCII')
                regras[j][2] = normalize('NFKD', regras[j][2]).encode('ASCII', 'ignore').decode('ASCII')
                for k in range (0, len(regras[j][3])):
                    regras[j][3][k] = normalize('NFKD', regras[j][3][k]).encode('ASCII', 'ignore').decode('ASCII')
            self.__regras.append(regras)
            arquivo = open('regras.txt', 'w')
            arquivo.writelines(str(self.__regras))
            arquivo.close()

    def carregarCorpus(self):
        dir = './corpus'
        diretorio = listdir(dir)
        c = 0
        files = []
        for file in diretorio:
            arquivo = open('{}/{}'.format(dir, file), 'r')
            texto = arquivo.readlines()
            for t in texto:
                resultado = re.search('^(Palavra(s)?|palavra(s)?|PALAVRA(s)?|Unitermos|UNITERMOS)', t)
                if resultado:
                    c += 1
                    files.append(file)
        files = list(set(files))
        files_sorted = sorted(files)
        print(len(files_sorted))
    def analiseLexica(self):
        textoAL = self.texto_original.lower() #texto para letras minusculas
        textoAL = normalize('NFKD', textoAL).encode('ASCII', 'ignore').decode('ASCII')#retirada de acentuações
        textoAL = re.sub('[^a-zA-Z0-9 ]', '', textoAL) #retirada de caracteres especiais
        self.texto_analise_lexica = textoAL.split()
        return self.texto_analise_lexica

    def retiraStopWord(self):
        stop_words = stopwords.words('portuguese') #obtendo lista de stopwords da lingua portuguesa
        for palavra in self.texto_analise_lexica:
            if palavra not in stop_words:
                self.texto_stop_words.append(palavra) #lista com somente a palavra que não são stopwords
        return self.texto_stop_words
    
    def radicalizacao(self):
        self.regras()
        removido = False
        for p in self.texto_stop_words:
            if p[-1] == 's':
                p = self.reducao_plural(p)
            if p[-1] == 'a':
                p = self.reducao_feminino(p)
            
            p = self.reducao_aumentativo(p)
            p = self.reducao_adverbio(p)
            p, removido = self.reducao_nominal(p)
            if removido:
                self.texto_radicalizado.append(p)
            else:
                p, removido = self.reducao_verbo(p)
                if not removido:
                    p = self.remove_vogal(p)
                    self.texto_radicalizado.append(p)
            if p not in self.texto_radicalizado:
                self.texto_radicalizado.append(p)
        return self.texto_radicalizado
    def reducao_plural(self, palavra):
        regras = self.__regras[0]
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra)
            if resultado:
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]:
                    if palavra not in regra[3]:
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra)
                        palavra += regra[2]
                        break
                
        return palavra
    def reducao_feminino(self, palavra):
        regras = self.__regras[1]
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra)
            if resultado:
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]:
                    if palavra not in regra[3]:
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra)
                        palavra += regra[2]
                        break
        return palavra
    def reducao_aumentativo(self, palavra):
        regras = self.__regras[3]
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra)
            if resultado:
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]:
                    if palavra not in regra[3]:
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra)
                        palavra += regra[2]
                        break
        return palavra
    def reducao_adverbio(self, palavra):
        regras = self.__regras[2]
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra)
            if resultado:
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]:
                    if palavra not in regra[3]:
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra)
                        palavra += regra[2]
                        break
        return palavra
    def reducao_nominal(self, palavra):
        removido = False
        regras = self.__regras[4]
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra)
            if resultado:
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]:
                    if palavra not in regra[3]:
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra)
                        palavra += regra[2]
                        break
        return palavra, removido
    def reducao_verbo(self, palavra):
        removido = False
        regras = self.__regras[5]
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra)
            if resultado:
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]:
                    if palavra not in regra[3]:
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra)
                        palavra += regra[2]
                        break
        return palavra, removido
    def remove_vogal(self, palavra):
        regras = self.__regras[6]
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra)
            if resultado:
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]:
                    if palavra not in regra[3]:
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra)
                        palavra += regra[2]
                        break
        return palavra
    