from ModeloRI_vetorial import ModeloVetorial
if __name__ == "__main__":
    arquivo = open('./corpus/1.txt', 'r')
    texto = ''
    linhas = arquivo.readlines()
    for linha in linhas:
        texto += linha

    print(":"*40+"MODELO VETORIAL"+":"*40)
    ri = ModeloVetorial('De pé , à cabeceira da cama , com os olhos estúpidos , a boca entreaberta , a orelhas gigante')
    analise_lexica = ri.analiseLexica()
    print("análise léxica: ",analise_lexica)
    stop_word = ri.retiraStopWord()
    print('='*80)
    print("stop_words: ", stop_word)
    ri.carregarCorpus()
    radicalizados = ri.radicalizacao()
    print('='*80)
    print("radicalização: ",radicalizados)
    print(len(radicalizados))