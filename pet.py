import pandas as pd

import matplotlib.pyplot as plt

import os

import csv


def get_path():
    path_save = input(f'Укажите директорию сохранения графиков. '
                      f'По умолчанию - {os.getcwd()}:')
    if os.path.exists(path_save) is True:
        return path_save
    else:
        return os.getcwd()


def get_title():
    title = ['Время, с',
             'Давление О2 (кислорода) на входе аппарата,бар',
             'Давление He (гелия) на входе аппарата, бар',
             'Значение датчика потока О2, литры в минуту',
             'Значение датчика потока He, литры в минуту',
             'Концентрация кислорода в смеси (датчик 1), %',
             'Концентрация кислорода в смеси (датчик 2), %',
             'Давление в маске, сантиметров водного столба',
             'Температура в маске, градусы Цельсия',
             'Температура нагревателя, градусы Цельсия',
             'Объем вдоха, мл',
             'Частота дыхания , раз в минуту',
             'Заданная температура, градусы Цельсия',
             'Концентрация кислорода в смеси -заданное, %',
             'Flags',
             'Date']
    return title


def get_dataframe_and_date(file):
    count = 1
    date = set()
    DATA = []
    for line in file_reader:
        if count == 1:
            count += 1
            continue
        elif len(line) == 1:
            for elem in line:
                date_moment = elem[10:29]
        elif len(line) == 16:
            date.add(date_moment)
            line_int = []
            for elem in line:
                line_int.append(int(elem))
            if line_int[8] == 135:
                line_int[8] = 0
            if line_int[9] == 135:
                line_int[9] = 0
            line_int.pop()
            line_int.append(date_moment)
            DATA.append(line_int)
            title = get_title()
            data_frame = pd.DataFrame(DATA, columns=title)
    return data_frame, date


def get_figure():
    args = get_title()
    args = args[1:14]
    for arg in args:
        new_data_frame.plot(x='Время, с', y=arg, ylabel=arg, linewidth=1.5)
        plt.grid()
        plt.savefig(arg, bbox_inches='tight', dpi=250)
        plt.close(plt.gcf())


main_folder = get_path()
dir_name = os.getcwd()
all_files = os.listdir(dir_name)

mylist = []
for file in all_files:
    if '.LOG' in file:
        if 'NO_DATE_.LOG' in file:
            pass
        else:
            mylist.append(file)
count_progress = 100/len(mylist)
progress_bar = 0

for file in all_files:
    if 'NO_DATE_.LOG' in file:
        pass
    elif '.LOG' in file:
        progress_bar += count_progress
        print(f'Обрабатывается файл {file} '
              f'Прогресс: {round(progress_bar,2)} %')
        with open(file, encoding='utf-8', newline='') as read_file:
            file_reader = csv.reader(read_file, delimiter=";")
            data_frame, date = get_dataframe_and_date(file_reader)
            os.chdir(main_folder)
            folder = file[:9]
            os.mkdir(folder)
            os.chdir(folder)
            path_date = os.getcwd()

            for curr_date in date:
                new_data_frame = data_frame.query('Date == @curr_date')

                folder_time = str(curr_date[11:13]
                                  + curr_date[14:16]
                                  + curr_date[17:19])
                os.mkdir(folder_time)
                os.chdir(folder_time)
                get_figure()
                os.chdir(path_date)
            os.chdir(dir_name)
