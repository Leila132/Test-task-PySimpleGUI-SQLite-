import psutil
import time
from database import create_tables, insert_data, return_data, get_db_connection

conn = get_db_connection()
create_tables(conn)
conn.close()

# Переменная булевая, благодаря которой осуществляется запись
recording = False
start_time = None  # Время начала записи

def get_parameters():
    # Уровень нагруженности ЦП
    cpu = psutil.cpu_percent(interval=0.9)

    # Уровень нагруженности ОЗУ
    ram_av = round(psutil.virtual_memory().available / (1024 ** 3), 2)  # доступно
    ram_tot = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # всего

    # Уровень нагруженности ПЗУ
    disk_av = round(psutil.disk_usage('/').free / (1024 ** 3), 2)  # доступно
    disk_tot = round(psutil.disk_usage('/').total / (1024 ** 3), 2)  # всего
    return cpu, ram_av, ram_tot, disk_av, disk_tot

# Обновление данных в основном окне
def update_main(window):
    global start_time

    # Получаем параметры
    r = get_parameters()
    # Обновляем текст
    window['-text-1'].update("ЦП: {}".format(r[0]))
    window['-text-2'].update("ОЗУ: {}".format(r[1]) + "/{}".format(r[2]))
    window['-text-3'].update("ПЗУ: {}".format(r[3]) + "/{}".format(r[4]))

    # Обновляем таймер
    if recording and start_time is not None:
        elapsed_time = time.time() - start_time
        window['-TIMER-'].update(f"Запись: {int(elapsed_time)} сек")
    else:
        window['-TIMER-'].update("Запись: 0 сек")

    if recording:  # Если включена запись, то записываем в БД
        conn = get_db_connection()
        insert_data(conn, str(r[0]), str(r[1]), str(r[2]), str(r[3]), str(r[4]))
        conn.close()

# Обновление данных во втором окне
def update_sec(window):
    # Выборка с условием
    conn = get_db_connection()
    rows = return_data(conn)
    conn.close()
    window['-TABLE-'].update(values=rows)

# Создание основного окна
def create_main_window():
    import PySimpleGUI as sg
    layout = [
        [sg.Text('Мониторинг системы', font=('Helvetica', 20), justification='center')],
        [sg.Text('ЦП:', size=(20, 1), key='-text-1', font='Helvetica 14')],
        [sg.Text('ОЗУ:', size=(20, 1), key='-text-2', font='Helvetica 14')],
        [sg.Text('ПЗУ:', size=(20, 1), key='-text-3', font='Helvetica 14')],
        [sg.Text('Запись: 0 сек', size=(20, 1), key='-TIMER-', font='Helvetica 14')],
        [sg.Button('Начать запись', enable_events=True, key='-FUNCTION-1', font='Helvetica 14', size=(15, 1))],
        [sg.Button('Остановить запись', enable_events=True, key='-FUNCTION-2', font='Helvetica 14', size=(15, 1), visible=False)],
        [sg.Button("Посмотреть БД", key="-OPEN-", font='Helvetica 14', size=(15, 1))],
    ]
    return sg.Window("Мониторинг системы", layout, finalize=True)

# Создание второго окна
def create_second_window():
    import PySimpleGUI as sg
    conn = get_db_connection()
    rows = return_data(conn)
    conn.close()
    # Заголовки столбцов
    headers = ["ID", "CPU", "RAM Available", "RAM Total", "Disk Available", "Disk Total"]
    # Создаем таблицу
    layout = [
        [sg.Table(values=rows, headings=headers, auto_size_columns=True,
                  display_row_numbers=False, justification='right', key='-TABLE-', font='Helvetica 12')],
    ]
    return sg.Window("Данные из БД", layout, finalize=True)

# Основная функция
def main():
    global recording, start_time
    import PySimpleGUI as sg
    
    main_window = create_main_window()
    second_window = None

    while True:
        window, event, values = sg.read_all_windows(timeout=100)

        # Если окно закрыто
        if event == sg.WIN_CLOSED:
            if window == main_window:  # Если закрыто основное окно
                break
            elif window == second_window:  # Если закрыто второе окно
                second_window.close()
                second_window = None

        # Если нажата кнопка "Посмотреть БД"
        if event == "-OPEN-" and second_window is None:
            second_window = create_second_window()

        # Обновляем данные в основном окне
        update_main(main_window)
        if second_window is not None:
            update_sec(second_window)

        # Обрабатываем нажатие на кнопки
        if event == "-FUNCTION-1":  # Начать запись
            main_window["-FUNCTION-1"].update(visible=False)
            main_window["-FUNCTION-2"].update(visible=True)
            recording = True
            start_time = time.time()  # Запускаем таймер

        if event == "-FUNCTION-2":  # Остановить запись
            main_window["-FUNCTION-2"].update(visible=False)
            main_window["-FUNCTION-1"].update(visible=True)
            recording = False
            start_time = None  # Сбрасываем таймер

    # Закрываем все окна и соединение с БД
    main_window.close()
    if second_window is not None:  # Проверяем, что second_window не равно None
        second_window.close()

if __name__ == "__main__":
    main()