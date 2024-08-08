import tkinter as tk


def create_macro_menu(m_menu, macros, title):
    macro_menu = tk.Menu(m_menu, tearoff=0)
    m_menu.add_cascade(label=title, menu=macro_menu)

    macro_var = tk.StringVar()  # создаём переменную, которая будет хранить значение выбранного макроса

    buttons_dict = {}  # словарь для хранения кнопок

    for macro in macros:
        button_name = "Macro " + str(macro)
        macro_menu.add_radiobutton(label=button_name, variable=macro_var,
                                   value=button_name, command=lambda var=macro_var: None)
        buttons_dict[button_name] = macro  # сохраняем кнопку в словаре

    # Макросы на стадии разработки
    disabled_macros = ["Macro 11", "Macro 12", "Macro 14", "Macro 17", "Macro 22", "Macro 23",
                       "Macro 25", "Macro 26", "Macro 28"]

    for macro in disabled_macros:
        if macro in buttons_dict:  # проверка существования макроса
            macro_menu.entryconfigure(macro, state="disabled")

    print(macro_var.get())

    return macro_var  # возвращаем переменны