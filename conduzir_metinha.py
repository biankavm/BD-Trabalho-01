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
        self.id = None
        self.asin = ""
        self.title = ""
        self.group = ""
        self.salesrank = ""
        self.similar_count = 0
        self.similar = []
        self.categories_count = 0
        self.categories = []
        self.total_reviews = 0
        self.dowloaded_reviews = 0
        self.avgrating_reviews = 0
        self.reviews = []
    
    def insere_no_bd(self, conexao):
        
        produto_inserido = f""" INSERT INTO produto VALUES ({self.id}, '{self.asin}', '{self.title}',
        '{self.group}', {self.salesrank}, {self.similar_count}, {self.categories_count});
        """
        
        conexao.cursor.execute(produto_inserido)
        
        print('produto inserido no banco!!!')
        print(produto_inserido)


        
    def printa(self):
        printado = "Produto: " + self.id + " " + self.asin
        print(printado)

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
    print("lendo")
    while ((line != "\n") and (line != '')):
        #print(line.strip().split(':'))
        if (len(line.strip().split(':')) > 1):
            # não é uma categoria
            #print(f'classes : {line}')
            if 'Id' in line:
                id = line.strip().split()[1] # peguei o id
                produto.id = id
                print('achei o id:', id)
                # vou guardar o id no banco de dados
            elif 'ASIN' in line:
                asin = line.strip().split()[1] # peguei o asin
                produto.asin = asin
                print('achei o asin:', asin)
                # vou guardar o asin no banco de dados
            elif 'title' in line:
                title = ' '.join(line.strip().split()[1:]) # peguei o título
                produto.title = title
                print('achei o título:', title)
                # vou guardar o título no banco de dados
            elif 'group' in line:
                group = ' '.join(line.strip().split()[1:])
                produto.group = group
                print('achei o grupo: ', group)
                # vou guardar o grupo no banco de dados
            elif 'salesrank' in line:
                salesrank = line.strip().split()[1]
                produto.salesrank = salesrank
                print('achei o salesrank: ', salesrank)
                # vou guardar o salesrank no banco de dados
            elif ('similar' == line.strip().split(':')[0]):
                qtd_similares = line.strip().split()[1]
                lista_similares = line.strip().split()[2:]
                print('a quantidade de similares é:', qtd_similares)
                print('os ids dos similares são: ', lista_similares)
            
            # primeira linha das reviews
            elif ('reviews' in line):
                reviews = line.strip().split()
                total = reviews[2]
                downloaded = reviews[4]
                avg_rating = reviews[7]
                print('total reviews:', total)
                print('downloaded: ', downloaded)
                print('avg: ', avg_rating)
            
            elif ("cutomer:" in line):
                info_reviews = line.strip().split()
                data = info_reviews[0]
                cutomer = info_reviews[2]
                rating = info_reviews[4]
                votes = info_reviews[6]
                helpful = info_reviews[8]
                print(f'data:{data}, cutomer:{cutomer}, rating:{rating}, votes:{votes}, helpful:{helpful}')
                     
        else:
            # é uma categoria
            # TODO: MUDAR AS CONDIÇÕES PRA SER EXATAMENTE O FORMATO DE UM PRODUTO VÁLIDO
            # E EVITAR GUARDAR COISAS ERRADO
            # print(line.strip().split('|'))
            '''if ('|' in line):
                print("categoriaaaaaaaaaaaaaaaaaaa")
                for categoria in list(line.strip().split('|')):
                    if '[' in categoria and ']' in categoria:
                        nome, numero = categoria.split('[')[0], categoria.split('[')[1].split(']')[0]'''
            root = Node("", "")
            categories = line.split('|')
            for category in categories:
                if '[' in category and ']' in category:
                    nome, numero = category.split('[')[0], category.split('[')[1].split(']')[0]
                    Tree.add_category(root, numero, nome)
            Tree.print_tree(root)
                    #print("Nome:", nome)
                    #print("Número:", numero)
        #print("nova linha") # colocar o id_arvore
            #     print (categoria)
            #     nome, numero = categoria.split('[')[0], categoria.split('[')[1].split(']')[0]
            #     print(nome, numero)
        
        line = file.readline()
    
    # GUARDAR NO BANDO CADOS
    
    print(produto.id)
    if produto.id != None:
        produto.printa()
        return produto
    else:
        return None
