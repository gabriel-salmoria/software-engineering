from logic.banco_de_pecas import BancoDePecas
from logic.mesa import Mesa
from logic.jogador import Jogador

class Jogo:
    def __init__(self, interface_jogador, cronometro):
        self.listaJogadores = [Jogador(self) for _ in range(2)]
        self.mesa = Mesa()
        self.bancoDePecas = None
        self.status_partida = 0
        self.turnoAtual = False
        self.cronometro = cronometro
        self.interface_jogador = interface_jogador


    def abandonar_partida(self):
        pass # TODO : terminar execucao do jogo.


    def enviar_jogada(self, peca_atualizada: "InterfacePeca") -> bool:
        pass # TODO : lidar com dog


    def finalizar_partida(self, partida_encerrada: bool) -> bool:
        pass


    def receber_estado_elementos(self):
        self.interface_jogador.interface.atualizar_elementos()
        pass # TODO : nao sei oq fazer


    def verificar_turno(self) -> bool:
        if self.turnoAtual == 1:
            return True

        return False

    def receber_nome_vencedor(self) -> str:
        for jogador in self.listaJogadores:
            if jogador.vencedor:
                return jogador.nome

        return ""


    def identificar_jogada(self, jogada):
        if jogada["tipo"] == "peca_movida":
            peca = jogada["move"]["peca"]
            x = jogada["move"]["x"]
            y = jogada["move"]["y"]
            self.listaJogadores[0].colocar_peca(peca, x, y)

        if jogada["tipo"] == "pecas_distribuidas":
            self.bancoDePecas.efetuar_distribuicao_pecas()

        if jogada["tipo"] == "vez_passada":
            self.listaJogadores[0].efetuar_passagem_vez()

        self.interface_jogador.interface.atualizar_elementos()


    def validar_jogada(self) -> bool:
        return self.mesa.validar_mesa()


    def inverter_turno(self):
        for jogador in self.listaJogadores:
            jogador.atualizar_turno()

        self.turnoAtual = not self.turnoAtual



    def inicializar_jogo(self, players, local_player_id):
        for i in range(len(self.listaJogadores)):
            self.listaJogadores[i].inicializar(players[i][2], players[i][2])

        self.bancoDePecas = BancoDePecas(self)

        if players[0][2] == "1":
            self.listaJogadores[0].atualizar_turno()
        else:
            self.listaJogadores[0].atualizar_turno()

        estado = self.receber_estado_elementos()

        move = {
            "tipo" : "inicializar",
            "estado" : estado
        }

        self.interface_jogador.send_move(move)
        self.interface_jogador.interface.atualizar_elementos()


    def receber_status_partida(self):
        return self.status_partida


    def reiniciar_jogo(self):
        info = []

        for i in range(2):
            info.append([
                self.listaJogadores[i].nome,
                self.listaJogadores[i].cor
            ])

        self.listaJogadores = []

        for i in range(2):
            jogador = Jogador(self)
            jogador.inicializar(info[i][0], info[i][1])
            self.listaJogadores.append(jogador)

        self.mesa = Mesa()
        self.interface_jogador.interface.atualizar_elementos()

    def efetuar_passagem_vez(self):
        pass # TODO : nao sei oq fazer


    def tempo_acabou(self):
        self.listaJogadores[0].passar_vez()


    def peca_comprada(self, peca: "Peca"):
        self.bancoDePecas.pecas.remove(peca)


    def pecas_distribuidas(self):
        self.receber_estado_elementos()
        self.interface_jogador.atualizar_estado()


    def verificar_partida_encerrada(self):
        jog1 = self.listaJogadores[0].get_vencedor()
        jog2 = self.listaJogadores[1].get_vencedor()

        return jog1 or jog2
