'''
    DEFINIÇÃO DA CLASSE DE ENDEREÇO 

    ESTA CLASSE SERÁ UTILIZADA TANTO PARA O ENDEREÇO DO USUÁRIO COMUM E ADMINISTRADOR COMO PARA CLASSE 


'''

class Endereco:

    def __init__(self, cep, bairro, cidade, uf):
        self.cep = cep 
        self.bairro = bairro 
        self.cidade = cidade 
        self.uf = uf 
    
