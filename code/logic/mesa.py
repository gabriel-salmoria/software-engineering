from logic.peca import Peca

class Mesa:
    def __init__(self):
        self.linhas = 20
        self.colunas = 50
        self.pecas_dispostas = [[ None for _ in range(self.colunas)] for _ in range(self.linhas)] 
        self.atualizando = False
        self.valido = True


    def validar_mesa(self) -> bool:
        for linha in range(len(self.pecas_dispostas)):
            for coluna in range(len(self.pecas_dispostas[0])):
                proximo_bloco, ret = self.obter_proximo_bloco(self.pecas_dispostas[linha], coluna)

                if ret != -1:
                    coluna = ret

                if (self.grupo_valido(proximo_bloco)):
                    continue

                elif (self.sequencia_valida(proximo_bloco)):
                    continue

                else:
                    return False

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
        usou_coringa = False
        cores = []

        for peca in range(len(bloco)):
            if bloco[peca].valor == -1:
                if usou_coringa == False:
                    usou_coringa = True
                else:
                    return False

                continue

            if bloco[peca].cor in cores:
                return False
            else:
                cores.append(bloco[peca].cor)

        return True


    def sequencia_valida(self, bloco: list) -> bool:
        usou_coringa = False
        n_operando = 1
        cor_sequencia = bloco[0].cor
        peca_anterior = bloco[0].valor - 1

        for peca in range(len(bloco)):
            if bloco[peca].valor != -1:
                if bloco[peca].cor != cor_sequencia:
                    return False

                if bloco[peca].valor == peca_anterior + n_operando:
                    peca_anterior = bloco[peca]

            else:
                if usou_coringa == True:
                    return False

                usou_coringa = True
                if bloco[peca].tipoCoringa == 1:
                    peca_anterior += 1

                elif bloco[peca].tipoCoringa == 2:
                    peca_anterior += 2

                elif bloco[peca].tipoCoringa == 3:
                    peca_anterior += 1
                    n_operando = -1

                elif bloco[peca].tipoCoringa == 2:
                    cor_sequencia = bloco[peca+1].cor

                continue

        return True
