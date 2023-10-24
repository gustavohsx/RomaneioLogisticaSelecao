class DestinatarioDTO:

    def __init__(self, nota_fiscal, nome, cnpj, longradouro, numero, bairro, codigo_municipio, municipio, uf, cep, pais, peso_bruto, peso_liquido):
        self._nota_fiscal = nota_fiscal
        self._nome = nome
        self._cnpj = cnpj
        self._longradouro = longradouro
        self._numero_estabelecimento = numero
        self._bairro = bairro
        self._codigo_municipio = codigo_municipio
        self._municipio = municipio
        self._uf = uf
        self._cep = cep
        self._pais = pais
        self._peso_bruto = peso_bruto
        self._peso_liquido = peso_liquido
        self._produtos = []

    # Getters
    def get_nota_fiscal(self):
        return self._nota_fiscal

    def get_nome(self):
        return self._nome

    def get_cnpj(self):
        return self._cnpj

    def get_longradouro(self):
        return self._longradouro

    def get_numero_estabelecimento(self):
        return self._numero_estabelecimento

    def get_bairro(self):
        return self._bairro

    def get_codigo_municipio(self):
        return self._codigo_municipio

    def get_municipio(self):
        return self._municipio

    def get_uf(self):
        return self._uf

    def get_cep(self):
        return self._cep

    def get_pais(self):
        return self._pais

    def get_peso_bruto(self):
        return self._peso_bruto

    def get_peso_liquido(self):
        return self._peso_liquido
    
    def get_produtos(self):
        return self._produtos

    # Setters
    def set_nota_fiscal(self, nota_fiscal):
        self._nota_fiscal = nota_fiscal

    def set_nome(self, nome):
        self._nome = nome

    def set_cnpj(self, cnpj):
        self._cnpj = cnpj

    def set_longradouro(self, longradouro):
        self._longradouro = longradouro

    def set_numero_estabelecimento(self, numero):
        self._numero_estabelecimento = numero

    def set_bairro(self, bairro):
        self._bairro = bairro

    def set_codigo_municipio(self, codigo_municipio):
        self._codigo_municipio = codigo_municipio

    def set_municipio(self, municipio):
        self._municipio = municipio

    def set_uf(self, uf):
        self._uf = uf

    def set_cep(self, cep):
        self._cep = cep

    def set_pais(self, pais):
        self._pais = pais

    def set_peso_bruto(self, peso_bruto):
        self._peso_bruto = peso_bruto

    def set_peso_liquido(self, peso_liquido):
        self._peso_liquido = peso_liquido
    
    def adicionarProdutos(self, produto):
        self._produtos.append(produto)
    
    def adicionarListaProdutos(self, lista_produtos):
        self._produtos = lista_produtos
    
    def __str__(self) -> str:
        return f'{self._nome} - {self._cnpj}'