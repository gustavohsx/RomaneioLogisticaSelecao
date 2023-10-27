from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog as fd
import fontes
import message
import DadosXML
import ProdutosDTO
import GeradorPDF

class App:


    def __init__(self, tk):
        self.tk = tk
        self.filter_type = ('Nota Fiscal', 'Cidade', 'Destinatário')
        self.have_source = False
        self.recipients = []
        self.fontes = fontes.Fontes()
        self.message = message.Messager()
        self.mainFrame()


    def getData(self):
        sources = self.getArchivesSelect()
        if sources == '':
            self.have_source = False
            self.message.fileNotOpen()
            print('Não foi Selecionado Nenhum Arquivo')
        else:
            self.message.quantSelectedFiles(len(sources))
            self.have_source = True
            self.restartRecipientsList()
            for source in sources:
                dados = DadosXML.DadosXML(source)
                recipient = dados.dados()
                self.recipients.append(recipient)
            self.showDataFiltered()


    def getArchivesSelect(self):
        initialdir = './'
        filetypes = (('XML', '*.xml'), ('Todos os Arquivos', '*.*'))
        return fd.askopenfilenames(title='Selecione os Arquivos', initialdir=initialdir, filetypes=filetypes)


    def restartRecipientsList(self):
        self.recipients = []


    def showDataFiltered(self):
        if self.have_source:
            filter_type = self.getComboboxValue()

            if filter_type == 'Nota Fiscal':
                self.showDataFilterdByNotaFiscal()
            elif filter_type == 'Cidade':
                self.showDataFilteredByCidade()
            elif filter_type == 'Destinatário':
                self.showDataFilteredByDestinatario()
            else:
                # Criar Janela de Erro
                pass


    def changeShowDataFiltered(self, event):
        self.showDataFiltered()


    def getComboboxValue(self):
        return self.filter_select_combobox.get()


    def showDataFilterdByNotaFiscal(self):
        self.data = {}
        for recipient in self.recipients:
            self.data[recipient.get_nota_fiscal()] = recipient
        self.createCheckedButtonAndViewData(self.data)


    def showDataFilteredByCidade(self):
        self.data = {}
        for recipient in self.recipients:
            try:
                self.data[recipient.get_municipio()].append(recipient)
            except:
                self.data[recipient.get_municipio()] = []
                self.data[recipient.get_municipio()].append(recipient)
        self.createCheckedButtonAndViewData(self.data)


    def showDataFilteredByDestinatario(self):
        self.data = {}
        for recipient in self.recipients:
            try:
                self.data[recipient.get_nome()].append(recipient)
            except:
                self.data[recipient.get_nome()] = []
                self.data[recipient.get_nome()].append(recipient)
        self.createCheckedButtonAndViewData(self.data)


    def createCheckedButtonAndViewData(self, data):
        self.checkbutton_vars = []
        self.createCanvasAndDataView()
        for recipient in data.keys():
            var = IntVar()
            recipient_checked_button = Checkbutton(self.checked_button_frame, text=recipient, variable=var)
            recipient_checked_button.pack(anchor=W, pady=2)
            self.checkbutton_vars.append(var)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.onMousewheel)
        self.main.update_idletasks()
        self.createButtonPDF()


    def createCanvasAndDataView(self):
        try:
            self.canvas.unbind("<Configure>")
            self.canvas.unbind("<MouseWheel>")
            self.canvas.destroy()
            self.scroll.destroy()
            self.checked_button_frame.destroy()
        except:
            print('Não foi possivel apagar o Canvas')
        self.main.update_idletasks()
        self.canvas = Canvas(self.main, border=10)
        self.canvas.grid(column=0, row=4, sticky=NSEW, columnspan=4)

        self.scroll = Scrollbar(self.main, orient=VERTICAL, command=self.canvas.yview)
        self.scroll.grid(column=4, row=4, sticky=NS)
        self.canvas.config(yscrollcommand=self.scroll.set)

        self.checked_button_frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.checked_button_frame, anchor=NW)


    def createButtonPDF(self):
        try:
            self.pdf_button.destroy()
        except:
            print('Botão de Imprimir Não Existe')
        self.main.update_idletasks()
        self.pdf_button = Button(self.main, text='Gerar PDF', command=self.getValuesConfirmatePDFCreate)
        self.select_all = Button(self.main, text='Selecionar Tudo', command=self.setValuesCheckbuttonTrue)
        self.deselect_all = Button(self.main, text='Desmarcar Tudo', command=self.setValuesCheckbuttonFalse)
        self.pdf_button.grid(column=0, row=6, sticky=NSEW, columnspan=3, pady=10)
        self.select_all.grid(column=0, row=5, sticky=NSEW, pady=20, padx=10)
        self.deselect_all.grid(column=2, row=5, sticky=NSEW, pady=20, padx=10)


    def getValuesConfirmatePDFCreate(self):
        valores_selecionados = []
        for i, item in enumerate(self.data.keys()):
            if self.checkbutton_vars[i].get() == 1:
                valores_selecionados.append(item)

        if len(valores_selecionados) != 0:
            self.selected_products = []

            filter_type = self.getComboboxValue()

            if filter_type == 'Cidade':
                for item in valores_selecionados:
                    for valor in self.data[item]:
                        self.selected_products.append(valor)
            elif filter_type == 'Destinatário':
                for item in valores_selecionados:
                    for valor in self.data[item]:
                        self.selected_products.append(valor)
            else:
                for valor in valores_selecionados:
                    self.selected_products.append(self.data[valor])

            self.selected_products = sorted(self.selected_products, key=self.sortByName)
            self.confirmatePDFCreate()
            self.addValuesTreeview(self.selected_products)
        else:
            self.message.unselectedItens()


    def sortByName(self, e):
        return e.get_nome()


    def sortByMunicipio(self, e):
        return e.split(' / ')[1]
    

    def setValuesCheckbuttonTrue(self):
        for i, item in enumerate(self.data.keys()):
            self.checkbutton_vars[i].set(1)
    

    def setValuesCheckbuttonFalse(self):
        for i, item in enumerate(self.data.keys()):
            self.checkbutton_vars[i].set(0)
    

    def addValuesTreeview(self, values):
        for data in values:
            nome = (f'{data.get_nome()}', f'{data.get_nota_fiscal()}', '', '', '')
            head = self.products_treeview.insert('', END, values=nome)
            products = data.get_produtos()
            for product in products:
                aux = ('', '', product.get_codigo_fabrica(), product.get_descricao(), f'{int(float(product.get_quantidade()))} {product.get_unidade()}')
                self.products_treeview.insert(head, END, values=aux)
    

    def geratePDF(self):
        todos_produtos = {}
        peso_bruto = 0
        peso_liquido = 0
        notas_fiscais = []
        quantidade_total_produtos = 0
        produtos = []
        informacoes = {}
        for arquivo in self.selected_products:
            notas_fiscais.append(arquivo.get_nota_fiscal())
            peso_bruto += float(arquivo.get_peso_bruto())
            peso_liquido += float(arquivo.get_peso_liquido())

            try:
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['peso_bruto'] += float(arquivo.get_peso_bruto())
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['peso_liquido'] += float(arquivo.get_peso_liquido())
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['notas_fiscais'].append(arquivo.get_nota_fiscal())
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['valor'] += float(arquivo.get_valor_pagamento())
            except Exception as e:
                # print(e)
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}'] = {'notas_fiscais':[], 'peso_bruto':0, 'peso_liquido':0, 'valor':0, 'quantidade_produtos_sku':{}, 'quantidade_itens':0}
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['peso_bruto'] += float(arquivo.get_peso_bruto())
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['peso_liquido'] += float(arquivo.get_peso_liquido())
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['notas_fiscais'].append(arquivo.get_nota_fiscal())
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['valor'] += float(arquivo.get_valor_pagamento())
            for produto in arquivo.get_produtos():
                try:
                    codigo = produto.get_codigo_fabrica()
                    quantidade = float(todos_produtos[codigo].get_quantidade()) + float(produto.get_quantidade())
                    produto_novo = ProdutosDTO.ProdutosDTO(codigo_fabrica=produto.get_codigo_fabrica(), ean=produto.get_ean(), ean_tributavel=produto.get_ean_tributavel(), ncm=produto.get_ncm(), cest=produto.get_cest(), cfop=produto.get_cfop(), descricao=produto.get_descricao(), unidade=produto.get_unidade(), quantidade=quantidade, codigo_barras=produto.get_codigo_barras(), v_un_com=produto.get_v_un_com(), v_prod=produto.get_v_prod(), u_trib=produto.get_u_trib(), q_trib=produto.get_q_trib(), v_un_trib=produto.get_v_un_trib(), ind_tot=produto.get_ind_tot)
                    todos_produtos[codigo] = produto_novo
                except Exception as e:
                    codigo = produto.get_codigo_fabrica()
                    todos_produtos[codigo] = produto
                try:
                    informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['quantidade_produtos_sku'][codigo] += 1
                except:
                    informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['quantidade_produtos_sku'][codigo] = 1
                quantidade_total_produtos += float(produto.get_quantidade())
                informacoes[f'{arquivo.get_nome()} / {arquivo.get_municipio()}']['quantidade_itens'] += float(produto.get_quantidade())
        for key in todos_produtos.keys():
            produtos.append(todos_produtos[key])
        
        produtos_pdf = sorted(produtos, key=lambda x: x.get_descricao())

        print(notas_fiscais, peso_bruto, peso_liquido)
        informacoes_ref = dict(sorted(informacoes.items(), key=lambda item: item[0].split(' / ')[1]))

        print('-'*20, '\n', informacoes_ref.items(), '\n', '-'*20)
        caminho = fd.asksaveasfilename(filetypes=(('PDF', '*.pdf'), ('Todos os Arquivos', '*.*')))
        if caminho != '':
            pdf = GeradorPDF.GerarPDF(caminho)
            pdf.geraPDF(produtos=produtos_pdf, notas_fiscais=notas_fiscais, peso_bruto=peso_bruto, peso_liquido=peso_liquido, quantidade_total=quantidade_total_produtos, quantidade_sku=len(produtos_pdf), informacoes=informacoes_ref)
            self.message.sucessPDFCreate()
            self.destroyConfirmatePDFCreate()
        else:
            self.message.unsucessPDFCreate()
            self.confirmate_main.focus_set()

    def destroyConfirmatePDFCreate(self):
        self.confirmate_main.destroy()
        self.main.focus_set()


    def onMousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def mainFrame(self):
        self.main = Frame(self.tk)

        label = Label(self.main, text='Lista de Separação', font=self.fontes.tituloPaginaInicial())

        selections_frame = Frame(self.main)
        archive_select_label = Label(selections_frame, text='Selecione os Arquivos: ', font=self.fontes.label12())
        archive_select_button = Button(selections_frame, text='Selecionar Arquivos', command=self.getData)

        filter_select_label = Label(selections_frame, text='Selecione o Tipo de Filtragem: ', font=self.fontes.label12())
        self.filter_select_combobox = Combobox(selections_frame, values=self.filter_type)
        self.filter_select_combobox.set(self.filter_type[0])
        self.filter_select_combobox.bind("<<ComboboxSelected>>", self.changeShowDataFiltered)
        
        label.grid(column=0, row=0, columnspan=3, pady=(20, 30))

        archive_select_label.grid(column=0, row=0, sticky=W)
        archive_select_button.grid(column=1, row=0, sticky=NSEW)
        filter_select_label.grid(column=0, row=1, sticky=W, padx=(0, 5), pady=(5, 20))
        self.filter_select_combobox.grid(column=1, row=1, pady=(5, 20))

        selections_frame.grid(column=0, row=1, columnspan=3)

        self.main.pack()
    

    def confirmatePDFCreate(self):
        self.confirmate_main = Toplevel(self.main)
        self.confirmate_main.title('Produtos Selecionados')
        confirmation_title_label = Label(self.confirmate_main, text='Verifique os Produtos', font=self.fontes.tituloPaginaInicial())

        columns = ['id', 'nf', 'codigo_fabrica', 'descricao', 'quantidade']
        self.products_treeview = Treeview(self.confirmate_main, columns=columns, show='headings', height=20)

        self.products_treeview.column( 0, anchor=W, width=300)
        self.products_treeview.column( 1, anchor=CENTER, width=100)
        self.products_treeview.column( 2, anchor=E, width=150)
        self.products_treeview.column( 3, anchor=W, width=450)
        self.products_treeview.column( 4, anchor=E, width=100)

        self.products_treeview.heading('id', text='ID', anchor=CENTER)
        self.products_treeview.heading('nf', text='Nota Fiscal', anchor=CENTER)
        self.products_treeview.heading('codigo_fabrica', text='Código de Fabrica', anchor=CENTER)
        self.products_treeview.heading('descricao', text='Descrição', anchor=CENTER)
        self.products_treeview.heading('quantidade', text='Quantidade', anchor=CENTER)

        back_buton = Button(self.confirmate_main, text='Voltar', command=self.destroyConfirmatePDFCreate)
        confirmate_button = Button(self.confirmate_main, text='Gerar PDF', width=20, command=self.geratePDF)

        confirmation_title_label.pack(pady=(20, 10))
        self.products_treeview.pack(padx=20, pady=20)
        back_buton.pack()
        confirmate_button.pack(pady=(10, 20))

        self.confirmate_main.focus_set()

        larguraTela = self.confirmate_main.winfo_screenwidth()
        alturaTela = self.confirmate_main.winfo_screenheight()
        self.confirmate_main.geometry(f'{larguraTela}x{alturaTela}+-10+0')


tk = Tk()
aa = App(tk)
tk.title('Romaneio')
larguraTela = tk.winfo_screenwidth()
alturaTela = tk.winfo_screenheight()
tk.geometry(f'{larguraTela}x{alturaTela}+-10+0')
tk.mainloop()
