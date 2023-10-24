from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog as fd
import fontes
import DadosXML

class App:


    def __init__(self, tk):
        self.tk = tk
        self.filter_type = ('Nota Fiscal', 'Cidade', 'Destinatário')
        self.fontes = fontes.Fontes()
        self.mainFrame()
    
    
    def getData(self):
        sources = self.getArchivesSelect()
        if sources == '':
            print('Não foi Selecionado Nenhum Arquivo')
        else:
            pass
    

    def getComboboxValue(self, e):
        print(self.filter_select_combobox.get())
        return self.filter_select_combobox.get()


    def getArchivesSelect(self):
        initialdir = './'
        filetypes = (('XML', '*.xml'), ('Todos os Arquivos', '*.*'))
        return fd.askopenfilenames(title='Selecione os Arquivos', initialdir=initialdir, filetypes=filetypes)


    def mainFrame(self):
        main = Frame(self.tk)

        label = Label(main, text='Lista de Separação', font=self.fontes.tituloPaginaInicial())

        archive_select_label = Label(main, text='Selecione os Arquivos: ', font=self.fontes.label12())
        archive_select_button = Button(main, text='Selecionar Arquivos', command=self.getData)

        filter_select_label = Label(main, text='Selecione o Tipo de Filtragem: ', font=self.fontes.label12())
        self.filter_select_combobox = Combobox(main, values=self.filter_type)
        self.filter_select_combobox.set(self.filter_type[0])
        self.filter_select_combobox.bind('<<ComboboxSelected>>', self.getComboboxValue)

        label.grid(column=0, row=0, columnspan=3, pady=(10, 30))
        archive_select_label.grid(column=0, row=1, sticky=W)
        archive_select_button.grid(column=1, row=1, sticky=NSEW)
        filter_select_label.grid(column=0, row=2, sticky=W, padx=(0, 5), pady=(5, 20))
        self.filter_select_combobox.grid(column=1, row=2, pady=(5, 20))

        main.pack()


tk = Tk()
aa = App(tk)
tk.geometry('600x400')
tk.mainloop()