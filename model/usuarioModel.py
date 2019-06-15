 #Definição da classe usuário
import mysql.connector

from flask import redirect
from .enderecoModel import Endereco

def novaConexao(self):
        return mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='DB_LOCALIZA', auth_plugin='mysql_native_password')

class Usuario:

    def __init__(self, nome = None, email = None, senha = None, cpf = None, rg = None, telefone = None, tipo = None, status = None, enderecoUsuario = None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.rg = rg
        self.telefone = telefone
        self.tipo = tipo
        self.status = status
        self.enderecoUsuario = enderecoUsuario
        
    ## ============
    ## Gets e Sets
    ## ============
  
    def setNome(self, nome):
        self.nome = nome
    def getNome(self):
        return self.nome
    
    def setEmail(self, email):
        self.email = email
    def getEmail(self):
        return self.email

    def setSenha(self, senha):
        self.senha = senha
    def getSenha(self):
        return self.senha

    def setCpf(self, cpf):
        self.cpf = cpf
    def getCpf(self):
        return self.cpf

    def setRg(self, rg):
        self.rg = rg
    def getRg(self):
        return self.rg

    def setTelefone(self, telefone):
        self.telefone = telefone
    def getTelefone(self):
        return self.telefone

    def setTipo(self, tipo):
        self.tipo = tipo
    def getTipo(self):
        return self.tipo

    def setStatus(self, status):
        self.status = status
    def getStatus(self):
        return self.status

    def setEnderecoUsuario(self, enderecoUsuario):
        self.enderecoUsuario = enderecoUsuario
    def getEnderecoUsuario(self):
        return self.enderecoUsuario



    def criaUsuarioLogin(self, email, senha):
        self.email = email
        self.senha = senha
        return Usuario()

    def __repr__(self):
        return f'Usuario (nome={self.nome}; email={self.email}; senha={self.senha}; cpf={self.cpf}; rg={self.rg}; telefone={self.telefone}; tipo={self.tipo}; status={self.status};)'
    
    
    
    #VALIDAÇÃO DO NOVO USUARIO 
    def validaDadosUsuario(self, usuario):

        if(len(usuario.getNome()) == 0 or len(usuario.getEmail()) == 0):
            return "Usuário com nome ou e-mail zero"
        elif(len(usuario.senha) < 3):
            return "Senha com menos que 3 caracteres"
        else:
            return usuario.cadastraUsuario(usuario)
            
            

    #CADASTRO EFETIVO  DE USUÁRIO E ENDEREÇO DO USUÁRIO 
    def cadastraUsuario(self, novoUsuario):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f"INSERT INTO USUARIO (CPF_USUARIO, NOME_USUARIO, RG_USUARIO, EMAIL_USUARIO, SENHA_USUARIO, STATUS_USUARIO, ID_TIPO_CONTA) VALUES ('{novoUsuario.getCpf()}', '{novoUsuario.getNome()}', '{novoUsuario.getRg()}', '{novoUsuario.getEmail()}', '{novoUsuario.getSenha()}', '{novoUsuario.getStatus()}', '{novoUsuario.getTipo()}')")
        cursor.execute(f"INSERT INTO ENDERECO (CEP_ENDERECO, BAIRRO_ENDERECO, CIDADE_ENDERECO, UF_ENDERECO, ID_USUARIO) VALUES ('{novoUsuario.enderecoUsuario.getCep()}','{novoUsuario.enderecoUsuario.getBairro()}','{novoUsuario.enderecoUsuario.getCidade()}','{novoUsuario.enderecoUsuario.getUf()}',(SELECT ID_USUARIO FROM USUARIO ORDER BY 1 DESC LIMIT 1))")
        conexao.commit()
        if (int(novoUsuario.getTipo()) == 1):
            return redirect('consultaUsuarios')
        else:
            return redirect('/')

    def buscaUsuario(self, id_usuario):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f'SELECT U.NOME_USUARIO, U.EMAIL_USUARIO, U.SENHA_USUARIO, U.CPF_USUARIO, U.RG_USUARIO, U.ID_TIPO_CONTA, U.STATUS_USUARIO, E.CEP_ENDERECO, E.BAIRRO_ENDERECO, E.CIDADE_ENDERECO, E.UF_ENDERECO FROM USUARIO AS U INNER JOIN ENDERECO AS E ON U.ID_USUARIO = E.ID_USUARIO WHERE U.ID_USUARIO={int(id_usuario)}')
        usu = cursor.fetchall()
        endereco = Endereco(usu[0][7], usu[0][8], usu[0][9], usu[0][10])
        return Usuario(usu[0][0], usu[0][1], usu[0][2], usu[0][3], usu[0][4],"", usu[0][5], usu[0][6], endereco)

    def alteraUsuario(self, usuarioAlterado, id_usuario):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f'UPDATE USUARIO SET CPF_USUARIO="{usuarioAlterado.getCpf()}", NOME_USUARIO="{usuarioAlterado.getNome()}", RG_USUARIO="{usuarioAlterado.getRg()}", EMAIL_USUARIO="{usuarioAlterado.getEmail()}", SENHA_USUARIO="{usuarioAlterado.getSenha()}", STATUS_USUARIO="1", ID_TIPO_CONTA={usuarioAlterado.getTipo()} WHERE ID_USUARIO={id_usuario}')
        conexao.commit()
        return redirect('consultaUsuarios')
        
    #VERIFICA SE O USUÁRIO ESTÁ CADASTRADO NO SISTEMA 
    def consultaUsuario(self, usuarioLogin):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f"SELECT * FROM VW_SELECIONA_USUARIO WHERE EMAIL_USUARIO = '{usuarioLogin.email}' AND SENHA_USUARIO = '{usuarioLogin.senha}'")
        user = cursor.fetchall()
        return user
        

    # ================================================
    # Retorna todos os usuários cadastrados no sistema
    # ================================================

    def consultaUsuarios(self):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM VW_SELECIONA_USUARIO")
        users = cursor.fetchall()
        return users 


   # ===============
   # Remove usuário
   # ===============

    def removeUsuario(self, idUsuario):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f"DELETE FROM ENDERECO WHERE ID_USUARIO = {idUsuario}")
        cursor.execute(f"DELETE FROM USUARIO WHERE ID_USUARIO = {idUsuario}")
        conexao.commit()
        return redirect('consultaUsuarios')