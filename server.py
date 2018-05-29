
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


@app.route('/', methods=['POST'])
def my_form_post():
    afd = AFD()
    afnd = AFNDmV()
    text = request.form['regex']
    try:
        ExpressaoPosfixa = afnd.validacao_input(text)
        print('PreFixa: ', text)
        print('PosFixa: ', ExpressaoPosfixa)
        afnd = afnd.gerar_AFND(ExpressaoPosfixa)
        print(afnd.matrizTransicao)
        # representacao do fechos epslon do afnd-e
        strAFND_E = afnd.matrizTransicao
        afd.calcular_fechoE(afnd)
        afd = afd.afd(afnd, afd.fecho_E, afnd.matrizTransicao)
        fecho_E = afd.fecho_E
        #print(strExpressao, strAFND)
        strExpressao = ''.join(ExpressaoPosfixa)
        print(strExpressao)
        # limpando as variaveis do submit do forms ( cade o js ??)
        del text
        ExpressaoPosfixa.clear()
        # retornando a reposta do submit passando as variaveis pra plotar o html
        # ,strAFD=strAFD, fechos_E=fechos_E)
        return render_template("main_page.html", strExpressao=strExpressao, afnd=strAFND_E, fecho_E=fecho_E, afd=afd.matrizTransicao)
    except:
        # caso a expressão seja inválida
        return render_template("main_page.html", erro="Expressão Inválida")


@app.route("/teste")
def teste_table():
    return render_template("main_page.html")


@app.route("/teste", methods=['POST'])
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
        TableAFD  = afnd_html_table(afd)
        fecho = fecho_html(afd.fecho_E) 
        
        del text
        ExpressaoPosfixa.clear()
        return render_template("main_page.html", strExpressao=strExpressao, fecho_E=fecho, tabelaAFND=TableAFND, tabelaAFD=TableAFD)
    except:
        return render_template("main_page.html", erro="Expressão Inválida")

# Funcao pra htmlzar os fechos
def fecho_html(fechos):
    fecho_html = ""
    for i in range(len(fechos)):
        # lista de estados
        fecho_html += "Fecho-ε(q"+str(i)+")  =  {q"+ str(fechos[i])
        fecho_html += "}<br>"
    return Markup(fecho_html)
    
# Funcao pra parsear o automato em uma tabela html
def afnd_html_table(afnd):
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
            print( '->q'+str(i),afnd.matrizTransicao.get((i,simbolos)) )
            if afnd.matrizTransicao.get((i,simbolos)) == None:
                table_html += "<td class='tg-yw4l'> </td>"           
            else:
                table_html += "<td class='tg-yw4l'>{q"+str(afnd.matrizTransicao.get((i,simbolos)))+"}</td>"   
            
        table_html += "</tr>"
    return Markup(table_html)

# Funcao pra parsear o afd em uma tablea html
def afd_html_table(afd):
    pass