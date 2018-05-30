
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, Markup

'''
    Import dos trabalhos de compiladores
'''
from Compiladores.infixposfix.convert import Converter
from Compiladores.afnd.automata import AFNDmV
from Compiladores.afd.afd import AFD

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main_page.html")

@app.route("/", methods=['POST'])
def teste_table_form():
    # pegar o afnd
    # pegar o afd
    # gerar as tabelas dos 2
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
        
        # Parsers das estruturas em HTML
        TableAFND = afnd_html_table(automato)
        TableAFD  = afd_html_table(afd.rename_state(afd))
        fecho = fecho_html(afd.fecho_E) 
        
        del text
        ExpressaoPosfixa.clear()
        return render_template("main_page.html", strExpressao=strExpressao, fecho_E=fecho, tabelaAFND=TableAFND, tabelaAFD=TableAFD)
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
    table_html = "<table class='table table-striped table-bordered dataTable' cellspacing=0 cellpadding=5 border=1 ><tr><th class='tg-yw4l'></th>"
    for alfabeto in afnd.alfabeto:
        table_html += "<th class='tg-yw4l'>"+ str(alfabeto) +"</th>"
    table_html += "</tr>"
    for i in range(len(afnd.matrizTransicao.keys())):
        table_html += "<tr>"
        if i == 0:
            table_html += "<td class='tg-yw4l'>->q"+str(i)+"</td>"
        elif i == len(afnd.matrizTransicao.keys())-1:
            table_html += "<td class='tg-yw4l'>*q"+str(i)+"</td>"
        else:
            table_html += "<td class='tg-yw4l'>q"+str(i)+"</td>"   

        for simbolos in afnd.alfabeto:
            if afnd.matrizTransicao.get((i,simbolos)) == None:
                table_html += "<td class='tg-yw4l'> </td>"           
            else:
                table_html += "<td class='tg-yw4l'>{q"+str(afnd.matrizTransicao.get((i,simbolos)))+"}</td>"   
        table_html += "</tr>"
    return Markup(table_html)

# Funcao pra parsear o afd em uma tablea html
def afd_html_table(tupla: (object, [int])):
    # for fazendo cabeçalho da tabela
    print("matrizTransiacao AFD", tupla[0].matrizTransicao)
    print("estados renomeados", tupla[1])
    table_html = "<table class='table table-striped table-bordered dataTable' cellspacing=0 cellpadding=5 border=1 ><tr><th class='tg-yw4l'></th>"
    for alfabeto in tupla[0].alfabeto:
        table_html += "<th class='tg-yw4l'>"+ str(alfabeto) +"</th>"
    table_html += "</tr>"
    for i in range(len(tupla[1])):
        table_html += "<tr>"
        # testo se é final ou ñ
        if tupla[0].matrizTransicao.get((i, tupla[0].alfabeto[0], 'final')) != None and i == 0 :
            table_html += "<td class='tg-yw4l'>->*q"+str(i)+"</td>"
        # final + inicial
        elif tupla[0].matrizTransicao.get((i, tupla[0].alfabeto[0], 'final')) != None: 
            table_html += "<td class='tg-yw4l'>*q"+str(i)+"</td>"
        # estados 
        else:
            table_html += "<td class='tg-yw4l'>q"+str(i)+"</td>"
        
        for j in range(len(tupla[0].alfabeto)):
            if tupla[0].matrizTransicao.get((i,tupla[0].alfabeto[j],'final')) != None:
                table_html += "<td class='tg-yw4l'>{q"+str(tupla[0].matrizTransicao.get((i,tupla[0].alfabeto[j],'final')))+"}</td>"       
            else:
                table_html += "<td class='tg-yw4l'>{q"+str(tupla[0].matrizTransicao.get((i,tupla[0].alfabeto[j])))+"}</td>"       
    table_html += "</tr>"

    return Markup(table_html)