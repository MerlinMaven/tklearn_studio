import traceback

class CodeExecutor:
    def __init__(self, editor, preview, console, inspector=None):
        self.editor = editor
        self.preview = preview
        self.console = console
        self.inspector = inspector

    def run_code(self):
        # Nettoyer la zone de prévisualisation
        self.preview.clear()
        
        # Effacer l'inspecteur
        if self.inspector:
            self.inspector.tree.delete(*self.inspector.tree.get_children())
        
        # Récupérer le code de l'éditeur
        code = self.editor.get_code().strip()
        if not code:
            self.console.write("Aucun code à exécuter.")
            return

        # Rediriger print vers la console
        def custom_print(*args, **kwargs):
            sep = kwargs.get("sep", " ")
            message = sep.join(map(str, args))
            self.console.write(message)
            
        # Créer un faux module tkinter pour intercepter `tk.Tk()` et `mainloop()`
        import tkinter as real_tk
        import types
        
        mock_tk = types.ModuleType("tkinter")
        # Copier tout le contenu de real_tk dans mock_tk
        for attr in dir(real_tk):
            setattr(mock_tk, attr, getattr(real_tk, attr))
            
        # Surcharger get_tk_class pour qu'il retourne notre frame de preview
        class MockTk(real_tk.Frame):
            def __init__(self, *args, **kwargs):
                super().__init__(self._preview_frame, *args, **kwargs)
                self.pack(fill=real_tk.BOTH, expand=True)
                
            def title(self, *args, **kwargs):
                pass
                
            def geometry(self, *args, **kwargs):
                pass
                
            def mainloop(self, *args, **kwargs):
                pass
                
            def quit(self, *args, **kwargs):
                pass

            def destroy(self, *args, **kwargs):
                super().destroy()

            def config(self, *args, **kwargs):
                if 'menu' in kwargs:
                    del kwargs['menu']
                super().config(*args, **kwargs)
                
            def configure(self, *args, **kwargs):
                if 'menu' in kwargs:
                    del kwargs['menu']
                super().configure(*args, **kwargs)
                
            def maxsize(self, *args, **kwargs): pass
            def minsize(self, *args, **kwargs): pass
            def resizable(self, *args, **kwargs): pass
            def iconbitmap(self, *args, **kwargs): pass
            def protocol(self, *args, **kwargs): pass
                
        MockTk._preview_frame = self.preview.inner_frame
        mock_tk.Tk = MockTk
        
        environment = {
            "preview_frame": self.preview.inner_frame,
            "print": custom_print,
            "tkinter": mock_tk,
            "tk": mock_tk,
            "__builtins__": __builtins__
        }
        
        # S'assurer que les imports à l'intérieur du exec utilisent notre mock
        import sys
        original_tkinter = sys.modules.get('tkinter')
        sys.modules['tkinter'] = mock_tk
        
        self.console.write("--- Exécution démarrée ---")
        try:
            # Exécuter le code dans l'environnement fourni
            exec(code, environment)
            self.console.write("--- Exécution terminée avec succès ---")
            
            # Mettre à jour l'inspecteur une fois que les widgets ont été créés
            if self.inspector:
                # Rafraîchissement avec un très léger décalage pour laisser Tkinter dessiner
                self.inspector.after(100, lambda: self.inspector.refresh(self.preview.inner_frame))
                
        except Exception as e:
            # Capturer et afficher les erreurs
            error_msg = traceback.format_exc()
            self.console.write("Erreur d'exécution :")
            self.console.write(error_msg)
        finally:
            # Restaurer le module tkinter original
            if original_tkinter is not None:
                sys.modules['tkinter'] = original_tkinter
            else:
                del sys.modules['tkinter']
