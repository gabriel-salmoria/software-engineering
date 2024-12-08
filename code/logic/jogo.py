from logic.banco_de_pecas import BancoDePecas
from logic.peca_numero import PecaNumero
from interface.interface_mesa import InterfaceMesa
from interface.interface_peca import InterfacePeca
from tkinter import messagebox
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
        estado_jogo = {}

        pecas1 = []
        pecas2 = []
        for peca in self.listaJogadores[0].pecasMao:
            pecas1.append(self.traduzir_peca(peca))

        for peca in self.listaJogadores[1].pecasMao:
            pecas2.append(self.traduzir_peca(peca))
            
        mesa = self.mesa.pecas_dispostas
        mesa_info = []

        for i in range(len(mesa)):
            pecas_linha = []
            for j in range(len(mesa[0])):
                if mesa[i][j] is not None:
                    peca = mesa[i][j]
                    pecas_linha.append([self.traduzir_peca(peca), i, j])

            mesa_info.append(pecas_linha)
 
        estado_jogo['jogador1'] = pecas1
        estado_jogo['jogador2'] = pecas2
        estado_jogo['mesa'] = mesa_info

        self.estado_anterior = estado_jogo


    def traduzir_peca(self, peca):
        valor, cor = peca.valor, peca.cor
        nova = PecaNumero(valor, cor)

        if peca.int is None:
            return nova, None

        if isinstance(peca.int.parent, InterfaceMesa):
            parent = "mesa"
        else:
            parent = "sup"

        nova_int = {
            "linha": peca.int.linha,
            "coluna": peca.int.coluna,
            "parent": parent
        }

        return [nova, nova_int]


    def reconstruir_estado(self):
        jogador1 = self.estado_anterior['jogador1']
        jogador2 = self.estado_anterior['jogador2']
        mesa_info = self.estado_anterior['mesa']

        interface = self.interface_jogador.interface
        suporte = interface.suporte_jogador
        inter_mesa = interface.mesa_principal

        # Limpar o estado atual da mesa
        mesa = self.mesa.pecas_dispostas
        for i in range(len(mesa)):
            for j in range(len(mesa[0])):
                peca = mesa[i][j]
                if peca is not None:
                    peca.int.destroy()
                    mesa[i][j] = None


        self.pecas_dispostas = [[ None for _ in range(self.mesa.colunas)] for _ in range(self.mesa.linhas)] 
        for peca in suporte.pecas:
            peca.destroy()
        for peca in inter_mesa.pecas:
            peca.destroy()

        suporte.pecas = []
        inter_mesa.pecas = []

        # Limpar as peças na mão dos jogadores
        for jog in self.listaJogadores:
            for peca in jog.pecasMao:
                if peca.int is not None:
                    peca.int.destroy()
            jog.pecasMao = []

        # Reconstruir as peças na mão dos jogadores
        for peca, peca_info in jogador1:
            self.listaJogadores[0].pecasMao.append(peca)
            if peca_info is not None:
                peca.int = InterfacePeca(
                    master=suporte.canvas,
                    numero=peca.valor,
                    cor=peca.cor,
                    linha=peca_info['linha'],
                    coluna=peca_info['coluna'],
                    parent=suporte,
                    interface=interface
                )
                suporte.pecas.append(peca.int)
                peca.int.start_x = peca_info['coluna']-15
                peca.int.start_y = peca_info['linha']-15

        for peca, peca_info in jogador2:
            self.listaJogadores[1].pecasMao.append(peca)
            
        for linha_info in mesa_info:
            for info, linha, coluna in linha_info:
                peca = info[0]
                peca_info = info[1]
                self.mesa.pecas_dispostas[linha][coluna] = peca
                peca.int = InterfacePeca(
                    master=inter_mesa.canvas,
                    numero=peca.valor,
                    cor=peca.cor,
                    linha=peca_info['linha'],
                    coluna=peca_info['coluna'],
                    parent=inter_mesa,
                    interface=interface
                )
                inter_mesa.pecas.append(peca.int)
                peca.int.start_x = peca_info['coluna']
                peca.int.start_y = peca_info['linha']


    def abandonar_partida(self):
        messagebox.showinfo(message="O jogador adversario desistiu da partida.")
        self.turnoAtual = False


    def finalizar_partida(self):
        message = "O jogo acabou, o jogador: "
        message += self.receber_nome_vencedor()
        message += "venceu!"
        messagebox.showinfo(message="")
        self.turnoAtual = False


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
            peca, local = jogada["peca"], jogada["local"]
            x, y = jogada["x"], jogada["y"]
            
            print("colocar peca")
            self.listaJogadores[1].colocar_peca(peca, local, x, y)


        elif jogada["tipo"] == "pecas_distribuidas":
            self.pecas_distribuidas(jogada["pecas"])
            self.bancoDePecas.efetuar_distribuicao_pecas()


        elif jogada["tipo"] == "vez_passada":
            self.inverter_turno()
            self.receber_estado_elementos()
            self.cronometro.iniciar_cronometro()


        elif jogada["tipo"] == "peca_comprada":
            self.reconstruir_estado()
            self.listaJogadores[1].pegar_peca()
            self.inverter_turno()
            self.cronometro.iniciar_cronometro()


        self.interface_jogador.interface.atualizar_elementos()


    def validar_jogada(self) -> bool:
        return self.mesa.validar_mesa()


    def inverter_turno(self):
        for jogador in self.listaJogadores:
            jogador.atualizar_turno()

        self.turnoAtual = not self.turnoAtual



    def inicializar_jogo(self, players):
        for i in range(len(self.listaJogadores)):
            self.listaJogadores[i].inicializar(players[i][0], players[i][2])
            self.interface_jogador.interface.jogadores[i].label.config(text=players[i][0])

        if players[0][2] == "1":
            self.listaJogadores[0].atualizar_turno()
            self.turnoAtual = True
            self.cronometro.iniciar_cronometro()
        else:
            self.listaJogadores[1].atualizar_turno()

        self.interface_jogador.interface.atualizar_elementos()


    def receber_status_partida(self):
        return self.status_partida


    def reiniciar_jogo(self):
        self.estado_anterior['jogador1'] = []
        self.estado_anterior['jogador2'] = []
        self.estado_anterior['mesa'] = []

        self.reconstruir_estado()

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
        self.bancoDePecas = BancoDePecas(self)

        self.interface_jogador.interface.atualizar_elementos()


    def efetuar_passagem_vez(self):
        valido = self.validar_jogada()
        dog = self.interface_jogador.dog_server_interface

        if valido:
            print("valido")

            dog.send_move({
                "match_status" : "fodase",
                "tipo" : "vez_passada",
                })

        else:
            self.reconstruir_estado()

            self.listaJogadores[0].comprar_peca()
            self.receber_estado_elementos()

            dog.send_move({
                "match_status" : "fodase",
                "tipo" : "peca_comprada",
                })
            self.inverter_turno()


        self.interface_jogador.interface.atualizar_elementos()


    def tempo_acabou(self):
        self.listaJogadores[0].passar_vez()


    def peca_comprada(self, peca):
        self.bancoDePecas.pecas.remove(peca)


    def pecas_distribuidas(self, string_codificada):
        pecas = []
        pecas_str = string_codificada.split(',')

        for i, peca_str in enumerate(pecas_str):
            valor, cor = peca_str.split('-')
            peca = PecaNumero(int(valor), cor)
            
            if i < 14:
                pecas.append(peca)
            elif i < 28:
                pecas.insert(i - 14, peca)

            else:
                pecas.append(peca)

        self.bancoDePecas.pecas = pecas



    def verificar_partida_encerrada(self):
        jog1 = self.listaJogadores[0].get_vencedor()
        jog2 = self.listaJogadores[1].get_vencedor()

        return jog1 or jog2
