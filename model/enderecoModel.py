'''
    DEFINIÇÃO DA CLASSE DE ENDEREÇO 

    ESTA CLASSE SERÁ UTILIZADA TANTO PARA O ENDEREÇO DO USUÁRIO COMUM E ADMINISTRADOR COMO PARA CLASSE 


'''
import mysql.connector

def novaConexao(self):
        return mysql.connector.connect(user='mercado', password='mercado', host='127.0.0.1', database='DB_LOCALIZA', auth_plugin='mysql_native_password')


class Endereco:

    def __init__(self, cep = None, bairro = None, cidade = None, uf = None):
        self.cep = cep 
        self.bairro = bairro 
        self.cidade = cidade 
        self.uf = uf 
    
    def setCep(self, cep):
        self.cep = cep 
    
    def getCep(self):
        return self.cep

    def setBairro(self, bairro):
        self.bairro = bairro
    
    def getBairro(self):
        return self.bairro

    def setCidade(self, cidade):
        self.cidade = cidade

    def getCidade(self):
        return self.cidade

    def setUf(self, uf):
        self.uf = uf

    def getUf(self):
        return self.uf 
    
       
    def retornaEnderecos(self):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM VW_CONSULTA_ENDERECO")
        logs = cursor.fetchall()
        return logs 