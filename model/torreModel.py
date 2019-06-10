import mysql.connector

def novaConexao(self):
        return mysql.connector.connect(user='mercado', password='mercado', host='127.0.0.1', database='DB_LOCALIZA', auth_plugin='mysql_native_password')

class Torre:

    
    
    def __init__(self):
        pass
    
    def retornaTorres(self):
        conexao = novaConexao(self)
        cursor =  conexao.cursor()
        cursor.execute(f"SELECT * FROM V_CONSULTA_TORRE_ANTENA")
        torres = cursor.fetchall()
        return torres


    def retornaTorresPesquisaEnd(self):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute("SELECT LATITUDE, LONGITUDE FROM V_CONSULTA_TORRE_ANTENA")
        torresEnd = cursor.fetchall()
        return torresEnd


    def retornaAntenasPesquisaEnd(self):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute("SELECT DESC_ANTENA, AZIMUTE_ANTENA, STATUS_ANTENA FROM ANTENA_SETOR")
        antenasEnd = cursor.fetchall()
        return antenasEnd

    def registraLogPesquisa(self, localizacao, retorno):
        conexao = novaConexao(self)
        cursor = conexao.cursor()
        cursor.execute(f"INSERT INTO LOG_CONSULTA_ENDERECO (LOCALIZACAO, RETORNO, DATA_CONSULTA) VALUES ('{localizacao}','{retorno}', NOW())")
        conexao.commit()
        return True