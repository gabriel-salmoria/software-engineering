from logic.banco_de_pecas import BancoDePecas
from logic.peca_numero import PecaNumero
from interface.interface_mesa import InterfaceMesa
from logic.mesa import Mesa
from logic.jogador import Jogador
from copy import copy

class Jogo:
    def __init__(self, interface_jogador, cronometro):
        self.listaJogadores = [Jogador(self) for _ in range(2)]
        self.mesa = Mesa()
        self.bancoDePecas = BancoDePecas(self)
        self.status_partida = 0
        self.jogada_atual = None
        self.estado_anterior = None
        self.turnoAtual = False
        self.cronometro = cronometro
        self.cronometro.jogo = self
        self.interface_jogador = interface_jogador


    def receber_estado_elementos(self):
        pass

    def abandonar_partida(self):
        pass # TODO : terminar execucao do jogo.


    def enviar_jogada(self, peca_atualizada: "InterfacePeca") -> bool:
        pass # TODO : lidar com dog


    def finalizar_partida(self, partida_encerrada: bool) -> bool:
        pass


    def verificar_turno(self) -> bool:
        if self.turnoAtual == 1:
            return True

        return False


    def receber_nome_vencedor(self) -> str:
        for jogador in self.listaJogadores:
            if jogador.vencedor:
                return jogador.nome

        return ""


    # identifica e trata a jogada, tinham umas 2-3 funcoes que fariam a mesma
    # coisa do que essa, acabei continuando com isso.
    def identificar_jogada(self, jogada):
        if jogada["tipo"] == "peca_movida":
            peca, local = jogada["peca"], jogada["local"]
            x, y = jogada["x"], jogada["y"]
            
            self.listaJogadores[1].colocar_peca(peca, local, x, y)


        elif jogada["tipo"] == "pecas_distribuidas":
            self.pecas_distribuidas(jogada["pecas"])
            self.bancoDePecas.efetuar_distribuicao_pecas()


        elif jogada["tipo"] == "vez_passada":
            self.listaJogadores[0].efetuar_passagem_vez()
            self.inverter_turno()
            self.receber_estado_elementos()
            self.cronometro.iniciar_cronometro()


        elif jogada["tipo"] == "peca_comprada":
            # obter o estado anterior.

            self.listaJogadores[1].comprar_peca()
            self.receber_estado_elementos()
            self.inverter_turno()
            self.cronometro.iniciar_cronometro()


        self.interface_jogador.interface.atualizar_elementos()


    def validar_jogada(self) -> bool:
        return self.mesa.validar_mesa()


    def inverter_turno(self):
        for jogador in self.listaJogadores:
            jogador.atualizar_turno()

        self.turnoAtual = not self.turnoAtual



    # de acordo com os diagramas, só tem o cronometro a mais ali.
    def inicializar_jogo(self, players):
        for i in range(len(self.listaJogadores)):
            # inicializar os jogadores
            self.listaJogadores[i].inicializar(players[i][0], players[i][2])

            # atualizar o quadradinho na interface
            self.interface_jogador.interface.jogadores[i].label.config(text=players[i][0])

        # definir a ordem de execucao
        if players[0][2] == "1":
            self.listaJogadores[0].atualizar_turno()
            self.turnoAtual = True
            self.cronometro.iniciar_cronometro()
        else:
            self.listaJogadores[1].atualizar_turno()

        self.interface_jogador.interface.atualizar_elementos()


    # inutil ate agr
    def receber_status_partida(self):
        return self.status_partida


    # inutil ate agr
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


    # 99% feito, só preciso conseguir salvar o estado
    def efetuar_passagem_vez(self):
        valido = self.validar_jogada()
        dog = self.interface_jogador.dog_server_interface

        if valido:

            dog.send_move({
                "match_status" : "fodase",
                "tipo" : "vez_passada",
                })

        else:
            # obtem o estado anterior.

            self.listaJogadores[0].comprar_peca()
            self.receber_estado_elementos()
            self.inverter_turno()

            dog.send_move({
                "match_status" : "fodase",
                "tipo" : "peca_comprada",
                })

        self.interface_jogador.interface.atualizar_elementos()



    def tempo_acabou(self):
        self.listaJogadores[0].passar_vez()


    def peca_comprada(self, peca):
        self.bancoDePecas.pecas.remove(peca)


    # chamado pelo player remoto no receive move. apenas faz
    # a alteracao na ordem das pecas
    def pecas_distribuidas(self, string_codificada):
        pecas = []
        pecas_str = string_codificada.split(',')

        # recebo as pecas de quem iniciou, dou aquela arrumada
        # e depois distribuo as peças localmente no inicialiar_jogo
        for i, peca_str in enumerate(pecas_str):
            valor, cor = peca_str.split('-')
            peca = PecaNumero(int(valor), cor)
            
            if i < 14:
                pecas.append(peca)
            elif i < 28:
                pecas.insert(i - 14, peca)

        self.bancoDePecas.pecas = pecas



    # de acordo com diagrama
    def verificar_partida_encerrada(self):
        jog1 = self.listaJogadores[0].get_vencedor()
        jog2 = self.listaJogadores[1].get_vencedor()

        return jog1 or jog2
