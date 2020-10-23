"""
        Problema: 3 missionarios e 3 canibais estão em uma margem do rio,
    e precisam chegar ao outro lado.
        A solução do problema consiste em atravessar todos personagens
    para a margem oposta.
        Para isso existe um barco que leva 1 ou 2 personagens por vez,
    porém, o número de missionarios nunca deve ser menor que o numero
    de canibais em qualquer uma das margens, caso contrário, os
    missionários viram lanchinho.

        Para a resolução do problema será utilizado o método de
    busca por profundidade iterativa.
    São geradas árvores de possibilidades de altura h (1 -> final),
    onde a altura final é a primeira altura que contém uma ou mais
    soluções.
        Cada árvore criada é percorrida a procura de soluções.
        Cada solução encontrada tem seu caminho armazenado em um
    arquivo com todas as soluçoes encontradas na árvore com altura mínima
    para resolver o problema.

    P.S.: espero que os missionários sejam suficientemente inteligentes
    para não virarem snacks (=
"""
import sys


class Estado:

    def __init__(
                    self, missionarios_esq, missionarios_dir,
                    canibais_esq, canibais_dir,
                    barco
                ):
        self.missionarios_esq = missionarios_esq
        self.missionarios_dir = missionarios_dir
        self.canibais_esq = canibais_esq
        self.canibais_dir = canibais_dir
        self.barco = barco
        self.pai = None
        self.filhos = []

    def __str__(self):
        return '\nmissionarios ({}, {}) \ncanibais({}, {}) \nbarco: {} '.format(
            self.missionarios_esq, self.missionarios_dir,
            self.canibais_esq, self.canibais_dir, self.barco
        )

    def valido(self):
        """
            testa a validade de um estado
        """
        # se 3 < numero_pessoas < 0, o estado é inválido
        if (((self.missionarios_esq < 0) or (self.missionarios_dir < 0) or
             (self.canibais_esq < 0) or (self.canibais_dir < 0)) or
                ((self.missionarios_esq > 3) or (self.missionarios_dir > 3) or
                 (self.canibais_esq > 3) or (self.canibais_dir > 3))):
            return False
        # se retorna ao estado inicial, o estado não é adicionado
        if self.missionarios_esq == self.canibais_esq == 3:
            return False
        # se o numero de canibais é maior que o numero de missiconarios
        # lado esquerdo
        if self.missionarios_esq > 0:
            if self.canibais_esq > self.missionarios_esq:
                return False
        # se o numero de canibais é maior que o numero de missiconarios
        # lado esquerdo
        if self.missionarios_dir > 0:
            if self.canibais_dir > self.missionarios_dir:
                return False
        # após passar os testes, estado válido
        return True

    def final(self):
        """
            analisa se o estado atual é o estado solução:
            todos os personagens atravessaram para a outra margem
        """
        return ((self.missionarios_esq == self.canibais_esq == 0) and
                (self.missionarios_dir == self.canibais_dir == 3))

    def gera_filhos(self):
        """
            gera uma lista de todos os estados válidos
            adjacentes ao estado atual
        """
        # barco para o outro lado do rio
        if self.barco == 'esq':
            novo_lado = 'dir'
        else:
            novo_lado = 'esq'
        # lista de possiveis movimentos para os estados
        possibilidades = [
            {'missionarios': 1, 'canibais': 0},
            {'missionarios': 2, 'canibais': 0},
            {'missionarios': 0, 'canibais': 1},
            {'missionarios': 0, 'canibais': 2},
            {'missionarios': 1, 'canibais': 1}
        ]
        # gera os possiveis estados adjacentes ao atual,
        # testa a validade dos estados e adiciona os válidos
        for p in possibilidades:
            # se o barco está na esquerda do rio, os personagens
            # vão para a margem direita
            if self.barco == 'esq':
                missionarios_esq = self.missionarios_esq - p['missionarios']
                missionarios_dir = self.missionarios_dir + p['missionarios']
                canibais_esq = self.canibais_esq - p['canibais']
                canibais_dir = self.canibais_dir + p['canibais']
            # caso o barco esteja na margem direita,
            # os personagens vão para a esquerda
            else:
                missionarios_esq = self.missionarios_esq + p['missionarios']
                missionarios_dir = self.missionarios_dir - p['missionarios']
                canibais_esq = self.canibais_esq + p['canibais']
                canibais_dir = self.canibais_dir - p['canibais']
            # cria o estado filho e, caso seja válido, é adicionado.
            # também analisa se o estado é a solução e marca flag
            estado = Estado(missionarios_esq, missionarios_dir, canibais_esq,
                            canibais_dir, novo_lado)
            estado.pai = self
            if estado.valido():
                # if estado.final(): estado.solucao = True
                self.filhos.append(estado)

    def gera_estados(self, altura, altura_final):
        """
            gera uma arvore de estados com altura pré-definida
            utilizando recursividade
        """
        # verifica se a altura da árvore atual já foi alcançada para
        # continuar ou não gerando galhos
        altura += 1
        if altura <= altura_final:
            # gera filhos do estado atual
            self.gera_filhos()
            # acessa filhos do estado atual para continuar gerando árvore
            # chama a mesma função para os filhos (recursividade)
            for filho in self.filhos:
                filho.gera_estados(altura, altura_final)

    def percorre_estados(self, solucao):
        """
            percorre a árvore com altura h a procura de soluções
        """
        # se encontra solução. adiciona em uma lista
        if self.final():
            solucao.append(self)
        # continua a percorrer a árvore de forma recursiva
        for filho in self.filhos:
            filho.percorre_estados(solucao)

    # noinspection PyMethodFirstArgAssignment
    def caminho(self):
        """
            extrai o caminho feito para chegar em uma solução
            buscando pelo estado pai do estado atual, e armazena
            em uma lista (final -> inicial)
        """
        # lista para armazenamento dos nós do caminho
        caminho = []
        # adiciona estado atual à lista e busca estado pai
        while self.pai is not None:
            caminho.append(self)
            self = self.pai
        # inverte a lista (inicial -> final)
        caminho.reverse()
        # caminho percorrido do estado inicial ao final
        return caminho


def print_solucoes(altura, solucoes):
    """
        formata e escreve soluções encontradas em arquivo
    """
    # abre arquivo com nome provido na execução
    nome_arquivo = sys.argv[1]
    arquivo = open(nome_arquivo, 'w')
    # numero de soluções encontradas e qual a altura mínima
    arquivo.write('{} primeiras soluções foram encontradas na altura {}\n'
                  .format(solucoes.__len__(), altura))
    # salva soluções (caminhos) em arquivo
    for solucao in solucoes:
        # enumera soluções
        arquivo.write('\n<-----------------------> \nSolução: {}\n'
                      .format(solucoes.index(solucao)))
        # descreve caminho percorrido
        for passo in solucao.caminho():
            arquivo.write('{}\n'.format(passo))
    # fecha arquivo
    arquivo.close()


def main():
    """
        cria, percorre e extrai soluções de árvores de altura h
        através da busca de profundidade iterativa
    """
    # lista de soluções encontradas com altura mínima
    solucao = []
    # altura 0 = estado inicial, então altura inicial = 1
    altura = 1
    # altura++ enquanto não encontrar soluções
    while not solucao:
        # estado inicial do problema
        estados = Estado(3, 0, 3, 0, 'esq')
        # gera árvore com altura atual
        estados.gera_estados(0, altura)
        # percorre árvore atual em busca de solucões
        estados.percorre_estados(solucao)

        # salva solucoes no arquivo
        if solucao:
            print_solucoes(altura, solucao)
        # incrementa altura
        altura += 1


if __name__ == '__main__':
    main()
