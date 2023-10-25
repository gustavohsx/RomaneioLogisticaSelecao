import tkinter as tk
from tkinter import ttk



class Application(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.geometry("400x500")
        
        notebook = ttk.Notebook(self)

        frame = tk.Frame(notebook)
        frame2 = tk.Frame(notebook)

        label1 = tk.Label(frame, text='Teste')
        label2 = tk.Label(frame2, text='Teste2')

        notebook.add(frame, text='aba')
        notebook.add(frame2, text='aba2')

        label1.pack()
        label2.pack(padx=10, pady=10)

        notebook.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.pack(expand=True, fill='both')
    root.mainloop()