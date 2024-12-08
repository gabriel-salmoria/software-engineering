from random import shuffle
from interface.interface_peca import InterfacePeca
from logic.peca_numero import PecaNumero
from logic.peca_coringa import PecaCoringa

class BancoDePecas:
    def __init__(self, jogo):
        self.pecas = []
        self.jogo = jogo


    # dada uma instancia de peca, precisamos criar a correspondente
    # instancia de interfacePeca. perceba que as unicas instancias que devem ser
    # renderizadas sao as que pertencem ao jogador local ou mesa.
    def criar_peca_interface(self, peca, i):
        interface = self.jogo.interface_jogador.interface
        suporte = interface.suporte_jogador

        int_peca = InterfacePeca(
            master=suporte.canvas,
            parent=suporte,
            interface=interface,
            cor = peca.cor,
            numero=peca.valor,
            linha=14 + i // 10,
            coluna=9 + i % 10,
        )

        int_peca.place(
            x=suporte.rect_bounds[0]+20 + (i % 10) * 50,
            y=suporte.rect_bounds[1]+25 + (i // 10) * 50
        )

        suporte.pecas.append(int_peca)
        peca.int = int_peca



    def pegar_peca(self):
        peca = self.pecas[0]
        self.pecas.remove(peca)

        return peca



    # funcao que vai ser chamada quando o jogador realmente
    # passar a vez e der errado, precisa instanciar uma interfacePeca.
    def comprar_peca(self):
        peca = self.pecas[0]
        self.pecas.remove(peca)
        self.criar_peca_interface(peca, 49)

        return peca



    # de fato inicializa as pecas e embaralha elas. apenas feito por quem
    # iniciou a partida.
    def criar_baralho(self):
        valores = list(range(1, 14))
        cores = ['red', 'blue', 'green', 'yellow']
        coringas = list(range(1,5))

        baralho = [PecaNumero(valor, cor) for valor in valores for cor in cores for _ in range(2)]

        for i in range(4):
            for _ in range(2):
                peca = PecaCoringa(coringas[i]*-1, cores[i], coringas[i])
                baralho.append(peca)

        
        shuffle(baralho)

        self.pecas = baralho

        estado_baralho = ""
        for peca in baralho:
            if peca.valor > 0:
                estado_baralho += f"{peca.valor}_{peca.cor},"
            else:
                estado_baralho += f"{peca.valor}_{peca.cor}_{peca.tipoCoringa},"



        self.jogo.jogada_atual = {
            "match_status": "fodase",
            "tipo": "pecas_distribuidas",
            "pecas": estado_baralho
        }

        self.efetuar_distribuicao_pecas()



    # ta de acordo com os diagramas
    def efetuar_distribuicao_pecas(self):

        mao_jogador1 = []
        mao_jogador2 = []

        for i in range(10):
            peca = self.pegar_peca()
            mao_jogador1.append(peca)
            self.criar_peca_interface(peca, i)

        self.jogo.listaJogadores[0].receber_pecas(mao_jogador1)

        for i in range(10):
            mao_jogador2.append(self.pegar_peca())

        print(len(self.pecas))

        self.jogo.listaJogadores[1].receber_pecas(mao_jogador2)
        self.jogo.receber_estado_elementos()
