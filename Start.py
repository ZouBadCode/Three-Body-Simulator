import tkinter as tk
import game
import threading
from tkinter import simpledialog
from classroom import Body
from tkinter import Toplevel, Label, Entry, Button
from tkinter import colorchooser

# 創建tkinter窗口
root = tk.Tk()
root.title("Start Simulation")

def thread_game():
    start_button.config(state="disabled")  # 禁用按鈕
    thread_game_main= threading.Thread(target=game.nima)
    thread_game_main.start()
    thread_game_main.join()  # 等待pygame迴圈結束
    start_button.config(state="normal")



def add_body():
    def submit():
        try:
            pos_x = float(entry_pos_x.get())
            pos_y = float(entry_pos_y.get())
            vel_x = float(entry_vel_x.get())
            vel_y = float(entry_vel_y.get())
            mass = float(entry_mass.get())
            color = color_label.cget("text")
            color_str = color 
            color_str_no_p = color_str.replace("(", "").replace(")", "")
            color_tuple = tuple(int(value.strip()) for value in color_str_no_p.split(','))
            game.add_body_game([pos_x, pos_y], [vel_x, vel_y], mass, color_tuple)
            input_window.destroy()  # 關閉輸入視窗
        except ValueError:
            print("請確保所有輸入都是有效的數字。")




    # 創建一個新視窗
    input_window = Toplevel(root)
    input_window.title("新增 Body")

    # 位置 X
    Label(input_window, text="位置 X").pack()
    entry_pos_x = Entry(input_window)
    entry_pos_x.pack()

    # 位置 Y
    Label(input_window, text="位置 Y").pack()
    entry_pos_y = Entry(input_window)
    entry_pos_y.pack()

    # 速度 X
    Label(input_window, text="速度 X").pack()
    entry_vel_x = Entry(input_window)
    entry_vel_x.pack()

    # 速度 Y
    Label(input_window, text="速度 Y").pack()
    entry_vel_y = Entry(input_window)
    entry_vel_y.pack()

    # 質量
    Label(input_window, text="質量").pack()
    entry_mass = Entry(input_window)
    entry_mass.pack()

    # 顏色
    color_label = tk.Label(input_window, text='顏色代碼將顯示在這裡')
    color_label.pack()

    def choose_color():
        color_code = colorchooser.askcolor(title ="Choose color")
        RGB_code = color_code[0]
        if RGB_code:  # 確保用戶選擇了顏色
            color_label.config(text=str(RGB_code))

    button_choose = tk.Button(input_window, text='選擇顏色', command=choose_color)
    button_choose.pack(pady=20)
    # 提交按鈕
    Button(input_window, text="提交", command=submit).pack()

# 創建一個按鈕，點擊後啟動pygame迴圈
start_button = tk.Button(root, text="Start Simulation", command=thread_game)
start_button.pack(pady=20)

# 新增 Body 的按鈕
add_body_button = tk.Button(root, text="新增 Body", command=add_body)
add_body_button.pack(pady=10)

# 運行tkinter事件迴圈
root.mainloop()