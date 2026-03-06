import tkinter as tk

class PreviewFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#252526")
        
        # Header
        self.header = tk.Label(self, text=" PRÉVISUALISATION", bg="#007acc", fg="#ffffff", font=("Segoe UI", 9, "bold"), anchor="w", padx=15, pady=8)
        self.header.pack(side=tk.TOP, fill=tk.X)
        
        self.inner_frame = tk.Frame(self, bg="#f0f0f0") # Keep white/gray for preview to look like normal windows
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
    def clear(self):
        # Destroy all children inside inner_frame
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
