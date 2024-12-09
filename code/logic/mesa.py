from logic.peca import Peca

class Mesa:
    def __init__(self):
        self.linhas = 20
        self.colunas = 50
        self.pecas_dispostas = [[ None for _ in range(self.colunas)] for _ in range(self.linhas)] 
        self.atualizando = False
        self.valido = True


    def validar_mesa(self) -> bool:
        self.atualizando = True
        for i in range(self.linhas):
            j = 0
            while j != self.colunas:
                proximo_bloco, ret = self.obter_proximo_bloco(self.pecas_dispostas[i], j)

                if ret == -1 or ret == self.colunas:
                    break

                j = ret

                if len(proximo_bloco) < 3:
                    self.atualizando = True
                    self.valido = False
                    return False

                if (self.grupo_valido(proximo_bloco)):
                    continue

                elif (self.sequencia_valida(proximo_bloco)):
                    continue

                self.atualizando = False
                self.valido = False
                return False

        self.atualizando = False
        self.valido = True
        return True


    def obter_proximo_bloco(self, linha_atual: list, posicao_atual: int):
        for i in range(posicao_atual, len(linha_atual)):
            if linha_atual[i] is not None:
                bloco = []
                while linha_atual[i] is not None:
                    bloco.append(linha_atual[i])
                    i += 1

                return bloco, i

        return [], -1
            

    def grupo_valido(self, bloco: list) -> bool:
        coringa_usado = False
        valido = True
        numero_sequencia = bloco[0].valor
        cores = []

        for peca in range(len(bloco)):
            if bloco[peca].valor < 0:
                if coringa_usado == False:
                    coringa_usado = True
                else:
                    valido = False

                continue

            if bloco[peca].valor != numero_sequencia:
                valido = False

            if bloco[peca].cor in cores:
                valido = False
            else:
                cores.append(bloco[peca].cor)

        return valido


    def sequencia_valida(self, bloco: list) -> bool:
        coringa_usado = False
        valido = True

        n_operando = 1
        cor_sequencia = bloco[0].cor
        peca_anterior = bloco[0].valor - 1


        for peca in range(len(bloco)):
            if bloco[peca].valor > 0:
                if bloco[peca].cor != cor_sequencia:
                    valido = False

                if bloco[peca].valor == peca_anterior + n_operando:
                    peca_anterior = bloco[peca].valor

            else:
                if coringa_usado == True:
                    valido = False

                coringa_usado = True
                if bloco[peca].tipoCoringa == 1:
                    peca_anterior += 1

                elif bloco[peca].tipoCoringa == 2:
                    peca_anterior += 2

                elif bloco[peca].tipoCoringa == 3:
                    peca_anterior += 1
                    n_operando = -1

                elif bloco[peca].tipoCoringa == 4:
                    cor_sequencia = bloco[peca+1].cor

                continue

        return valido
