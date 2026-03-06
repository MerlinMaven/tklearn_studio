import tkinter as tk

class ConsoleOutput(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#252526")
        
        # Header
        self.header = tk.Label(self, text=" TERMINAL ET SORTIE", bg="#1e1e1e", fg="#cccccc", font=("Segoe UI", 9), anchor="w", padx=15, pady=8)
        self.header.pack(side=tk.TOP, fill=tk.X)
        
        self.text_widget = tk.Text(self, height=8, state='disabled', bg="#000000", fg="#4af626", font=("Consolas", 11), relief=tk.FLAT, padx=10, pady=5)
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 2))
        
    def write(self, message):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, message + "\n")
        self.text_widget.configure(state='disabled')
        self.text_widget.see(tk.END)
        
    def clear(self):
        self.text_widget.configure(state='normal')
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.configure(state='disabled')
