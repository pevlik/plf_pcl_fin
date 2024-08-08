import os
import shutil
import tkinter as tk
import math
import csv
import re

def write_csv(data, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Profile Type", "Profile Value"])
        for value in data:
            writer.writerow(value)

def extract_height(profile_type):
    match = re.search(r'(HP|ST)(\d+)x', profile_type)
    if match:
        return match.group(2)
    return None

def plf_to_pcl(macro_var_polosa, macro_var_bulb, macro_var, input_filepath, output_filepath):
    data = {}  # Словарь для хранения данных
    profile_values = []  # Список для значений профилей
    with open(input_filepath, 'r') as plf_file:
        for line in plf_file:
            items = line.strip().split(",")
            key = items[0]
            values = items[1:]
            if key in data:
                data[key].append(values)
            else:
                data[key] = [values]

    # Извлечение необходимых данных
    profile_type = data['[PROFILE]'][0][0].replace('X', 'x')
    base_length = data['[BODY]'][0][5]
    ship_name = data['[PROFILE]'][0][3]
    grade = data['[PROFILE]'][0][1]
    part_name = data['[PROFILE]'][0][7]
    section_name = data['[PROFILE]'][0][4]
    l_v2 = data['[BEM_LA]'][0][1]
    r_v2 = data['[BEM_LE]'][0][1]
    height = extract_height(profile_type)
    vert_dot = int(int(height) / 2)
    horizon_cent = int(int(base_length) / 2)
    
    material = data['[PROFILE]'][0][1]
    if 'HP' in profile_type:
        p_shape = 'B'
    elif 'ST' in profile_type:
        p_shape = 'F'
    else:
        p_shape = 'Профиль не определен'  # You can specify a default value here
    
    # Сбор значений из [PROFILE][0][0] и [PROFILE][0][1]
    profile_values.append((profile_type, material))

    with open(output_filepath, 'w') as pcl_file:
        s_line = f"S,{ship_name},{profile_type}\n"
        s_line = s_line.replace('ST','F')
        p_line = f"P,{ship_name},{section_name},{base_length},{p_shape},{grade},{section_name}-{part_name},,1,0\n"
        pcl_file.write(s_line)
        pcl_file.write(p_line)

        for key in data:
            if '[ABS_LA]' in key:
                if 'ST' in profile_type:
                    for item in data[key]:
                        if item[0] == "016": # Макрос 10
                            side_len_l = math.tan(math.radians(float(item[1]))) * float(item[2])
                            m_line_l = "M,10L,{0},{1},{2},{3},".format(item[2], round(side_len_l), item[2], round(side_len_l))
                        
                        elif item[0] == "001" or item[0] == "102": # Макрос 11
                            m_line_l = "M,11L,{0},{1},{2},".format(0, 0, item[1])

                        elif item[0] == "004": # Макрос 11
                            m_line_l = "M,11L,{0},{1},{2},".format(0, 0, item[1])

                        elif item[0] == "012": # Макрос 11
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_l = "M,11L,{0},{1},{2},".format(item[4], 0, item[1])

                        elif item[0] == "015": # Макрос 11
                            m_line_l = "M,11L,{0},{1},{2},".format(0, 0, item[1])

                        elif item[0] == "": # Макрос 12
                            m_line_l = "M,12L,0,0,0,0,\n".format()
                        
                        elif item[0] == "103": # Макрос 13
                            m_line_l = "M,13L,{0},90,{1},0,".format(item[3], item[1])    

                        elif item[0] == "003": # Макрос 13
                            m_line_l = "M,13L,{0},90,{1},0,".format(item[3], item[1])   
                        
                        elif item[0] == "033" or item[0] == "133": # Макрос 13
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_l = "M,13L,{0},{1},{2},{3},".format(item[3], item[1], item[7], item[4])
                        
                        elif item[0] == "": # Макрос 14
                            m_line_l = "M,14L,0,0,0,0,\n".format()
                        
                        elif item[0] == "": # Макрос 17
                            m_line_l = "M,17L,0,0,\n".format()

                elif 'HP' in profile_type:
                    for item in data[key]:

                        if item[0] == "002": # Макрос 21
                            m_line_l = "M,21L,{0},{1},0,".format(item[1], l_v2)

                        elif item[0] == "001": # Макрос 21
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_l = "M,21L,{0},{1},{2},".format(item[1], r_v2, item[4])
                        
                        elif item[0] == "012" or item[0] == "112": # Макрос 21
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_l = "M,21L,{0},{1},{2},".format(item[1], l_v2, item[4])

                        elif item[0] == "102": # Макрос 21
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_l = "M,21L,{0},{1},{2},".format(item[1], l_v2, item[4])
                        
                        elif item[0] == "031" or item[0] == "131": # Макрос 22
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_l = "M,22L,{0},{1},C,{2},90,{3},r1,".format(item[5], item[6], item[1], item[4])
                        
                        elif item[0] == "109": # Макрос 23
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_l = "M,23L,{0},{1},{2},{3},{4},".format(item[3], item[1], item[4], l_v2, item[7])

                        elif item[0] == "033": # Макрос 23
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_l = "M,23L,{0},{1},{2},{3},{4},".format(item[3], item[1], item[4], l_v2, item[7])

                        elif item[0] == "003" or item[0] == "004": # Макрос 23
                            m_line_l = "M,23L,{0},{1},{2},{3},{4},".format(item[3], 90, 0, l_v2, item[1])

                        elif item[0] == "": # Макрос 25
                            m_line_l = "M,{0}L,0,0,0,0,0,0,\n".format()

                        elif item[0] == "013" or item[0] =="113": # Макрос 26
                            m_line_l = "M,26L,0,0,0,0,0,".format()

                        elif item[0] == "": # Макрос 28
                            m_line_l = "M,{0}L,0,0,0,0,0,0,".format()

                        else: 
                            m_line_l = "Такого макроса нет\n".format()

            if key.startswith('[BEM_LA]'):
                for item in data[key]:
                    if 'm_line_l' in locals():
                        if m_line_l.startswith ("M,1"):
                            m_line_l += "{0},{1},{2},{3},{4}\n".format(0,0,0,90,90)
                        elif m_line_l.startswith ("M,2"):
                            m_line_l += "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(0, 0, 0, 90, 90, 0, 0, 90, 90)
                        pcl_file.write(m_line_l)

        t_line = f"T,{horizon_cent},{vert_dot},{ship_name}-{section_name}-{part_name},\n"
        pcl_file.write(t_line)

        for key in data:
            if key.startswith('[CUTOUT]'):
                i_line = ""  # Инициализация переменной 'i_line'
                for item in data[key]:
                    if len(item) == 3:
                        i_line = "I,{0},R,0,0,{1}\n".format(item[1], item[2])
                    elif item[3] == "0": 
                        i_line = "I,{0},R,0,0,{1}\n".format(item[1], item[2])
                    elif item[3]!= "0":
                        i_line = "I,{0},D,{1},0,{2}\n".format(item[1], item[3], item[2])
                    elif len(item) == 5:
                        i_line = "I,{0},HO,{1},0,{2},{3}\n".format(item[1], item[2], item[3], item[4])
                    pcl_file.write(i_line)

            if'[ABS_LE]' in key:
                if 'ST' in profile_type:
                    for item in data[key]:
                        if item[0] == "016":  # Макрос 10
                            side_len_r = math.tan(math.radians(float(item[1]))) * float(item[2])
                            m_line_r = "M,10R,{0},{1},{2},{3},".format(item[2], round(side_len_r), item[2], round(side_len_r))
                        
                        elif item[0] == "001" or item[0] == "102": # Макрос 11
                            m_line_r = "M,11R,{0},{1},{2},".format(0, 0, item[1])

                        elif item[0] == "015": # Макрос 11
                            item_value = int(item[1])
                            m_line_r = "M,11R,{0},{1},{2},".format(0, 0, (180 - item_value))

                        elif item[0] == "004": # Макрос 11
                            m_line_r = "M,11R,{0},{1},{2},".format(0, 0, item[1])

                        elif item[0] == "012": # Макрос 11
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,11R,{0},{1},{2},".format(item[4], 0, item[1])

                        elif item[0] == "": # Макрос 12
                            m_line_r = "M,12R,\n".format()
                        
                        elif item[0] == "103": # Макрос 13
                            m_line_r = "M,13R,{0},90,{1},0,".format(item[3], item[1])

                        elif item[0] == "003": # Макрос 13
                            m_line_r = "M,13R,{0},90,{1},0,".format(item[3], item[1])  
                        
                        elif item[0] == "033" or item[0] == "133": # Макрос 13
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,13R,{0},{1},{2},{3},".format(item[3], item[1], item[7], item[4])
                        
                        elif item[0] == "": # Макрос 14
                            m_line_r = "M,14R,\n".format()
                        
                        elif item[0] == "": # Макрос 17
                            m_line_r = "M,17R,\n".format()

                elif 'HP' in profile_type:
                    for item in data[key]:
                        
                        if item[0] == "002": # Макрос 21
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,21R,{0},{1},{2},".format(item[1], r_v2, item[4])

                        elif item[0] == "001" or item[0] == "112": # Макрос 21
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,21R,{0},{1},{2},".format(item[1], r_v2, item[4])

                        elif item[0] == "012": # Макрос 21
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,21R,{0},{1},{2},".format(item[1], r_v2, item[4])

                        elif item[0] == "102": # Макрос 21
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,21R,{0},{1},{2},".format(item[1], r_v2, item[4])

                        elif item[0] == "031" or item[0] == "131": # Макрос 22
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,22R,{0},{1},C,{2},90,{3},r1,".format(item[5], item[6], item[1], item[4])

                        elif item[0] == "009" or item[0] == "109": # Макрос 23
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,23R,{0},{1},{2},{3},{4},".format(item[3], item[1], item[4], r_v2, item[7])

                        elif item[0] == "033": # Макрос 23
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,23R,{0},{1},{2},{3},{4},".format(item[3], item[1], item[4], r_v2, item[7])

                        elif item[0] == "003" or item[0] == "004": # Макрос 23
                            if item[4] == "10":
                                item[4] = "-10"
                            m_line_r = "M,23R,{0},{1},{2},{3},{4},".format(item[3], 90, 0, r_v2, item[1]) 

                        elif item[0] == "": # Макрос 25
                            m_line_r = "M,25R,\n".format()

                        elif item[0] == "013" or item[0] =="113": # Макрос 26
                            m_line_r = "M,26R,0,0,0,0,0,".format()

                        elif item[0] == "": # Макрос 28
                            m_line_r = "M,28R,0,0,0,0,0,0,\n".format()

                        else:
                            m_line_r = "Такого макроса нет\n".format()
                        
            elif key.startswith('[BEM_LE]'):
                for item in data[key]:
                    if 'm_line_r' in locals():
                        if m_line_r.startswith ("M,1"):
                            m_line_r += "{0},{1},{2},{3},{4}\n".format(0,0,0,90,90)
                        elif m_line_r.startswith ("M,2"):
                            m_line_r += "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(0, 0, 0, 90, 90, 0, 0, 90, 90)
                        pcl_file.write(m_line_r)
        
        pcl_file.write('E\n')
    
    # Вернем собранные значения
    return profile_values, profile_type, material

def remove_lines(input_filepath):
    with open(input_filepath, 'r') as plf_file:
        lines = plf_file.readlines()
    modified_lines = []
    for line in lines:
        if not line.startswith(('[ANZ]', '[SPB]', 'END')):
            modified_lines.append(line.replace("]", "],").replace(",,", ","))
    with open(input_filepath, 'w') as plf_file:
        plf_file.writelines(modified_lines)

def run_conversion(macro_var_polosa, macro_var_bulb, macro_var, input_files_str, text_widget):
    input_files = input_files_str.split(',')
    all_profile_values = []  # Список для всех значений профилей из всех файлов

    for input_file in input_files:
        # output_file = input_file.replace('.plf', '.pcl')
        temp_file = input_file.replace('.plf', '_temp.plf')
        # Создание временной копии файла .plf
        shutil.copy(input_file, temp_file)
        # Удаление ненужных строк из временного файла
        remove_lines(temp_file)
        # Преобразование временного файла в .pcl
        try:
            # Создание выходного файла .pcl
            output_file = temp_file.replace('_temp.plf', '.pcl')
            profile_values, profile_type, material = plf_to_pcl(macro_var_polosa, macro_var_bulb, macro_var, temp_file, output_file)  # получаем значения профилей
            all_profile_values.extend(profile_values)  # добавляем значения в общий список
            # Создание папки для профиля
            profile_folder = f"{profile_type.replace('[PROFILE],', '')}_{material}"
            if not os.path.exists(profile_folder):
                os.makedirs(profile_folder)
            
            # Перемещение выходного файла .pcl в соответствующую папку
            shutil.move(output_file, os.path.join(profile_folder, os.path.basename(output_file)))
            text_widget.insert(tk.END, f"Файл обработан и сохранен в: {os.path.join(profile_folder, os.path.basename(output_file))}\n")
        except Exception as error:
            text_widget.insert(tk.END, f"Ошибка при обработке файла {os.path.basename(input_file)}: {str(error)}\n")
        finally:
            # Удаление временного файла, если он не был перемещен
            if os.path.exists(temp_file):
                os.remove(temp_file)

    # Запись всех значений профилей в один общий CSV файл
    csv_output_file = "all_profiles.csv"  # имя файла CSV для всех значений
    write_csv(all_profile_values, csv_output_file)
    text_widget.insert(tk.END, f"Все значения профилей сохранены в {csv_output_file}\n")