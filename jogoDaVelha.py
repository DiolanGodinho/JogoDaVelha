from tabulate import tabulate
from random import choice

def validaEntradaCorreta(letra, numero):
    """
    Confere se as coordenadas recebidas estão dentro das opções válidas
    Parâmetros: letra, numero
    Retorno: True(Opção válida)/False(Opção inválida)
    """
    if letra not in ["A", "B", "C"] or numero not in ["1", "2", "3"]:
        return False
    else:
        return True

def validaEntradaDisponivel(tabuleiro, letra, numero):
    """
    Confere se a coordenada recebida está disponível
    Parâmetros: tabuleiro, letra, numero
    Retorno: True(Disponivel)/False(Indisponivel)
    """
    if tabuleiro[letra][numero-1] != "":
        return False
    else:
        return True

def validaEntrada(tabuleiro, letraNumero):
    """
    Valida entrada do usuário para possíveis erros de digitação, cordenadas inválidas ou já utilizadas
    Parâmetros: tabuleiro, letraNumero (coordenadas da jogada)
    Retorno: letra e numero (coordenadas da jogada validadas)
    """
    # Valida digitações fora do esperado
    try:
        letra, numero = letraNumero.upper().split()
    except:
        return validaEntrada(tabuleiro, input(f"Coordenada inválida, digite uma válida: "))
    # Se entrada correta e disponível retorna, caso contrário chama a função novamente
    if validaEntradaCorreta(letra, numero):
        if validaEntradaDisponivel(tabuleiro, letra, int(numero)):
            return letra, int(numero)
        else:
            return validaEntrada(tabuleiro, input(f"Coordenadas indisponíveis, digite uma livre: ")) 
    else:
        return validaEntrada(tabuleiro, input(f"Coordenada inválida, digite uma válida: "))  

def jogada(tabuleiro):
    """
    Pede a jogada ao usuario e aplica ao tabuleiro
    Parâmetros: tabuleiro
    Retorno: tabuleiro
    """
    letra, numero = validaEntrada(tabuleiro, input(f"Vez do jogador: "))

    tabuleiro[letra][numero-1] = "O"

    return tabuleiro

def parabenizaGanhador(tabuleiro, jogador):
    """
    Imprime o tabuleiro e parabeniza o ganhador
    Parâmetros: tabuleiro e jogador que ganhou
    """
    imprimiTabuleiro(tabuleiro)
    # Parabenização invertida pois jogador da vez veio depois da jogada onde a vitória ocorreu
    if jogador == "X":
        print("A máquina ganhou!")
    else:
        print("O jogador ganhou! (Não deve acontecer)")

def imprimiTabuleiro(tabuleiro):
    """
    Imprime o tabuleiro utilizando o tabulate para estilização
    Parâmetros: tabuleiro
    """
    print(tabulate(tabuleiro, headers="keys", tablefmt="fancy_grid"))

def confereGanhador(tabuleiro):
    """
    Confere linhas, colunas e diagonais pelo padrão de vitória
    Parâmetros: tabuleiro
    Retorno: True(Vitória)/False(Sem vitória)
    """
    jogadores = ["X", "O"]
    for jogador in jogadores:
        if True in [True if fila.count(jogador) == 3 else False for fila in filasDo(tabuleiro)]:
            parabenizaGanhador(tabuleiro, jogador)
            return True

def confereEmpate(tabuleiro):
    """
    Confere se há espaços disponíveis no tabuleiro
    Parâmetros: tabuleiro
    Retorno: True(Empate)/False(Sem empate)
    """
    if "" not in tabuleiro["A"] and "" not in tabuleiro["B"] and "" not in tabuleiro["C"]:
        imprimiTabuleiro(tabuleiro)
        print("O jogo empatou!")
        return True
    else:
        return False

def confereFim(tabuleiro):
    """
    Confere se os possiveis finais (vitória de alguma parte) ou empate ocorreram
    Parâmtros: tabuleiro, jogador (que fez a última jogada)
    Retorno: True(Acabou o jogo)/ False(Não acabou o jogo)
    """
    acabou = False
    acabou = confereGanhador(tabuleiro)
    if not acabou:
        acabou = confereEmpate(tabuleiro)
    return acabou

def jogadaMaquina(tabuleiro):
    """
    Processa a jogada que deve ser feita pela máquina
    Parâmetros: tabuleiro, rodada (Contagem de quantas jogadas foram feitas)
    Retorno: tabuleiro
    """
    rodada = verificaRodada(tabuleiro)
    if rodada == 1:
        tabuleiro = jogadaInicial(tabuleiro)
        reflexao = decideReflexao(tabuleiro)
        guardaReflexao(reflexao)
    
    else:
        reflexao = leReflexao()
        tabuleiro = refletir(tabuleiro, reflexao)

        if rodada == 2:
            tabuleiro = jogadaSegundaRodada(tabuleiro)

        elif ehPossivelFinalizar("Ganhando", tabuleiro):
            tabuleiro = jogarPara("Ganhar", tabuleiro)

        else:
            if ehPossivelFinalizar("Perdendo", tabuleiro):
                tabuleiro = jogarPara("Nao Perder", tabuleiro)
            else:
                if rodada == 3:
                    tabuleiro = jogadaTerceiraRodada(tabuleiro)

        tabuleiro = refletir(tabuleiro, reflexao)      
    return tabuleiro

def verificaRodada(tabuleiro):
    colunas = tabuleiro.values()
    emBranco = sum([coluna.count("") for coluna in colunas])
    if emBranco == 9:
        return 1
    elif emBranco == 7:
        return 2
    elif emBranco == 5:
        return 3

def jogadaInicial(tabuleiro):
    coordenadasDasQuinas = [["A", 0], ["C", 0], ["C", 2], ["A", 2]]
    coluna, linha = choice(coordenadasDasQuinas)
    tabuleiro[coluna][linha] = "X"
    return tabuleiro

def decideReflexao(tabuleiro):
    quinas = [
        tabuleiro["A"][0],
        tabuleiro["C"][0],
        tabuleiro["C"][2],
        tabuleiro["A"][2]
        ]

    reflexaoPorQuina = {
        0: "identidade",
        1: "colunaB",
        2: "diagonalSecundaria",
        3: "linha2"
    }

    quina = quinas.index("X")
    return reflexaoPorQuina[quina]
    
def guardaReflexao(nome):
    arquivo = open("reflexao.txt", mode="w", encoding="utf-8")
    arquivo.write(nome)
    arquivo.close()

def leReflexao():
    arquivo = open("reflexao.txt", mode="r", encoding="utf-8")
    reflexao = arquivo.read()
    arquivo.close()
    return reflexao

def refletir(tabuleiro, reflexao):
    refletirPor = {
        "identidade": tabuleiro,
        "colunaB": refletirPelaColunaB(tabuleiro),
        "diagonalSecundaria": refletirPelaDiagonalSecundaria(tabuleiro),
        "linha2": refletirPelaLinha2(tabuleiro)
    }

    return refletirPor[reflexao]

def refletirPelaColunaB(tabuleiro):
    refletido = tabuleiro.copy()
    refletido["A"] = tabuleiro["C"].copy()
    refletido["C"] = tabuleiro["A"].copy()
    return refletido

def refletirPelaDiagonalSecundaria(tabuleiro):
    refletido = tabuleiro.copy()
    linhas = linhasDo(tabuleiro)
    for linha in linhas:
        linha.reverse()

    refletido["A"] = linhas[2].copy()
    refletido["B"] = linhas[1].copy()
    refletido["C"] = linhas[0].copy()
    return refletido

def refletirPelaLinha2(tabuleiro):
    refletido = tabuleiro.copy()
    colunas = colunasDo(tabuleiro)
    for coluna in colunas:
        coluna.reverse()

    refletido["A"] = colunas[0].copy()
    refletido["B"] = colunas[1].copy()
    refletido["C"] = colunas[2].copy()
    return refletido

def jogadaSegundaRodada(tabuleiro):
    if [
        tabuleiro["B"][0], 
        tabuleiro["C"][0], 
        tabuleiro["C"][1], 
        tabuleiro["C"][2],
        tabuleiro["B"][2]
        ]\
        .count("O") > 0:
        tabuleiro["A"][2] = "X"

    elif [tabuleiro["A"][1], tabuleiro["A"][2]].count("O") > 0:
        tabuleiro["C"][0] = "X"
    else:
        tabuleiro["C"][2] = "X"
    return tabuleiro

def jogadaTerceiraRodada(tabuleiro):
    linha3 = [tabuleiro[chave][2] for chave in tabuleiro if chave != " "]
    if linha3.count("") == 3 or tabuleiro["C"].count("") == 3:
        tabuleiro["B"][1] = "X"
    elif [tabuleiro["A"][2], tabuleiro["C"][0]].count("O") > 0:
        tabuleiro["C"][2] = "X"
    else:
        tabuleiro["C"][0] = "X"
    return tabuleiro

def ehPossivelFinalizar(modo: str, tabuleiro):
    if modo == "Ganhando":
        jogador = "X"
    else:
        jogador = "O"

    for fila in filasDo(tabuleiro):
        if fila.count(jogador) == 2 and fila.count("") == 1:
            return True
    return False

def jogarPara(acao, tabuleiro):
    if acao == "Ganhar":
        jogador = "X"
    else:
        jogador = "O"

    lacuna = ondeMarcar(jogador, tabuleiro)
    tabuleiro = marcarNa(lacuna, tabuleiro)
    return tabuleiro

def ondeMarcar(jogador, tabuleiro):
    filas = filasDo(tabuleiro).copy()
    for fila in filas:
        if fila.count(jogador) == 2 and fila.count("") == 1:
            return filas.index(fila), fila.index("")

def marcarNa(lacuna, tabuleiro):
    (coluna, linha) = decodifica(lacuna)
    tabuleiro[coluna][linha] = "X"
    return tabuleiro

def decodifica(lacuna):
    colunas = {
        "A": [(0,0), (3,0), (6,0), (0,1), (4,0), (0,2), (5, 0), (7,2)],
        "B": [(1,0), (3,1), (1,1), (4,1), (6,1), (7,1), (1,2), (5,1)], 
        "C": [(2,0), (3,2), (7,0), (2,1), (4,2), (2,2), (5,2), (6,2)]
    }

    linhas = {
        0: [(0,0), (3,0), (6,0), (1,0), (3,1), (2,0), (3,2), (7,0)],
        1: [(0,1), (4,0), (1,1), (4,1), (6,1), (7,1), (2,1), (4,2)],
        2: [(0,2), (5, 0), (7,2), (1,2), (5,1), (2,2), (5,2), (6,2)]
    }
    
    for chave, codigos in colunas.items():
        if lacuna in codigos:
            coluna = chave
            break

    for chave, codigos in linhas.items():
        if lacuna in codigos:
            linha = chave
            break
    
    return coluna, linha

def filasDo(tabuleiro):
    colunas = colunasDo(tabuleiro)
    linhas = linhasDo(tabuleiro)
    diagonais = diagonaisDo(tabuleiro)
    return colunas + linhas + diagonais

def colunasDo(tabuleiro):
    return [tabuleiro[chave].copy() for chave in tabuleiro if chave != " "]

def linhasDo(tabuleiro):
    linhas = []
    for i in range(3):
        linha = [tabuleiro[chave][i] for chave in tabuleiro if chave != " "]
        linhas.append(linha)
    return linhas

def diagonaisDo(tabuleiro):
    diagonais = []
    diagonalPrincipal = [
        tabuleiro["A"][0],
        tabuleiro["B"][1],
        tabuleiro["C"][2]
    ]
    
    diagonalSecundaria = [
        tabuleiro["C"][0],
        tabuleiro["B"][1],
        tabuleiro["A"][2]
    ]

    diagonais.append(diagonalPrincipal)
    diagonais.append(diagonalSecundaria)

    return diagonais

# Dicionário para registro do jogo
tabuleiro = {
                " ": ["1", "2", "3"],
                "A": ["", "", ""],
                "B": ["", "", ""],
                "C": ["", "", ""]
            }
# Flag que é acionada para finalizar o jogo
acabou = False
# String para acompanhar qual o jogador da vez
jogador = "X"
# Inteiro para contar em qual rodada estamos
# rodada = 0

print("Instruções:\nDigite as coordenadas da sua jogada no formato letra e numero (Exs: 'A 1', 'B 2', 'C 3', etc)\n")
# Loop enquanto jogo não acabar que cicla em jogada da maquina e jogada do usuario com as devidas validações de entrada e fim de jogo
while not acabou:
    # rodada += 1
    tabuleiro = jogadaMaquina(tabuleiro)
    acabou = confereFim(tabuleiro)
    if not acabou:
        imprimiTabuleiro(tabuleiro)
        tabuleiro = jogada(tabuleiro)
        acabou = confereFim(tabuleiro)
