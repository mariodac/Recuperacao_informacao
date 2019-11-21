from ModeloRI_vetorial import ModeloVetorial
if __name__ == "__main__":
    print(':'*50, 'MODELO VETORIAL', ':'*50)
    ri = ModeloVetorial()
    ri.carregarCorpus()
    busca = 'Inteligência Artificial'#input('Digite o(s) termo(s) de busca\n>> ')
    nova_busca = ri.operacoes_texto(busca)
    print(nova_busca)
    # ri.carregarRepresentacao()
    resultado = ri.similaridade(nova_busca)
    print('Foram encontrados: {} documentos.'.format(len(resultado)))
    for item in sorted(resultado, key = resultado.get, reverse = True):
        print (item)