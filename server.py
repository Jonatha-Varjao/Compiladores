
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, Markup, escape

'''
    Import dos trabalhos de compiladores
'''
from Compiladores.infixposfix.convert import Converter
from Compiladores.afnd.automata import AFNDmV
from Compiladores.afd.afd import AFD
from Compiladores.lexico.fistfollow import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main_page.html")

@app.route("/", methods=['POST'])
def infix_posfix_afnd_afd():
    afnd = AFNDmV()
    text = request.form['regex']
    try:
        ExpressaoPosfixa = afnd.validacao_input(text)
        automato = AFNDmV()
        automato = automato.gerar_AFND(automato.validacao_input(text))
        afd = AFD(automato)
        afd.fecho_E = afd.calcular_fechoE(automato)
        afd = afd.gerar_AFD(automato, afd.fecho_E, automato.matrizTransicao)
        strExpressao = ''.join(ExpressaoPosfixa)
        Infixa = text
        # Parsers das estruturas em HTML
        TableAFND = afnd_html_table(automato)
        TableAFD  = afd_html_table(afd.rename_state(afd))
        fecho = fecho_html(afd.fecho_E) 
        
        del text
        ExpressaoPosfixa.clear()
        return render_template("main_page.html", Infixa=Infixa ,strExpressao=strExpressao, fecho_E=fecho, tabelaAFND=TableAFND, tabelaAFD=TableAFD)
    except:
        return render_template("main_page.html", erro="Expressão Inválida")

# Funcao pra htmlzar os fechos
def fecho_html(fechos: [int]):
    fecho_html = ""
    for i in range(len(fechos)):
        # lista de estados
        fecho_html += "Fecho-ε(q"+str(i)+")  =  {q"+ str(fechos[i])
        fecho_html += "}<br>"
    return Markup(fecho_html)
    
# Funcao pra parsear o automato em uma tabela html
def afnd_html_table(afnd: object):
    # for fazendo cabeçalho da tabela
    table_html = "<table class='table table-bordered table-hover table-striped'><tr><th class='tg-yw4l'></th>"
    for alfabeto in afnd.alfabeto:
        table_html += "<th class='tg-yw4l'>"+ str(alfabeto) +"</th>"
    table_html += "</tr>"
    for i in range(len(afnd.matrizTransicao.keys())):
        table_html += "<tr>"
        if i == 0:
            table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>->q"+str(i)+"</td>"
        elif i == len(afnd.matrizTransicao.keys())-1:
            table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>*q"+str(i)+"</td>"
        else:
            table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>q"+str(i)+"</td>"   

        for simbolos in afnd.alfabeto:
            if afnd.matrizTransicao.get((i,simbolos)) == None:
                table_html += "<td class='tg-yw4l' style ='word-break:break-all;'> </td>"           
            else:
                table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>{q"+str(afnd.matrizTransicao.get((i,simbolos)))+"}</td>"   
        table_html += "</tr>"
    
    table_html += "</table>"
    
    return Markup(table_html)

# Funcao pra parsear o afd em uma tablea html
def afd_html_table(tupla: (object, [int])):
    # for fazendo cabeçalho da tabela
    print("matrizTransiacao AFD", tupla[0].matrizTransicao)
    print("estados renomeados", tupla[1])
    table_html = "<table class='table table-bordered table-hover table-striped'><tr><th class='tg-yw4l'></th>"
    for alfabeto in tupla[0].alfabeto:
        table_html += "<th class='tg-yw4l'>"+ str(alfabeto) +"</th>"
    table_html += "</tr>"
    for i in range(len(tupla[1])):
        table_html += "<tr>"    
        # testo se é final ou ñ
        if tupla[0].matrizTransicao.get((i, tupla[0].alfabeto[0], 'final')) != None:
            # final + inicial
            if i == 0 : 
                table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>->*q"+str(i)+"</td>"
            else:
                table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>*q"+str(i)+"</td>"
            # estados 
        elif i==0:
            table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>->q"+str(i)+"</td>"
        else:
            table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>q"+str(i)+"</td>"
        
        
        for j in range(len(tupla[0].alfabeto)):
            if tupla[0].matrizTransicao.get((i,tupla[0].alfabeto[j],'final')) != None:
                table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>q"+str(tupla[0].matrizTransicao.get((i,tupla[0].alfabeto[j],'final')))+"</td>"       
            else:
                table_html += "<td class='tg-yw4l'>q"+str(tupla[0].matrizTransicao.get((i,tupla[0].alfabeto[j])))+"</td>"       
        table_html += "</tr>"
    table_html += "</table>"

    return Markup(table_html)

@app.route("/sintatica/")
def ff_index():
    return render_template("firstfollow.html") 


@app.route("/sintatica/", methods=['POST'])
def ff():
    variaveis = request.form['variaveis']
    terminais = request.form['terminais']
    regras = request.form['regras']
    partida = request.form['partida']
    expressao = request.form['expressao']
    first, follow = first_follow(partida,variaveis,terminais,regras)
    tabela = tabela_sintatica(partida,variaveis,terminais,regras)
    tabela_html = tabela_html_sintatica(tabela)
    expressao_sintatica = analisador_sintatico(expressao, partida,variaveis,terminais,regras)

    return render_template("firstfollow.html", 
            variaveis=variaveis,
            terminais=terminais,
            regras=regras,
            partida=partida,
            expressao=expressao_sintatica,
            first=first,
            follow=follow,
            tabelaSintatica=tabela_html,
            ) 


def tabela_html_sintatica(tabela: object):
    table_html = "<table class='table table-bordered table-hover table-striped'><tr><th class='tg-yw4l'></th>"
    for key in tabela[list(tabela.keys())[0]]:
        table_html += "<th class='tg-yw4l'>"+ str(escape(key)) +"</th>"
    table_html += "</tr>"

    for key,value in tabela.items():
        table_html += "<tr>"
        table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>"+ str(escape(key))+"</td>"
        
        for k,v in value.items():
            if v != None:
                table_html += "<td class='tg-yw4l' style ='word-break:break-all;'>"+ str(escape(v))+"</td>"
            else:
                table_html += "<td class='tg-yw4l' style ='word-break:break-all;'></td>"
        table_html += "</tr>"
    
    table_html += "</table>"

    return Markup(table_html)