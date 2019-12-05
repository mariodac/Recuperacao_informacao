from ModeloRI_vetorial import ModeloVetorial
if __name__ == "__main__":
    print(':'*50, 'MODELO VETORIAL', ':'*50)
    ri = ModeloVetorial()
    ri.carregarCorpus()
    busca = input('Digite o(s) termo(s) de busca\n>> ')
    lista_busca = ri.operacoes_texto(busca)
    bf = ri.buscaFacetada()
    # print(nova_busca)
    # ri.carregarRepresentacao()
    resultado = ri.similaridade(lista_busca, bf)
    # print(resultado)
    print('Foram encontrados: {} documentos.'.format(len(resultado)))
    # ordenando os documentos
    print("Documentos por ordem decrescente de relevância:")
    docs_ordenados = sorted(resultado, key = resultado.get, reverse = True)
    for item in range(0, len(docs_ordenados)):
        if item == 0:
            print(docs_ordenados[item], end="")
        else:
            print(", " + docs_ordenados[item], end="")
    print()