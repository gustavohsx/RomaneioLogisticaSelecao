import xmltodict
import DestinatarioDTO
import ProdutosDTO

class DadosXML:


    def __init__(self, xml):
        self._xml = xml
        self.destinatario = None
    

    def dados(self):
        with open(self._xml, encoding="utf8") as arquivo:
            self.dados = xmltodict.parse(arquivo.read())
            nota_fiscal = self.dados['nfeProc']['NFe']['infNFe']['ide']['nNF']
            dados_destinatario = self.dados['nfeProc']['NFe']['infNFe']['dest']
            dados_produtos = self.dados['nfeProc']['NFe']['infNFe']['det']
            peso_bruto = self.dados['nfeProc']['NFe']['infNFe']['transp']['vol']['pesoB']
            peso_liquido = self.dados['nfeProc']['NFe']['infNFe']['transp']['vol']['pesoL']
            # valor_pagamento = self.dados['nfeProc']['NFe']['infNFe']['pag']['detPag']['vPag']
            valor_pagamento = self.dados['nfeProc']['NFe']['infNFe']['total']['ICMSTot']['vNF']
            self.destinatario = self.dadosDestinatario(nota_fiscal, dados_destinatario, peso_bruto, peso_liquido, valor_pagamento)

            tipo_dados_produtos = type(dados_produtos)

            if tipo_dados_produtos == dict:
                produto = self.dadosProduto(dados_produtos['prod'])
                self.destinatario.adicionarProdutos(produto)
            elif tipo_dados_produtos == list:
                for produto_dados in dados_produtos:
                    produto = self.dadosProduto(produto_dados['prod'])
                    self.destinatario.adicionarProdutos(produto)
        return self.destinatario
    

    def dadosDestinatario(self, nota_fiscal, dados_destinatario, peso_bruto, peso_liquido, valor_pagamento):
        return DestinatarioDTO.DestinatarioDTO(
            nota_fiscal = nota_fiscal, 
            nome = dados_destinatario['xNome'], 
            cnpj = dados_destinatario['CNPJ'], 
            longradouro = dados_destinatario['enderDest']['xLgr'], 
            numero = dados_destinatario['enderDest']['nro'], 
            bairro = dados_destinatario['enderDest']['xBairro'], 
            codigo_municipio = dados_destinatario['enderDest']['cMun'], 
            municipio = dados_destinatario['enderDest']['xMun'], 
            uf = dados_destinatario['enderDest']['UF'], 
            cep = dados_destinatario['enderDest']['CEP'], 
            pais = dados_destinatario['enderDest']['cPais'],
            valor_pagamento = valor_pagamento,
            peso_bruto = peso_bruto, 
            peso_liquido = peso_liquido
        )
        
        
    def dadosProduto(self, produto):

        return ProdutosDTO.ProdutosDTO(
            codigo_fabrica = produto['cProd'], 
            ean = produto['cEAN'], 
            ean_tributavel = produto['cEANTrib'], 
            ncm = produto['NCM'], 
            cest = produto['CEST'], 
            cfop = produto['CFOP'], 
            descricao = produto['xProd'], 
            unidade = produto['uCom'], 
            quantidade = produto['qCom'], 
            codigo_barras = produto['cEANTrib'], 
            v_un_com = produto['vUnCom'], 
            v_prod = produto['vProd'], 
            u_trib = produto['uTrib'], 
            q_trib = produto['qTrib'], 
            v_un_trib = produto['vUnTrib'], 
            ind_tot = produto['indTot']
        )
    
