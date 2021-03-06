from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from unicodedata import normalize
from os import listdir, path
from nltk.stem import RSLPStemmer
import re
import time
from math import log10, sqrt, pow
import csv
import pandas as pd

class ModeloVetorial:
    __rlsp = RSLPStemmer()
    __regras = []
    def __init__(self):
        self.texto_original = []
        self.texto_stop_words = []
        self.texto_analise_lexica = []
        self.texto_radicalizado = []
        self.dic_documentos = {}
        self.representacao = {}

    def regras(self):
        for i in range(0, 7):
            regras = self.__rlsp.read_rule('step{}.pt'.format(i)) #lendo regras de sufixos
            for j in range (0, len(regras)):
                #retirando acentuação dos sufixos
                regras[j][0] = normalize('NFKD', regras[j][0]).encode('ASCII', 'ignore').decode('ASCII') 
                regras[j][2] = normalize('NFKD', regras[j][2]).encode('ASCII', 'ignore').decode('ASCII')
                for k in range (0, len(regras[j][3])):
                    #retirando acentuação das excessões
                    regras[j][3][k] = normalize('NFKD', regras[j][3][k]).encode('ASCII', 'ignore').decode('ASCII')
            self.__regras.append(regras)
            if not path.isfile('./regras.txt'): #verifica se arquivo existe
                arquivo = open('regras.txt', 'w')
                arquivo.writelines(str(self.__regras))
                arquivo.close()
    def salvarDocs(self, documentos):
        if not path.isfile('./documentos.txt'):
            arquivo = open('documentos.txt','w')
            for d in documentos:
                arquivo.writelines('{} : {}\n'.format(d, documentos[d][0]))
            arquivo.close()
    def salvarRepresentacao(self, dic):
        if not path.isfile('./representacao.csv'):
            #criando arquivo csv
            arquivo = csv.writer(open('representacao.csv', 'w'))
            arquivo.writerow(['DOCS','TF-IDF', 'TERMOS'])
            tf_idf = ''
            for d in dic:
                #convertendo lista de string em uma unica string
                termos = ','.join(dic[d][0])
                for p in dic[d][1]:
                    #salvando palavra e seu idf
                    tf_idf += p + ':' + str(dic[d][1][p][3]) + ',' 
                    #escrevendo um linha no arquivo csv
                arquivo.writerow([d, tf_idf, termos])
                tf_idf = ''
                termos = ''
    def carregarRepresentacao(self):
        dados = pd.read_csv('representacao.csv') #lendo arquivo invertido
        df = dados.T #transpondo a tabela
        representacao = {}
        dic_tf_idf = {}
        for c in df.columns:
            doc = df[c].values
            palavras = doc[1].split(',')
            for palavra in palavras:
                if palavra:
                    tf_idf = float(palavra.split(':')[1])
                    dic_tf_idf.update({palavra.split(':')[0] : tf_idf})
            representacao.update({doc[0] : [dic_tf_idf, doc[2]]})
            dic_tf_idf = {}
        return representacao
    def carregarCorpus(self):
        if not path.isfile('./documentos.txt'):
            dir = './corpus'
            diretorio = listdir(dir)
            texto_completo = ''
            t_o = time.time () 
            for arquivo in diretorio:
                t_o2 = time.time ()
                arq = open('{}/{}'.format(dir, arquivo), 'r')
                linhas = arq.readlines()
                #tranforma lista de string em uma única string
                texto_completo = ' '.join(map(str, linhas)) 
                #aplicando todas as operações no texto
                texto_final = self.operacoes_texto(texto_completo)
                texto_completo = ''
                millis = int((time.time () - t_o2) * 1000)
                hours = int(millis / 3.6e+6)
                x = millis % 3.6e+6
                minutes = int(x / 60000)
                y = x % 60000
                seconds = int(y / 1000)
                k = y % 1000
                milliseconds = int(k)
                print('CONCLUÍDO ' + str(arquivo)+' executado em ' + str(hours) + ' hora(s) ' + str(minutes) + ' minuto(s) ' + str(seconds) + ' segundos(s) e ' + str(milliseconds) + ' milisegundo(s).')
                #criando dicionario com os termos 
                self.dic_documentos.update({arquivo : [texto_final]})
                arq.close()
            #salvando dicionario de termos
            self.salvarDocs(self.dic_documentos)
            #armazenando representação dos documentos
            self.representacao = self.tf(self.dic_documentos)
            self.salvarRepresentacao(self.representacao)
            self.salvarRepresentacaoCompleta(self.representacao)
            millis = int((time.time () - t_o) * 1000)
            hours = int(millis / 3.6e+6)
            x = millis % 3.6e+6
            minutes = int(x / 60000)
            y = x % 60000
            seconds = int(y / 1000)
            k = y % 1000
            milliseconds = int(k)
            print('CONCLUÍDO ' + str(len(diretorio))+' arquivos executados em ' + str(hours) + ' hora(s) ' + str(minutes) + ' minuto(s) ' + str(seconds) + ' segundos(s) e ' + str(milliseconds) + ' milisegundo(s).')
    def tf(self, dic_documentos):
        # dic_documentos = self.dic_documentos
        freq = {}
        for d in dic_documentos:
            #eliminando termos repetidos
            termos = list(set(dic_documentos[d][0]))
            #convertendo lista de string em uma unica string
            texto_doc = ' '.join(map(str, dic_documentos[d][0]))
            for t in termos:
                resultado = re.findall(t, texto_doc)
                freq.update({t : [len(resultado)]})
            #obtendo maior frequencia
            maxfreq = freq[max(freq, key=freq.get)]
            tf = 0
            for v in freq:
                #calculo tf
                tf = freq[v][0]/maxfreq[0]
                #armazenando no dicionario
                freq[v] = [freq[v][0], tf]
            #adicionando no dicionario dos documentos
            dic_documentos[d] = [dic_documentos[d][0], freq]
            freq = {}
        return self.idf(dic_documentos, freq)
    def idf(self,docs_texto, freq):
        c = 0
        #obtendo numero total de documentos
        N = len(docs_texto)
        idf = 0
        for doc in docs_texto:
            for t in docs_texto[doc][0]:
                for d in docs_texto:
                    #verificando se a palavra existe dentro do documento atual
                    if t in docs_texto[d][0]: 
                        c += 1
                ni = c
                c = 0
                #realizando o calculo do idf
                idf = log10(N/ni)
                #armazenando no dicionario de documentos
                docs_texto[doc][1][t].append(idf)
                #calculando e armazenando o calculo do tf-idf
                docs_texto[doc][1][t].append(docs_texto[doc][1][t][1] * idf)
        #salvando no dicionario a representacao
        # self.representacao = docs_texto
        #dicionario onde cada chave (nome do documento) possui um vetor de 2 posições na posição 0 é armazenado os resultado da operação do texto sobre o documento, na posição 1 está outro dicionario onde cada chave (palavra) possui um vetor de 4 posições na posição 0 armazena a frequencia da palavra naquele documento, na posição 1 armazena o tf, na posição 2 armazena o idf, na posição 3 armazena o calculo do tf-idf
        return docs_texto
    def salvarRepresentacaoCompleta(self, dicionario):
        arquivo = open('documentosCompleto.txt', 'w')
        arquivo.writelines(str(dicionario))
    def similaridade(self, consulta, buscaFacetada):
        dic_busca = self.peso_consulta(consulta)
        # self.representacao = self.carregarRepresentacao()
        # dicionario para armazenar q*d do documento e consulta, i sendo o nome do documento
        qd = {i : [] for i in self.representacao}
        # norma da consulta
        normaQ = {i : [] for i in self.representacao}
        # norma da consulta
        normaD = {i : [] for i in self.representacao}
        similaridade = 0
        #dicionario para armazenar resultado da busca
        resultado = {}
        lista = []
        for b in dic_busca: #percorrendo termos da busca
            for i in dic_busca[b]: #percorrendo nome dos documentos
                try:
                    lista = [(dic_busca[b][i] * self.representacao[i][0][b])]
                    #unindo lista
                    qd[i] += lista
                    lista =  [pow(dic_busca[b][i], 2)]
                    normaD[i] += lista
                    lista = [pow(self.representacao[i][0][b], 2)]
                    normaQ[i] += lista
                # se esse termo não está no documento então o seu peso é zero
                except KeyError:
                    lista = [0]
                    qd[i] += lista
                    normaD[i] += lista
                    normaQ[i] += lista
        for c in normaQ.keys():
            try:
                if normaQ[c]:
                    if buscaFacetada:
                        for i in buscaFacetada:
                            resultado2 = re.search(i, self.representacao[c][1])
                            if resultado2:
                                similaridade = sum(qd[c])/(sqrt(sum(normaQ[c])) * sqrt(sum(normaD[c])))
                                resultado.update({c : similaridade})
                    else:
                        similaridade = sum(qd[c])/(sqrt(sum(normaQ[c])) * sqrt(sum(normaD[c])))
                        resultado.update({c : similaridade})
            #se ocorrer divisão por zero então documento é irrelevante
            except ZeroDivisionError:
                pass
        return resultado
    def buscaFacetada(self):
        areas = ['aprendizado de máquina', 'robotica', 'previsão de série temporais', 'aprendizado profundo', 'processamento da linguagem natural']
        buscaFacetada = []
        for i in areas:
            buscaFacetada.append(self.operacoes_texto(i))
        print("*"*40+"BUSCA FACETADA"+"*"*40)
        print("0 -  Sem filtro")
        print("1 -  Filtrar por subárea aprendizado de máquina")
        print("2 -  Filtrar por subárea robotica")
        print("3 -  Filtrar por subárea previsão de série temporais")
        print("4 -  Filtrar por subárea aprendizado profundo")
        print("5 -  Filtrar por subárea processamento da linguagem natural")
        try:
            escolha = int(input("Digite a opção\n>> "))
            if escolha == 0:
                return ""
            return (buscaFacetada[escolha-1])
        except Exception:
            return ""
        

    def peso_consulta(self, consulta):
        #carregando representação do arquivo csv
        self.representacao = self.carregarRepresentacao()
        # dicionario para armazenar frequencia
        dic_freq = {}
        #dicionario para armazenar dicionario 
        dic_busca = {}
        # numero total de documentos
        N = len(self.representacao)
        # c -> para cada documento, ni-> numero de documento que o termo da busca ocorre
        ni, c = 0, 0
        for b in consulta:
            # dic_busca.update({b: []})
            dic_busca.update({b: {}})
            for d in self.representacao:
                # if d == '50.txt':
                    #armazenando em lista os termos do documentos
                    termos = list(set(self.representacao[d][1].split(',')))
                    #unindo todas os termos em unica string
                    texto = ' '.join(map(str, termos))
                    #armazenando frequencia do termo no documento
                    for t in termos:
                        dic_freq.update({t : len(re.findall(t, texto))})
                    #obtendo maior frequencia
                    max_freq = dic_freq[max(dic_freq, key=dic_freq.get)]
                    # print(dic_freq)
                    freq = len(re.findall(b, self.representacao[d][1]))
                    # contando documentos que possuem o termo de busca
                    if b in termos:
                        c += 1
                    ni = c
                    c = 0
                    try:
                        peso = (0.5 + ((0.5 * freq)/max_freq)) * log10(N/ni)
                    #se ocorrer divisão por zero então documento é irrelevante
                    except ZeroDivisionError:
                        peso = 0
                    dic_busca[b].update({d : peso})
                    # dic_busca[b].append([peso, d])
        return dic_busca

    def operacoes_texto(self, texto):
        self.texto_original = texto.split()
        self.analiseLexica()
        self.retiraStopWord()
        texto_final = []
        for t in self.radicalizacao():
            if len(t) > 1: #pegando somente palavra maior que 1
                texto_final.append(t)
        return texto_final
    def analiseLexica(self):
        self.texto_analise_lexica = []
        for p in self.texto_original:
            textoAL = p.lower() #texto para letras minusculas
            textoAL = normalize('NFKD', textoAL).encode('ASCII', 'ignore').decode   ('ASCII')#retirada de acentuações
            textoAL = re.sub('[^a-zA-Z \\\ ]', '', textoAL) #retirada de caracteres especiais
            self.texto_analise_lexica.append(textoAL)
        while('' in self.texto_analise_lexica) : #eliminar string vazia
            self.texto_analise_lexica.remove('')
        else:
            while(' ' in self.texto_analise_lexica) : #eliminar string com somente espaço
                self.texto_analise_lexica.remove(' ')
        return self.texto_analise_lexica

    def retiraStopWord(self):
        self.texto_stop_words = []
        stop_words = stopwords.words('portuguese') #obtendo lista de stopwords da lingua portuguesa
        for palavra in self.texto_analise_lexica:
            if palavra not in stop_words:
                self.texto_stop_words.append(palavra) #lista com somente a palavra que não são stopwords
        return self.texto_stop_words
        
    
    def radicalizacao(self):
        self.texto_radicalizado = []
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
            resultado = re.search('{}$'.format(regra[0]), palavra) #busca sufixo na palavra
            if resultado:
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]:
                    if palavra not in regra[3]:
                        #retira o sufixo
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra)
                        #junta o radical com sufixo de substituição
                        palavra += regra[2]
                        break
                
        return palavra
    def reducao_feminino(self, palavra):
        regras = self.__regras[1] #carregando regras para sufixo do feminino
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra) #busca sufixo na palavra
            if resultado: #se resultado encontrado
                tamanho_sufixo = len(regra[0]) 
                if len(palavra) >= tamanho_sufixo + regra[1]: #verifica se o radical possui o tamanho minimo
                    if palavra not in regra[3]: #verifica se a palavra não está na lista de excessões
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra) #retira o sufixo
                        palavra += regra[2] #junta o radical com sufixo de substituição
                        break
        return palavra
    def reducao_aumentativo(self, palavra):
        regras = self.__regras[3] #carregando regras para sufixo do aumentativo
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra) #busca sufixo na palavra
            if resultado: #se resultado encontrado
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]: #verifica se o radical possui o tamanho minimo
                    if palavra not in regra[3]: #verifica se a palavra não está na lista de excessões
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra) #retira o sufixo
                        palavra += regra[2] #junta o radical com sufixo de substituição
                        break
        return palavra
    def reducao_adverbio(self, palavra):
        regras = self.__regras[2] #carregando regras para sufixo adverbial
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra) #busca sufixo na palavra
            if resultado: #se resultado encontrado
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]: #verifica se o radical possui o tamanho minimo
                    if palavra not in regra[3]: #verifica se a palavra não está na lista de excessões
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra) #retira o sufixo
                        palavra += regra[2] #junta o radical com sufixo de substituição
                        break
        return palavra
    def reducao_nominal(self, palavra):
        removido = False #verificador para sufixo removido
        regras = self.__regras[4] #carregando regras para sufixo nominal
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra) #busca sufixo na palavra
            if resultado: #se resultado encontrado
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]: #verifica se o radical possui o tamanho minimo
                    if palavra not in regra[3]: #verifica se a palavra não está na lista de excessões
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra) #retira o sufixo
                        palavra += regra[2] #junta o radical com sufixo de substituição
                        break
        return palavra, removido
    def reducao_verbo(self, palavra):
        removido = False #verificador para sufixo removido
        regras = self.__regras[5] #carregando regras para sufixo verbial
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra) #busca sufixo na palavra
            if resultado: #se resultado encontrado
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]: #verifica se o radical possui o tamanho minimo
                    if palavra not in regra[3]: #verifica se a palavra não está na lista de excessões
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra) #retira o sufixo
                        palavra += regra[2] #junta o radical com sufixo de substituição
                        break
        return palavra, removido
    def remove_vogal(self, palavra):
        regras = self.__regras[6] #carregando regras para sufixo vogais
        for regra in regras:
            resultado = re.search('{}$'.format(regra[0]), palavra) #busca sufixo na palavra
            if resultado: #se resultado encontrado
                tamanho_sufixo = len(regra[0])
                if len(palavra) >= tamanho_sufixo + regra[1]: #verifica se o radical possui o tamanho minimo
                    if palavra not in regra[3]: #verifica se a palavra não está na lista de excessões
                        palavra = re.sub('{}$'.format(regra[0]), '', palavra) #retira o sufixo
                        palavra += regra[2] #junta o radical com sufixo de substituição
                        break
        return palavra
    def testeCarregarCorpus(self):
        dir = './corpus'
        diretorio = listdir(dir)
        c = 0
        files = []
        texto_completo = ''
        for file in diretorio:
            arquivo = open('{}/{}'.format(dir, file), 'r')
            texto = arquivo.readlines()
            for t in texto:
                texto_completo += t + ' '
                resultado = re.search('^(Palavra(s)?|palavra(s)?|PALAVRA(s)?|Unitermos|UNITERMOS)', t) #procurando palavra chaves
                if resultado:
                    c += 1
                    files.append(file)
            self.dic_documentos.update({file: [texto_completo]})
            texto_completo = ''
            arquivo.close()
        files = list(set(files))
        files_sorted = sorted(files)
        arquivo = open('documentos.txt', 'w')
        chaves = list(self.dic_documentos.keys())
        valores = list(self.dic_documentos.values())
        for i in range(0,len(self.dic_documentos)-1):
            arquivo.writelines('{}\t:\t{}\n'.format(chaves[i], valores[i]))
        arquivo.close()
        print(len(files_sorted))
    