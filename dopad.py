# Dopad Text Editor
# Version 1.0
# Doyok Developer
# https://github.com/yogasaputra2896

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import Menu, filedialog, messagebox, simpledialog, colorchooser, END
from datetime import datetime
import os
import win32api
import subprocess
import sys

# Inisialisasi Variabel Global
current_file = None
current_font_size = 10
font_color = "black"
bg_color = "white"
app_path = os.path.dirname(os.path.abspath(__file__))
app_data_local_path = os.getenv('LOCALAPPDATA')
app_data_path = os.path.join(app_data_local_path, "dopad")
config_path = os.path.join(app_data_path, "config")
temp_path = os.path.join(app_data_path, "temp")
icon_path = os.path.join(app_path, "icon-dopad.ico")

# Fungsi Membuat Folder
def make_folder():
    # Membuat Folder config
    if not os.path.exists(config_path):
        try:
            os.makedirs(config_path)
        except OSError as e:
            messagebox.showerror("Error", "Unable to create the 'config' folder. Please check your access permissions or run as administrator.")
           

    # Membuat Folder temp
    if not os.path.exists(temp_path):
        try:
            os.makedirs(temp_path)
        except OSError as e:
            messagebox.showerror("Error", "Unable to create the 'config' folder. Please check your access permissions or run as administrator.")
            
# Membuat Fungsi Update Title
def update_title():
    global current_file
    if current_file:
        window.title(f"{os.path.basename(current_file)} - Dopad")
    else:
        window.title("Untitled - Dopad")

# Membuat Fungsi New File
def new_file(event=None):
    global current_file
    if textbox_scrol.get("1.0", tk.END).strip():
        respon = messagebox.askyesnocancel("Dopad", "Do you want to save changes to the current document?")
        if respon == True:
            save_file()
        elif respon == None:  
            return  
    textbox_scrol.delete("1.0", tk.END) 
    current_file = None
    update_title()

# Membuat Fungsi Open File
def open_file(event=None):
    global current_file
    
    if textbox_scrol.get("1.0", tk.END).strip():
        respon = messagebox.askyesnocancel("Dopad", "Do you want to save changes to the current document?")
        if respon == True:
            save_file()

    file_path = filedialog.askopenfilename(defaultextension=".dopad", filetypes=[("Dopad Files", "*.dopad"), ("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_file = file_path  
        try:
            with open(current_file, "r") as file:
                content = file.read()
                if current_file.endswith(".dopad"):
                    load_format(file_path)
                textbox_scrol.delete("1.0", tk.END)
                textbox_scrol.insert(tk.INSERT, content)
            update_title()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening file: {e}. The file may be corrupted or the format is unsupported")

# Membuat Fungsi Save File
def save_file(event=None):
    global current_file
    if current_file:
        try:
            save_dopad_file()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save the file: {e}. Please verify file path and permissions")
    else:
        save_as_file()

# Membuat Fungsi Save As File
def save_as_file(event=None):
    global current_file
    file_path = filedialog.asksaveasfilename(defaultextension=".dopad", filetypes=[("Dopad Files", "*.dopad"), ("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_file = file_path
        if current_file.endswith(".dopad"):
            save_dopad_file()  
        else:
            save_text_file() 
        update_title()

# Membuat Fungsi Save Dopad File
def save_dopad_file():
    content = textbox_scrol.get("1.0", tk.END)
    with open(current_file, "w") as file:
        file.write(content)
    save_format(current_file) 

# Membuat Fungsi Save Text File
def save_text_file():
    content = textbox_scrol.get("1.0", tk.END)
    try:
        with open(current_file, "w") as file:
            file.write(content)
        textbox_scrol.config(font=("Lucida Console", 10), bg='white', fg='black')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save text file: {e}")

# Membuat Fungsi Save Format di .ini
def save_format(file_path):
    ini_file = os.path.join(config_path, os.path.basename(file_path) + ".ini") 
    with open(ini_file, "w") as file:
        file.write(f"font_size={current_font_size}\n")
        file.write(f"font_color={font_color}\n")
        file.write(f"bg_color={bg_color}\n")

# Membuat Fungsi Load Format dari .ini
def load_format(file_path):
    ini_file = os.path.join(config_path, os.path.basename(file_path) + ".ini")  # Muat dari sub-folder config
    if os.path.exists(ini_file):
        with open(ini_file, "r") as file:
            lines = file.readlines()
            size_line = lines[0].split("=")[1].strip()
            color_line = lines[1].split("=")[1].strip()
            bg_line = lines[2].split("=")[1].strip()
            apply_format(int(size_line), color_line, bg_line)
    else:
        messagebox.showwarning("config", "Unable to locate the configuration file. Default text formatting will be applied")
        apply_format(10, "black", "white")

# Membuat Fungsi Apply Format
def apply_format(size, color, bg):
    global current_font_size, font_color, bg_color
    current_font_size = size
    font_color = color
    bg_color = bg
    textbox_scrol.config(font=("Lucida Console", current_font_size), fg=font_color, bg=bg_color)

# Membuat Fungsi Exit
def exit_app(event=None):
    if textbox_scrol.get("1.0", tk.END).strip():
        respon = messagebox.askyesnocancel("Dopad", "Do you want to save changes before exiting?")
        if respon == True:
            save_file() 
            window.quit() 
        elif respon == False:  
            window.quit() 
    else:
        window.quit()


# Membuat Fungsi Undo
def undo(event=None):
    try:
        textbox_scrol.edit_undo()
    except tk.TclError:
        pass

# Membuat Fungsi Redo
def redo(event=None):
    try:
        textbox_scrol.edit_redo()
    except tk.TclError:
        pass

# Membuat Fungsi Cut
def cut(event=None):
    textbox_scrol.event_generate("<<Cut>>")

# Membuat Fungsi Copy
def copy(event=None):
    textbox_scrol.event_generate("<<Copy>>")

# Membuat Fungsi Paste
def paste(event=None):
    textbox_scrol.event_generate("<<Paste>>")

# Membuat Fungsi Delete
def delete(event=None):
    textbox_scrol.delete("sel.first", "sel.last")

# Membuat Fungsi Find
def find_text(event=None):
    find_string = simpledialog.askstring("Find", "Enter text:", parent=window)
    textbox_scrol.tag_remove("found", "1.0", tk.END)
    if find_string:
        idx = "1.0"
        while True:
            idx = textbox_scrol.search(find_string, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            lastidx = f"{idx}+{len(find_string)}c"
            textbox_scrol.tag_add("found", idx, lastidx)
            idx = lastidx
        textbox_scrol.tag_config("found", foreground="white", background="blue")
        first_found = textbox_scrol.tag_ranges("found")
        if first_found:
            textbox_scrol.see(first_found[0])  
            textbox_scrol.mark_set("insert", first_found[0])

# Membuat Fungsi Clear Find
def clear_highlight(event=None):
    textbox_scrol.tag_remove("found", "1.0", tk.END)
    

# Membuat Fungsi Replace
def replace_text(event=None):
    find_string = simpledialog.askstring("Find", "Enter text to find:", parent=window)
    replace_string = simpledialog.askstring("Replace", "Enter text to replace with:",parent=window)
    content = textbox_scrol.get("1.0", tk.END)
    new_content = content.replace(find_string, replace_string)
    textbox_scrol.delete("1.0", tk.END)
    textbox_scrol.insert("1.0", new_content)

# Membuat Fungsi Select All
def select_all(event=None):
    textbox_scrol.tag_add("sel", "1.0", "end")

# Membuat Fungsi Mode Light
def mode_light(event=None):
    window.configure(bg='white')
    textbox_scrol.configure(bg='white', fg='black', insertbackground='black')

# Membuat Fungsi Mode Dark
def mode_dark(event=None):
    window.configure(bg='grey15')
    textbox_scrol.configure(bg='grey15', fg='white', insertbackground='white')

# Membuat Fungsi Insert 
def insert_time_date(event=None):
    now = datetime.now()
    format_dt = now.strftime("%A, %d %B %Y, %H:%M:%S")
    textbox_scrol.insert(tk.INSERT, format_dt)

# Membuat Fungsi Insert From File
def insert_from_file(event = None):
    file_path = filedialog.askopenfilename(defaultextension=".dopad", filetypes=[("Dopad Files", "*.dopad"), ("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read().rstrip('\n')
            textbox_scrol.insert(END, content)

# Membuat Fungsi Insert Charakter Spesial
def insert_special_character():
    try:
        subprocess.Popen('charmap.exe')
        char = simpledialog.askstring("Special Character", "Enter character to insert:",parent=window)
        window.clipboard_get() 
        if char:
            textbox_scrol.insert(tk.INSERT, char)
    except FileNotFoundError:
        print("Character Map not found in your system.")
    
    
# Membuat Fungsi Ukuran Font
def change_font_size(event=None):
    global current_font_size
    new_size = simpledialog.askinteger("Font Size", "Enter new font size:", parent=window, minvalue=1, maxvalue=5000)
    if new_size:
        current_font_size = new_size
        textbox_scrol.config(font=("Lucida Console", current_font_size))

# Membuat Fungsi Warna Font
def change_font_color(event=None):
    global font_color
    color = colorchooser.askcolor(title="Choose Font Color")
    if color[1]:
        font_color = color[1]
        textbox_scrol.config(fg=font_color)

# Membuat Fungsi Warna Background
def change_bg_color(event=None):
    global bg_color
    color = colorchooser.askcolor(title="Choose Background Color")
    if color[1]:
        bg_color = color[1]
        textbox_scrol.config(bg=bg_color)

# Convert .dopad to .html
def save_as_html():
    global current_font_size, font_color, bg_color
    if not current_file:
        messagebox.showerror("Error", "Please save the file before exporting it to HTML.")
        return None

    base_filename = os.path.basename(current_file).replace(".dopad", ".html")
    html_file = os.path.join(temp_path, base_filename)
    content = textbox_scrol.get("1.0", tk.END)
    escaped_content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    html_content = f"""
    <html>
    <head>
    <style>
        body {{
            font-family: 'Lucida Console';
            font-size: {current_font_size}px;
            color: {font_color};
            background-color: {bg_color} !important;
            white-space: pre-wrap;
        }}
        @media print {{
            body {{
                -webkit-print-color-adjust: exact;  
                print-color-adjust: exact;         
            }}
        }}
    </style>
    </head>
    <body>{escaped_content}</body>
    </html>
    """
    
    try:
        with open(html_file, "w") as file:
            file.write(html_content)
        return html_file
    except Exception as e:
        messagebox.showerror("Error", f"Unable to save the HTML file: {e}. Please verify the file path and permissions")
        return None

# Membuat Fungsi Print
def print_file(event=None):
    global current_file
    if not current_file:
        messagebox.showerror("Error", "Please save the file before printing")
        return
    
    try:
        html_file = save_as_html()
        if html_file:
            win32api.ShellExecute(0, "print", html_file, None, ".", 1)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to print the file: {e}. Please verify printer settings or try again")

# Membuat Fungsi About me
def about_me():
    messagebox.showinfo("About Me", " Dopad Text Editor\n Version : 1.0\n Build : 241010 \n By Doyok Developer")

# Membuat Fungsi Open Dari File Dopad
def open_file_from_args():
    global current_file
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            try:
                current_file = file_path
                with open(current_file, "r") as file:
                    content = file.read()
                    if current_file.endswith(".dopad"):
                        load_format(current_file)
                    textbox_scrol.delete("1.0", tk.END)
                    textbox_scrol.insert(tk.INSERT, content)
                update_title()
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open the file from argument: {e}")
        else:
            messagebox.showerror("Error", f"The file '{file_path}' does not exist. Please check the file path and try again.")


# Membuat Fungsi Show Window
def show_window():
    global window, textbox_scrol

    window = tk.Tk()
    window_width = 850
    window_height = 550
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_win = int((screen_width - window_width) / 2)
    y_win = int((screen_height - window_height) / 2)
    window.title("Untitled - Dopad")
    window.geometry(f"{window_width}x{window_height}+{x_win}+{y_win}")
    window.resizable(True, True)
    window.minsize(550, 350)

    #Cek icon file
    try:
        window.iconbitmap(icon_path)
    except:
        pass

    #Menjalankan Fungsi Membuat folder
    make_folder()

    dopad_menu = Menu(window)
    window.configure(menu=dopad_menu)

    # Menu File
    file_menu = Menu(dopad_menu, tearoff=False)
    dopad_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New                Ctrl + N", command=new_file)
    file_menu.add_command(label="Open              Ctrl + O", command=open_file)
    file_menu.add_command(label="Save                Ctrl + S", command=save_file)
    file_menu.add_command(label="Save As          Ctrl + Shift + S", command=save_as_file)
    file_menu.add_separator()
    file_menu.add_command(label="Print                Ctrl + P", command=print_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit                 Alt + F4", command=exit_app)

    # Menu Edit
    edit_menu = Menu(dopad_menu, tearoff=False)
    dopad_menu.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Undo                Ctrl + Z", command=undo)
    edit_menu.add_command(label="Redo                Ctrl + Y", command=redo)
    edit_menu.add_separator()
    edit_menu.add_command(label="Cut                   Ctrl + X", command=cut)
    edit_menu.add_command(label="Copy                Ctrl + C", command=copy)
    edit_menu.add_command(label="Paste                Ctrl + V", command=paste)
    edit_menu.add_command(label="Delete                  Del", command=delete)
    edit_menu.add_separator()
    edit_menu.add_command(label="Find                  Ctrl + F", command=find_text)
    edit_menu.add_command(label="Replace            Ctrl + H", command=replace_text)
    edit_menu.add_separator()
    edit_menu.add_command(label="Select All         Ctrl + A", command=select_all)

    # Menu Format
    format_menu = Menu(dopad_menu, tearoff=False)
    dopad_menu.add_cascade(label="Format", menu=format_menu)
    format_menu.add_command(label="Change Font Size", command=change_font_size)
    format_menu.add_command(label="Change Font Color", command=change_font_color)
    format_menu.add_command(label="Change Background Color", command=change_bg_color)

    # Menu View
    view_menu = Menu(dopad_menu, tearoff=False)
    dopad_menu.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Light Mode         Ctrl + 1", command=mode_light)
    view_menu.add_command(label="Dark Mode          Ctrl + 2", command=mode_dark)

    # Menu Insert
    insert_menu = Menu(dopad_menu, tearoff=False)
    dopad_menu.add_cascade(label="Insert", menu=insert_menu)
    insert_menu.add_command(label="Insert Date/Time        Ctrl + D", command=insert_time_date)
    insert_menu.add_command(label="Insert From File     .dopad |.txt", command=insert_from_file)
    insert_menu.add_command(label="Insert Special Characters", command=insert_special_character)

     # Menu Help
    help_menu = Menu(dopad_menu, tearoff=False)
    dopad_menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About Me", command=about_me)

    # Textbox
    textbox_scrol = ScrolledText(window, wrap=tk.WORD, font=("Lucida Console", current_font_size), fg=font_color, bg=bg_color, undo=True)
    textbox_scrol.pack(expand=True, fill='both')

    # Shortcut keys
    window.bind('<Control-n>', new_file)
    window.bind('<Control-o>', open_file)
    window.bind('<Control-s>', save_file)
    window.bind('<Control-Shift-s>', save_as_file)
    window.bind('<Control-f>', find_text)
    window.bind('<Control-y>', redo)
    window.bind('<Control-x>', cut)
    window.bind('<Control-c>', copy)
    window.bind('<Control-p>', print_file)
    window.bind('<Control-a>', select_all)
    window.bind('<Control-h>', replace_text)
    window.bind('<Control-Key-1>', mode_light)
    window.bind('<Control-Key-2>', mode_dark)
    window.bind('<Control-Key-d>', insert_time_date)
    textbox_scrol.bind("<Button-1>", clear_highlight)
    window.protocol("WM_DELETE_WINDOW", exit_app)

    #Menjalankan Fungsi Open Dari File Dopad
    open_file_from_args()

    # Menampilkan Window
    window.mainloop()

# Menjalankan Program
if __name__ == "__main__":
    show_window()
