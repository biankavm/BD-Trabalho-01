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
    
    def insere_no_bd(self):
        # Consulta SQL
        pass

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
                #print('achei o id:', id)
                # vou guardar o id no banco de dados
            elif 'ASIN' in line:
                asin = line.strip().split()[1] # peguei o asin
                produto.asin = asin
                #print('achei o asin:', asin)
                # vou guardar o asin no banco de dados
            elif 'title' in line:
                title = ' '.join(line.strip().split()[1:]) # peguei o título
                produto.title = title
                #print('achei o título:', title)
                # vou guardar o título no banco de dados
            elif 'group' in line:
                group = ' '.join(line.strip().split()[1:])
                produto.group = group
                #print('achei o grupo: ', group)
                # vou guardar o grupo no banco de dados
            elif 'salesrank' in line:
                salesrank = line.strip().split()[1]
                produto.salesrank = salesrank
                #print('achei o salesrank: ', salesrank)
                # vou guardar o salesrank no banco de dados
            elif ('similar' == line.strip().split(':')[0]):
                palavras = line.strip().split()
                produto.similar_count = palavras[1]
                produto.similar = palavras[2:]
            
            # primeira linha das reviews
            elif ('reviews' == line.strip().split(':')[0]):
                palavras = line.strip().split()
                #print(palavras)
                produto.total_reviews = palavras[2]
                produto.dowloaded_reviews = palavras[4]
                produto.avgrating_reviews_reviews = palavras[7]
            
            elif ("cutomer:" == line.strip().split()[1]):
                palavras = line.strip().split()
                print(palavras)
                rev = Review()
                rev.date = palavras[0]
                rev.cutomer = palavras[2]
                rev.rating = palavras[4]
                rev.votes = palavras[6]
                rev.helpful = palavras[8]

                produto.reviews.append(rev)
                

                
        else:
            # é uma categoria
            # TODO: MUDAR AS CONDIÇÕES PRA SER EXATAMENTE O FORMATO DE UM PRODUTO VÁLIDO
            # E EVITAR GUARDAR COISAS ERRADO
            # print(line.strip().split('|'))
            if ('|' in line):
                print("categoriaaaaaaaaaaaaaaaaaaa")
                for categoria in list(line.strip().split('|')):
                    if '[' in categoria and ']' in categoria:
                        nome, numero = categoria.split('[')[0], categoria.split('[')[1].split(']')[0]
                    #print("Nome:", nome)
                    #print("Número:", numero)
        #print("nova linha") # colocar o id_arvore
            #     print (categoria)
            #     nome, numero = categoria.split('[')[0], categoria.split('[')[1].split(']')[0]
            #     print(nome, numero)
        
        line = file.readline()
    
    # GUARDAR NO BANDO CADOS
    
    
    if produto.id != None:
        produto.printa()
        return True
    else:
        return False

txt = 'metinha.txt'     
existe = True
with open(txt, 'r') as file:
    while(existe):
        existe = le_um_produto(file)
        print("#####################################################################")