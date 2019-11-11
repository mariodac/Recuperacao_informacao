from ModeloRI_vetorial import ModeloVetorial
if __name__ == "__main__":
    print(":"*40+"MODELO VETORIAL"+":"*40)
    ri = ModeloVetorial('De pé , à cabeceira da cama , com os olhos estúpidos , a boca entreaberta , a orelhas')
    analise_lexica = ri.analiseLexica()
    print("análise léxica: ",analise_lexica)
    stop_word = ri.retiraStopWord()
    print("stop_words: ", stop_word)