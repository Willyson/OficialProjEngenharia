 #Definição da classe usuário
import mysql.connector

from flask import redirect

def novaConexao(self):
        return mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='DB_LOCALIZA', auth_plugin='mysql_native_password')

class Usuario:

    def __init__(self, nome, email, senha, cpf, rg, telefone, tipo, status, enderecoUsuario):

        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.rg = rg
        self.telefone = telefone
        self.tipo = tipo
        self.status = status
        self.enderecoUsuario = enderecoUsuario

    def __repr__(self):
        return f'Usuario (nome={self.nome}; email={self.email}; senha={self.senha}; cpf={self.cpf}; rg={self.rg}; telefone={self.telefone}; tipo={self.tipo}; status={self.status};)'
    
    
    
    #VALIDAÇÃO DO NOVO USUARIO 
    def validaDadosUsuario(self, usuario):

        if(len(usuario.nome) == 0 or len(usuario.email) == 0):
            return "Usuário com nome ou e-mail zero"
        elif(len(usuario.senha) < 3):
            return "Senha com menos que 3 caracteres"
        else:
            return usuario.cadastraUsuario(usuario)

    #CADASTRO EFETIVO  DE USUÁRIO E ENDEREÇO DO USUÁRIO 
    def cadastraUsuario(self, novoUsuario):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f"INSERT INTO USUARIO (CPF_USUARIO, NOME_USUARIO, RG_USUARIO, EMAIL_USUARIO, SENHA_USUARIO, STATUS_USUARIO, ID_TIPO_CONTA) VALUES ('{novoUsuario.cpf}', '{novoUsuario.nome}', '{novoUsuario.rg}', '{novoUsuario.email}', '{novoUsuario.senha}', '{novoUsuario.status}', '{novoUsuario.tipo}')")
        cursor.execute(f"INSERT INTO ENDERECO (CEP_ENDERECO, BAIRRO_ENDERECO, CIDADE_ENDERECO, UF_ENDERECO, ID_USUARIO) VALUES ('{novoUsuario.enderecoUsuario.cep}','{novoUsuario.enderecoUsuario.bairro}','{novoUsuario.enderecoUsuario.cidade}','{novoUsuario.enderecoUsuario.uf}',(SELECT ID_USUARIO FROM USUARIO ORDER BY 1 DESC LIMIT 1))")
        conexao.commit()
        return redirect('/')

        
    #VERIFICA SE O USUÁRIO ESTÁ CADASTRADO NO SISTEMA 
    def consultaUsuario(self, email, senha):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f"SELECT * FROM VW_SELECIONA_USUARIO WHERE EMAIL_USUARIO = '{email}' AND SENHA_USUARIO = '{senha}'")
        user = cursor.fetchall()
        return user
        
