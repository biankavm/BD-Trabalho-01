import psycopg2

class Produto:
    def __init__(self):
        self.id = -1
        self.asin = ""
        self.title = ""
        self.group = ""
        self.salesrank = 0
        self.similar_count = 0
        self.similares = []
        self.categories_count = 0
        self.categories = []
        self.total_reviews = 0
        self.dowloaded_reviews = 0
        self.avgrating_reviews = 0
        self.reviews = []
    
    def insere_no_bd(self, conexao):
        print(self.id)
        print(self.similar_count)
        
        produto_inserido = f""" INSERT INTO produto VALUES ({self.id}, '{self.asin}', '{self.title}',
        '{self.group}', {self.salesrank}, {self.similar_count});
        """
        conexao.cursor.execute(produto_inserido)

        similares_inseridos = ""
        for sim in self.similares:
            similares_inseridos = f" INSERT INTO similares (id_produto_og, asin_similar) VALUES ({self.id}, '{sim}')"
            #similares_inseridos = f"INSERT INTO similares VALUES ({self.id}, '{sim}');"
            conexao.cursor.execute(similares_inseridos)      
            
        categorias_unicas_inseridas = ""
        for nome, id in self.categories:
            existe = f"SELECT * FROM categorias_unicas WHERE id_original = {id}"
            conexao.cursor.execute(existe)
            res = conexao.cursor.fetchone()
            if (not res):
                categorias_unicas_inseridas = f"INSERT INTO categorias_unicas VALUES ({id}, '{nome}');"
                conexao.cursor.execute(categorias_unicas_inseridas)
            

                   
    def printa(self):
        #printado = "Produto: " + self.id + " " + self.asin
        #print(printado)
        pass

class Review:
    def __init__(self):
        self.date = None
        self.cutomer = ""
        self.rating = 0
        self.votes = 0
        self.helpful = 0

def le_um_produto(file):
    produto = Produto()

    line = file.readline()
    print('a linha é:', line)
    

    while ((line != "\n") and (line != '')):
        if (len(line.strip().split(':')) > 1):
            # não é uma categoria
            #print(f'classes : {line}')
            if 'Id' in line:
                id = line.strip().split()[1] # peguei o id
                produto.id = id
                # vou guardar o id no banco de dados
            elif 'ASIN' in line:
                asin = line.strip().split()[1] # peguei o asin
                produto.asin = asin
                # vou guardar o asin no banco de dados
    
            elif 'title' in line:
                title = ' '.join(line.strip().split()[1:]) # peguei o título
                produto.title = title
                # vou guardar o título no banco de dados
            elif 'group' in line:
                group = ' '.join(line.strip().split()[1:])
                produto.group = group
                # vou guardar o grupo no banco de dados
            elif 'salesrank' in line:
                salesrank = line.strip().split()[1]
                produto.salesrank = salesrank
                # vou guardar o salesrank no banco de dados
            elif ('similar' == line.strip().split(':')[0]):
                qtd_similares = line.strip().split()[1]
                lista_similares = line.strip().split()[2:]
                produto.similar_count = qtd_similares
                produto.similares = lista_similares
            
            # primeira linha das reviews
            elif ('reviews' in line):
                reviews = line.strip().split()
                total = reviews[2]
                downloaded = reviews[4]
                avg_rating = reviews[7]
            
            elif ("cutomer:" in line):
                info_reviews = line.strip().split()
                data = info_reviews[0]
                cutomer = info_reviews[2]
                rating = info_reviews[4]
                votes = info_reviews[6]
                helpful = info_reviews[8]
                     
        else:
            if 'discontinued product' in line:
                break
            
            elif ('|' in line):
                categories = line.split('|')
                for category in categories:
                    if '[' in category and ']' in category:
                        nome, numero = category.split('[')[0], category.split('[')[1].split(']')[0]
                        produto.categories.append((nome, numero))


               
        
        line = file.readline()
    
    # GUARDAR NO BANDO CADOS
    
    #print(produto.id)
    '''if (line == "\n"):
        se_fim_do_arquivo = False
        e_produto = False
    elif (produto.id != -1):
        se_fim_do_arquivo = False
        e_produto = True
    else:
        print('deu errado pq entrei no else que nao devia')
        se_fim_do_arquivo = True
        e_produto = False
    print(produto.id)
    return (se_fim_do_arquivo, e_produto, produto)'''
    
    
    if (produto.id != -1):
        print('é produto')
        se_fim_do_arquivo = False
        e_produto = True
    elif (line == ""):
        print('é barra n')
        se_fim_do_arquivo = True
        e_produto = False
    else:
        print('é outra coisa')
        se_fim_do_arquivo = False
        e_produto = False
    return (se_fim_do_arquivo, e_produto, produto)

