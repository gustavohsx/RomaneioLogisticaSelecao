import tkinter.messagebox as message

class Messager:

    def fileNotOpen(self):
        return message.showerror('Selecionar Arquivos', 'Nenhum Arquivo Foi Selecionado!')