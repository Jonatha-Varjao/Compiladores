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
        self.tokens = { '+': 1, '-': 1, '*': 4, '/': 3, '.': 3, '(':0, ')':0 }
    # TODO : o Alias do '\' para aceitar operando/operadores como operando
    # Ex :   Infixa: a+\+ -> Posfixa: a\++
    # TODO : Aceitar a concatenação explicita no input  

    def isOperando(self, palavra):
        # melhorar isso aqui
        if palavra != '+' and palavra != '-' and palavra !=  '/' and palavra  != '(' and palavra != ')' and palavra != '*' and palavra != '.' :
            return True
        else:
            return False

    def remove_whitespace(self, string):
        return string.replace(" ","")
    
    def concatenacao_implicita(self, string):
        if list(string).count('(') - list(string).count(')') != 0:
            sys.exit("Expressao invalida")
        lista = []
        for i in range(len(string)):
            if not lista:
                lista.append(string[i])
            # Operando + Operando -> Concatenacao Implicida
            elif self.isOperando(string[i]) and self.isOperando(lista[-1]):
                lista.append(".")
                lista.append(string[i])
            # Fecha parenteses + Operando
            elif self.isOperando(string[i]) and lista[-1] == ')':
                lista.append(".")
                lista.append(string[i])
            # )( ->  ).(
            elif string[i] == '(' and lista[-1] == ')':
                lista.append(".")
                lista.append(string[i])
            # Operando + (
            elif self.isOperando(lista[-1]) and string[i] == '(':
                lista.append(".")
                lista.append(string[i])
            # Operando + * ->   
            elif self.isOperando(string[i]) and lista[-1] == '*' :
                lista.append(".")
                lista.append(string[i])
            # Operador -> Adiciono na lista
            elif not self.isOperando(string[i]):
                lista.append(string[i])
                print(lista)
            # Operador + Operando -> Adiciono o Operando na lista 
            elif self.isOperando(string[i]) and not self.isOperando(lista[-1]):
                lista.append(string[i])
        
        print("Concatenacao Implicita", lista)
        return lista

    def infixa_posfixa(self, string):
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
                            sys.exit("Expressao invalidA ")
                    else:
                        sys.exit("Expressao invalida")
            
            print(self.lista, self.pilhaOP)
            op1 = self.pilhaOP.pop()
            if not self.pilhaOP:
                print("Expressao valida")
            return self.lista

    def validacao_input(self, expressao):
        return self.validacao_posfixa(self.infixa_posfixa(self.concatenacao_implicita(self.remove_whitespace(expressao))))
        

if __name__ ==  "__main__":
    
    c = Converter()
    #c.concatenacao_implicita(sys.argv[1])
    #c.validacao_posfixa(c.infixa_posfixa(sys.argv[1]))
    print(c.validacao_input(sys.argv[1]))