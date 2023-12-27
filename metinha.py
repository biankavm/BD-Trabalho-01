import psycopg2

class ConexaoDB:
    def __init__(self, host='localhost', port='5432'):
        self.database = None
        self.user = None
        self.password = None
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None
    
    def conf_banco(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password  
        self.conn = None
        self.cursor = None
    
    def conectar(self):
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
            
    def criar_banco(self, new_database):
        sql_create_db = f'CREATE DATABASE {new_database};'
        self.cursor.execute(sql_create_db)


class GerenciadorDeTabelas:
    def __init__(self, conexao):
        self.conexao = conexao

    def criar_tabela_produto(self):
        sql_create_table_produto = """
            CREATE TABLE produto (
                id INT PRIMARY KEY,
                asin CHAR(10) UNIQUE NOT NULL,
                titulo VARCHAR(100) NOT NULL,
                grupo VARCHAR(20) NOT NULL,
                salesrank INT NOT NULL,
                qtd_similares INT,
                qtd_categorias INT
            );
        """
        self.conexao.cursor.execute(sql_create_table_produto)

    def criar_tabela_similares(self):
        sql_create_table_similares = """
            CREATE TABLE similares (
                id_similar SERIAL PRIMARY KEY,
                id_produto_og INT REFERENCES produto(id),
                asin_similar CHAR(10) NOT NULL
            );
        """
        self.conexao.cursor.execute(sql_create_table_similares)

    def criar_tabela_categorias(self):
        sql_create_table_categorias = """
        CREATE TABLE categorias (
            id_produto INT REFERENCES produto(id),
            id_arvore INT PRIMARY KEY,
            id_categoria INT NOT NULL,
            nome_categoria VARCHAR(100) NOT NULL
        );
        """
        self.conexao.cursor.execute(sql_create_table_categorias)
        
    def criar_tabela_reviews(self):
        sql_create_table_reviews = """
        CREATE TABLE reviews (
            id_produto INT REFERENCES produto(id),
            total INT NOT NULL,
            downloaded INT NOT NULL,
            avg_rating FLOAT(1) NOT NULL
        );  
        """
        self.conexao.cursor.execute(sql_create_table_reviews)


    def criar_tabela_info_reviews(self):
        sql_create_table_info_reviews = """
        CREATE TABLE info_reviews (
            id_produto INT REFERENCES produto(id),
            data DATE NOT NULL,
            cutomer VARCHAR(20) NOT NULL,
            rating INT NOT NULL,
            votes INT NOT NULL,
            helpful INT NOT NULL
        );
        """
        self.conexao.cursor.execute(sql_create_table_info_reviews)

    def criar_tabelas(self):
        self.criar_tabela_produto()
        self.criar_tabela_similares()
        self.criar_tabela_categorias()
        self.criar_tabela_reviews()
        self.criar_tabela_info_reviews()

class Arquivo:
    def processar_arquivo(self):
        with open('metinha.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if (len(line.strip().split(':')) > 1):
                    # não é uma categoria
                    print(f'classes : {line}')
                    if 'Id' in line:
                        id = line.strip().split()[1] # peguei o id
                        print('achei o id:', id)
                        # vou guardar o id no banco de dados
                    elif 'ASIN' in line:
                        asin = line.strip().split()[1] # peguei o asin
                        print('achei o asin:', asin)
                        # vou guardar o asin no banco de dados
                    elif 'title' in line:
                        title = ' '.join(line.strip().split()[1:]) # peguei o título
                        print('achei o título:', title)
                        # vou guardar o título no banco de dados
                    elif 'group' in line:
                        group = ' '.join(line.strip().split()[1:])
                        print('achei o grupo: ', group)
                        # vou guardar o grupo no banco de dados
                    elif 'salesrank' in line:
                        salesrank = line.strip().split()[1]
                        print('achei o salesrank: ', salesrank)
                        # vou guardar o salesrank no banco de dados
                        
                else:
                    # é uma categoria
                    for categoria in list(line.strip().split('|')):
                        if '[' in categoria and ']' in categoria:
                            nome, numero = categoria.split('[')[0], categoria.split('[')[1].split(']')[0]
                            print("Nome:", nome)
                            print("Número:", numero)
                print("nova linha") # colocar o id_arvore
                    #     print (categoria)
                    #     nome, numero = categoria.split('[')[0], categoria.split('[')[1].split(']')[0]
                    #     print(nome, numero)
            
            
    
# Utilização das classes    
conexao = ConexaoDB()

conexao.conf_banco(database='postgres', user='postgres', password='jusbrasil!00')
conexao.conectar()
# criar banco de dados Amazon
conexao.criar_banco(new_database='amazon')
conexao.fechar_conexao();

# #conectar ao Amazon
conexao.conf_banco(database='amazon', user='postgres', password='jusbrasil!00')
conexao.conectar()

criador_tabelas = GerenciadorDeTabelas(conexao)
criador_tabelas.criar_tabelas()

conexao.fechar_conexao()
