# -*- coding: utf-8 -*-
import sys
#Class converter infixa->posfixa
class Converter:
    # construtor contendo
    # - pilha de operadores
    # - lista contendo a construção da expressão posfixa
    def __init__(self):
        self.pilhaOP = []
        self.lista = []
        self.tokens = { '+': 1, '-': 1, '*': 3, '/': 3, '.': 3, '(':0, ')':0 }
    # criar funções auxiliadoras / nem precisa essa merda é python
    # isEmpty
    # peek
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
                    print("Expressao invalida")
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
        if self.pilhaOP.count('(') - self.pilhaOP.count(')') > 0:
            print('Expressao invalida')
            return -1
        while( self.pilhaOP != [] ):
            print("Pilha OP nao vazia ao final da leitura")
            self.lista.append(self.pilhaOP.pop())
        return print(self.pilhaOP, self.lista)

if __name__ ==  "__main__":
    
    c = Converter()
    c.infixa_posfixa(sys.argv[1])
    