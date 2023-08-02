import tkinter as tk
from tkinter import Misc
import keyboard
import time
import pyautogui as pag

BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
FONT = "Consolas"


def logger():
    def log(func):
        def wrapper(*args, **kwargs):
            print(f"Called {func.__name__} with {args} {kwargs}")
            return func(*args, **kwargs)
        return wrapper
    return log


class AutoClicker(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.cursor_position = None
        self.event = None
        self.interval = None

    @staticmethod
    def calculate_interval(s: str):
        s = s.strip()
        if s.isnumeric():
            return int(s)
        if (len(s) == 0 or len(s) == 1):   
            return 0
        if (s[-2:] == "ms"):
            return int(s[:-2])
        if s[-1] == "s":
            return int(s[:-1]) * 1000
        elif s[-1] == "m":
            return int(s[:-1]) * 60 * 1000
        elif s[-1] == "h":
            return int(s[:-1]) * 60 * 60 * 1000
        elif s[-1] == "d":
            return int(s[:-1]) * 60 * 60 * 24 * 1000

    def wait_here(self):
        var = tk.IntVar()
        self.master.after(self.interval, var.set, 1)
        self.master.wait_variable(var)

    def change_interval(self):
        self.interval = self.calculate_interval(self.interval_area.get())

    def change_event(self, event_name):
        if event_name == "Left Click":
            self.event = pag.click
        elif event_name == "Right Click":
            self.event = pag.rightClick
        elif event_name == "Middle Click":
            self.event = pag.middleClick
        elif event_name == "Double Click":
            self.event = pag.doubleClick
        # event should take a argument, even if it's not used
        elif event_name == "Key Up":
            self.event = lambda p: keyboard.press(keyboard.KEY_UP)
        elif event_name == "Key Down":
            self.event = lambda p: keyboard.press(keyboard.KEY_DOWN)
        elif event_name == "Key Left":
            self.event = lambda p: keyboard.press("left")
        elif event_name == "Key Right":
            self.event = lambda p: keyboard.press("right")
        elif event_name == "Enter":
            self.event = lambda p: keyboard.press("enter")
        elif event_name == "Space":
            self.event = lambda p: keyboard.press("space")

    def usage(self):
        usage = tk.Toplevel(self.master)
        usage.title("Usage")
        usage.geometry("700x800")
        usage.maxsize(700, 800)
        usage_frame = tk.Frame(usage, relief=tk.RAISED, width=300,
                               height=200, padx=10, pady=10)
        usage_frame.pack()
        usage_label = tk.Label(usage_frame, text="""1. Press the "Record" button to start 
   recording the position of the mouse.
2. Press "enter" to record 
   the position of your mouse.
3. Select the event you want to perform 
   from the list.
4. Enter the interval between each event.
   We support the following units:
       ms - milliseconds
       s - seconds
       m - minutes
       h - hours
       d - days
   enter like this: 1ms, 2s, 40m, 10h, 3d
5. Press the "Start" button to start 
   the autoclicker.
6. HOLD pressing "esc" to stop 
   the autoclicker.""", anchor=tk.W, justify=tk.LEFT)
        usage_label.config(state=tk.DISABLED)
        usage_label.pack()
        usage_button = tk.Button(
            usage_frame, text="Close", command=usage.destroy)
        usage_button.pack()

    def about(self):
        about = tk.Toplevel(self.master)
        about.title("About")
        about.geometry("300x200")
        about.maxsize(300, 200)
        about_frame = tk.Frame(about, relief=tk.RAISED, width=300,
                               height=200, padx=10, pady=10)
        about_frame.pack()
        about_label = tk.Label(about_frame, text="AutoClicker v1.0.0")
        about_label.pack()
        about_button = tk.Button(
            about_frame, text="Close", command=about.destroy)
        about_button.pack()

    def start(self):
        self.change_event(self.key_listbox.get(
            self.key_listbox.curselection()))
        while True:
            if (keyboard.is_pressed("esc")):
                break
            self.wait_here()
            self.event(self.cursor_position)

    def record(self):
        while True:
            if (keyboard.is_pressed("enter")):
                position = pag.position()
                break

    def create_widgets(self):
        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.grid(row=0, column=0, sticky=tk.W +
                          tk.E, columnspan=3, padx=10)

        self.record_button = tk.Button(self, text="Record", command=self.record)
        self.record_button.grid(row=1, column=0, sticky=tk.W +
                           tk.E, columnspan=1, padx=10)
        
        self.key_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.key_listbox.grid(row=1, column=1, sticky=tk.W+tk.E,
                     columnspan=2, rowspan=3, padx=10)


        keys = ["Left Click", "Right Click", "Middle Click",
            "Double Click", "Key Up", "Key Down", "Key Left", "Key Right", "Enter", "Space"]
        for key in keys:
            self.key_listbox.insert(tk.END, key)    
        
        self.interval_frame = tk.Frame(self)

        self.interval_frame.grid(row=2, column=0, sticky=tk.W+tk.E, rowspan=2, padx=10)
        self.interval_area = tk.Entry(self.interval_frame)

        self.interval_submit = tk.Button(
            self.interval_frame, text="Set Interval", command=self.change_interval)

        self.interval_area.pack(padx=10)
        self.interval_submit.pack()

        menu = tk.Menu(self.master)
        help = tk.Menu(menu)
        help.add_command(label="Usage", command=self.usage)
        help.add_command(label="About", command=self.about)
        menu.add_cascade(label="Help", menu=help)
        self.master.config(menu=menu)


"""def main():

    # Implemented by record
    position = None
    # Implemented by change_event
    event = None
    # Implemented by calculate_interval
    interval = None

    pag.FAILSAFE = False

    root = tk.Tk()
    root.title("AutoClicker")
    root.geometry("500x350")
    root.minsize(500, 350)
    frame = tk.Frame(root, relief=tk.RAISED, width=500,
                     height=300, padx=10, pady=10)
    frame.pack()

    @logger()
    def start():
        def waithere():
            var = tk.IntVar()
            root.after(interval, var.set, 1)
            root.wait_variable(var)

        change_event(key_listbox.get(key_listbox.curselection()))
        while True:
            if (keyboard.is_pressed("esc")):
                break
            waithere()
            event(position)

        print("Stopped")

    start_button = tk.Button(frame, text="Start", command=start)
    start_button.grid(row=0, column=0, sticky=tk.W+tk.E, columnspan=3, padx=10)

    @logger()
    def record():
        nonlocal position
        while True:
            if (keyboard.is_pressed("enter")):
                position = pag.position()
                break

    record_button = tk.Button(frame, text="Record", command=record)
    record_button.grid(row=1, column=0, sticky=tk.W +
                       tk.E, columnspan=1, padx=10)

    def calculate_interval(s: str):
        s = s.strip()
        if s.isnumeric():
            return int(s)
        if (len(s) == 0 or len(s) == 1):
            return 0
        if (s[-2:] == "ms"):
            return int(s[:-2])
        if s[-1] == "s":
            return int(s[:-1]) * 1000
        elif s[-1] == "m":
            return int(s[:-1]) * 60 * 1000
        elif s[-1] == "h":
            return int(s[:-1]) * 60 * 60 * 1000
        elif s[-1] == "d":
            return int(s[:-1]) * 60 * 60 * 24 * 1000

    @logger()
    def change_interval():
        nonlocal interval
        interval = calculate_interval(interval_area.get())

    interval_frame = tk.Frame(frame)

    interval_frame.grid(row=2, column=0, sticky=tk.W+tk.E, rowspan=2, padx=10)
    interval_area = tk.Entry(interval_frame)

    interval_submit = tk.Button(
        interval_frame, text="Set Interval", command=change_interval)

    interval_area.pack(padx=10)
    interval_submit.pack()

    @logger()
    def change_event(event_name):
        nonlocal event
        if event_name == "Left Click":
            event = pag.click
        elif event_name == "Right Click":
            event = pag.rightClick
        elif event_name == "Middle Click":
            event = pag.middleClick
        elif event_name == "Double Click":
            event = pag.doubleClick
        elif event_name == "Key Up":
            def event(p): return keyboard.press(keyboard.KEY_UP)
        elif event_name == "Key Down":
            def event(p): return keyboard.press(keyboard.KEY_DOWN)
        elif event_name == "Key Left":
            def event(p): return keyboard.press("left")
        elif event_name == "Key Right":
            def event(p): return keyboard.press("right")
        elif event_name == "Enter":
            def event(p): return keyboard.press("enter")
        elif event_name == "Space":
            def event(p): return keyboard.press("space")

    key_listbox = tk.Listbox(frame)
    keys = ["Left Click", "Right Click", "Middle Click",
            "Double Click", "Key Up", "Key Down", "Key Left", "Key Right", "Enter", "Space"]
    for key in keys:
        key_listbox.insert(tk.END, key)

    key_listbox.bind(lambda:
                     change_event(key_listbox.get(
                         key_listbox.curselection()))
                     )

    key_listbox.grid(row=1, column=1, sticky=tk.W+tk.E,
                     columnspan=2, rowspan=3, padx=10)

    menu = tk.Menu(root)
    help = tk.Menu(menu)

    def usage():
        usage = tk.Toplevel(root)
        usage.title("Usage")
        usage.geometry("700x800")
        usage.maxsize(700, 800)
        usage_frame = tk.Frame(usage, relief=tk.RAISED, width=300,
                               height=200, padx=10, pady=10)
        usage_frame.pack()
        usage_label = tk.Label(usage_frame, text=""""""1. Press the "Record" button to start 
   recording the position of the mouse.
2. Press "enter" to record 
   the position of your mouse.
3. Select the event you want to perform 
   from the list.
4. Enter the interval between each event.
   We support the following units:
       ms - milliseconds
       s - seconds
       m - minutes
       h - hours
       d - days
   enter like this: 1ms, 2s, 40m, 10h, 3d
5. Press the "Start" button to start 
   the autoclicker.
6. HOLD pressing "esc" to stop 
   the autoclicker."""""", anchor=tk.W, justify=tk.LEFT)
        usage_label.config(state=tk.DISABLED)
        usage_label.pack()
        usage_button = tk.Button(
            usage_frame, text="Close", command=usage.destroy)
        usage_button.pack()
    help.add_command(label="Usage", command=usage)

    def about():
        about = tk.Toplevel(root)
        about.title("About")
        about.geometry("300x200")
        about.maxsize(300, 200)
        about_frame = tk.Frame(about, relief=tk.RAISED, width=300,
                               height=200, padx=10, pady=10)
        about_frame.pack()
        about_label = tk.Label(about_frame, text="AutoClicker v1.0.0")
        about_label.pack()
        about_button = tk.Button(
            about_frame, text="Close", command=about.destroy)
        about_button.pack()
    help.add_command(label="About", command=about)
    menu.add_cascade(label="Help", menu=help)
    root.config(menu=menu)

    root.mainloop()

"""

if __name__ == '__main__':
    root = tk.Tk()
    root.title("AutoClicker")
    root.geometry("500x350")
    root.maxsize(500, 350)
    autoclicker = AutoClicker(root)
    autoclicker.create_widgets()
    root.mainloop()