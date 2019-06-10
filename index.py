from flask import Flask, render_template, request, url_for, redirect, session
from model import usuarioModel, enderecoModel, torreModel, importacaoModel
from geopy.geocoders import GoogleV3
from math import radians, sin, cos, asin, sqrt, atan, degrees
from werkzeug.utils import secure_filename
import os
import csv, sys


ALLOWED_EXTENSIONS = set(['csv'])


app = Flask(__name__)
app.secret_key = os.urandom(24)

## ====================================
## Página inicial para login do usuário
## ====================================

@app.route('/')
def index():
    return render_template('login.html')
    






## =============================
## Render do cadastro do usuário
## =============================

@app.route('/cadastro')
def paginaCadastroUsuario():
    return render_template('cadastro.html')











# NA VERDADE ISSO FAZ PARTE DO CONTROLLER DO USUARIO
@app.route('/cadastro', methods=['POST'])
def controllerCadastroUsuario():

    ## ==================================================
    ## Recupera dados do formulário 
    ## ==================================================

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    cpf = request.form.get('cpf')
    telefone = request.form.get('telefone')
    tipo = request.form.get('tipo')
    rg = request.form.get('rg')

    ## =====================
    ## Endereço do usuário
    ## =====================

    cep = request.form.get('cep')
    bairro = request.form.get('bairro')
    cidade = request.form.get('cidade')
    uf = request.form.get('uf')

    usuarioEndereco = enderecoModel.Endereco(cep, bairro, cidade, uf)

    # ## =================
    # ## Cria novo usuário
    # ## =================

    NovoUsuario = usuarioModel.Usuario(nome, email, senha, cpf, rg, telefone, tipo, '1', usuarioEndereco)

    return NovoUsuario.validaDadosUsuario(NovoUsuario)




## =======================
## REALIZA LOGIN 
## =======================


@app.route('/login', methods=['POST'])
def loginUsuario():

    #DADOS PARA O LOGIN

    email = request.form.get('email')
    senha = request.form.get('senha')

    userLogin = usuarioModel.Usuario() 
    userLogin.criaUsuarioLogin(email, senha)

    usuario = userLogin.consultaUsuario(userLogin)

    session['tipoUsuario'] = usuario[0][6]

    if(len(usuario) > 0):
        return render_template('menu.html', tu = session['tipoUsuario'])
    else:
         return redirect('/')




## ================
## Página pós login 
## ================

@app.route('/home')
def homeLogin():
    return render_template('home.html')







## ======================
## Retorna torres da base 
## ======================

@app.route('/consultaTorresSites')
def consultaTorresSites():
    torres = torreModel.Torre()
    return render_template('consultaTorresSites.html', torres = torres.retornaTorres())







## ==============================
## Retorna todos usuários da base
##===============================

@app.route('/consultaUsuarios')
def consultaUsuarios():
    U = usuarioModel.Usuario()
    return render_template('consultaUsuarios.html', usuarios = U.consultaUsuarios())



## ============================
## Tela de pesquisa de endereço 
## ============================

@app.route('/consultaEndereco')
def consultaEndereco():

    end = enderecoModel.Endereco()
    end = end.retornaEnderecos()
    
    return render_template('consultaEndereco.html', logs = end)




## ===================
## Funções necessárias
## ===================


def areaInside(a, b, c, d):
    # Formula de Haversine
    
    # Constante que definirá o raio da terra em km
    r = 6371

    # Converte coordenadas de graus para radianos
    lat1, lon1, lat2, lon2 = map(radians, [ float(a), float(b), float(c), float(d) ] )

    # Formula de Haversine
    dlat = lat2 - lat1 
    dlon = lon2 - lon1
    hav = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    distancia = 2 * r * asin( sqrt(hav) )

    if distancia <= 1.5:
        return True
    else:
        return False




def azi(a, b, c, d):
    # Converte coordenadas de graus para radianos
    lat1, lon1, lat2, lon2 = map(radians, [ float(a), float(b), float(c), float(d) ] )

    # Formula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    azimute = atan(dlat/dlon)
    return degrees(azimute)








@app.route('/consultaEndereco', methods=['POST'])
def retornaLocalizacao():

    # Recebe a informação do formulário de pesquisa
    geolocator = GoogleV3(api_key='AIzaSyDLxvmCIqDmidp84dgKwXemApra3XtUhUE')
    location = geolocator.geocode(str(request.form.get('enderecoPesquisa')))
    
    # Recebe as torres 
    tower = torreModel.Torre().retornaTorresPesquisaEnd()

    #Recebe antenas
    antenas = torreModel.Torre().retornaAntenasPesquisaEnd()

    saida = {"antena": "", "retorno": 0}
    
    for j, i in enumerate(tower):   
        if areaInside(location.latitude, location.longitude, i[0], i[1]) == True:
            if j == 0:
                for k in antenas[0:3]:
                    azimute = azi(location.latitude, location.longitude, i[0], i[1])
                    if float(azimute)>=k[1]-32.5 and float(azimute)<=k[1]+32.5:
                        saida["antena"] = k[0]
                        saida["retorno"] = 1
                        break
                    else:
                        saida["retorno"] = 0  
                      
            if j == 1:
                for k in antenas[3:6]:
                    azimute = azi(location.latitude, location.longitude, i[0], i[1])
                    if float(azimute)>=k[1]-32.5 and float(azimute)<=k[1]+32.5:
                        saida["antena"] = k[0]
                        saida["retorno"] = 1
                        break
                    else:
                        saida["retorno"] = 0  
                    
            if j == 2:
                for k in antenas[6:9]:
                    azimute = azi(location.latitude, location.longitude, i[0], i[1])
                    if float(azimute)>=k[1]-32.5 and float(azimute)<=k[1]+32.5:
                        saida["antena"] = k[0]
                        saida["retorno"] = 1
                        break
                    else:
                        saida["retorno"] = 0  
                    
            if j==3:
                for k in antenas[9:12]:
                    azimute = azi(location.latitude, location.longitude, i[0], i[1])
                    if float(azimute)>=k[1]-32.5 and float(azimute)<=k[1]+32.5:
                        saida["antena"] = k[0]
                        saida["retorno"] = 1
                        break
                    else:
                        saida["retorno"] = 0 
          


    ## ====================================
    ## Registra LOG do Endereço consultado
    ## ====================================

    if(torreModel.Torre().registraLogPesquisa(str(location), str(saida["retorno"]))):
        return redirect(url_for('consultaEndereco'))
    else:
        return "Erro no registro de log"
    


## =========================
## Consulta Endereço em Lote
## =========================

@app.route('/consultaEnderecoEmLote')
def consultaEnderecoEmLote():

    Logs = importacaoModel.Importacao.retornaImportacoes(None)

    return render_template("consultaEnderecoEmLote.html", logs = Logs)

@app.route('/consultaEnderecoEmLote', methods=['POST'])
def importaEnderecoEmLote():

    #API do Google 
    geolocator = GoogleV3(api_key='AIzaSyDLxvmCIqDmidp84dgKwXemApra3XtUhUE')

    # Chama o arquivo e retorna o conteudo 
    arquivo = request.files['arqImportacao']
    conteudo = arquivo.readlines()

    saida = {"antena": "", "retorno": 0}

    # Registra o log de importacao 
    importacaoModel.Importacao.registraImportacao(None, arquivo.filename)

 


    # Recebe as torres 
    tower = torreModel.Torre().retornaTorresPesquisaEnd()

    #Recebe antenas
    antenas = torreModel.Torre().retornaAntenasPesquisaEnd()

    #Para cada linha será feita a pesquisa do CEP formatado
    for linha in conteudo:
        cep = str(linha)[2:10] + " "

         # Recebe o cep vindo de conteudo
        location = geolocator.geocode(cep)
        

        for j, i in enumerate(tower):   
            if areaInside(location.latitude, location.longitude, i[0], i[1]) == True:
                if j == 0:
                    for k in antenas[0:3]:
                        azimute = azi(location.latitude, location.longitude, i[0], i[1])
                        if float(azimute)>=k[1]-32.5 and float(azimute)<=k[1]+32.5:
                            saida["antena"] = k[0]
                            saida["retorno"] = 1
                            break
                        else:
                            saida["retorno"] = 0  
                      
                if j == 1:
                    for k in antenas[3:6]:
                        azimute = azi(location.latitude, location.longitude, i[0], i[1])
                        if float(azimute)>=k[1]-32.5 and float(azimute)<=k[1]+32.5:
                            saida["antena"] = k[0]
                            saida["retorno"] = 1
                            break
                        else:
                            saida["retorno"] = 0  
                        
                if j == 2:
                    for k in antenas[6:9]:
                        azimute = azi(location.latitude, location.longitude, i[0], i[1])
                        if float(azimute)>=k[1]-32.5 and float(azimute)<=k[1]+32.5:
                            saida["antena"] = k[0]
                            saida["retorno"] = 1
                            break
                        else:
                            saida["retorno"] = 0  
                        
                if j==3:
                    for k in antenas[9:12]:
                        azimute = azi(location.latitude, location.longitude, i[0], i[1])
                        if float(azimute)>=k[1]-32.5 and float(azimute)<=k[1]+32.5:
                            saida["antena"] = k[0]
                            saida["retorno"] = 1
                            break
                        else:
                            saida["retorno"] = 0
            
        importacaoModel.Importacao.registraLogEnderecoImportacao(None, location, saida["retorno"])

    return redirect(url_for('consultaEnderecoEmLote'))
    
## ================
## Excluir usuário
## ================
@app.route('/excluirUsuario')
def excluirUsuario():
    u = request.args.get('usuario')
    return usuarioModel.Usuario.removeUsuario(None,u)
    


## INICIA A APLICAÇÃO 
if __name__ == '__main__':
    app.run(debug=True)