from tabulate import tabulate

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

def parabenizaGanhador(tabuleiro, jogadorGanhou):
    """
    Imprime o tabuleiro e parabeniza o ganhador
    Parâmetros: tabuleiro e jogador que ganhou
    """
    imprimiTabuleiro(tabuleiro)
    # Parabenização invertida pois jogador da vez veio depois da jogada onde a vitória ocorreu
    if jogadorGanhou == "X":
        print("A máquina ganhou!")
    else:
        print("O jogador ganhou! (Não deve acontecer)")

def imprimiTabuleiro(tabuleiro):
    """
    Imprime o tabuleiro utilizando o tabulate para estilização
    Parâmetros: tabuleiro
    """
    print(tabulate(tabuleiro, headers="keys", tablefmt="fancy_grid"))

def confereGanhador(tabuleiro, jogador):
    """
    Confere linhas, colunas e diagonais pelo padrão de vitória
    Parâmetros: tabuleiro
    Retorno: True(Vitória)/False(Sem vitória)
    """
    # Confere Colunas
    if tabuleiro["A"].count("X") == 3 or tabuleiro["A"].count("O") == 3 or \
       tabuleiro["B"].count("X") == 3 or tabuleiro["B"].count("O") == 3 or \
       tabuleiro["C"].count("X") == 3 or tabuleiro["C"].count("O") == 3:
        parabenizaGanhador(tabuleiro, jogador)
        return True
    # Confere Linhas
    elif tabuleiro["A"][0] == tabuleiro["B"][0] == tabuleiro["C"][0] and tabuleiro["A"][0] != "" or \
         tabuleiro["A"][1] == tabuleiro["B"][1] == tabuleiro["C"][1] and tabuleiro["A"][1] != "" or \
         tabuleiro["A"][2] == tabuleiro["B"][2] == tabuleiro["C"][2] and tabuleiro["A"][2] != "":
        parabenizaGanhador(tabuleiro, jogador)
        return True
    # Confere Diagonais
    elif tabuleiro["A"][0] == tabuleiro["B"][1] == tabuleiro["C"][2] or tabuleiro["C"][0] == tabuleiro["B"][1] == tabuleiro["A"][2] and tabuleiro["B"][1] != "":
        parabenizaGanhador(tabuleiro, jogador)
        return True
    return False

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

def confereFim(tabuleiro, jogador):
    """
    Confere se os possiveis finais (vitória de alguma parte) ou empate ocorreram
    Parâmtros: tabuleiro, jogador (que fez a última jogada)
    Retorno: True(Acabou o jogo)/ False(Não acabou o jogo)
    """
    acabou = False
    acabou = confereGanhador(tabuleiro, jogador)
    if not acabou:
        acabou = confereEmpate(tabuleiro)
    return acabou

def jogadaMaquina(tabuleiro, rodada):
    """
    Processa a jogada que deve ser feita pela máquina
    Parâmetros: tabuleiro, rodada (Contagem de quantas jogadas foram feitas)
    Retorno: tabuleiro
    """
    if rodada == 1:
        tabuleiro["A"][0] = "X"

    elif rodada == 2:
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
    
    elif ehPossivelFinalizar("Ganhando", tabuleiro):
        tabuleiro = ganhar(tabuleiro)
        
    else:
        if ehPossivelFinalizar("Perdendo", tabuleiro):
            tabuleiro = evitarPerda(tabuleiro)
        
        else:
            if rodada == 3:
                linha3 = [tabuleiro[chave][2] for chave in tabuleiro if chave != " "]
                if linha3.count("") == 3 or tabuleiro["C"].count("") == 3:
                    tabuleiro["B"][1] = "X"
                elif [tabuleiro["A"][2], tabuleiro["C"][0]].count("O") > 0:
                    tabuleiro["C"][2] = "X"
                else:
                    tabuleiro["C"][0] = "X"
                
    return tabuleiro

def filasDo(tabuleiro):
    filas = [tabuleiro[chave].copy() for chave in tabuleiro if chave != " "]

    for i in range(3):
        linha = [tabuleiro[chave][i] for chave in tabuleiro if chave != " "]
        filas.append(linha)

    diagonalPrincipal = [
        tabuleiro["A"][0],
        tabuleiro["B"][1],
        tabuleiro["C"][2]
    ]
    filas.append(diagonalPrincipal)

    diagonalSecundaria = [
        tabuleiro["C"][0],
        tabuleiro["B"][1],
        tabuleiro["A"][2]
    ]
    filas.append(diagonalSecundaria)

    return filas

def ehPossivelFinalizar(modo: str, tabuleiro):
    if modo == "Ganhando":
        marca = "X"
    else:
        marca = "O"

    for fila in filasDo(tabuleiro):
        if fila.count(marca) == 2 and fila.count("") == 1:
            return True
    return False

def ganhar(tabuleiro):
    lacuna = ondeMarcarPara("Ganhar", tabuleiro)
    tabuleiro = marcarNa(lacuna, tabuleiro)
    return tabuleiro

def evitarPerda(tabuleiro):
    lacuna = ondeMarcarPara("NaoPerder", tabuleiro)
    tabuleiro = marcarNa(lacuna, tabuleiro)
    return tabuleiro

def ondeMarcarPara(acao, tabuleiro):
    if acao == "Ganhar":
        marca = "X"
    else:
        marca = "O"

    fileiras = filasDo(tabuleiro).copy()
    for fila in fileiras:
        if fila.count(marca) == 2 and fila.count("") == 1:
            return fileiras.index(fila), fila.index("")

def marcarNa(lacuna, tabuleiro):
    (coluna, linha) = decodifica(lacuna)
    tabuleiro[coluna][linha] = "X"
    return tabuleiro

def decodifica(lacuna):
    colunaA = [(0,0), (3,0), (6,0), (0,1), (4,0), (0,2), (5, 0), (7,2)]
    colunaB = [(1,0), (3,1), (1,1), (4,1), (6,1), (7,1), (1,2), (5,1)]
    colunaC = [(2,0), (3,2), (7,0), (2,1), (4,2), (2,2), (5,2), (6,2)]

    linha1 = [(0,0), (3,0), (6,0), (1,0), (3,1), (2,0), (3,2), (7,0)]
    linha2 = [(0,1), (4,0), (1,1), (4,1), (6,1), (7,1), (2,1), (4,2)]
    linha3 = [(0,2), (5, 0), (7,2), (1,2), (5,1), (2,2), (5,2), (6,2)]
    
    if lacuna in colunaA:
        coluna = "A"
    elif lacuna in colunaB:
        coluna = "B"
    else:
        coluna = "C"

    if lacuna in linha1:
        linha = 0
    elif lacuna in linha2:
        linha = 1
    else:
        linha = 2
    
    return coluna, linha

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
rodada = 0

print("Instruções:\nDigite as coordenadas da sua jogada no formato letra e numero (Exs: 'A 1', 'B 2', 'C 3', etc)\n")
# Loop enquanto jogo não acabar que cicla em jogada da maquina e jogada do usuario com as devidas validações de entrada e fim de jogo
while not acabou:
    rodada += 1
    tabuleiro = jogadaMaquina(tabuleiro, rodada)
    acabou = confereFim(tabuleiro, "X")
    if not acabou:
        imprimiTabuleiro(tabuleiro)
        tabuleiro = jogada(tabuleiro)
        acabou = confereFim(tabuleiro, "O")
