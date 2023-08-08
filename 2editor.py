import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import shutil
import time

class SimpleTextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("pyTextEditor32")
        self.root.geometry("600x450")  # Set the default window size to 600x450

        # Frame for line numbers and text widget
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)

        # Text widget for line numbers
        self.line_numbers = tk.Text(self.frame, width=3, padx=3, takefocus=0, border=0, background='lightgray', state='disabled', wrap='none')  # Change the background color to lightgray
        self.line_numbers.pack(side='left', fill='y')

        # Main Text widget
        self.text_widget = tk.Text(self.frame, wrap='none', undo=True)
        self.text_widget.pack(side='right', fill='both', expand=True)

        # Scrollbars
        self.scrollbar = tk.Scrollbar(self.text_widget)
        self.scrollbar.pack(side='right', fill='y')
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_widget.yview)

        # Create menu
        self.create_menu()

        # Create buttons
        self.create_buttons()

        self.file_name = None
        self.auto_save_time = 5.0  # 5 seconds

        # Bind events
        self.root.bind('<Configure>', self.on_resize)
        self.text_widget.bind('<<Change>>', self.on_change)
        self.text_widget.bind('<Configure>', self.on_change)
        self.text_widget.bind('<Control-KeyPress-equal>', self.zoom_in)  # Changed from Plus to equal
        self.text_widget.bind('<Control-minus>', self.zoom_out)  # Changed from Minus to minus
        self.text_widget.bind('<Control-a>', self.select_all)  # Add binding for select all
        self.text_widget.bind('<Control-c>', self.copy_text)  # Add binding for copy
        self.text_widget.bind('<Control-v>', self.paste_text)  # Add binding for paste
        self.text_widget.bind('<Control-z>', self.undo_text)  # Add binding for undo
        self.text_widget.bind('<Control-y>', self.redo_text)  # Add binding for redo

        # Bind the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.handle_window_close)

        # Flag for dark mode
        self.dark_mode = False

    def create_menu(self):
        # Create the main menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.handle_window_close)

        # Create Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo_text)
        edit_menu.add_command(label="Redo", command=self.redo_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)

        # Create View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)

        # Create Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_info)

    def create_buttons(self):
        # Placeholder for button creation
        pass

    def start(self):
        self.root.mainloop()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = 'black' if self.dark_mode else 'white'
        text_color = 'white' if self.dark_mode else 'black'
        self.root.config(bg=bg_color)
        self.text_widget.config(bg=bg_color, fg=text_color)

    def zoom_in(self, event):
        self.text_widget.config(font=("Helvetica", self.text_widget['font'].actual()["size"] + 2))

    def zoom_out(self, event):
        self.text_widget.config(font=("Helvetica", self.text_widget['font'].actual()["size"] - 2))

    def on_resize(self, event):
        # Placeholder for window resize handling
        pass

    def on_change(self, event):
        # Update line numbers
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        lines = self.text_widget.get('1.0', tk.END).split('\\n')  # Changed from '' to '\n'
        line_numbers_string = '\\n'.join(str(no+1) for no in range(len(lines)))  # Add 1 to the line numbers
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')

    def handle_window_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit? All unsaved work will be lost."):
            self.root.destroy()

    def new_file(self):
        self.text_widget.delete(1.0, tk.END)
        self.file_name = None

    def open_file(self):
        self.file_name = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.file_name:
            self.text_widget.delete(1.0, tk.END)
            with open(self.file_name, "r") as file:
                self.text_widget.insert(1.0, file.read())

    def save_file(self):
        if not self.file_name:
            self.save_file_as()
        else:
            with open(self.file_name, "w") as file:
                file.write(self.text_widget.get(1.0, tk.END))

    def save_file_as(self):
        self.file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.file_name:
            with open(self.file_name, "w") as file:
                file.write(self.text_widget.get(1.0, tk.END))

    def redo_text(self):
        self.text_widget.edit_redo()

    def undo_text(self):
        self.text_widget.edit_undo()

    def cut_text(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_widget.event_generate("<<Paste>>")

    def select_all(self):
        self.text_widget.tag_add('sel', '1.0', 'end')

    def show_about_info(self):
        messagebox.showinfo("About", "A simple text editor made with Python and Tkinter.")

if __name__ == "__main__":
    editor = SimpleTextEditor()
    editor.start()
