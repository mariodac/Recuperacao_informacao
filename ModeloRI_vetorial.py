from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from unicodedata import normalize
import re

class ModeloVetorial:
    def __init__(self, texto_original):
        self.texto_original = texto_original
        self.texto_stop_words = []
        self.texto_analise_lexica = []
        self.texto_radicalizado = []

    def carregarCorpus(self):
        pass
    def analiseLexica(self):
        textoAL = self.texto_original.lower() #letras minusculas
        textoAL = normalize('NFKD', textoAL).encode('ASCII', 'ignore').decode('ASCII')#retirada de acentuações
        textoAL = re.sub('[^a-zA-Z0-9 ]', '', textoAL) #retirada de caracteres especiais
        self.texto_analise_lexica = textoAL.split()
        return self.texto_analise_lexica

    def retiraStopWord(self):
        stop_words = stopwords.words('portuguese')
        for palavra in self.texto_analise_lexica:
            if palavra not in stop_words:
                self.texto_stop_words.append(palavra)
        return self.texto_stop_words

