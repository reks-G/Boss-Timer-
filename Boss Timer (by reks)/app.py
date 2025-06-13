import time
import pygame
import threading
import tkinter as tk
from tkinter import messagebox, filedialog

pygame.mixer.init()

def load_sound_file():
    sound_file = filedialog.askopenfilename(title="Выберите звуковой файл", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")])
    if sound_file:
        try:
            pygame.mixer.music.load(sound_file)
        except pygame.error as e:
            print(f"Ошибка загрузки звукового файла: {e}")
            exit()

timers = {}

def timer(name, total_seconds):
    for remaining in range(total_seconds, 0, -1):
        timers[name] = remaining
        time.sleep(1)
    pygame.mixer.music.play()
    print(f"\nВремя вышло для таймера '{name}'!")
    timers.pop(name, None)
    update_timer_display()

def update_timer_display():
    for widget in timer_frame.winfo_children():
        widget.destroy()
    
    if not timers:
        label = tk.Label(timer_frame, text="Нет активных таймеров.", font=("Helvetica", 14), bg="#f0f0f0")
        label.pack(pady=10)
    else:
        for name, remaining in timers.items():
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60
            label = tk.Label(timer_frame, text=f"{name}: Осталось {hours} ч {minutes} мин {seconds} сек", font=("Helvetica", 12), bg="#f0f0f0")
            label.pack(pady=5)

def add_timer():
    timer_name = name_entry.get()
    timer_time = time_entry.get()
    
    try:
        hours, minutes = map(int, timer_time.split(':'))
        total_seconds = hours * 3600 + minutes * 60
        timer_thread = threading.Thread(target=timer, args=(timer_name, total_seconds))
        timers[timer_name] = total_seconds
        timer_thread.start()
        name_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        update_timer_display()
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите время в правильном формате ЧЧ:ММ.")

def refresh_timers():
    update_timer_display()
    root.after(1000, refresh_timers)

root = tk.Tk()
root.title("Таймеры")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

load_sound_file()

timer_frame = tk.Frame(root, bg="#f0f0f0")
timer_frame.pack(pady=10)

name_label = tk.Label(root, text="Имя таймера:", font=("Helvetica", 14), bg="#f0f0f0")
name_label.pack(pady=5)
name_entry = tk.Entry(root, font=("Helvetica", 12))
name_entry.pack(pady=5)

time_label = tk.Label(root, text="Время (ЧЧ:ММ):", font=("Helvetica", 14), bg="#f0f0f0")
time_label.pack(pady=5)
time_entry = tk.Entry(root, font=("Helvetica", 12))
time_entry.pack(pady=5)

add_button = tk.Button(root, text="Добавить таймер", command=add_timer, font=("Helvetica", 12), bg="#4CAF50", fg="white")
add_button.pack(pady=10)

refresh_timers()
root.mainloop()
