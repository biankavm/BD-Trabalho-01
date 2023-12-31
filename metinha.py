import psycopg2
from conduzir_metinha import *

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
                asin VARCHAR(15),
                titulo VARCHAR(100),
                grupo VARCHAR(20),
                salesrank INT,
                qtd_similares INT,
                qtd_categorias INT
            );
        """
        self.conexao.cursor.execute(sql_create_table_produto)

    def criar_tabela_similares(self):
        sql_create_table_similares = """
            CREATE TABLE similares (
                id_similar SERIAL PRIMARY KEY,
                id_produto_og INT,
                asin_similar VARCHAR(15) 
            );
        """
        self.conexao.cursor.execute(sql_create_table_similares)

    def criar_tabela_categorias_unicas(self):
        sql_create_table_categorias_unicas = """
        CREATE TABLE categorias_unicas (
            id_unico SERIAL ,
            id_original INT,
            nome_categoria VARCHAR(100) NOT NULL
        );
        """
        self.conexao.cursor.execute(sql_create_table_categorias_unicas)
        
    def criar_tabela_categorias_produto(self):
        sql_create_table_categorias_produto = """
        CREATE TABLE categorias_produto (
            id SERIAL PRIMARY KEY,
            id_produto INT,
            id_categoria INT,
            id_arvore INT
        );
        """
        self.conexao.cursor.execute(sql_create_table_categorias_produto)
        
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
        self.criar_tabela_categorias_unicas()
        self.criar_tabela_categorias_produto()
        self.criar_tabela_reviews()
        self.criar_tabela_info_reviews()

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

txt = 'metinha.txt'     
existe = (False, False, None)
with open(txt, 'r') as file:

    while(not existe[0]):
        existe = le_um_produto(file)

        if (existe[1]):

            existe[2].insere_no_bd(conexao)
          
conexao.fechar_conexao()
