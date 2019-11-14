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
        self.representacao = {}

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
            self.representacao.update({file: None})
            for t in texto:
                resultado = re.search('^(Palavra(s)?|palavra(s)?|PALAVRA(s)?|Unitermos|UNITERMOS)', t)
                if resultado:
                    c += 1
                    files.append(file)
            arquivo.close()
        files = list(set(files))
        files_sorted = sorted(files)
        arquivo = open('representacao.txt', 'w')
        chaves = list(self.representacao.keys())
        valores = list(self.representacao.values())
        for i in range(0,len(self.representacao)-1):
            arquivo.writelines('{}\t:\t{}\n'.format(chaves[i], valores[i]))
        arquivo.close()
        print(len(files_sorted))
    def analiseLexica(self):
        textoAL = self.texto_original.lower() #texto para letras minusculas
        textoAL = normalize('NFKD', textoAL).encode('ASCII', 'ignore').decode('ASCII')#retirada de acentuações
        textoAL = re.sub('[^a-zA-Z ]', '', textoAL) #retirada de caracteres especiais
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
        removido = False #verificador para sufixo removido
        for p in self.texto_stop_words:
            if p[-1] == 's': #verifica se palavra termina em s
                p = self.reducao_plural(p)
            if p[-1] == 'a': #verifica se palavra termina em a
                p = self.reducao_feminino(p)
            #realiza redução do aumentativo
            p = self.reducao_aumentativo(p)
            #realiza redução adverbial
            p = self.reducao_adverbio(p)
            #realiza redução nominal
            p, removido = self.reducao_nominal(p)
            if removido: #caso removido a radicalização foi completa
                self.texto_radicalizado.append(p)
            else: #se não realizar redução verbal
                p, removido = self.reducao_verbo(p)
                if not removido: #se não foi removido realiza redução de vogais 
                    p = self.remove_vogal(p)
                    self.texto_radicalizado.append(p)
            if p not in self.texto_radicalizado: #verificação para não adicionar palavras repetidas
                self.texto_radicalizado.append(p)
        return self.texto_radicalizado
    def reducao_plural(self, palavra):
        regras = self.__regras[0] #carregando regras para sufixo do plural
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
        regras = self.__regras[1] #carregando regras para sufixo do feminino
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
        regras = self.__regras[3] #carregando regras para sufixo do aumentativo
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
        regras = self.__regras[2] #carregando regras para sufixo adverbial
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
        removido = False #verificador para sufixo removido
        regras = self.__regras[4] #carregando regras para sufixo nominal
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
        removido = False #verificador para sufixo removido
        regras = self.__regras[5] #carregando regras para sufixo verbial
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
        regras = self.__regras[6] #carregando regras para sufixo vogais
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
    