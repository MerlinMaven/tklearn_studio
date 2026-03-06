import traceback

class CodeExecutor:
    def __init__(self, editor, preview, console, inspector=None, status_bar=None):
        self.editor = editor
        self.preview = preview
        self.console = console
        self.inspector = inspector
        self.status_bar = status_bar
        self._active_bindings = []

    def run_code(self):
        self.preview.clear()
        
        # Nettoyer les anciens bindings clavier
        self._cleanup_bindings()
        
        if self.inspector:
            self.inspector.tree.delete(*self.inspector.tree.get_children())
        
        code = self.editor.get_code().strip()
        if not code:
            self.console.write("Aucun code a executer.", "system")
            return

        if self.status_bar:
            self.status_bar.set_status("Execution...", running=True)

        def custom_print(*args, **kwargs):
            sep = kwargs.get("sep", " ")
            message = sep.join(map(str, args))
            self.console.write(message)
            
        import tkinter as real_tk
        import types
        
        executor_self = self
        root_window = self.preview.winfo_toplevel()
        
        mock_tk = types.ModuleType("tkinter")
        for attr in dir(real_tk):
            setattr(mock_tk, attr, getattr(real_tk, attr))
            
        class MockTk(real_tk.Frame):
            def __init__(self, *args, **kwargs):
                super().__init__(self._preview_frame, *args, **kwargs)
                self.pack(fill=real_tk.BOTH, expand=True)
                # Rendre le frame focusable
                self.configure(takefocus=1)
                
            def title(self, *args, **kwargs): pass
            def geometry(self, *args, **kwargs): pass
            def mainloop(self, *args, **kwargs): pass
            def quit(self, *args, **kwargs): pass

            def destroy(self, *args, **kwargs):
                super().destroy()

            def bind(self, sequence, func=None, add=None):
                """Redirige les bindings clavier vers la fenetre principale."""
                binding_id = root_window.bind(sequence, func, add)
                executor_self._active_bindings.append((sequence, binding_id))
                return binding_id
            
            def bind_all(self, sequence, func=None, add=None):
                """Redirige bind_all vers la fenetre principale."""
                binding_id = root_window.bind(sequence, func, add)
                executor_self._active_bindings.append((sequence, binding_id))
                return binding_id
            
            def unbind(self, sequence, funcid=None):
                root_window.unbind(sequence, funcid)
            
            def after(self, ms, func=None, *args):
                """Redirige after vers la fenetre principale avec error handling."""
                if func is None:
                    return root_window.after(ms)
                def safe_callback(*cb_args):
                    try:
                        func(*cb_args)
                    except Exception as e:
                        import traceback
                        executor_self.console.write("Erreur dans callback :", "error")
                        executor_self.console.write(traceback.format_exc(), "error")
                return root_window.after(ms, safe_callback, *args)
            
            def after_cancel(self, id):
                root_window.after_cancel(id)
            
            def focus_set(self):
                executor_self.preview.inner_frame.focus_set()

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
            
            def winfo_screenwidth(self):
                return root_window.winfo_screenwidth()
            
            def winfo_screenheight(self):
                return root_window.winfo_screenheight()
                
        MockTk._preview_frame = self.preview.inner_frame
        mock_tk.Tk = MockTk
        
        environment = {
            "preview_frame": self.preview.inner_frame,
            "print": custom_print,
            "tkinter": mock_tk,
            "tk": mock_tk,
            "__builtins__": __builtins__
        }
        
        import sys
        original_tkinter = sys.modules.get('tkinter')
        sys.modules['tkinter'] = mock_tk
        
        self.console.write("Execution demarree", "info")
        try:
            exec(code, environment)
            self.console.write("Execution terminee avec succes", "success")
            
            # Donner le focus au preview pour les controles clavier
            self.preview.inner_frame.focus_set()
            
            if self.inspector:
                self.inspector.after(100, lambda: self.inspector.refresh(self.preview.inner_frame))
                
        except Exception as e:
            error_msg = traceback.format_exc()
            self.console.write("Erreur d'execution :", "error")
            self.console.write(error_msg, "error")
        finally:
            if original_tkinter is not None:
                sys.modules['tkinter'] = original_tkinter
            else:
                del sys.modules['tkinter']
            
            if self.status_bar:
                self.status_bar.set_status("Pret")
    
    def _cleanup_bindings(self):
        """Nettoie les bindings clavier des executions precedentes."""
        root_window = self.preview.winfo_toplevel()
        for sequence, binding_id in self._active_bindings:
            try:
                root_window.unbind(sequence, binding_id)
            except:
                pass
        self._active_bindings.clear()
