import tkinter as tk
from tkinter import ttk

class WidgetInspector(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#252526")
        
        # Header
        self.header = tk.Label(self, text=" INSPECTEUR D'INTERFACE", bg="#252526", fg="#cccccc", font=("Segoe UI", 9), anchor="w", padx=15, pady=8)
        self.header.pack(side=tk.TOP, fill=tk.X)
        
        # Container
        self.tree_frame = tk.Frame(self, bg="#1e1e1e")
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Styling Treeview to look dark-themed
        style = ttk.Style()
        # Le thème 'clam' gère beaucoup mieux la personnalisation des couleurs sur Windows
        if "clam" in style.theme_names():
            style.theme_use("clam")
        else:
            style.theme_use("default")
            
        style.configure("Treeview", 
                        background="#1e1e1e",
                        foreground="#d4d4d4",
                        fieldbackground="#1e1e1e",
                        borderwidth=0,
                        font=("Segoe UI", 10))
                        
        style.map('Treeview', 
                  background=[('selected', '#37373d')], 
                  foreground=[('selected', 'white')])
                  
        # Fix heading styling 
        style.configure("Treeview.Heading", 
                        background="#252526", 
                        foreground="#cccccc", 
                        font=("Segoe UI", 9, "bold"), 
                        borderwidth=0,
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#333333')])
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse", yscrollcommand=self.scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("#0", text=" Arborescence des Composants", anchor="w")
        self.tree.column("#0", width=200, stretch=True)

    def refresh(self, parent_widget):
        """Récursivement populer l'arbre avec tous les widgets enfants de parent_widget"""
        self.tree.delete(*self.tree.get_children())
        
        # Lancer l'exploration à partir du conteneur de preview
        preview_node = self.tree.insert("", "end", text=" 🪟 Fenêtre Principale (Preview)", open=True)
        self._populate_tree(preview_node, parent_widget)

    def _populate_tree(self, parent_node, current_widget):
        for child in current_widget.winfo_children():
            # Construire le nom lisible
            class_name = child.__class__.__name__
            
            # Essayer de récupérer des infos utiles (texte, cfg de bg...)
            extra_info = ""
            try:
                # Si c'est un bouton/label avec texte
                text = child.cget("text")
                if text:
                    # Tronquer le texte si trop long
                    display_text = text if len(text) < 15 else text[:12] + "..."
                    extra_info = f" \"{display_text}\""
            except:
                pass
                
            node_text = f"▪ {class_name}{extra_info}"
            if class_name in ("Frame", "LabelFrame", "PanedWindow"):
                node_text = f"📂 {class_name}{extra_info}"
            elif class_name in ("Button", "Radiobutton", "Checkbutton"):
                node_text = f"🔘 {class_name}{extra_info}"
            elif class_name in ("Label", "Message"):
                node_text = f"📝 {class_name}{extra_info}"
            elif class_name in ("Entry", "Text"):
                node_text = f"🔤 {class_name}{extra_info}"
            
            # Insérer le composant
            node_id = self.tree.insert(parent_node, "end", text=node_text, open=True)
            
            # Récursion s'il a des enfants
            self._populate_tree(node_id, child)
