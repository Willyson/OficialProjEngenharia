class UsuarioTeste: 
    email = ""
    senha = ""
    mais_dados = ""

    def __init__(self):
        pass

    def usuarioLogin(self, email, senha):
        self.email = email 
        self.senha = senha 

    def usuarioCompleto(self, email, senha, mais_dados):
        self.email = email 
        self.senha = senha
        self.mais_dados = mais_dados    

teste = UsuarioTeste()
teste.usuarioLogin('william@email.com', '1234')

novoUsuario = UsuarioTeste()
novoUsuario.usuarioCompleto('William@email.com', '1234', ['dado1', 'dado2'])


print(novoUsuario)