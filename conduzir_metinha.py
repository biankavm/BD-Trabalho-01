import psycopg2

class Node:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name
        self.children = {}

class Tree:
    def add_category(current_node, category_id, category_name):
        categories = category_name.split('|')
        for category in categories:
            if category not in current_node.children:
                current_node.children[category] = Node(category_id, category)
            current_node = current_node.children[category]

    def print_tree(node, depth=0):
        print(f"{node.category_name}\n{node.category_id}")
        for child in node.children.values():
            Tree.print_tree(child, depth + 1)

class Produto:
    def __init__(self):
        self.id = -1
        self.asin = ""
        self.title = ""
        self.group = ""
        self.salesrank = 0
        self.similar_count = 0
        self.similar = []
        self.categories_count = 0
        self.categories = []
        self.total_reviews = 0
        self.dowloaded_reviews = 0
        self.avgrating_reviews = 0
        self.reviews = []
    
    def insere_no_bd(self, conexao):
        print(self.id)
        produto_inserido = f""" INSERT INTO produto VALUES ({self.id}, '{self.asin}', '{self.title}',
        '{self.group}', {self.salesrank}, {self.similar_count}, {self.categories_count});
        """
        
        conexao.cursor.execute(produto_inserido)
             
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
                root = Node("", "")
                categories = line.split('|')
                for category in categories:
                    if '[' in category and ']' in category:
                        nome, numero = category.split('[')[0], category.split('[')[1].split(']')[0]
                        Tree.add_category(root, numero, nome)
                #Tree.print_tree(root)
                    #print("Nome:", nome)
                    #print("Número:", numero)
        #print("nova linha") # colocar o id_arvore
            #     print (categoria)
            #     nome, numero = categoria.split('[')[0], categoria.split('[')[1].split(']')[0]
            #     print(nome, numero)
        
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