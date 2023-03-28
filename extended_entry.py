import tkinter as tk

class EntryWithPlaceholder(tk.Entry):

    def __init__(self, master=None, placeholder = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = 'gray'
        self.default_fg_color = self['foreground']

        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)

        self.set_placeholder()

    def set_placeholder(self):
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color
    
    def on_focus_in(self, event):
        if self['foreground'] == self.placeholder_color:
            self.delete(0,tk.END)
            self['foreground'] = self.default_fg_color
    
    def on_focus_out(self, event):
        if not self.get():
            self.set_placeholder()