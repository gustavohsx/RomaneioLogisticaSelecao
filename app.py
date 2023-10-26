from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog as fd
import fontes
import message
import DadosXML

class App:


    def __init__(self, tk):
        self.tk = tk
        self.filter_type = ('Nota Fiscal', 'Cidade', 'Destinatário')
        self.recipients = []
        self.fontes = fontes.Fontes()
        self.message = message.Messager()
        self.mainFrame()


    def getData(self):
        sources = self.getArchivesSelect()
        if sources == '':
            self.message.fileNotOpen()
            print('Não foi Selecionado Nenhum Arquivo')
        else:
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
        self.createCheckedButtonViewData(self.data)


    def showDataFilteredByCidade(self):
        self.data = {}
        for recipient in self.recipients:
            self.data[recipient.get_municipio()] = recipient
        self.createCheckedButtonViewData(self.data)


    def showDataFilteredByDestinatario(self):
        self.data = {}
        for recipient in self.recipients:
            self.data[recipient.get_nome()] = recipient
        self.createCheckedButtonViewData(self.data)


    def createCheckedButtonViewData(self, data):
        self.checkbutton_vars = []
        self.createCanvasAndDataView()
        for recipient in data.keys():
            var = IntVar()
            recipient_checked_button = Checkbutton(self.checked_button_frame, text=recipient, variable=var)
            recipient_checked_button.pack(anchor=W)
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
        self.canvas = Canvas(self.main)
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
        self.pdf_button = Button(self.main, text='Imprimir', command=self.getValuesCheckbutton)
        self.select_all = Button(self.main, text='Selecionar Tudo', command=self.setValuesCheckbuttonTrue)
        self.deselect_all = Button(self.main, text='Desmarcar Tudo', command=self.setValuesCheckbuttonFalse)
        self.pdf_button.grid(column=0, row=6, sticky=NSEW, columnspan=3, pady=10)
        self.select_all.grid(column=0, row=5, sticky=NSEW, pady=20, padx=10)
        self.deselect_all.grid(column=2, row=5, sticky=NSEW, pady=20, padx=10)


    def getValuesCheckbutton(self):
        valores_selecionados = []
        for i, item in enumerate(self.data.keys()):
            if self.checkbutton_vars[i].get() == 1:
                valores_selecionados.append(item)
        print(valores_selecionados)


    def setValuesCheckbuttonTrue(self):
        for i, item in enumerate(self.data.keys()):
            self.checkbutton_vars[i].set(1)
    

    def setValuesCheckbuttonFalse(self):
        for i, item in enumerate(self.data.keys()):
            self.checkbutton_vars[i].set(0)


    def onMousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def mainFrame(self):
        self.main = Frame(self.tk)

        label = Label(self.main, text='Lista de Separação', font=self.fontes.tituloPaginaInicial())

        archive_select_label = Label(self.main, text='Selecione os Arquivos: ', font=self.fontes.label12())
        archive_select_button = Button(self.main, text='Selecionar Arquivos', command=self.getData)

        filter_select_label = Label(self.main, text='Selecione o Tipo de Filtragem: ', font=self.fontes.label12())
        self.filter_select_combobox = Combobox(self.main, values=self.filter_type)
        self.filter_select_combobox.set(self.filter_type[0])
        self.filter_select_combobox.bind("<<ComboboxSelected>>", self.changeShowDataFiltered)
        
        label.grid(column=0, row=0, columnspan=3, pady=(10, 30))
        archive_select_label.grid(column=1, row=1, sticky=W)
        archive_select_button.grid(column=2, row=1, sticky=NSEW)
        filter_select_label.grid(column=1, row=2, sticky=W, padx=(0, 5), pady=(5, 20))
        self.filter_select_combobox.grid(column=2, row=2, pady=(5, 20))

        self.main.pack()


tk = Tk()
aa = App(tk)
tk.geometry('800x600')
tk.mainloop()