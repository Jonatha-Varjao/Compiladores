# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('/home/jonatha/Documentos/GitClones/Compiladores/')
from typing import List
from infixposfix.convert import Converter

class Automata(Converter):
    def __init__(self, *args, **kwargs):
        self.alfabeto = List[str]
        self.estados  = List[int]
        self.matrizTransicao = []
        self.estado_inicial: int
        self.estados_final = List[int]
    

    # ehSimbolo(a) : int
    # ehEstado(q)  : int
    # ehEstadoFinal(q) : bool
    # funcaoTransicao(q,a) : int[]
    # funcaoTransicaoEstendida(q, w) : int[]
    # renomeiaEstado(q,nome) : bool
    # uneAlfabetos(alfabeto1,alfabeto2) : bool
    # uneEstado(estados1,estado2) : bool
    # fechoE(q) : int[]
    # afd() : NULL
    # minimizaAFD() : NULL


if __name__ == '__main__':
    automato = Automata()