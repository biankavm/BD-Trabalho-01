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
        self.id_arvore = 1
        self.total_reviews = 0
        self.dowloaded_reviews = 0
        self.avgrating_reviews = 0
        self.reviews = []
    
    def insere_no_bd(self, conexao):
        print(self.id)
        print('ESSE É O TÍTULOOOOOO: ', self.title)
        
        self.title = self.title.replace("'", "''") 
        
        produto_inserido = ""
        if self.title == "":
            produto_inserido = f""" INSERT INTO produto VALUES ({self.id}, '{self.asin}', null,
            null, {self.salesrank}, {self.similar_count}, {self.categories_count}, {self.total_reviews},
            {self.dowloaded_reviews}, {self.avgrating_reviews});;
            """
        else:
            produto_inserido = f""" INSERT INTO produto VALUES ({self.id}, '{self.asin}', '{self.title}',
            '{self.group}', {self.salesrank}, {self.similar_count}, {self.categories_count}, {self.total_reviews},
            {self.dowloaded_reviews}, {self.avgrating_reviews});;
            """
        print('PRODUTO INSERIDO: ', produto_inserido)
        conexao.cursor.execute(produto_inserido)

        similares_inseridos = ""
        for sim in self.similares:
            similares_inseridos = f""" INSERT INTO similares (id_produto_og, asin_similar) 
                                    VALUES ({self.id}, '{sim}');"""
            #similares_inseridos = f"INSERT INTO similares VALUES ({self.id}, '{sim}');"
            conexao.cursor.execute(similares_inseridos)    
                    
        categorias_unicas_inseridas = []
        categorias_produtos_inseridas = []
        for nome, id, id_arvore in self.categories:
            nome = nome.replace("'", "''") 
            existe = f"SELECT * FROM categorias_unicas WHERE id_original = {id}"
            conexao.cursor.execute(existe)
            res = conexao.cursor.fetchone()
            
            if not res:
                categorias_unicas_inseridas.append((id, nome))  
                nome = nome.replace("'", "''") 
                insert_query = f""" INSERT INTO categorias_unicas (id_original, nome_categoria) 
            VALUES ({id}, '{nome}');        
                """
                conexao.cursor.execute(insert_query)

            categorias_produtos_inseridas.append((self.id, id, id_arvore))  # Armazenar para inserção em categorias_produto
                
        for id_produto, id_categoria, id_arvore in categorias_produtos_inseridas:
            insert_query = f"""INSERT INTO categorias_produto (id_produto, id_categoria, id_arvore) 
            VALUES ({id_produto}, {id_categoria}, {id_arvore});"""
            conexao.cursor.execute(insert_query)
        
        for data, cutomer, rating, votes, helpful in self.reviews:
            insert_query = f"""INSERT INTO reviews (id_produto, data, cutomer, rating, votes, helpful) 
            VALUES ({self.id}, '{data}', '{cutomer}', {rating}, {votes},
            {helpful});
            """
            conexao.cursor.execute(insert_query)
                                
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

    while ((line != "\n") and (line != '')):
        if (len(line.strip().split(':')) > 1):
            # não é uma categoria
            #print(f'classes : {line}')
            if line[0:3] == "Id:":
                id = line.strip().split()[1] # peguei o id
                
                produto.id = id
                # vou guardar o id no banco de dados
            elif line[0:5] == "ASIN:":
                asin = line.strip().split()[1] # peguei o asin
                produto.asin = asin
                # vou guardar o asin no banco de dados
    
            elif line[0:8] == "  title:":
                title = ' '.join(line.strip().split()[1:]) # peguei o título
                produto.title = title
                # vou guardar o título no banco de dados
            elif line[0:8] == "  group:":
                group = ' '.join(line.strip().split()[1:])
                produto.group = group
                # vou guardar o grupo no banco de dados
            elif line[0:12] == "  salesrank:":
                salesrank = line.strip().split()[1]
                produto.salesrank = salesrank
                # vou guardar o salesrank no banco de dados
            elif ('similar' == line.strip().split(':')[0]):
                qtd_similares = line.strip().split()[1]
                lista_similares = line.strip().split()[2:]
                produto.similar_count = qtd_similares
                produto.similares = lista_similares
            
            # primeira linha das reviews
            elif (line[0:10] == "  reviews:"):
                reviews = line.strip().split()
                total = reviews[2]
                downloaded = reviews[4]
                avg_rating = reviews[7]
                produto.total_reviews = total
                produto.dowloaded_reviews = downloaded
                produto.avgrating_reviews = avg_rating
            
            elif ("cutomer:" in line):
                info_reviews = line.strip().split()
                data = info_reviews[0]
                cutomer = info_reviews[2]
                rating = info_reviews[4]
                votes = info_reviews[6]
                helpful = info_reviews[8]
                produto.reviews.append((data, cutomer, rating, votes, helpful))
                     
        else:
            if 'discontinued product' in line:
                break

            elif ('|' in line):
                categories = line.split('|')
                for category in categories:
                    if '[' in category and ']' in category:
                        # pega tudo que vem antes do último [
                        nome = "[".join(category.split('[')[0:-1])

                        # pega a última string depois do [
                        numero = "".join(category.split('[')[-1][0:-1].split(']'))

                        produto.categories.append((nome, numero, produto.id_arvore))
                produto.id_arvore += 1
                produto.categories_count += 1
     
        line = file.readline()
    
    if (produto.id != -1):
        se_fim_do_arquivo = False
        e_produto = True
    elif (line == ""):
        se_fim_do_arquivo = True
        e_produto = False
    else:
        se_fim_do_arquivo = False
        e_produto = False
    return (se_fim_do_arquivo, e_produto, produto)

