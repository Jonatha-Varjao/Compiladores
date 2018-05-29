# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('/home/jonatha/Documentos/GitClones/Compiladores/')
#import uuid
#from typing import *
from afnd.automata import AFNDmV

'''
    classe de conversao de afnd-e para afd pelo metodo de construção de subconjutos
    recebe um afnd calcula os fechos e retorna um afd
'''
class AFD(AFNDmV):
    # herdando o construtor do pai
    def __init__(self, afnd):
        # copiando o alfabeto do afnd, removendo transicao vazia
        # como o ε é sempre o ultimo alfabeto, só copiar a lista 0 ~ -1
        self.alfabeto = afnd.alfabeto[:-1]
        self.fecho_E = []
        
    # vou renomear no html
    def rename_state(self, estados: []) -> []:
        pass
    
    def gerar_AFD(self, afnd: object, fecho_E: [int], matrizTransicao: dict ) -> object:
        '''
            Recebe o primeiro conjunto de estados e calcula os outros    
        '''
        afd = AFD(afnd)
        estados = []
        estados.append(fecho_E[0])
        new_state = []
        fechos = []
        transicoes = []
        afd_Transicoes = {}
        # print(estados)
        # print('Estado final', afnd.estado_final)
        # print('Alfabeto:', afnd.alfabeto)
        
        # percorre os estados iniciais do fecho_E[0]
        for itens in estados:
            for j in afd.alfabeto:
                for i in itens:
                    # print('Estado[i]:',i,'Simbolo:',j)
                    # print('Transicao: ',matrizTransicao.get((i,j)))
                    # pego os estados pra dps calcular seus fechos
                    if matrizTransicao.get((i,j)) != None:
                        #new_state.append(fecho_E[matrizTransicao.get((i,j))])
                        fechos.append(matrizTransicao.get((i,j)))
                # apos o termino dos estados calcula-se seus fechos
                # print(fechos)
                for i in fechos:
                    print(i)
                    transicoes += fecho_E[i]
                new_state += (list(set(transicoes)))
                # print('new_state',new_state)
                # se o new_state for vazia estado representa erro -> '$' = ERRO
                if not new_state:
                    new_state = ['$']
                    # print('Novo Estado Vazio',new_state)
                    # adiciona o erro na lista de estados
                    if new_state not in estados:
                        # print('novo estado ta na lista de estados')
                        estados.append(['$'])
                    # se o estado final estiver indo pra o estado de erro, adicionar nas transicoes
                    if afnd.estado_final in itens:
                        # print("Final -> adiciona index 'final' na tupla do afd")
                        afd_Transicoes[ (tuple(itens), j,'final') ] = new_state.copy()     
                    else:
                        afd_Transicoes[ (tuple(itens), j) ] = new_state.copy()
                # novo estado != vazio e nao ta lista de estados
                elif new_state not in estados:
                    # estado final contem no novo estado
                    if afnd.estado_final in itens:
                        afd_Transicoes[ (tuple(itens), j,'final') ] = new_state.copy()     
                    else:
                        afd_Transicoes[ (tuple(itens), j) ] = new_state.copy()
                    estados.append(new_state.copy())  
                # estado na lista de estados
                else:
                    if afnd.estado_final in itens:
                        afd_Transicoes[ (tuple(itens), j,'final') ] = new_state.copy()     
                    else:
                        afd_Transicoes[ (tuple(itens), j) ] = new_state.copy()
                # limpando os vetores
                new_state.clear()
                transicoes.clear()
                fechos.clear()
        # atribuições do objeto que representa o afd
        afd.matrizTransicao = afd_Transicoes
        afd.fecho_E = fecho_E
        print(estados)
        print(afd.matrizTransicao)
        #print(afd.matrizTransicao)
        #print(afd.fecho_E)
        
        return afd
            # adicionar os conjuntos novos 
    
    def minimize_afd(self, automata: object) -> object:
        '''
            Minimzação do afd utilizando a tabela de estados finais
        '''
        pass

    def calcular_fechoE(self, automato: object) -> []:
        '''
            Recebe as transicoes do automato e calcula os fechos de cada estado
            TODO: tentar fazer DP, passando lista de estados já visitados e calculados
        '''
        for keys in automato.matrizTransicao:
            self.fecho_E.append(self.fechoE(automato.matrizTransicao, keys[0]))
        
        # removendo redundancia
        for i in range(len(self.fecho_E)):
            self.fecho_E[i] = list(set(self.fecho_E[i]))
        
        # removendo as tuplas dentros dos fechos
        for i in range(len(self.fecho_E)):
            for j in (self.fecho_E[i]):
                if type(j) is tuple:
                    self.fecho_E[i].remove(j)

        return self.fecho_E
    
    def fechoE(self, transicoes: dict, estado_atual: int) -> []:
        fecho_E = []
        fecho_E.append(estado_atual)
        #print("estado atual: ", estado_atual)
        if (estado_atual,'ε') in transicoes.keys():
            # lista de estados alcançados pelo fecho-ε
            try:
                for i in transicoes.get((estado_atual,'ε')):
                    if not (i in self.fecho_E): 
                        fecho_E += self.fechoE(transicoes, i)
            # só um estado alcançável pelo fecho-ε
            except:
                fecho_E += self.fechoE(transicoes, transicoes.get((estado_atual,'ε')))

        return fecho_E

if __name__ == '__main__':
    
    automato = AFNDmV()
    automato = automato.gerar_AFND(automato.validacao_input(sys.argv[1]))
    
    print("afnd alfabeto", automato.alfabeto)
    afd = AFD(automato)
    print("afd alfabeto", afd.alfabeto)
    
    afd.fecho_E = afd.calcular_fechoE(automato)
    afd = afd.gerar_AFD(automato, afd.fecho_E, automato.matrizTransicao)
    '''
        Futura funcao pra transformar em uma tabela html
    '''
    print("afnd alfabeto",automato.alfabeto)
    for keys in afd.matrizTransicao.keys():
        print(keys[0])
        for simbolos in afd.alfabeto:
            pass

        # for simbolos in afd.alfabeto:
        #     # estado inicial
        #     if i == 0:
        #         print( '->q'+str(i),afd.matrizTransicao.get((i,simbolos)) )    
        #     # estado final
        #     elif i == len(afd.matrizTransicao.keys())-1:
        #         print( '*q'+str(i),afd.matrizTransicao.get((i,simbolos)) )    
        #     else:
        #         print( 'q'+str(i) ,afd.matrizTransicao.get((i,simbolos)) )

