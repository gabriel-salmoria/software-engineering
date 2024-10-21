from logic.peca_numero import PecaNumero
from logic.peca_coringa import PecaCoringa

class Mesa:
    def __init__(
            self,
            linhas: int,
            colunas: int,
         ):
        self.linhas = linhas
        self.colunas = colunas
        self.pecas = [[None for _ in range(colunas)] for _ in range(linhas)]


    def verificar(self):
        """ Checks all linhas in the table for valid sequencias. """
        for i in range(self.linhas):
            sequencia_atual = []

            for j in range(self.colunas):

                peca = self.pecas[i][j]
                if peca is not None:
                    sequencia_atual.append(peca)
                else:
                    if sequencia_atual:
                        if not self.checar_sequencia(sequencia_atual):
                            return False
                        sequencia_atual = []

            if sequencia_atual:
                if not self.checar_sequencia(sequencia_atual):
                    return False

        return True


    def checar_sequencia(self, sequencia: list[PecaNumero]):
        """ Checks if the given sequencia is a valid run or group. """

        if len(sequencia) < 3:
            return False

        if self.is_valid_run(sequencia) or self.is_valid_group(sequencia):
            return True

        return False


    def is_valid_run(self, sequencia: list):
        """Checks if the sequencia is a valid run (consecutive numeros, same cor)."""

        numeros = []
        cor = sequencia[0].cor

        for peca in sequencia:
            if isinstance(peca, PecaCoringa):
                numeros.append(numeros[-1]+1) 

            elif peca.get_cor() != cor:
                return False

            numeros.append(peca.get_numero())

        for i in range(len(numeros) - 1):
            if numeros[i] + 1 != numeros[i + 1]:
                return False

        return True


    def is_valid_group(self, sequencia: list):
        """Checks if the sequencia is a valid group (same numero, different cors)."""

        if len(sequencia) > 4:
            return False

        numero = sequencia[0].numero
        cores = set()

        for peca in sequencia:
            if isinstance(peca, PecaCoringa):
                continue

            elif peca.get_numero() != numero or peca.get_cor() in cores:
                return False

            cores.add(peca.get_cor())

        return True

