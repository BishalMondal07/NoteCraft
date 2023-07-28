import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, scrolledtext,  OptionMenu
from tkinter import font
from tkinter import ttk
from tkinter import *
import tkinter.font as tkfont
import enchant
from datetime import datetime

current_file = None
unsaved_changes = False

def toggle_theme():
    global current_theme
    if current_theme == "light":
        set_dark_theme()
    else:
        set_light_theme()

def set_dark_theme():
    global current_theme
    current_theme = "dark"
    root.config(bg="#363636")
    entry.config(bg="#000000", fg="#ffffff", selectbackground="#4a4a4a", selectforeground="#ffffff")
    menu_bar.config(bg="#363636", fg="#ffffff")
    file_menu.config(bg="#363636", fg="#ffffff")
    edit_menu.config(bg="#363636", fg="#ffffff")
    format_menu.config(bg="#363636", fg="#ffffff")
    view_menu.config(bg="#363636", fg="#ffffff")
    theme_menu.config(bg="#363636", fg="#ffffff")
    theme_menu.entryconfig("Dark Mode", state="disabled")
    theme_menu.entryconfig("Light Mode", state="normal")

def set_light_theme():
    global current_theme
    current_theme = "light"
    root.config(bg="#ffffff")
    entry.config(bg="#ffffff", fg="#000000", selectbackground="#c5c5c5", selectforeground="#000000")
    menu_bar.config(bg="#ffffff", fg="#000000")
    file_menu.config(bg="#ffffff", fg="#000000")
    edit_menu.config(bg="#ffffff", fg="#000000")
    format_menu.config(bg="#ffffff", fg="#000000")
    view_menu.config(bg="#ffffff", fg="#000000")
    theme_menu.config(bg="#ffffff", fg="#000000")
    theme_menu.entryconfig("Dark Mode", state="normal")
    theme_menu.entryconfig("Light Mode", state="disabled")

def cut():
    entry.event_generate("<<Cut>>")

def copy():
    entry.event_generate("<<Copy>>")

def paste():
    entry.event_generate("<<Paste>>")

def delete():
    entry.event_generate("<<Clear>>")

def undo():
    entry.event_generate("<<Undo>>")

def redo():
    entry.event_generate("<<Redo>>")

def select_all():
    entry.event_generate("<<SelectAll>>")

def find_replace():
    find_replace_window = tk.Toplevel(root)
    find_replace_window.title("Find/Replace")

    find_label = tk.Label(find_replace_window, text="Find:")
    find_label.grid(row=0, column=0, sticky=tk.W)

    find_entry = tk.Entry(find_replace_window)
    find_entry.grid(row=0, column=1)

    replace_label = tk.Label(find_replace_window, text="Replace:")
    replace_label.grid(row=1, column=0, sticky=tk.W)

    replace_entry = tk.Entry(find_replace_window)
    replace_entry.grid(row=1, column=1)

    find_button = tk.Button(find_replace_window, text="Find", command=lambda: find_text(find_entry.get()))
    find_button.grid(row=2, column=0, pady=5)

    replace_button = tk.Button(find_replace_window, text="Replace", command=lambda: replace_text(find_entry.get(), replace_entry.get()))
    replace_button.grid(row=2, column=1, pady=5)

def make_bold():
    current_font = tkfont.Font(entry, entry.cget("font"))
    if current_font.actual()["weight"] == "normal":
        entry.config(font=(current_font.actual()["family"], current_font.actual()["size"], "bold"))
    else:
        entry.config(font=(current_font.actual()["family"], current_font.actual()["size"], "normal"))

def make_italic():
    current_font = tkfont.Font(entry, entry.cget("font"))
    if current_font.actual()["slant"] == "roman":
        entry.config(font=(current_font.actual()["family"], current_font.actual()["size"], "italic"))
    else:
        entry.config(font=(current_font.actual()["family"], current_font.actual()["size"], "roman"))

def underline():
    current_tags = entry.tag_names('sel.first')
    if 'underline' in current_tags:
        entry.tag_remove('underline', 'sel.first', 'sel.last')
    else:
        entry.tag_add('underline', 'sel.first', 'sel.last')
        entry.tag_config('underline', underline=True)

def find_text(find_str):
    entry.tag_remove("highlight", "1.0", tk.END)
    count = tk.StringVar()
    count_label = tk.Label(root, textvariable=count, bg="#e1e1e1")
    count_label.place(x=10, y=10, anchor=tk.NW)
    count.set("Matches: 0")

    start_pos = "1.0"
    match_count = 0
    while True:
        start_pos = entry.search(find_str, start_pos, tk.END, nocase=True, stopindex=tk.END)
        if not start_pos:
            break
        end_pos = f"{start_pos}+{len(find_str)}c"
        entry.tag_add("highlight", start_pos, end_pos)
        match_count += 1
        start_pos = end_pos

    count.set(f"Matches: {match_count}")

def open_find_replace_window():
    find_replace_window = tk.Toplevel(root)
    find_replace_window.title("Find/Replace")

    find_label = tk.Label(find_replace_window, text="Find:")
    find_label.grid(row=0, column=0, padx=5, pady=5)

    find_entry = tk.Entry(find_replace_window)
    find_entry.grid(row=0, column=1, padx=5, pady=5)

    replace_label = tk.Label(find_replace_window, text="Replace:")
    replace_label.grid(row=1, column=0, padx=5, pady=5)

    replace_entry = tk.Entry(find_replace_window)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)

    find_button = tk.Button(find_replace_window, text="Find", command=lambda: find_text(find_entry.get()))
    find_button.grid(row=2, column=0, padx=5, pady=5)

    replace_button = tk.Button(find_replace_window, text="Replace", command=lambda: replace_text(find_entry.get(), replace_entry.get()))
    replace_button.grid(row=2, column=1, padx=5, pady=5)

def find_text(find_str):
    entry.tag_remove("highlight", "1.0", tk.END)
    count = 0
    start_pos = "1.0"
    while True:
        start_pos = entry.search(find_str, start_pos, tk.END, nocase=True)
        if start_pos == "":
            break
        end_pos = f"{start_pos}+{len(find_str)}c"
        entry.tag_add("highlight", start_pos, end_pos)
        count += 1
        start_pos = end_pos
    if count == 0:
        messagebox.showinfo("Find", "Text not found.")

def replace_text(find_str, replace_str):
    start_pos = "1.0"
    while True:
        start_pos = entry.search(find_str, start_pos, tk.END, nocase=True)
        if start_pos == "":
            break
        end_pos = f"{start_pos}+{len(find_str)}c"
        entry.delete(start_pos, end_pos)
        entry.insert(start_pos, replace_str)
        start_pos = end_pos

def update_line_numbers(event=None):
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete("1.0", tk.END)
    line_count = str(entry.get("1.0", tk.END)).count("\n")
    for line in range(1, line_count + 2):
        line_numbers.insert(tk.END, str(line) + "\n")
    line_numbers.config(state=tk.DISABLED)

def update_unsaved_changes(event=None):
    global unsaved_changes
    unsaved_changes = True
    update_window_title()

def open_file():
    global current_file, unsaved_changes
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            entry.delete("1.0", tk.END)
            entry.insert(tk.END, content)
        current_file = file_path
        unsaved_changes = False
        update_window_title()

def align_left():
    entry.tag_configure("left", justify="left")
    entry.tag_add("left", "sel.first", "sel.last")

def align_center():
    entry.tag_configure("center", justify="center")
    entry.tag_add("center", "sel.first", "sel.last")

def align_right():
    entry.tag_configure("right", justify="right")
    entry.tag_add("right", "sel.first", "sel.last")

def check_spelling():
    text = entry.get("1.0", "end-1c")  
    words = text.split()  
    spell_checker = enchant.Dict("en_US")

    misspelled_words = []
    for word in words:
        if not spell_checker.check(word):
            misspelled_words.append(word)

    if misspelled_words:
        message = "Misspelled words:\n" + "\n".join(misspelled_words)
    else:
        message = "No misspelled words found."

    messagebox.showinfo("Spell Check Results", message)

def save_file():
    global current_file, unsaved_changes
    if current_file:
        content = entry.get("1.0", tk.END)
        with open(current_file, "w") as file:
            file.write(content)
        unsaved_changes = False
        update_window_title()

def save_file_as():
    global current_file, unsaved_changes
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        content = entry.get("1.0", tk.END)
        with open(file_path, "w") as file:
            file.write(content)
        current_file = file_path
        unsaved_changes = False
        update_window_title()

def new_file():
    global current_file, unsaved_changes
    if unsaved_changes:
        result = messagebox.askyesnocancel("Save Changes", "Do you want to save the changes?")
        if result is None:
            return
        elif result:
            save_file()
    current_file = None
    entry.delete("1.0", tk.END)
    unsaved_changes = False
    update_window_title()

def update_window_title():
    global current_file, unsaved_changes
    if current_file:
        file_name = current_file.split("/")[-1]
        if unsaved_changes:
            file_name += "*"
        root.title(file_name)
    else:
        if unsaved_changes:
            root.title("Untitled*")
        else:
            root.title("Untitled")
            
def insert_time_date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    entry.insert(tk.INSERT, f"{current_date} {current_time}")

root = tk.Tk()
root.geometry("800x600")
root.title("NoteCraft")

# Set Roboto font
font = ("Roboto", 12)
root.option_add("*Font", font)

# Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", accelerator="Ctrl+N", command=new_file)
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Alt+F4", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=cut)
edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=copy)
edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=paste)
edit_menu.add_command(label="Delete", accelerator="Del", command=delete)
edit_menu.add_separator()
edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=undo)
edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=select_all)
edit_menu.add_command(label="Find/Replace", command=open_find_replace_window)
edit_menu.add_command(label="Spell Check", command=check_spelling)
edit_menu.add_separator()
edit_menu.add_command(label="Time/Date", command=insert_time_date)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
# Format Menu
format_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Format", menu=format_menu)
available_fonts = [
    "Arial",
    "Times New Roman",
    "Courier New",
    "Verdana",
    "Georgia",
    "Comic Sans MS",
    "Roboto",
    "Calibri",
    "Helvetica",
    "Impact",
    "Lucida Console",
    "Tahoma",
    "Trebuchet MS",
    "Consolas",
    "Monaco",
    "Candara",
    "Garamond",
    "Palatino",
    "Century Gothic",
    "MS Sans Serif"
]
font_menu = tk.Menu(format_menu, tearoff=0)
format_menu.add_cascade(label="Font", menu=font_menu)
font_var = tk.StringVar()
font_var.set("Roboto")
for font_name in available_fonts:
    font_menu.add_radiobutton(label=font_name, variable=font_var, command=lambda font=font_name: entry.config(font=(font, 12)))
format_menu.add_separator()
format_menu.add_command(label="Bold", command=make_bold)
format_menu.add_command(label="Italic", command=make_italic)
format_menu.add_command(label="Underline", command=underline)
align_menu = tk.Menu(format_menu, tearoff=False)
format_menu.add_cascade(label="Alignment", menu=align_menu)
align_menu.add_command(label="Left", command=align_left)
align_menu.add_command(label="Center", command=align_center)
align_menu.add_command(label="Right", command=align_right)

# View Menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
zoom_menu = tk.Menu(view_menu, tearoff=False)
theme_menu = tk.Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Dark Mode", command=set_dark_theme)
theme_menu.add_command(label="Light Mode", command=set_light_theme)
view_menu.add_checkbutton(label="Send Feedback", command=lambda: messagebox.showinfo("Contact Us", """Email - vidbishalmondal528@gmail.com, mondalbishal9518@gmail.com
Github - BishalMondal07
Discord - BishlMondal#3219 """))
view_menu.add_checkbutton(label="About NoteCraft", command=lambda: messagebox.showinfo("About", """NoteCraft - A Simple Text Editor

NoteCraft is a lightweight and easy-to-use text editor built using the Tkinter library in Python. It provides basic text editing features along with some additional functionalities such as find/replace, spell check, and formatting options.

Features:
- Create, open, save, and save files as different formats
- Cut, copy, paste, delete, undo, and redo operations
- Select all text in the editor
- Find and replace specific words or phrases within the text
- Spell check to identify misspelled words
- Insert current date and time in the text
- Customize font style and size
- Apply bold, italic, and underline formatting
- Enable or disable word wrap
- Zoom in or out for better readability
- Display line numbers for easier navigation
- Automatically update line numbers when text is modified

Usage:
1. File Menu:
   - New: Create a new file.
   - Open: Open an existing file.
   - Save: Save the current file.
   - Save As: Save the current file with a different name or format.
   - Exit: Quit the application.

2. Edit Menu:
   - Cut: Cut the selected text.
   - Copy: Copy the selected text.
   - Paste: Paste the copied or cut text.
   - Delete: Delete the selected text.
   - Undo: Undo the last edit operation.
   - Redo: Redo the previously undone edit operation.
   - Select All: Select all text in the editor.
   - Find/Replace: Find and replace specific words or phrases in the text.
   - Spell Check: Check the spelling of the text.
   - Time/Date: Insert the current date and time in the text.

3. Format Menu:
   - Font: Choose the font style for the text.
   - Bold: Apply bold formatting to the selected text.
   - Italic: Apply italic formatting to the selected text.
   - Underline: Apply underline formatting to the selected text.
   - Alignment : Align the text to left, right and center.

4. View Menu:
   - Theme : Chnage the theme to Black or White
   - Disable Word Wrap: Toggle word wrap on or off for the text.

NoteCraft provides a simple and intuitive interface for basic text editing tasks. It can be used for taking notes, writing code snippets, or any other text-related activities. Enjoy using NoteCraft!
"""))

line_numbers = tk.Text(root, width=4, padx=5, takefocus=0, border=0, background="#e1e1e1", state=tk.DISABLED)
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

entry = scrolledtext.ScrolledText(root, font=font, undo=True, wrap="word")
entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

entry.bind("<<Modified>>", update_unsaved_changes)
entry.bind("<KeyRelease>", update_line_numbers)

root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-S>", lambda event: save_file_as())
root.bind("<Alt-F4>", lambda event: root.quit())
root.bind("<Control-x>", lambda event: cut())
root.bind("<Control-c>", lambda event: copy())
root.bind("<Control-v>", lambda event: paste())
root.bind("<Delete>", lambda event: delete())
root.bind("<Control-z>", lambda event: undo())
root.bind("<Control-y>", lambda event: redo())
root.bind("<Control-a>", lambda event: select_all())
root.bind("<Control-F7>", lambda event: check_spelling())

root.protocol("WM_DELETE_WINDOW", root.quit)

update_line_numbers()

root.mainloop() 