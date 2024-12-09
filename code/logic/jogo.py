from logic.banco_de_pecas import BancoDePecas
from logic.peca_coringa import PecaCoringa
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
        self.status_partida = "0"
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
        if isinstance(peca, PecaCoringa):
            valor, cor, tipo_coringa = peca.valor, peca.cor, peca.tipoCoringa
            nova = PecaCoringa(valor, cor, tipo_coringa)
        else:
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
        self.status_partida = "6"
        self.turnoAtual = False


    def finalizar_partida(self):
        message = "O jogo acabou, o jogador: "
        message += self.receber_nome_vencedor()
        message += "venceu!"
        messagebox.showinfo(message=message)
        self.turnoAtual = False


    def verificar_turno(self) -> bool:
        if self.turnoAtual == 1:
            return True

        return False

    def receber_nome_vencedor(self) -> str:
        for jogador in self.listaJogadores:
            if jogador.get_vencedor():
                return jogador.nome

        return ""

    def reiniciar_elementos(self):
        estado_jogo = {}

        estado_jogo['jogador1'] = [] 
        estado_jogo['jogador2'] = []
        estado_jogo['mesa'] = []

        self.estado_anterior = estado_jogo
        self.bancoDePecas = BancoDePecas(self)
        self.reconstruir_estado()
        self.bancoDePecas.criar_baralho()
        self.receber_estado_elementos()


    def identificar_jogada(self, jogada):
        if jogada["tipo"] == "peca_movida":
            peca, local = jogada["peca"], jogada["local"]
            x, y = jogada["x"], jogada["y"]
            
            self.listaJogadores[1].colocar_peca(peca, local, x, y)


        elif jogada["tipo"] == "pecas_distribuidas":
            self.pecas_distribuidas(jogada["pecas"])
            self.bancoDePecas.efetuar_distribuicao_pecas()


        elif jogada["tipo"] == "vez_passada":
            vencedor = self.verificar_partida_encerrada()

            if vencedor:
                self.finalizar_partida()

            else:
                self.receber_estado_elementos()
                self.inverter_turno()
                self.cronometro.iniciar_cronometro()


        elif jogada["tipo"] == "peca_comprada":
            self.reconstruir_estado()
            self.listaJogadores[1].pegar_peca()
            self.inverter_turno()
            self.cronometro.iniciar_cronometro()

        elif jogada["tipo"] == "partida_reiniciada":
            self.turnoAtual = False
            self.listaJogadores[1].seu_turno = True
            self.reiniciar_elementos()


        self.interface_jogador.interface.atualizar_elementos()


    def validar_jogada(self) -> bool:
        return self.mesa.validar_mesa()


    def inverter_turno(self):
        for jogador in self.listaJogadores:
            jogador.atualizar_turno()

        self.turnoAtual = not self.turnoAtual



    def inicializar_jogo(self, players):
        self.status_partida = "3"
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


    def passar_vez(self):
        if not self.turnoAtual:
            return

        valido = self.validar_jogada()
        dog = self.interface_jogador.dogActor

        if valido:
            vencedor = self.verificar_partida_encerrada()

            if vencedor:
                messagebox.showinfo(message="Parabéns, você venceu!")
                self.turnoAtual = False

            dog.send_move({
                "match_status" : self.status_partida,
                "tipo" : "vez_passada",
                })

        else:
            self.reconstruir_estado()

            self.listaJogadores[0].comprar_peca()
            self.receber_estado_elementos()

            dog.send_move({
                "match_status" : self.status_partida,
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
            info = peca_str.split('_')

            if len(info) == 2:
                peca = PecaNumero(int(info[0]), info[1])

            elif len(info) == 3:
                peca = PecaCoringa(int(info[0]), info[1], int(info[2]))

            else:
                continue
            
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
