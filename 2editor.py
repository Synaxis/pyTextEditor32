import tkinter as tk
import threading
import time
from tkinter import filedialog
import os
import shutil

class SimpleTextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.create_widgets()

        self.file_name = None
        self.auto_save_time = 5.0  # 5 seconds
        self.auto_save_thread = threading.Thread(target=self.auto_save)
        self.auto_save_thread.daemon = True
        self.auto_save_thread.start()

        # Bind the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.handle_window_close)

    def create_widgets(self):
        # Create a frame for line numbers and text widget
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)

        # Create a Text widget for line numbers
        self.line_numbers = tk.Text(self.frame, width=4, padx=3, takefocus=0, border=0, background='khaki', state='disabled', wrap='none')
        self.line_numbers.pack(side='left', fill='y')

        # Create the main Text widget
        self.text_widget = tk.Text(self.frame, wrap='none')
        self.text_widget.pack(side='right', fill='both', expand=True)

        # Bind events
        self.root.bind('<Configure>', self.on_resize)
        self.text_widget.bind('<<Change>>', self.on_change)
        self.text_widget.bind('<Configure>', self.on_change)

        # Create menu
        self.create_menu()

    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Close", command=self.close_file)
        filemenu.add_command(label="Duplicate", command=self.duplicate_file)

    def auto_save(self):
        while True:
            time.sleep(self.auto_save_time)
            if self.file_name is not None:
                current_text = self.text_widget.get('1.0', 'end-1c')
                with open(self.file_name, 'w') as f:
                    f.write(current_text)

    def handle_window_close(self):
        """Handles the window close event."""
        # You can add any additional cleanup here before destroying the window
        self.root.destroy()

    def on_resize(self, event):
        """Handles the window resize event."""
        width, height = event.width, event.height
        self.text_widget.config(width=width, height=height)

    def on_change(self, event):
        """Update line numbers"""
        lines = self.text_widget.get("1.0", "end-1c").count("\n") + 1
        line_numbers = "\n".join(str(i) for i in range(1, lines + 1))
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        self.line_numbers.insert('1.0', line_numbers)
        self.line_numbers.config(state='disabled')

    def new_file(self):
        self.file_name = "untitled.txt"
        self.text_widget.delete('1.0', 'end')

    def open_file(self):
        self.file_name = filedialog.askopenfilename(defaultextension=".txt",
                                                    filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.file_name == "":
            self.file_name = None
        else:
            self.root.title(os.path.basename(self.file_name) + " - Editor")
            self.text_widget.delete(1.0, "end")
            with open(self.file_name, "r") as file:
                self.text_widget.insert(1.0, file.read())

    def save_file(self):
        if self.file_name is None:
            self.file_name = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if self.file_name == "":
                self.file_name = None
            else:
                # Try to save the file
                with open(self.file_name, "w") as file:
                    file.write(self.text_widget.get(1.0, "end"))
                self.root.title(os.path.basename(self.file_name) + " - Editor")
        else:
            with open(self.file_name, "w") as file:
                file.write(self.text_widget.get(1.0, "end"))

    def close_file(self):
        self.file_name = None
        self.text_widget.delete('1.0', 'end')

    def duplicate_file(self):
        if self.file_name is not None:
            new_file_path = os.path.splitext(self.file_name)[0] + '_copy' + os.path.splitext(self.file_name)[1]
            shutil.copy(self.file_name, new_file_path)

    def start(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error during application execution: {e}")
        finally:
            # Ensure the application window is destroyed before exiting
            if self.root:
                try:
                    self.root.destroy()
                except tk.TclError:
                    pass


if __name__ == "__main__":
    editor = SimpleTextEditor()
    editor.start()

