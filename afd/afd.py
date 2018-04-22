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
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.fecho_E = []
        self.estados_finais = []
    
    def rename_state(self, estados: []) -> []:
        pass

    
    def afd(self, afnd: object, fecho_E: [int], matrizTransicao: dict ) -> object:
        '''
            Recebe o primeiro conjunto de estados e calcula os outros    
        '''
        estados = []
        estados.append(fecho_E[0])
        new_state = []
        afd = {}
        print(estados)
        print('Estado final', afnd.estado_final)
        print('Alfabeto:', afnd.alfabeto)
        # percorre os estados iniciais do fecho_E[0]
        for itens in estados:
            print("Estados", estados)
            for j in afnd.alfabeto:
                print(afd)
                for i in itens:
                    print('Estado: ', itens)
                    print('Estado[i]:',i,'Simbolo:',j)
                    print(matrizTransicao.get((i,j)))
                    if matrizTransicao.get((i,j)) != None:
                        new_state.append(fecho_E[matrizTransicao.get((i,j))])
                        estados += new_state.copy()
                        print(estados)
                if not new_state:
                    new_state = ['$']
                    print('Novo Estado Vazio',new_state)
                    if new_state in estados:
                        print('novo estado ta na lista de estados')
                    else:
                        estados.append(['$'])
                        print(new_state,estados)
                elif new_state not in estados:
                    if afnd.estado_final in itens:
                        afd[ (tuple(itens), j,'final') ] = new_state[0]       
                    else:
                        afd[ (tuple(itens), j) ] = new_state[0]       
                    new_state.clear()
                print('new state limpo',new_state)
            break

        print(estados)
        print(afd)
            # adicionar os conjuntos novos 
    
    
    def minimize_afd(self, automata: object) -> object:
        '''
            Minimzação do afd utilizando a tabela de estados finais
        '''
        pass

    def calcular_fechoE(self, automato: object) -> []:
        '''
            Recebe as transicoes do automato e calcula os fechos de cada estado
        '''
        print(automato.alfabeto)
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

        print(self.fecho_E)
        
        return self.fecho_E
    
    def fechoE(self, transicoes: dict, estado_atual: int) -> []:
        fecho_E = []
        fecho_E.append(estado_atual)
        #print("estado atual: ", estado_atual)
        if (estado_atual,'&') in transicoes.keys():
            # lista de estados alcançados pelo fecho-&
            try:
                for i in transicoes.get((estado_atual,'&')):
                    if not (i in self.fecho_E): 
                        fecho_E += self.fechoE(transicoes, i)
            # só um estado alcançável pelo fecho-&
            except:
                fecho_E += self.fechoE(transicoes, transicoes.get((estado_atual,'&')))

        return fecho_E

if __name__ == '__main__':
    afd = AFD()
    automato = AFNDmV()
    #automato finito nao deterministico com transicoes/alfabeto/estados
    automato = automato.gerar_AFND(automato.validacao_input(sys.argv[1]))
    #representacao do fechos epslon do afnd-e
    afd.calcular_fechoE(automato)
    afd.afd(automato, afd.fecho_E, automato.matrizTransicao)