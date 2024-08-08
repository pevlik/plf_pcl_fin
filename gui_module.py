import os
import webbrowser
import tkinter as tk
from m_button_functions import create_macro_menu
from tkinter import filedialog, Text, BOTH


def open_pdf_manual():
    # замените на правильный путь к вашему файлу
    pdf_file = 'Macro_list\\Macrochecklist_PCL_V1_03.pdf'
    try:
        os.startfile(pdf_file)
    except FileNotFoundError:
        webbrowser.open_new(r'file://'+pdf_file)


def create_gui(runconv):
    # Create main window
    window = tk.Tk()
    window.title("plf to pcl conversion")
    window.iconbitmap('img/PB_logo.ico')
    window.minsize(545,380)
    window.maxsize(650,380)

    # Define padding
    padx = 4
    pady = 4
    side_padx = 5
    side_pady = 5

    # Create widgets
    file_label = tk.Label(window, text="Directory:")
    file_entry = tk.Entry(window, width=40)
    file_button = tk.Button(window, text="Browse", command=lambda: select_file_widget(file_entry))
    messagebox_text = Text(window, borderwidth=1, relief="solid")
    messagebox_text.config(width=1, height=20)
    macro_var = tk.StringVar()

    convert_button = tk.Button(window, text="Process PCL Files",
                               command=lambda: runconv(macro_var_polosa, macro_var_bulb, macro_var, file_entry.get(), messagebox_text))

    exit_button = tk.Button(window, text="Выход", command=window.destroy)

    # Создание основного меню
    menu = tk.Menu(window)
    window.config(menu=menu)

    # Создание пункта "Справка"
    help_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Справка', menu=help_menu)
    # Добавление пункта "Помощь" в меню "Справка"
    help_menu.add_command(label='Macro Checklist', command=open_pdf_manual)

    # генерируем меню Flat Bar
    macro_var_polosa = create_macro_menu(menu, [10, 11, 12, 13, 14, 17], 'Полоса')
    # генерируем меню Bulb
    macro_var_bulb = create_macro_menu(menu, [20, 21, 22, 23, 25, 26, 28], 'Бульб')

    messagebox_text.pack(side='top', padx=side_padx, pady=side_pady, expand=1, fill=BOTH)
    # Browse
    file_label.pack(side='left', padx=padx, pady=pady)
    file_entry.pack(side='left', padx=padx, pady=pady)
    file_button.pack(side='left', padx=side_padx, pady=side_pady)
    # Convert and exit buttons
    convert_button.pack(side='right', padx=side_padx, pady=side_pady)
    exit_button.pack(side='right', padx=side_padx, pady=side_pady)

    # Event loop
    window.mainloop()


def select_file_widget(entry_widget=None):
    selected_files = filedialog.askopenfilenames(filetypes=(("PLF files","*.plf"), ("all files","*.*")))
    # Если были выбраны файлы, записываем их все в поле file_entry
    if selected_files:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ','.join(selected_files))