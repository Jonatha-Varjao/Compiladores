# -*- coding: utf-8 -*-
import os
import sys
from typing import List
#Class converter infixa->posfixa
class Converter:
    # construtor contendo
    # - pilha de operadores
    # - lista contendo a construção da expressão posfixa
    def __init__(self):
        self.pilhaOP = []
        self.lista = []
        self.tokens = { '+': 1, '*': 3, '.': 2, '(':0, ')':0 }

    def isOperando(self, palavra: str) -> str:
        # melhorar isso aqui
        # que nada...deixa assim mesmo 
        if palavra != '+' and palavra != '-' and palavra !=  '/' and palavra  != '(' and palavra != ')' and palavra != '*' and palavra != '.' :
            return True
        else:
            return False

    # pra nao bugar a concatenacao explicita
    def remove_whitespace(self, string: str) -> str:
        return str(string).replace(" ","")
    
    # Se pedi pra por |( ou |) é sacanagem.....
    def conta_barra(self, string):
        soma = 0
        for i in range(len(string)):
            if string[i] == '(':
                try :
                    if string[i-1] != '|':
                        soma = soma + 1
                except:
                    soma = soma + 1
            elif string[i] == ')':
                try :
                    if string[i-1] != '|':
                        soma = soma - 1    
                except:
                    soma = soma - 1
        if soma != 0 :
            sys.exit("Expressao invalida: '(' e ')' ")

    # miu grau
    def concatenacao_implicita(self, string: str) -> str:
        self.conta_barra(string)
        lista = []
        for i in range(len(string)):
            print("Lista: ", lista, "String: ", string[i])
            if not lista:
                lista.append(string[i])
            elif lista[-1] == '|':
                if string[i] == '|':
                    sys.exit("Expressao invalida: |+|")
                lista.append(string[i])
            elif self.isOperando(lista[-1]):
                # Operando + Operando -> Concatenacao Implicida
                if self.isOperando(string[i]): 
                    lista.append(".")
                    lista.append(string[i])
                # Operando + ( -> a.(
                elif string[i] == '(':
                    print("openrando + (")
                    lista.append(".")
                    lista.append(string[i])
                elif not self.isOperando(string[i]):
                    lista.append(string[i])
            # ) + Operando -> ) . Operando
            elif lista[-1] == ')':
                if self.isOperando(string[i]):
                    print(" ) + x")
                    lista.append(".")
                    lista.append(string[i])
                elif string[i] == '(':
                    print(" ) + (")
                    lista.append(".")
                    lista.append(string[i])
                elif not self.isOperando(string[i]):
                    lista.append(string[i])
            elif lista[-1] == '*' :
                #  * + Operando ->   *.Operando
                if self.isOperando(string[i]):
                    lista.append(".")
                    lista.append(string[i])
                # * + ( ->  *.(
                elif string[i] == '(':
                    lista.append(".")
                    lista.append(string[i])
                elif not self.isOperando(string[i]):
                    lista.append(string[i])
            # Operador + Operando -> Adiciono o Operando na lista 
            elif not self.isOperando(lista[-1]):
                try:
                    if lista[-2] == '|':
                        if string[i] == '|' or self.isOperando(string[i]):
                            lista.append(".")
                            lista.append(string[i])
                        elif string[i] == '(' :
                            lista.append(".")
                            lista.append(string[i])
                        elif string[i] == ')':
                            lista.append(string[i])
                        elif string[i] == '*':
                            lista.append(string[i])
                    else:
                        lista.append(string[i])
                except:
                    lista.append(string[i])

        
        print("Concatenacao Implicita", lista)
        return lista

    # 
    def infixa_posfixa(self, string: str) -> str:
        for i in range(len(string)):
            #print('Posfixa: ', self.lista, 'PilhaOP: ', self.pilhaOP)
            # Caractere operando
            if string[i] == '|':
                try:
                    print("opa")
                    self.lista.append(string[i]+string[i+1])
                    string[i+1] = ""
                except IndexError:
                    sys.exit("Expressao invalida: | sozinho ")
            elif string[i] not in self.tokens:
                self.lista.append(string[i])
            elif string[i] == '(' :
                self.pilhaOP.append(string[i])
            elif string[i] == ')' :
                try:
                    while(self.pilhaOP[-1] != '('):
                        self.lista.append(self.pilhaOP.pop())
                    self.pilhaOP.pop()
                except (IndexError, ValueError):
                    return -1
            # Caractere operando
            elif string[i] in self.tokens:
                if self.pilhaOP == []:
                    self.pilhaOP.append(string[i])
                else:
                    try:
                        while( self.tokens.get(self.pilhaOP[-1]) >= self.tokens.get(string[i]) ):
                            print( self.tokens.get(self.pilhaOP[-1])," > ",self.tokens.get(string[i]) )
                            #print('Pilha antes do pop: ',self.pilhaOP)
                            self.lista.append(self.pilhaOP.pop())
                            #print('Lista: ',self.lista)
                            #print('Pilha depois do pop: ',self.pilhaOP)
                    except IndexError:
                        #self.lista.append(string[i])
                        print('Exception: ', self.lista)
                    self.pilhaOP.append(string[i])
        #print('Pilha dps de percorer a palavra: ', self.pilhaOP)
        while( self.pilhaOP != [] ):
            #print("Pilha OP nao vazia ao final da leitura")
            self.lista.append(self.pilhaOP.pop())
        #print(self.lista)
        # limpando os '' da minha lista antes de jogar na validacao pos_fixa
        new_list = []
        for i in range(len(self.lista)):
            if self.lista[i] == '':
                pass
            else:
                new_list.append(self.lista[i])
        self.lista = new_list
        #print(self.lista)
        return self.lista
        
    def validacao_posfixa(self, *kwargs):
        if kwargs.__contains__(-1) or not self.lista :
            sys.exit("Expressao invalida")
        else:
            for i in range(len(self.lista)):
                print(self.lista, self.pilhaOP)
                # simbolo operando
                if self.lista[i] not in self.tokens:
                    print("Operando", self.lista[i])
                    self.pilhaOP.append(self.lista[i])
                else :
                    if self.pilhaOP:
                        self.pilhaOP.pop()
                        if self.lista[i] == '*':
                            print("operador", self.lista[i])
                            self.pilhaOP.append("&")
                        elif self.pilhaOP :
                            self.pilhaOP.pop()
                            self.pilhaOP.append("&")
                        else:
                            sys.exit("Expressao invalida")
                    else:
                        sys.exit("Expressao invalida")
            print(self.lista, self.pilhaOP)
            self.pilhaOP.pop()
            if not self.pilhaOP:
                print("Expressao valida")
            return self.lista

    def validacao_input(self, expressao):
        return self.validacao_posfixa(self.infixa_posfixa(self.concatenacao_implicita(self.remove_whitespace(expressao))))
        

if __name__ ==  "__main__":
    
    c = Converter()
    print(c.validacao_input(sys.argv[1]))