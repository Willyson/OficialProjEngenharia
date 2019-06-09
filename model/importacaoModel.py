import mysql.connector

def novaConexao(self):
        return mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='DB_LOCALIZA', auth_plugin='mysql_native_password')

class Importacao:

    def __init__(self, nomeArquivo = None):
        self.nomeArquivo = nomeArquivo


    def getNomeArquivo(self):
        return self.nomeArquivo

    def setNomeArquivo(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo

    #Registra a importacao 

    def registraImportacao(self, nomeArquivo):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f"INSERT INTO IMPORTACAO (NOME_ARQUIVO_IMPORTADO, DATA_IMPORTACAO) VALUES ('{nomeArquivo}', NOW())")
        conexao.commit()
        return True

    #Registra endereços do lote no log 

    def registraLogEnderecoImportacao(self, localizacao, retorno):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f"INSERT INTO LOG_CONSULTA_ENDERECO (LOCALIZACAO, RETORNO, DATA_CONSULTA, ID_IMPORTACAO) VALUES ('{localizacao}', '{retorno}', NOW(), (SELECT MAX(ID_IMPORTACAO)  FROM IMPORTACAO ORDER BY DATA_IMPORTACAO LIMIT 1))")
        conexao.commit()
        return True

    # Retorna as importações do lote 
    def retornaImportacoes(self):
        conexao = novaConexao(self)
        cursor =  conexao.cursor()
        cursor.execute(f"SELECT * FROM VW_CONSULTA_IMPORTACOES")
        logs = cursor.fetchall()
        return logs

    # Retorna endereços das importações
    
