# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('/home/jonatha/Documentos/GitClones/Compiladores/')
import uuid
from infixposfix.convert import Converter
import collections

class State():
    def __init__(self, state_id=None):
        def generate_id():
            return int(uuid.uuid4())

        self.id = generate_id() if state_id is None else state_id

    def get_id(self):
        return int(self.id)

    def __hash__(self):
        return self.get_id()

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __cmp__(self, other):
        if self.get_id() < other.get_id():
            return -1
        elif self.get_id() > other.get_id():
            return 1
        else:
            return 0

    def __str__(self):
        return str(self.get_id())[:5]


class AFNDmV(Converter):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.alfabeto = []
        self.qtd_estados = 0
        self.estados  = []
        self.matrizTransicao = {} # [][]
        self.estado_inicial = 0
        self.qtd_estado_final = 0
        self.estados_final = []
        self.pilhaAutomato = [AFNDmV]
    
    # base miu grau
    def base(self, simbolo: str):
        automata = AFNDmV()
        automata.alfabeto.append(simbolo)
        automata.qtd_estados = 2
        automata.estados.append(0)
        automata.estados.append(1)
        automata.matrizTransicao[(0,simbolo)] = 1
        automata.estado_inicial = 0
        automata.qtd_estado_final = 1
        automata.estados_final.append(0)
        
        return automata
    
    # uniao alfabeto miu grau
    def uniao_alfabetos(self, alfabeto1: object, alfabeto2: object)-> object:
        new_alphabet = alfabeto1.copy()
        for i in range(len(alfabeto2)):
            if not alfabeto2[i] in alfabeto1:
                new_alphabet.append(alfabeto2[i])
        return new_alphabet

    # nem to usando mas deixa queto aqui
    def funcao_transicao(self, automato: object, estado: int, simbolo: str)-> int :
        return automato.matrizTransicao.get((estado,simbolo))

    def fecho_kleene(self, automato: object)->object:
        new_automata = AFNDmV()
        new_automata.alfabeto = self.uniao_alfabetos([""], automato.alfabeto)

        new_automata.qtd_estados = automato.qtd_estados + 2
        # preenchendo os estados do novo automato 
        for i in range(len(automato.estados)):
            new_automata.estados.append(i)

        # preenchendo as transicoes do automato1 no automato novo
        for i in automato.matrizTransicao.keys():
            try:
                new_automata.matrizTransicao[ (i[0]+1, i[1] ) ] = automato.matrizTransicao.get(i) + (new_automata.qtd_estados - automato.qtd_estados) - 1
            except :
                print(i)
                b = list(automato.matrizTransicao.get(i))
                print(b)
                print("automato com lista de transicoes")
                new_list = [x+1 for x in b]
                print('transicoes ',new_list)
                new_automata.matrizTransicao[ (i[0]+1, i[1] ) ] = tuple(new_list)
                print( new_automata.matrizTransicao[ (i[0]+1, i[1] ) ] )
        
        new_automata.matrizTransicao[(0,'&')] = (1,new_automata.qtd_estados-1)
        new_automata.matrizTransicao[(automato.qtd_estados,'&')] = (new_automata.qtd_estados - automato.qtd_estados -1, new_automata.qtd_estados-1)



        new_automata.estado_inicial = 0
        new_automata.estado_final = new_automata.qtd_estados-1
        new_automata.qtd_estado_final = 1
         
        return new_automata

    # funfando
    def concatenacao(self, automato1: object, automato2: object)-> object:
        automata = AFNDmV()
        automata.alfabeto = self.uniao_alfabetos(automato1.alfabeto, automato2.alfabeto)
        automata.qtd_estados = automato1.qtd_estados + automato2.qtd_estados
       
                
        # preencher os estados
        automata.estados = automato1.estados.copy()
        for i in range(len(automato2.estados)):
            automata.estados.append( automato1.qtd_estados + automato2.estados[i] )
        print(automata.estados)
        
        # preencher as transicoes
        print(automata.matrizTransicao, automato1.matrizTransicao, automato2.matrizTransicao)
        # transicoes do automato 1
        # copiar transaçõe do automato 1
        automata.matrizTransicao = automato1.matrizTransicao.copy()
        # transicoes do automato 2
        for i in automato2.matrizTransicao.keys():
            #automata.matrizTransicao[ (i[0]+automato1.qtd_estados, i[1] ) ] = automato2.matrizTransicao.get(i) + automato1.qtd_estados
            try:
                automata.matrizTransicao[ (i[0]+automato1.qtd_estados, i[1] ) ] = automato2.matrizTransicao.get(i) + automato1.qtd_estados
            except :
                b = list(automato2.matrizTransicao.get(i))
                new_list = [x+automato1.qtd_estados for x in b]
                automata.matrizTransicao[ (i[0]+automato1.qtd_estados, i[1] ) ] = tuple(new_list)
            

        # preencher final automato 1 + '&' -> 2 
        automata.matrizTransicao[(automato1.qtd_estados-1, '&')] = automato1.qtd_estados
        print(automata.matrizTransicao)
        #

        automata.estado_inicial   = 0
        automata.estado_final     = automata.qtd_estados-1
        automata.qtd_estado_final = 1
        
        print("estado inicial:", automata.estado_inicial)
        print("estado final:", automata.estado_final)

        return automata

    # gege
    def uniao(self, automato1: object, automato2: object) -> object:
        automata = AFNDmV()
        automata.alfabeto = self.uniao_alfabetos(automato1.alfabeto, automato2.alfabeto)
        automata.qtd_estados = automato1.qtd_estados + automato2.qtd_estados + 2
        
        # preencher os etados
        for i in range(automata.qtd_estados):
            automata.estados.append(i)

        # preencher as transicoes
        automata.matrizTransicao[(0,'&')] = automato1.estado_inicial + 1, automato2.estado_inicial + automato1.qtd_estados +1 
        # transicao do automato 1
        for i in automato1.matrizTransicao.keys():
            try:
                automata.matrizTransicao[ (i[0]+1, i[1] ) ] = automato1.matrizTransicao.get(i) + 1
                print(automata.matrizTransicao)
            except TypeError :
                print(automato1.matrizTransicao.get(i))
                b = list(automato1.matrizTransicao.get(i))
                new_list = [x+1 for x in b]
                automata.matrizTransicao[ (i[0]+1, i[1] ) ] = tuple(new_list)
        print("Transicao 1", automata.matrizTransicao)
        # transicao do automato 2       
        for i in automato2.matrizTransicao.keys():
            try: 
                automata.matrizTransicao[ (i[0]+automato1.qtd_estados + 1, i[1] ) ] = automato2.matrizTransicao.get(i) + automato1.qtd_estados + 1
            except TypeError :
                b = list(automato2.matrizTransicao.get(i))
                new_list = [x+automato1.qtd_estados + 1 for x in b]
                automata.matrizTransicao[ (i[0]+automato1.qtd_estados + 1, i[1] ) ] = tuple(new_list)
        print("Transicao 2", automata.matrizTransicao)
        # chave existe automato 1
        print (automato1.qtd_estados)
        if ((automato1.qtd_estados, '&')) in automata.matrizTransicao.keys():
            automata.matrizTransicao[(automato1.qtd_estados,'&')] = automato1.matrizTransicao.get((automato1.qtd_estados, '&')), automata.qtd_estados-1
        else:
            automata.matrizTransicao[(automato1.qtd_estados,'&')] = automata.qtd_estados-1
        print("Transicao if 1", automata.matrizTransicao)
        # chave existe automato 2
        print (automato2.qtd_estados+automato1.qtd_estados)
        if (automato2.qtd_estados+automato1.qtd_estados, '&') in automata.matrizTransicao.keys():
            automata.matrizTransicao[( automato2.qtd_estado+automato1.qtd_estados,'&')] = automato2.matrizTransicao.get((automato2.qtd_estados+automato1.qtd_estados, '&')), automata.qtd_estados-1
        else:
            automata.matrizTransicao[(automato2.qtd_estados + automato1.qtd_estados,'&')] = automata.qtd_estados-1
        print("Transicao if 2", automata.matrizTransicao)

        automata.estado_inicial   = 0
        automata.estado_final     = automata.qtd_estados-1
        automata.qtd_estado_final = 1
        
        return automata

    
    def gerar_AFND(self, posfixa: str)->str:
        for i in range(len(posfixa)):
            simbolo = posfixa[i]
            #print(self.pilhaAutomato)
            # simbolo operando
            if self.isOperando(simbolo):
                print("Base")
                self.pilhaAutomato.append(self.base(simbolo))
            else :
                if self.pilhaAutomato:
                    if simbolo == '*':
                        print("Kleene")
                        self.pilhaAutomato.append( self.fecho_kleene(self.pilhaAutomato.pop()) )
                    elif self.pilhaAutomato :
                        op2 = self.pilhaAutomato.pop()
                        op1 = self.pilhaAutomato.pop()
                        if simbolo == "+":
                            print("Uniao")
                            self.pilhaAutomato.append( self.uniao(op1,op2) )
                        elif simbolo == '.':
                            print("Concatenacao")
                            self.pilhaAutomato.append( self.concatenacao(op1,op2) )
        
        afn = self.pilhaAutomato.pop()
        if not self.pilhaAutomato:
            print(afn.matrizTransicao)
        ordered_afn = collections.OrderedDict(sorted(afn.matrizTransicao.items()))
        afn.matrizTransicao = dict(ordered_afn)
        print(len(afn.matrizTransicao.keys()))
        afn.matrizTransicao.update( {(len(afn.matrizTransicao.keys()), '*'): None } )
        print(afn.matrizTransicao)
        print(type(afn.matrizTransicao))
        return afn.matrizTransicao

    def calcular_fechoE(self, transicoes: dict) -> []:
        fecho_E = []

        for keys in transicoes:
            print(keys[0])
            fecho_E.append(self.fechoE(transicoes, keys[0]))
            print(fecho_E)
        
        return fecho_E

    def fechoE(self, transicoes: dict, estado_atual: int) -> []:
        #print(transicoes)
        fecho_E = []
        fecho_E.append(estado_atual)
        
        if (estado_atual,'&') in transicoes.keys():
            try:
                for i in transicoes.get((estado_atual,'&')):
                    fecho_E += self.fechoE(transicoes, i)
            except:
                fecho_E += self.fechoE(transicoes, transicoes.get((estado_atual,'&')))
        #print(fecho_E)
        return fecho_E


    #TODO ehSimbolo(a) : int
    #TODO ehEstado(q)  : int
    #TODO ehEstadoFinal(q) : bool
    #TODO funcaoTransicao(q,a) : int[]
    #TODO funcaoTransicaoEstendida(q, w) : int[]
    #TODO renomeiaEstado(q,nome) : bool
    #TODO uneAlfabetos(alfabeto1,alfabeto2) : bool
    #TODO uneEstado(estados1,estado2) : bool
    #TODO fechoE(q) : int[]
    #TODO afd() : NULL
    #TODO minimizaAFD() : NULL


if __name__ == '__main__':
    automato        = AFNDmV()
    expression      = Converter()
    #expression.validacao_input(sys.argv[1])
    transicoes = automato.gerar_AFND(expression.validacao_input(sys.argv[1]))
    automato.calcular_fechoE(transicoes)