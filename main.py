import tkinter as tk
from pynput import keyboard
import time
import threading

timer_running = False
start_time = None
elapsed_time = 0.0

def update_timer():
    global start_time, timer_running, elapsed_time
    while timer_running:
        elapsed_time = time.time() - start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        timer_label.config(text=f"{int(hours):02}:{int(minutes):02}:{seconds:04.1f}")
        root.update()
        time.sleep(0.1)
    
    # This displays just seconds
    # global start_time, timer_running, elapsed_time
    # while timer_running:
    #     elapsed_time = time.time() - start_time
    #     timer_label.config(text=f"{elapsed_time:.1f} sec")
    #     root.update()
    #     time.sleep(0.1)

def toggle_timer():
    global timer_running, start_time, elapsed_time
    if not timer_running:
        start_time = time.time() - elapsed_time
        timer_running = True
        threading.Thread(target=update_timer, daemon=True).start()
        root.deiconify()
    else:
        timer_running = False
        
def reset_timer():
    global start_time, elapsed_time, timer_running
    elapsed_time = 0.0
    start_time = time.time()
    if not timer_running:
        timer_label.config(text="00:00:00.0")
        root.update()

def exit_application():
    root.destroy()

def on_press(key):
    try:
        if key.char and key.char.lower() == '=':
            toggle_timer()
        elif key.char and key.char.lower() == '-':
            exit_application()
        elif key.char and key.char.lower() == '+':
            reset_timer()
    except AttributeError:
        pass

root = tk.Tk()
root.attributes('-topmost', True)
root.overrideredirect(True)
root.wm_attributes('-transparentcolor','black')
root.geometry("200x50+20+20")
root.configure(bg='black')
root.withdraw()

timer_label = tk.Label(root, text="0.0 sec", font=("Arial", 24), fg="white", bg="black")
timer_label.pack()


listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()
