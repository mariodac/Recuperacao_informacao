from ModeloRI_vetorial import ModeloVetorial
if __name__ == "__main__":
    print(":"*40+"MODELO VETORIAL"+":"*40)
    ri = ModeloVetorial('Clarissa risca com giz no quadro-negro a paisagem que os alunos devem copiar . Uma casinha de porta e janela , em cima duma coxilha .')
    analise_lexica = ri.analiseLexica()
    print("análise léxica: ",analise_lexica)
    stop_word = ri.retiraStopWord()
    print("stop_words: ", stop_word)
    ri.carregarCorpus()
    radicalizados = ri.radicalizacao()
    print("radicalização: ",radicalizados)