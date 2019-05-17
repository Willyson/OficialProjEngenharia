'''
    DEFINIÇÃO DA CLASSE DE ENDEREÇO 

    ESTA CLASSE SERÁ UTILIZADA TANTO PARA O ENDEREÇO DO USUÁRIO COMUM E ADMINISTRADOR COMO PARA CLASSE 


'''
import mysql.connector

def novaConexao(self):
        return mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='DB_LOCALIZA', auth_plugin='mysql_native_password')


class Endereco:

    def __init__(self):
        pass
        
    def criaEndereco(self, cep, bairro, cidade, uf):
        self.cep = cep 
        self.bairro = bairro 
        self.cidade = cidade 
        self.uf = uf 
        return Endereco 
    
    def retornaEnderecos(self):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM VW_CONSULTA_ENDERECO")
        logs = cursor.fetchall()
        return logs 