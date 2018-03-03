# -*- coding: utf-8 -*-
import sys
from tkinter import *
#Class converter infixa->posfixa
class Converter:
    # construtor contendo
    # - pilha de operadores
    # - lista contendo a construção da expressão posfixa
    def __init__(self):
        self.pilhaOP = []
        self.lista = []
        self.tokens = { '+': 1, '-': 1, '*': 3, '/': 3, '.': 3, '(':0, ')':0 }
    # TODO : o Alias do '\' para aceitar operando/operadores como operando
    # Ex :   Infixa: a+\+ -> Posfixa: a\++

    def concatenacao_implicita(self, expressao):
        
        return expressao

    def infixa_posfixa(self, string):
        if list(string).count('(') - list(string).count(')') != 0:
            return -1
        for i in range(len(string)):
            # Caractere operando
            if string[i] not in self.tokens:
                self.lista.append(string[i])
                print('Posfixa: ', self.lista)
            elif string[i] == '(':
                self.pilhaOP.append(string[i])
            elif string[i] == ')':
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
                    print('PilhaPOP: ', self.pilhaOP)
                else:
                    try:
                        while( self.tokens.get(self.pilhaOP[-1]) >= self.tokens.get(string[i]) ):
                            print( self.tokens.get(self.pilhaOP[-1])," > ",self.tokens.get(string[i]) )
                            print('Pilha antes do pop: ',self.pilhaOP)
                            self.lista.append(self.pilhaOP.pop())
                            print('Lista: ',self.lista)
                            print('Pilha depois do pop: ',self.pilhaOP)
                    except IndexError:
                        #self.lista.append(string[i])
                        print('Exception: ', self.lista)
                    self.pilhaOP.append(string[i])
                    print(self.pilhaOP)
        print('Pilha dps de percorer a palavra: ', self.pilhaOP)
        while( self.pilhaOP != [] ):
            print("Pilha OP nao vazia ao final da leitura")
            self.lista.append(self.pilhaOP.pop())
        return print(self.pilhaOP, self.lista) 
        #return self.lista
    
    def validacao_posfixa(self, *kwargs):
        if kwargs.__contains__(-1) or not self.lista :
            sys.exit("Expressao invalida")
        else:
            print(self.lista, self.pilhaOP)
            for i in range(len(self.lista)):
                print(self.lista, self.pilhaOP)
                # simbolo operando
                if self.lista[i] not in self.tokens:
                    print("Operando", self.lista[i])
                    self.pilhaOP.append(self.lista[i])
                else :
                    if self.pilhaOP:
                        op2 = self.pilhaOP.pop()
                        if op2 in self.tokens:
                            print("operador", self.lista[i])
                            self.pilhaOP.append("&")
                        else:
                            if self.pilhaOP :
                                self.pilhaOP.append(self.pilhaOP.pop())
                            else:
                                sys.exit("Expressao invalida")
                                break
                    else:
                        sys.exit("Expressao invalida")
                        break   
            print(self.pilhaOP)
            op1 = self.pilhaOP.pop()
            if not self.pilhaOP:
                print("Expressao valida")
            print(self.lista)

if __name__ ==  "__main__":
    
    c = Converter()
    #c.infixa_posfixa(sys.argv[1])
    c.validacao_posfixa(c.infixa_posfixa(sys.argv[1]))
