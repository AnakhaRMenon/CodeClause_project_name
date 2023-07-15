import tkinter as tk
from tkinter import filedialog, messagebox


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")

        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menubar)

        # Bind keyboard shortcuts
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-S>", lambda event: self.save_file_as())
        self.root.bind("<Control-q>", lambda event: self.exit_application())
        self.root.bind("<Control-z>", lambda event: self.text_area.edit_undo())
        self.root.bind("<Control-y>", lambda event: self.text_area.edit_redo())
        self.root.bind("<Control-x>", lambda event: self.cut_text())
        self.root.bind("<Control-c>", lambda event: self.copy_text())
        self.root.bind("<Control-v>", lambda event: self.paste_text())
        self.root.bind("<Control-a>", lambda event: self.select_all())

    def new_file(self):
        result = self.confirm_discard_changes()
        if result == "yes":
            self.text_area.delete("1.0", tk.END)
            self.root.title("Text Editor")

    def open_file(self):
        result = self.confirm_discard_changes()
        if result == "yes":
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if file_path:
                try:
                    with open(file_path, "r") as file:
                        content = file.read()
                        self.text_area.delete("1.0", tk.END)
                        self.text_area.insert(tk.END, content)
                    self.root.title("Text Editor - " + file_path)
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def save_file(self):
        file_path = self.root.title().replace("Text Editor - ", "")
        if file_path == "Text Editor":
            self.save_file_as()
        else:
            try:
                with open(file_path, "w") as file:
                    content = self.text_area.get("1.0", tk.END)
                    file.write(content)
                messagebox.showinfo("Saved", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    content = self.text_area.get("1.0", tk.END)
                    file.write(content)
                self.root.title("Text Editor - " + file_path)
                messagebox.showinfo("Saved", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def exit_application(self):
        result = self.confirm_discard_changes()
        if result == "yes":
            self.root.destroy()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return "break"

    def confirm_discard_changes(self):
        if self.text_area.edit_modified():
            return messagebox.askyesnocancel(
                "Unsaved Changes",
                "There are unsaved changes. Do you want to save them?",
                default=messagebox.YES,
            )
        return "yes"


# Create the main window
root = tk.Tk()
root.geometry("600x400")

# Create an instance of the TextEditor
text_editor = TextEditor(root)

root.mainloop()
