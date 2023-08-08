
import tkinter as tk
from tkinter import font, filedialog, messagebox, simpledialog

class SimpleTextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("pyTextEditor32")
        self.root.geometry("600x450")

        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side='right', fill='y')

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)

        self.line_numbers = tk.Text(self.frame, width=3, padx=3, takefocus=0, border=0, background='lightgray', state='disabled', wrap='none', yscrollcommand=self.scrollbar.set)
        self.line_numbers.pack(side='left', fill='y')

        self.font_family = self.get_font_family()
        self.base_font_size = 14
        self.text_font = font.Font(family=self.font_family, size=self.base_font_size)

        self.text_widget = tk.Text(self.frame, wrap='none', undo=True, font=self.text_font, yscrollcommand=self.scrollbar.set)
        self.text_widget.pack(side='right', fill='both', expand=True)
        self.scrollbar.config(command=self.yview)

        self.create_menu()

        self.file_name = None

        self.bind_events()

        self.dark_mode = False
        self.word_wrap = False

    def get_font_family(self):
        available_fonts = font.families()
        return next((f for f in ["OpenSans", "Helvetica", "Courier", "NotoSans"] if f in available_fonts), "Helvetica")

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.handle_window_close)

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

        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        view_menu.add_command(label="Increase Font Size", command=self.zoom_in)
        view_menu.add_command(label="Decrease Font Size", command=self.zoom_out)
        view_menu.add_command(label="Toggle Wrap", command=self.toggle_wrap)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_info)

    def bind_events(self):
        self.root.bind('<Configure>', self.update_line_numbers)
        self.text_widget.bind('<<Change>>', self.update_line_numbers)
        self.text_widget.bind('<Configure>', self.update_line_numbers)
        self.text_widget.bind('<Control-equal>', self.zoom_in)
        self.text_widget.bind('<Control-minus>', self.zoom_out)
        self.text_widget.bind('<Control-MouseWheel>', self.zoom_mousewheel)
        self.text_widget.bind('<Control-f>', self.find_text)
        self.text_widget.bind('<Control-a>', self.select_all)
        self.text_widget.bind('<Alt-z>', self.toggle_wrap)
        self.root.protocol("WM_DELETE_WINDOW", self.handle_window_close)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = 'black' if self.dark_mode else 'white'
        fg_color = 'white' if self.dark_mode else 'black'
        self.root.config(bg=bg_color)
        self.text_widget.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)

    def zoom_in(self, event=None):
        self.adjust_font_size(2)

    def zoom_out(self, event=None):
        self.adjust_font_size(-2)

    def zoom_mousewheel(self, event):
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def adjust_font_size(self, delta):
        self.base_font_size += delta
        self.base_font_size = max(min(self.base_font_size, 72), 1)  # Limit the font size between 1 and 72
        self.text_font.configure(size=self.base_font_size)
        self.text_widget.config(font=self.text_font)

    def find_text(self, event=None):
        find_string = simpledialog.askstring("Find...", "Enter text to find")
        if find_string:
            start = self.text_widget.index("1.0")
            end = self.text_widget.index("end")
            self.text_widget.tag_remove('find', start, end)
            idx = start
            while True:
                idx = self.text_widget.search(find_string, idx, nocase=1, stopindex=end)
                if not idx:
                    break
                lastidx = f'{idx}+{len(find_string)}c'
                self.text_widget.tag_add('find', idx, lastidx)
                idx = lastidx
            self.text_widget.tag_config('find', foreground='red', background='yellow')

    def toggle_wrap(self, event=None):
        self.word_wrap = not self.word_wrap
        wrap_mode = 'word' if self.word_wrap else 'none'
        self.text_widget.config(wrap=wrap_mode)

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        lines = self.text_widget.get('1.0', tk.END).split('\n')
        line_numbers_string = '\n'.join(str(no+1) for no in range(len(lines)))
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')

    def yview(self, *args):
        self.text_widget.yview(*args)
        self.line_numbers.yview(*args)

    def handle_window_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit? All unsaved work will be lost."):
            self.root.destroy()

    def new_file(self):
        self.text_widget.delete(1.0, tk.END)
        self.file_name = None

    def open_file(self):
        file_name = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if file_name:
            self.file_name = file_name

            self.load_file()

    def load_file(self):
        with open(self.file_name, "r") as file:
            file_contents = file.read()
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, file_contents)

    def save_file(self):
        if self.file_name is None:
            self.save_file_as()
        else:
            try:
                file_contents = self.text_widget.get(1.0, tk.END)
                with open(self.file_name, "w") as file:
                    file.write(file_contents)
            except Exception as e:
                messagebox.showerror("Error saving file", str(e))

    def save_file_as(self):
        try:
            new_file_name = filedialog.asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if new_file_name:
                self.file_name = new_file_name
                self.save_file()
        except Exception as e:
            messagebox.showerror("Error saving file", str(e))

    def undo_text(self, event=None):
        try:
            self.text_widget.edit_undo()
        except tk.TclError:
            pass

    def redo_text(self, event=None):
        try:
            self.text_widget.edit_redo()
        except tk.TclError:
            pass

    def cut_text(self, event=None):
        self.copy_text()
        self.text_widget.delete("sel.first", "sel.last")

    def copy_text(self, event=None):
        self.text_widget.clipboard_clear()
        text = self.text_widget.get("sel.first", "sel.last")
        self.text_widget.clipboard_append(text)

    def paste_text(self, event=None):
        self.text_widget.insert(tk.INSERT, self.text_widget.clipboard_get())

    def select_all(self, event=None):
        self.text_widget.tag_add("sel", "1.0", tk.END)

    def show_about_info(self):
        messagebox.showinfo("About", "A simple text editor built with Python and Tkinter.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    editor = SimpleTextEditor()
    editor.run()
