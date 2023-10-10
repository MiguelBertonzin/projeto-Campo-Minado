import random

def criar_mapa():
    L = 5  # Número de linhas
    C = 5  # Número de colunas

    mapa = [[' ' for _ in range(C)] for _ in range(L)] # (uma lista de listas)

    bombas = 10  # Número de bombas
    while bombas > 0:
        linha = random.randint(0, L - 1) #Gera aleatoriamente um número de linha
        coluna = random.randint(0, C - 1) #Gera aleatoriamente um número de coluna

        # Verifique se a célula já contém uma bomba
        if mapa[linha][coluna] != '*':
            mapa[linha][coluna] = '*'  # Defina a célula como uma bomba
            bombas -= 1

    return mapa

def criar_mapa_jogador(L, C):
    return [['#' for _ in range(C)] for _ in range(L)]

def desenhar_mapa(mapa):
    for linha in mapa:
        print(' '.join(linha))

def contar_bombas_adjacentes(mapa, linha, coluna):
    L = len(mapa)
    C = len(mapa[0]) #determinar os limites válidos das coordenadas
    count = 0

    for i in [-1, 0, 1]: # (acima, mesma linha, abaixo).
        for j in [-1, 0, 1]: # (à esquerda, mesma coluna, à direita).
            nova_linha = linha + i
            nova_coluna = coluna + j
            # verifica se a célula adjacente está dentro dos limites e se contém uma bomba
            if 0 <= nova_linha < L and 0 <= nova_coluna < C and mapa[nova_linha][nova_coluna] == '*':
                count += 1 #conta bomba

    return str(count) if count > 0 else '-' #retorna string indicando se tem pelo menos uma bomba ou nao '-'

def revelar(mapa, mapa_jogador, linha, coluna):
    L = len(mapa)
    C = len(mapa[0]) #determinar os limites válidos das coordenadas

    if mapa[linha][coluna] == '*':
        return  # Se a célula atual for uma bomba, não faça nada

    if mapa_jogador[linha][coluna] == '#':
        if mapa[linha][coluna] == ' ':#verifica se é nulo
            mapa_jogador[linha][coluna] = contar_bombas_adjacentes(mapa, linha, coluna) #atribui o numero de bombas adjacentes
        else:
            mapa_jogador[linha][coluna] = mapa[linha][coluna]#atualiza para o jogador o mapa

    if mapa_jogador[linha][coluna] == ' ':
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                nova_linha = linha + i
                nova_coluna = coluna + j
                #verifica se as coordenadas da célula adjacente estão dentro dos limites válidos do mapa.
                if 0 <= nova_linha < L and 0 <= nova_coluna < C and mapa_jogador[nova_linha][nova_coluna] == '#':
                    revelar(mapa, mapa_jogador, nova_linha, nova_coluna)

def verifica_vitoria(mapa, mapa_jogador):
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[0])):
            if mapa[linha][coluna] != '*' and mapa_jogador[linha][coluna] == '#':#verifica se ainda nao acabou
                return False

    # Verificar se todas as células vazias (' ') foram reveladas
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[0])): #len retorna o numero de colunas da matriz
            if mapa[linha][coluna] == ' ' and mapa_jogador[linha][coluna] == '#':
                return False

    return True

def main():
    print("Bem-vindo ao Campo Minado!")
    while True:
        mapa = criar_mapa()
        L = len(mapa)
        C = len(mapa[0])
        mapa_jogador = criar_mapa_jogador(L, C)
        mapa_bombas = [[c if c == '*' else '@' for c in linha] for linha in mapa]  # Cria uma cópia do mapa com '*' e '@'

        jogo_em_andamento = True  # Variável para controlar o loop do jogo

        desenhar_mapa(mapa_bombas)
        print("  ")

        while jogo_em_andamento:
            desenhar_mapa(mapa_jogador)

            try:
                linha = int(input("Digite o número da linha: "))
                coluna = int(input("Digite o número da coluna: "))

                if linha < 0 or linha >= L or coluna < 0 or coluna >= C:
                    print("Coordenadas fora do campo. Tente novamente.")
                    continue

                if mapa_jogador[linha][coluna] != '#':
                    print("Célula já revelada ou marcada. Tente novamente.")
                    continue

                if mapa[linha][coluna] == '*':
                    print("Você perdeu!")
                    jogo_em_andamento = False

                elif mapa[linha][coluna] == ' ':
                    revelar(mapa, mapa_jogador, linha, coluna)

                if verifica_vitoria(mapa, mapa_jogador):
                    print("Você venceu!")
                    jogo_em_andamento = False

            except ValueError:
                print("Entrada inválida. Digite números inteiros para as coordenadas.")

        # O jogo terminou, mostrando o mapa completo com '*' e '@'
        desenhar_mapa(mapa_bombas)

        opcao = input("Deseja jogar novamente? (S para sim, qualquer tecla para sair): ")
        if opcao.lower() != 's': # pega caixa alta
            print("Obrigado por jogar!")
            break

if __name__ == "__main__":
    main()