# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 34:
# 99235 Hugo Manuel Alves Henriques e Silva
# 99299 Pedro Charneca Florindo

import sys
from search import (
    InstrumentedProblem,
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    compare_searchers,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import time


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def three_in_a_row_vertical(self, key):
        row = key[0]
        col = key[1]
        adjacent = self.board.adjacent_vertical_numbers(row, col)
        above_adjacent = adjacent[1]
        below_adjacent = adjacent[0]
        #print(str(adjacent) + '\n')
        if (above_adjacent == below_adjacent and above_adjacent != None):
            if above_adjacent == 1:
                return [row, col, 0]
            elif above_adjacent == 0:
                return [row, col, 1]
        elif above_adjacent != 2 and above_adjacent != None:
            above_adjacent_2 = self.board.adjacent_vertical_numbers(row - 1, col)[1]
            if above_adjacent == above_adjacent_2:
                if above_adjacent == 1:
                    return [row, col, 0]
                else:
                    return [row, col, 1]
        if below_adjacent != 2 and below_adjacent != None:
            below_adjacent_2 = self.board.adjacent_vertical_numbers(row + 1, col)[0]
            if below_adjacent == below_adjacent_2:
                if below_adjacent == 1:
                    return [row, col, 0]
                else:
                    return [row, col, 1]

        return None
    
    def three_in_a_row_horizontal(self, key):
        row = key[0]
        col = key[1]
    
        adjacent = self.board.adjacent_horizontal_numbers(row, col)
        #print(str(adjacent) + '\n')
        right_adjacent = adjacent[1]
        left_adjacent = adjacent[0]

        if (right_adjacent == left_adjacent and right_adjacent != None):
            if right_adjacent == 1:
                return [row, col, 0]

            elif right_adjacent == 0:
                return [row, col, 1]

        if right_adjacent != 2 and right_adjacent != None:
            right_adjacent_2 = self.board.adjacent_horizontal_numbers(row, col + 1)[1]

            if right_adjacent == right_adjacent_2:

                if right_adjacent == 1:
                    return [row, col, 0]
                else:
                    return [row, col, 1]

        if left_adjacent != 2 and left_adjacent != None:
            left_adjacent_2 = self.board.adjacent_horizontal_numbers(row, col - 1)[0]

            if left_adjacent == left_adjacent_2:

                if left_adjacent == 1:
                    return [row, col, 0]
                else:
                    return [row, col, 1]
        
        return None

    def check_max_num_row(self, key):
        row = key[0]
        col = key[1]
        zeros = 0
        ones = 0
        if (self.board.N % 2 == 0):
            maxNum = self.board.N / 2
        else:
            maxNum = self.board.N / 2 + 1

        for i in range(self.board.N):
            if self.board.tab[row][i] == 1:
                ones += 1
            elif self.board.tab[row][i] == 0:
                zeros += 1

        if (zeros == maxNum):
            return [row, col, 1]
        elif (ones == maxNum):
            return [row,col, 0]
        else:
            return None

    def check_max_num_col(self, key):
        row = key[0]
        col = key[1]
        zeros = 0
        ones = 0
        if (self.board.N % 2 == 0):
            maxNum = self.board.N / 2
        else:
            maxNum = self.board.N / 2 + 1

        for i in range(self.board.N):
            if self.board.tab[i][col] == 1:
                ones += 1
            elif  self.board.tab[i][col] == 0:
                zeros += 1

        if (zeros == maxNum):
            return [row, col, 1]
        elif (ones == maxNum):
            return [row, col, 0]
        else:
            return None


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, tab, N, blankPositions, rowNums, colNums, lastPlayed, mandatoryPlay, auxMandatoryPlay):
        self.tab = tab
        self.N = N
        self.blankPositions = blankPositions
        self.rowNums = rowNums
        self.colNums = colNums
        self.lastPlayed = lastPlayed
        self.mandatoryPlay = mandatoryPlay
        self.auxMandatoryPlay = auxMandatoryPlay


    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.tab[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if row == 0:
            return (self.get_number(row + 1, col), None)
        elif row == self.N-1:
            return (None, self.get_number(row - 1, col))
        else:
            return (self.get_number(row + 1, col), self.get_number(row - 1, col))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return (None, self.get_number(row, col + 1))
        elif col == self.N - 1:
            return (self.get_number(row, col - 1), None)
        else:
            return (self.get_number(row, col - 1), self.get_number(row, col + 1))

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        N = eval(input())
        counter = 0;
        lines = [];
        for line in sys.stdin:
            if counter == N:
                break
            lines.append(line)


        tab = []
        blank = []
        colNums = []
        rowNums = []

        for i in range(N):
            colNums.append(0)
            rowNums.append(0)

        rowNum = 0
        for i in lines:
            colNum = 0
            rowVals = []
            for j in i.split():
                val = int(j)
                rowVals.append(val)
                if val != 2:
                    colNums[colNum] += 1
                    rowNums[rowNum] += 1
                else:
                    blank.append([rowNum, colNum])
                colNum += 1
            tab.append(rowVals)
            rowNum += 1

        #print(blank)
        #print(tab)
        
        board = Board(tab, N, blank, rowNums, colNums, (-1, -1, -1), False, False)

        return board

    def __str__(self):
        res = ""
        for i in range(0, self.N):
            for j in range(0, self.N):
                val = self.tab[i][j]
                res += str(val)
                if (j+1) == self.N and i != (self.N - 1):
                    res += "\n"
                elif j != (self.N - 1):
                    res += "\t"
        return res


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        maxNumsCols = []
        maxAdjacents = 0
        maxAdjList = []
        maxC = 0
        maxR = 0
        maxNumsRows = []
        actions = []
        rows_visited = {}
        cols_visited = {}

        aux = {}

        #print(state.board.blankPositions)
        #print("previous action: " + str(state.board.lastPlayed))

        for key in state.board.blankPositions:
            row = key[0]
            col = key[1]

            if state.board.rowNums[row] > maxR:
                maxNumsRows = [(row, col)]
                maxR = state.board.rowNums[row]

            elif state.board.rowNums[row] == maxR:
                maxNumsRows.append((row, col))

            if state.board.colNums[col] > maxC:
                maxNumsCols = [(row, col)]
                maxC = state.board.colNums[col]

            elif state.board.colNums[col] == maxC:
                maxNumsCols.append((row, col))


            act = state.three_in_a_row_horizontal(key)
            if act != None:
                #print("act1")
                state.board.auxMandatoryPlay = True
                #print(act)
                return [act]
            else:
                act2 = state.three_in_a_row_vertical(key)
                if act2 != None:
                    #print("act2")
                    state.board.auxMandatoryPlay = True
                    #print(act2)
                    return [act2]
            if (row not in rows_visited and state.board.rowNums[row] != state.board.N):
                act3 = state.check_max_num_row(key)
                rows_visited[row] = None
                if act3 != None:
                    #print("act3")
                    #print(act3)
                    state.board.auxMandatoryPlay = True
                    return [act3]
            if (col not in cols_visited and state.board.colNums[col] != state.board.N):
                act4 = state.check_max_num_col(key)
                cols_visited[col] = None
                if act4 != None:
                    #print(act4)
                    #print("act4")
                    state.board.auxMandatoryPlay = True
                    return [act4]
            
            adjVal = self.countAdjacents(state, key)
            if adjVal > maxAdjacents:
                maxAdjacents = adjVal
                maxAdjList = [(row, col)]
                
            elif adjVal == maxAdjacents:
                maxAdjList.append((row, col))

        if maxAdjacents >= 2:
            for i in maxAdjList:
                aux[i] = None
                actions.append([i[0], i[1], 0])
                actions.append([i[0], i[1], 1])    

        else:
            for i in maxNumsRows:
                if i not in aux:
                    aux[i] = None
                    actions.append([i[0], i[1], 0])
                    actions.append([i[0], i[1], 1])

            for i in maxNumsCols:
                if i not in aux:
                    actions.append([i[0], i[1], 0])
                    actions.append([i[0], i[1], 1])

        
        #print("nao ha obrigatorias: " + str(actions))

        if len(actions) > 2:
            return actions[:2]
        return actions

        
    def countAdjacents(self, state, key):
        row = key[0]
        col = key[1]
        count = 0

        horizontal = state.board.adjacent_horizontal_numbers(row, col)
        if horizontal[0] != 2 and horizontal[0] != None:
            count += 1
        if horizontal[1] != 2 and horizontal[1] != None:
            count += 1
        
        vertical = state.board.adjacent_vertical_numbers(row, col)
        if vertical[0] != 2 and vertical[0] != None:
            count += 1
        if vertical[1] != 2 and vertical[1] != None:
            count += 1
        
        return count

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        row = action[0]
        col = action[1]
        val = action[2]

        #print(action)

        tabAux = []
        for i in range(state.board.N):
            rowVals = []
            for j in range(state.board.N):
                rowVals.append(state.board.tab[i][j])
            tabAux.append(rowVals)


        tabAux[row][col] = val

        #print(tabAux)
        
        rowNumsAux = []
        colNumsAux = []

        for i in range(state.board.N):
            rowEl = state.board.rowNums[i]
            colEl = state.board.colNums[i]
            rowNumsAux.append(rowEl)
            colNumsAux.append(colEl)
        
        rowNumsAux[row] += 1
        colNumsAux[col] += 1

        blankAux = []

        for key in state.board.blankPositions:
            if key != [row, col]:
                blankAux.append(key)

        #print(blankAux)

        lastPlayedAux = (row, col, val)

        if state.board.auxMandatoryPlay:
            boardAux = Board(tabAux, state.board.N, blankAux, rowNumsAux, colNumsAux, lastPlayedAux, True, False)
        else:
            boardAux = Board(tabAux, state.board.N, blankAux, rowNumsAux, colNumsAux, lastPlayedAux, False, False)

        #print(boardAux)

        stateAux = TakuzuState(boardAux)

        return stateAux

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return state.board.blankPositions == []

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO

        heuristic = 10000
        
        lastMove = node.state.board.lastPlayed
        lastMoveRow = lastMove[0]
        lastMoveCol = lastMove[1]
        lastMoveVal = lastMove[2]

        # se coluna tem zeros ou uns a mais
        if self.checkMaxNumCol(node, lastMoveCol):
            return float('inf')

        # se linha tem zeros ou uns a mais
        if self.checkMaxNumRow(node, lastMoveRow):
            return float('inf')

        # se coluna estiver completa
        if node.state.board.colNums[lastMoveCol] == node.state.board.N:
            if self.checkRepeatedCols(node, lastMoveCol):
                return float('inf')

        # se linha estiver completa
        if node.state.board.rowNums[lastMoveRow] == node.state.board.N:
            if self.checkRepeatedRows(node, lastMoveRow):
                return float('inf')
        

        heuristic -= self.checkAdjacent(node, lastMoveRow, lastMoveCol, lastMoveVal)

        # here
        heuristic -= self.countAdjacents(node.state, lastMove)

        heuristic -= self.numFilledPositionsRowCol(node, lastMoveRow, lastMoveCol)

        if node.state.board.mandatoryPlay and heuristic != float('inf'):
           heuristic = 0

        return heuristic


    def checkMaxNumRow(self, node, row):

        N = node.state.board.N
        zeros = 0
        ones = 0

        if N % 2 == 0:
            maxNum = N / 2
        else:
            maxNum = N / 2 + 1

        for i in range(N):
            val = node.state.board.tab[row][i]
            if val == 1:
                ones += 1
            elif val == 0:
                zeros += 1

        if zeros > maxNum or ones > maxNum:
            return True

        return False

    def checkMaxNumCol(self, node, col):

        N = node.state.board.N
        zeros = 0
        ones = 0

        if N % 2 == 0:
            maxNum = N / 2
        else:
            maxNum = N / 2 + 1

        for i in range(N):
            val = node.state.board.tab[i][col]
            if val == 1:
                ones += 1
            elif val == 0:
                zeros += 1

        if zeros > maxNum or ones > maxNum:
            return True

        return False

    """quanto menor for o numero de espacos em branco na coluna e linha jogadas,
    mais beneficiada sera a heuristica"""
    def numFilledPositionsRowCol(self, node, row, col):
        aux = 0
        aux += node.state.board.rowNums[row]
        aux += node.state.board.colNums[col]
        return aux


    """2 numeros iguais seguidos beneficiam a heuristica, tanto vertical como horizontalmente aditivamente
    em principio nao eh relevante o que e adjacente aos adjacentes da ultima jogada"""
    def checkAdjacent(self, node, row, col, val):

        aux = 0
    
        adjacent_vertical_numbers = node.state.board.adjacent_vertical_numbers(row, col)
        below = adjacent_vertical_numbers[0]
        above = adjacent_vertical_numbers[1]

        if below != None:
            below2 = node.state.board.adjacent_vertical_numbers(row + 1, col)[0]
        else:
            below2 = None

        if above != None:
            above2 = node.state.board.adjacent_vertical_numbers(row - 1, col)[1]
        else:
            above2 = None

        adjacent_horizontal_numbers = node.state.board.adjacent_horizontal_numbers(row, col)
        left = adjacent_horizontal_numbers[0]
        right = adjacent_horizontal_numbers[1]

        if left != None:
            left2 = node.state.board.adjacent_horizontal_numbers(row, col - 1)[0]
        else:
            left2 = None

        if right != None:
            right2 = node.state.board.adjacent_horizontal_numbers(row, col + 1)[1]
        else:
            right2 = None

        if val != None:

            #print("bro?")

            if (below == below2) and (below == val):
                #print("NAO PODE SER")
                return float('-inf')
            if (above == above2) and (above == val):
                #print("NAO PODE SER")
                return float('-inf')
            if left == left2 and left == val:
                #print("NAO PODE SER")
                return float('-inf')
            if right == right2 and right == val:
                #print("NAO PODE SER")
                return float('-inf')

            if below == above and below == val:
                return float('-inf')
            elif below == val or above == val:
                aux += 1
            
            if left == right and left == val:
                return float('-inf')
            elif left == val or right == val:
                aux += 1

        return aux
        

        
    def checkRepeatedCols(self, node, col):
 
        broke = False

        for i in range(node.state.board.N):
            if i != col:
                broke = False
                for j in range(node.state.board.N):
                    if node.state.board.tab[j][col] != node.state.board.tab[j][i]:
                        broke = True
                        break
                if not broke:
                    return True

        return False

    def checkRepeatedRows(self, node, row):

        broke = False

        for i in range(node.state.board.N):
            if i != row:
                broke = False
                for j in range(node.state.board.N):
                    if node.state.board.tab[row][j] != node.state.board.tab[i][j]:
                        broke = True
                        break
                if not broke:
                    return True

        return False


if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    # Obter o nome do ficheiro da command line

    board = Board.parse_instance_from_stdin()

    
    takuzuStart = Takuzu(board)
    
    answer = greedy_search(takuzuStart)

    print(answer.state.board)

