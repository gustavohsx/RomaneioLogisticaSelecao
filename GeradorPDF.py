from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime
import locale


class GerarPDF():

    def __init__(self, local_salvamento):
        self.pdf = canvas.Canvas(f'{local_salvamento.replace(".pdf", "")}.pdf', pagesize=A4)
        self.pdf.setTitle('modelo')
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    def cabecalhoPaginaInicial(self):
        self.pdf.showPage()
        self.pdf.setFont('Helvetica-Bold', 18)
        self.pdf.drawString(190, 795, 'SPESSOA DISTRIBUIDOR')

        self.pdf.setFont('Helvetica-Bold', 12)
        self.pdf.drawString(35, 770, 'DE:')

        self.pdf.setFont('Helvetica', 12)
        self.pdf.drawString(35, 750, 'Motorista:')
        self.pdf.line(90, 750, 270, 750)
        self.pdf.drawString(35, 730, 'Placa:')
        self.pdf.line(70, 730, 270, 730)

        self.pdf.setFont('Helvetica-Bold', 12)
        self.pdf.drawString(300, 770, 'PARA:')

        self.pdf.setFont('Helvetica', 12)
        self.pdf.drawString(300, 750, 'Motorista:')
        self.pdf.line(355, 750, 535, 750)
        self.pdf.drawString(300, 730, 'Placa:')
        self.pdf.line(335, 730, 535, 730)

        self.pdf.drawString(35, 700, 'Nome Conferente:')
        self.pdf.line(135, 700, 335, 700)
        self.pdf.drawString(35, 680, 'Quant. Paletes:')
        self.pdf.line(120, 680, 210, 680)
        self.pdf.drawString(225, 680, 'Box:')
        self.pdf.line(250, 680, 335, 680)
        self.pdf.drawString(345, 700, 'Hora Inicio:')
        self.pdf.line(407, 700, 535, 700)
        self.pdf.drawString(345, 680, 'Hora Fim:')
        self.pdf.line(398, 680, 535, 680)

    def cabecalhoTabela(self, y):
        self.pdf.setFont('Helvetica-Bold', 11)
        self.pdf.drawString(30, y, 'Cod.Fábrica')
        self.pdf.drawString(200, y, 'Descrição')
        self.pdf.drawString(420, y, 'Cod.Barra')
        self.pdf.drawString(495, y, 'Qt')
        self.pdf.drawString(520, y, 'Unid.')
    
    def gerarQuadradoCheck(self, x, y):
        # linha de cima
        self.pdf.line(x[4]+20, y-5, x[4]+33, y-5)
        # linha de baixo
        self.pdf.line(x[4]+20, y+7, x[4]+33, y+7)
        # linha esquerda
        self.pdf.line(x[4]+20, y-5, x[4]+20, y+7)
        # linha direita
        self.pdf.line(x[4]+33, y-5, x[4]+33, y+7)
    
    def adicionarNotasFiscais(self, notas_fiscais):
        x = 60
        y = 652
        # 14 por linha
        for i in range(len(notas_fiscais)):
            if i == 14 or i == 28 or i == 42 or i == 56:
                x = 60
                y = y - 10
            self.pdf.setFont('Helvetica', 8)
            self.pdf.drawString(x, y, f'{notas_fiscais[i]}')
            if i != len(notas_fiscais)-1:
                self.pdf.drawString(x+30, y, f'-')
            x += 35
        
    def adicionarHora(self):
        data_e_hora_atuais = datetime.datetime.now()
        data_formatada = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S")
        self.pdf.drawString(30, 800, f'{data_formatada}')
    
    def adicionarImagemFundo(self):
        self.pdf.drawImage('logo_fundo.png', 35, 190, 500, 400)
    
    def cabecalhoResumo(self, pagina):
        self.pdf.setFont('Helvetica-Bold', 12)
        self.adicionarHora()
        self.pdf.drawString(500, 800, f'Página: {pagina}')
        self.adicionarImagemFundo()
        self.pdf.setFont('Helvetica-Bold', 18)
        self.pdf.drawString(190, 795, 'SPESSOA DISTRIBUIDOR')

        self.pdf.setFont('Helvetica-Bold', 16)
        self.pdf.drawString(230, 755, 'Resumo Romaneio')

        self.pdf.setFont('Helvetica-Bold', 10)
        self.pdf.drawString(150, 700, 'Razão Social')
        self.pdf.drawString(350, 700, 'Cidade')
        self.pdf.drawString(395, 700, 'Qt.Pedidos')
        self.pdf.drawString(460, 700, 'Peso Bruto')
        self.pdf.drawString(525, 700, 'Qt.Caixas')

        self.pdf.line(30, 695, 575, 695)
        self.pdf.setFont('Helvetica', 10)
    
    def gerarResumo(self, informacoes, quantidade_sku, quantidade_itens):
        
        numero_pagina = 1
        self.cabecalhoResumo(numero_pagina)

        y = 680
        qt_pedidos_total = 0
        valor_total = 0
        peso_bruto_total = 0
        for key in informacoes.keys():
            peso_bruto = locale.format_string("%.2f", informacoes[key]["peso_bruto"], grouping=True)
            valor = locale.format_string("%.2f", informacoes[key]["valor"], grouping=True)

            qt_pedidos_total += len(informacoes[key]["notas_fiscais"])
            valor_total += informacoes[key]["valor"]
            peso_bruto_total += informacoes[key]["peso_bruto"]
            cnpj, nome, cidade = key.split(' / ')
            for i in informacoes[key]['notas_fiscais']:
                numero_nota, peso_bruto_nota, qt_pedido_total_nota = i.split(' / ')
                print(numero_nota, peso_bruto_nota, qt_pedido_total_nota)
            nome = nome
            somar = False
            vezes = 1
            if len(nome) < 50:
                self.pdf.setFont('Helvetica', 10)
                self.pdf.drawString(35, y, f'{nome}')
            elif len(nome) < 55:
                self.pdf.setFont('Helvetica', 9)
                self.pdf.drawString(35, y, f'{nome}')
            elif len(nome) < 61:
                self.pdf.setFont('Helvetica', 8)
                self.pdf.drawString(35, y, f'{nome}')
            else:
                self.pdf.setFont('Helvetica', 7)
                self.pdf.drawString(35, y, f'{nome}')
            self.pdf.setFont('Helvetica', 10)
            if len(cidade) <= 8:
                self.pdf.drawString(345, y, f'{cidade}')
            else:
                self.pdf.setFont('Helvetica', 7)
                self.pdf.drawString(345, y+5, f'{cidade[:10]}')
                self.pdf.drawString(345, y-2, f'{cidade[10:]}')
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawRightString(430, y, f'{len(informacoes[key]["notas_fiscais"])}')
            self.pdf.drawRightString(515, y, f'{peso_bruto} kg')
            self.pdf.drawRightString(555, y, f'{int(informacoes[key]["quantidade_itens"])}')
            if somar:
                y -= (15 * vezes) - 5
            else:
                y -= 15
            if y <= 40:
                self.pdf.line(30, y+10, 575, y+10)
                self.pdf.showPage()
                numero_pagina += 1
                self.cabecalhoResumo(numero_pagina)
                y = 680
        
        self.pdf.line(30, y+10, 575, y+10)

        valor_total = locale.format_string("%.2f", valor_total, grouping=True)
        peso_bruto_total = locale.format_string("%.2f", peso_bruto_total, grouping=True)

        y -= 5
        self.pdf.setFont('Helvetica-Bold', 10)
        self.pdf.drawString(35, y, 'Total:')
        self.pdf.drawRightString(430, y, f'{qt_pedidos_total}')
        self.pdf.drawRightString(515, y, f'{peso_bruto_total} kg')
        self.pdf.drawRightString(555, y, f'{int(quantidade_itens)}')

    def cabecalhoResumoCompleto(self, pagina):
        self.pdf.setFont('Helvetica-Bold', 12)
        self.adicionarHora()
        self.pdf.drawString(500, 800, f'Página: {pagina}')
        # self.adicionarImagemFundo()
        self.pdf.setFont('Helvetica-Bold', 18)
        self.pdf.drawString(190, 795, 'SPESSOA DISTRIBUIDOR')

        self.pdf.setFont('Helvetica-Bold', 16)
        self.pdf.drawString(190, 755, 'Resumo Romaneio Completo')
        self.pdf.line(30, 715, 575, 715)
    
    def gerarResumoCompleto(self, informacoes, quantidade_sku, quantidade_itens):
        n_pagina = 1
        self.cabecalhoResumoCompleto(n_pagina)
        y = 700
        qt_pedidos_total = 0
        valor_total = 0
        peso_bruto_total = 0
        for key in informacoes.keys():
            peso_bruto = locale.format_string("%.2f", informacoes[key]["peso_bruto"], grouping=True)
            valor = locale.format_string("%.2f", informacoes[key]["valor"], grouping=True)

            qt_pedidos_total += len(informacoes[key]["notas_fiscais"])
            qt_pedidos_total_nota = len(informacoes[key]["notas_fiscais"])
            valor_total += informacoes[key]["valor"]
            peso_bruto_total += informacoes[key]["peso_bruto"]
            cnpj, nome, cidade = key.split(' / ')
            longradouro, numero, bairro, uf = informacoes[key]["endereco"].split(' / ')
            nome = nome
            self.pdf.line(30, y+17, 575, y+17)
            if y <= 80:
                self.pdf.showPage()
                n_pagina += 1
                self.cabecalhoResumoCompleto(n_pagina)
                y = 700
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawString(35, y, 'CNPJ:')
            self.pdf.setFont('Helvetica-Bold', 10)
            self.pdf.drawString(75, y, f'{cnpj}')

            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawString(345, y, f'Endereço:')
            endereco = f'{longradouro}, {numero} - {bairro}'
            if len(endereco) < 31:
                self.pdf.setFont('Helvetica-Bold', 10)
                self.pdf.drawString(395, y, endereco)
            elif len(endereco) < 35:
                self.pdf.setFont('Helvetica-Bold', 9)
                self.pdf.drawString(395, y, endereco)
            elif len(endereco) < 39:
                self.pdf.setFont('Helvetica-Bold', 8)
                self.pdf.drawString(395, y, endereco)
            elif len(endereco) < 43:
                self.pdf.setFont('Helvetica-Bold', 7)
                self.pdf.drawString(395, y, endereco)
            elif len(endereco) < 47:
                self.pdf.setFont('Helvetica-Bold', 6)
                self.pdf.drawString(395, y, endereco)
            else:
                self.pdf.setFont('Helvetica-Bold', 6)
                self.pdf.drawString(395, y+5, endereco[:47])
                self.pdf.drawString(395, y, endereco[47:])

            y -= 15

            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawString(35, y, f'Destinatário: ')
            if len(nome) < 42:
                self.pdf.setFont('Helvetica-Bold', 10)
                self.pdf.drawString(95, y, f'{nome}')
            elif len(nome) < 46:
                self.pdf.setFont('Helvetica-Bold', 9)
                self.pdf.drawString(95, y, f'{nome}')
            elif len(nome) < 61:
                self.pdf.setFont('Helvetica-Bold', 8)
                self.pdf.drawString(95, y, f'{nome}')
            else:
                self.pdf.setFont('Helvetica-Bold', 7)
                self.pdf.drawString(95, y, f'{nome}')

            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawString(345, y, f'Cidade:')
            self.pdf.setFont('Helvetica-Bold', 10)
            self.pdf.drawString(395, y, f'{cidade} - {uf}')

            y -= 15
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawString(35, y, 'Qt. Pedidos:')
            self.pdf.setFont('Helvetica-Bold', 10)
            self.pdf.drawString(95, y, f'{qt_pedidos_total_nota}')
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawString(120, y, 'Peso Total:')
            self.pdf.setFont('Helvetica-Bold', 10)
            self.pdf.drawString(175, y, f'{peso_bruto} kg')
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawString(250, y, 'Qt. Total Caixas:')
            self.pdf.setFont('Helvetica-Bold', 10)
            quantidade_itens_nota = 0
            for i in informacoes[key]['notas_fiscais']:
                numero_nota, peso_bruto_nota, qt_pedido_total_nota = i.split(' / ')
                quantidade_itens_nota += float(qt_pedido_total_nota)
            self.pdf.drawString(330, y, f'{int(quantidade_itens_nota)}')

            self.pdf.line(30, y-5, 575, y-5)
            y -= 15

            if y <= 40:
                self.pdf.showPage()
                n_pagina += 1
                self.cabecalhoResumoCompleto(n_pagina)
                y = 700

            for i in informacoes[key]['notas_fiscais']:
                self.pdf.line(30, y-5, 575, y-5)
                numero_nota, peso_bruto_nota, qt_pedido_total_nota = i.split(' / ')
                peso_bruto_nota = locale.format_string("%.2f", float(peso_bruto_nota), grouping=True)
                self.pdf.setFont('Helvetica', 10)
                self.pdf.setFont('Helvetica', 10)
                self.pdf.drawString(35, y, f'Nota:')
                self.pdf.setFont('Helvetica-Bold', 10)
                self.pdf.drawString(65, y, f'{numero_nota}')
                self.pdf.setFont('Helvetica', 10)
                self.pdf.drawString(120, y, f'Peso:')
                self.pdf.setFont('Helvetica-Bold', 10)
                self.pdf.drawString(150, y, f'{peso_bruto_nota} kg')
                self.pdf.setFont('Helvetica', 10)
                self.pdf.drawString(250, y, f'Qt. Caixas:')
                self.pdf.setFont('Helvetica-Bold', 10)
                self.pdf.drawString(310, y, f'{int(float(qt_pedido_total_nota))}')

                y -= 15

                if y <= 40:
                    self.pdf.showPage()
                    n_pagina += 1
                    self.cabecalhoResumoCompleto(n_pagina)
                    y = 700
            
            y -= 10
            
            if y <= 40:
                self.pdf.showPage()
                n_pagina += 1
                self.cabecalhoResumoCompleto(n_pagina)
                y = 700
        
        self.pdf.line(30, y+10, 575, y+10)

        valor_total = locale.format_string("%.2f", valor_total, grouping=True)
        peso_bruto_total = locale.format_string("%.2f", peso_bruto_total, grouping=True)

        y -= 5
        self.pdf.setFont('Helvetica-Bold', 10)
        self.pdf.drawString(35, y, f'Total:...')
        self.pdf.drawString(75, y, f'Qt. Total Pedidos: {qt_pedidos_total}')
        self.pdf.drawString(220, y, f'Peso Bruto Total: {peso_bruto_total} kg')
        self.pdf.drawString(400, y, f'Qt. Total Caixas: {int(quantidade_itens)}')
        

    def informacoesUltimaPagina(self, y, peso_bruto, peso_liquido, quantidade_total, quantidade_sku):
        peso_bruto_ref = locale.format_string("%.2f", float(peso_bruto), grouping=True)
        peso_liquido_ref = locale.format_string("%.2f", float(peso_liquido), grouping=True)
        self.pdf.setFont('Helvetica-Bold', 10)
        self.pdf.drawString(35, y-10, f'Peso Bruto:')
        self.pdf.setFont('Helvetica', 10)
        self.pdf.drawString(100, y-10, f'{peso_bruto_ref} kg')
        self.pdf.setFont('Helvetica-Bold', 10)
        self.pdf.drawString(200, y-10, f'Peso Liquido:')
        self.pdf.setFont('Helvetica', 10)
        self.pdf.drawString(270, y-10, f'{peso_liquido_ref} kg')
        self.pdf.setFont('Helvetica-Bold', 10)
        self.pdf.drawString(360, y-10, f'{int(quantidade_sku)} produtos listados')
        self.pdf.drawString(490, y-10, f'{int(quantidade_total)} caixas')

    def adicionarProdutosPaginaInicial(self, produtos, notas_fiscais=0, numero_pagina=1, peso_bruto=0, peso_liquido=0, quantidade_total=0, quantidade_sku=0, ultima_pagina=False, quant_paginas=1):
        self.pdf.setFont('Helvetica-Bold', 10)
        self.adicionarHora()
        self.pdf.drawString(500, 800, f'Página {numero_pagina} de {quant_paginas}')
        
        self.pdf.drawString(30, 652, 'NFs:')
        self.adicionarNotasFiscais(notas_fiscais)
        self.adicionarImagemFundo()
        x = [35, 100, 410, 510, 520]
        y = 580
        self.pdf.line(30, 590, 555, 590)
        for produto in produtos:
            self.pdf.setFont('Helvetica', 10)
            inicio = 0
            if len(produto.get_codigo_fabrica()) > 8:
                inicio = len(produto.get_codigo_fabrica()) - 8
            self.pdf.drawString(x[0], y, produto.get_codigo_fabrica()[inicio:])
            if len(produto.get_descricao()) <= 54:
                self.pdf.drawString(x[1], y, produto.get_descricao())
            elif len(produto.get_descricao()) <= 56:
                self.pdf.setFont('Helvetica', 9) 
                self.pdf.drawString(x[1], y+2, produto.get_descricao())
            else:
                self.pdf.setFont('Helvetica', 8) 
                self.pdf.drawString(x[1], y+3, produto.get_descricao()[:60])
                self.pdf.drawString(x[1], y-7, produto.get_descricao()[60:])
            self.pdf.setFont('Helvetica', 9)
            self.pdf.drawString(x[2], y, produto.get_codigo_barras())
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawRightString(x[3], y, f'{int(float(produto.get_quantidade()))}')
            self.pdf.drawString(x[4], y, produto.get_unidade())
            self.gerarQuadradoCheck(x, y)

            self.pdf.line(30, y-10, 555, y-10)

            y -= 20

        self.pdf.line(30, 590, 30, y+10)
        self.pdf.line(555, 590, 555, y+10)

        if ultima_pagina:
            self.informacoesUltimaPagina(y, peso_bruto, peso_liquido, quantidade_total, quantidade_sku)
    
    def adicionaProdutosPaginas(self, produtos, notas_fiscais=0, numero_pagina=2, peso_bruto=0, peso_liquido=0, quantidade_total=0, quantidade_sku=0, ultima_pagina=False, quant_paginas=1):
        self.pdf.setFont('Helvetica-Bold', 10)
        self.adicionarHora()
        self.pdf.drawString(500, 800, f'Página {numero_pagina} de {quant_paginas}')
        self.adicionarImagemFundo()
        x = [35, 100, 410, 510, 520]
        y = 740
        self.pdf.line(30, 750, 555, 750)
        for produto in produtos:
            self.pdf.setFont('Helvetica', 10)
            inicio = 0
            if len(produto.get_codigo_fabrica()) > 8:
                inicio = len(produto.get_codigo_fabrica()) - 8
            self.pdf.drawString(x[0], y, produto.get_codigo_fabrica()[inicio:])
            if len(produto.get_descricao()) <= 54:
                self.pdf.drawString(x[1], y, produto.get_descricao())
            elif len(produto.get_descricao()) <= 56:
                self.pdf.setFont('Helvetica', 9) 
                self.pdf.drawString(x[1], y+2, produto.get_descricao())
            else:
                self.pdf.setFont('Helvetica', 8) 
                self.pdf.drawString(x[1], y+3, produto.get_descricao()[:60])
                self.pdf.drawString(x[1], y-7, produto.get_descricao()[60:])

            self.pdf.setFont('Helvetica', 9)
            self.pdf.drawString(x[2], y, produto.get_codigo_barras())
            self.pdf.setFont('Helvetica', 10)
            self.pdf.drawRightString(x[3], y, f'{int(float(produto.get_quantidade()))}')
            self.pdf.drawString(x[4], y, produto.get_unidade())
            self.gerarQuadradoCheck(x, y)
            
            self.pdf.line(30, y-10, 555, y-10)

            y -= 20

        self.pdf.line(30, 750, 30, y+10)
        self.pdf.line(555, 750, 555, y+10)

        if ultima_pagina:
            self.informacoesUltimaPagina(y, peso_bruto, peso_liquido, quantidade_total, quantidade_sku)
    
    def paginaInicial(self, produtos, notas_fiscais=0, peso_bruto=0, peso_liquido=0, quantidade_total=0, quantidade_sku=0, ultima_pagina=False, quant_paginas=1, numero_pagina=1):
        self.cabecalhoPaginaInicial()
        self.cabecalhoTabela(y=600)
        self.adicionarProdutosPaginaInicial(produtos=produtos, notas_fiscais=notas_fiscais, numero_pagina=numero_pagina, peso_bruto=peso_bruto, peso_liquido=peso_liquido, quantidade_total=quantidade_total, quantidade_sku=quantidade_sku, ultima_pagina=ultima_pagina, quant_paginas=quant_paginas)

    def geraPDF(self, produtos, notas_fiscais=0, peso_bruto=0, peso_liquido=0, quantidade_total=0, quantidade_sku=0, informacoes=None, tipo_relatorio=0):
        if tipo_relatorio == 0:
            self.gerarResumo(informacoes, quantidade_sku, quantidade_total)
        elif tipo_relatorio == 1:
            self.gerarResumoCompleto(informacoes, quantidade_sku, quantidade_total)

        if ((len(produtos)//35)==0):
            quant_paginas = (len(produtos)//27) + 1
        else:
            numero = str(len(produtos)/35)
            numero_verif = f'0.{numero.split(".")[1]}'
            if float(numero_verif) >= 0.8:
                print(numero_verif + " maior")
                quant_paginas = (len(produtos)//35) + 2
                print(quant_paginas)
            else:
                print(numero_verif + " menor")
                quant_paginas = (len(produtos)//35) + 1
                print(quant_paginas)
        quant_inicial = 0
        quant_final = 27
        if quant_paginas == 1:
            self.paginaInicial(produtos=produtos[quant_inicial:quant_final], notas_fiscais=notas_fiscais, numero_pagina=1, peso_bruto=peso_bruto, peso_liquido=peso_liquido, quantidade_total=quantidade_total, quantidade_sku=quantidade_sku, ultima_pagina=True, quant_paginas=quant_paginas)
        else:
            self.paginaInicial(produtos=produtos[quant_inicial:quant_final], notas_fiscais=notas_fiscais, numero_pagina=1, peso_bruto=peso_bruto, peso_liquido=peso_liquido, quantidade_total=quantidade_total, quantidade_sku=quantidade_sku, quant_paginas=quant_paginas)
            for i in range(2, quant_paginas+1):
                self.pdf.showPage()
                if i == quant_paginas:
                    print(i)
                    quant_inicial = quant_final
                    quant_final += 35
                    self.cabecalhoTabela(y=760)
                    self.adicionaProdutosPaginas(produtos=produtos[quant_inicial:quant_final], notas_fiscais=notas_fiscais, numero_pagina=i, peso_bruto=peso_bruto, peso_liquido=peso_liquido, quantidade_total=quantidade_total, quantidade_sku=quantidade_sku, ultima_pagina=True, quant_paginas=quant_paginas)
                else:
                    quant_inicial = quant_final
                    quant_final += 35
                    self.cabecalhoTabela(y=760)
                    self.adicionaProdutosPaginas(produtos=produtos[quant_inicial:quant_final], notas_fiscais=notas_fiscais, numero_pagina=i, quant_paginas=quant_paginas)
        
        self.salvar()

    def salvar(self):
        self.pdf.save()