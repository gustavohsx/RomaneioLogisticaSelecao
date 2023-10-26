import tkinter.messagebox as message

class Messager:

    def fileNotOpen(self):
        return message.showerror('Selecionar Arquivos', 'Nenhum Arquivo Foi Selecionado!')

    def sucessPDFCreate(self):
        return message.showinfo('Sucesso', 'PDF Criado Com Sucesso!')

    def unsucessPDFCreate(self):
        return message.showwarning('Erro ao gerar o PDF', 'Operação Cancelada!')
    
    def quantSelectedFiles(self, quant):
        return message.showinfo('Quantidade de Arquivos', f'Foram selecionados {quant} arquivo(s)!')

    def unselectedItens(self):
        return message.showwarning('Selecione o Item', 'Nenhum Item foi Selecionado!')