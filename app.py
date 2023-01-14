import tkinter as tk
import customtkinter
import threading
import psutil
import os
import json

from utils import Utils
from time import sleep

# Initialize utils class
u = Utils()

not_inst = u.check_not_installed()

if len(not_inst) == 2:
    u.shown = 'install'
elif len(not_inst) == 0:
    u.shown = 'launcher'
else:
    u.shown = f'fix-{not_inst[0]}'

class Page(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

class InstallPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

       def install_groundseg():
           threading.Thread(target=u.install_groundseg, daemon=True).start()

       # Title
       label = customtkinter.CTkLabel(self,
                                      text="GroundSeg is not installed.",
                                      height=240
                                      )

       # Install button
       button = customtkinter.CTkButton(self,
                                        text="Install",
                                        corner_radius=12,
                                        fg_color="#008EFF",
                                        border_color="#008EFF",
                                        command=install_groundseg)

       # Pack
       label.pack()
       button.pack()

class FixPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

       def fix_groundseg():
           to_fix = u.shown.split('-')[1]
           threading.Thread(target=u.fix_groundseg, args=(to_fix,), daemon=True).start()

       # Title
       label = customtkinter.CTkLabel(self,text="GroundSeg is missing required files",height=240)

       # Fix button
       button = customtkinter.CTkButton(self,text="Fix",corner_radius=12,fg_color="#008EFF",border_color="#008EFF",command=fix_groundseg)

       # Pack
       label.pack()
       button.pack()

class InstallingPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = customtkinter.CTkLabel(self,
                                      text="Installing GroundSeg",
                                      height=320
                                      )

       label.pack(side="top", fill="both", expand=True)

class FixingPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = customtkinter.CTkLabel(self,
                                      text="Fixing GroundSeg",
                                      height=320
                                      )

       label.pack(side="top", fill="both", expand=True)

class LauncherPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.load_values()
        self.make_labels()
        self.make_ram_buttons()
        self.make_cpu_buttons()
        self.make_hdd_buttons()
        self.make_reset_buttons()
        self.make_start_button()
        self.place_widgets()

    # Default values
    def load_values(self):

        # convert bytes to gigabytes
        gb = 2**30
        cfg = {}

        # config file
        self.config_file = "/opt/nativeplanet/groundseg/launcher.json"

        # resources available
        self.total_ram = int(psutil.virtual_memory().total / gb) #GB
        self.total_cpu = int(os.cpu_count())
        self.free_hdd = int(psutil.disk_usage('/').free / gb) #GB

        # default setting
        self.default_ram = int(self.total_ram * 0.8) #GB
        self.default_cpu = int(self.total_cpu * 0.8)
        self.default_hdd = int(self.free_hdd * 0.8) #GB

        # minimum resources
        self.min_ram = 4
        self.min_cpu = 1
        self.min_hdd = 16

        # load from json
        try:
            with open(self.config_file, "r") as f:
                cfg = json.load(f)
                f.close()

            self.ram = cfg['ram']
            self.cpu = cfg['cpu']
            self.hdd = cfg['hdd']

        except Exception as e:
            print(e)
            print("Using default values")
            self.ram = self.default_ram
            self.cpu = self.default_cpu
            self.hdd = self.default_hdd

        # Decrement buttons default state
        self.ram_dec_init = 'normal'
        self.cpu_dec_init = 'normal'
        self.hdd_dec_init = 'normal'

        if self.min_ram >= self.ram:
            self.ram_dec_init = 'disabled'
        if self.min_cpu >= self.cpu:
            self.cpu_dec_init = 'disabled'
        if self.min_hdd >= self.hdd:
            self.hdd_dec_init = 'disabled'

        # Increment buttons default state
        self.ram_inc_init = 'normal'
        self.cpu_inc_init = 'normal'
        self.hdd_inc_init = 'normal'

        if self.total_ram - 1 <= self.ram:
            self.ram_inc_init = 'disabled'
        if self.total_cpu <= self.cpu:
            self.cpu_inc_init = 'disabled'
        if self.free_hdd <= self.hdd:
            self.hdd_inc_init = 'disabled'


    # Default inc/dec button
    def default_button(self, text, state, command):
        # Button theming
        w = 48 # width
        rad = 12 # corner_radius
        fg = "#008EFF" # fg_color
        bc = "#008EFF" # border_color

        return customtkinter.CTkButton(self,
                                       text=text,
                                       width=w,
                                       corner_radius=rad,
                                       fg_color=fg,
                                       border_color=bc,
                                       state=state,
                                       command=command
                                       )

    # Labels
    def make_labels(self):
        self.main_title = customtkinter.CTkLabel(self, text="GroundSeg Virtual Machine Settings", font=(None,16))
        self.ram_title = customtkinter.CTkLabel(self, text="RAM")
        self.ram_label = customtkinter.CTkLabel(self, text=f"{self.ram}/{self.total_ram - 1} GB")
        self.cpu_title = customtkinter.CTkLabel(self, text="CPU")
        self.cpu_label = customtkinter.CTkLabel(self, text=f"{self.cpu}/{self.total_cpu} cores")
        self.hdd_title = customtkinter.CTkLabel(self, text="Maximum Disk Usage (Piers and s3 buckets)")
        self.hdd_label = customtkinter.CTkLabel(self, text=f"{self.hdd}/{self.free_hdd} GB")
        self.defaults_title = customtkinter.CTkLabel(self, text="Reset To Default Settings")

    # Create Ram buttons
    def make_ram_buttons(self):
        # Ram decrement
        self.ram_d1 = self.default_button('-1', self.ram_dec_init, lambda: self.set_ram('dec',1)) # -1
        self.ram_d5 = self.default_button('-5', self.ram_dec_init, lambda: self.set_ram('dec',5)) # -5
        self.ram_dm = self.default_button('min', self.ram_dec_init, lambda: self.set_ram('dec',999999)) # min

        # Ram increment
        self.ram_i1 = self.default_button('+1', self.ram_inc_init, lambda: self.set_ram('inc',1)) # +1
        self.ram_i5 = self.default_button('+5', self.ram_inc_init, lambda: self.set_ram('inc',5)) # +5
        self.ram_im = self.default_button('max', self.ram_inc_init, lambda: self.set_ram('inc',999999)) # max

    # Create CPU buttons
    def make_cpu_buttons(self):
        # CPU decrement
        self.cpu_d1 = self.default_button('-1', self.cpu_dec_init, lambda: self.set_cpu('dec',1)) # -1
        self.cpu_d5 = self.default_button('-5', self.cpu_dec_init, lambda: self.set_cpu('dec',5)) # -5
        self.cpu_dm = self.default_button('min', self.cpu_dec_init, lambda: self.set_cpu('dec',999999)) # min

        # CPU increment
        self.cpu_i1 = self.default_button('+1', self.cpu_inc_init, lambda: self.set_cpu('inc',1)) # +1
        self.cpu_i5 = self.default_button('+5', self.cpu_inc_init, lambda: self.set_cpu('inc',5)) # +5
        self.cpu_im = self.default_button('max', self.cpu_inc_init, lambda: self.set_cpu('inc',999999)) # max

    # Create HDD buttons
    def make_hdd_buttons(self):
        # HDD decrement
        self.hdd_d1 = self.default_button('-1', self.hdd_dec_init, lambda: self.set_hdd('dec',1)) # -1
        self.hdd_d10 = self.default_button('-10', self.hdd_dec_init, lambda: self.set_hdd('dec',10)) # -10
        self.hdd_dm = self.default_button('min', self.hdd_dec_init, lambda: self.set_hdd('dec',999999)) # min

        # HDD increment
        self.hdd_i1 = self.default_button('+1', self.hdd_inc_init, lambda: self.set_hdd('inc',1)) # +1
        self.hdd_i10 = self.default_button('+10', self.hdd_inc_init, lambda: self.set_hdd('inc',10)) # +10
        self.hdd_im = self.default_button('max', self.hdd_inc_init, lambda: self.set_hdd('inc',999999)) # max

    # Create Reset to Default buttons
    def make_reset_buttons(self):
        self.reset_ram = self.default_button('Reset RAM', 'normal', self.ram_to_default)
        self.reset_cpu = self.default_button('Reset CPU', 'normal', self.cpu_to_default)
        self.reset_hdd = self.default_button('Reset HDD', 'normal', self.hdd_to_default)

    # Create Start button
    def make_start_button(self):
        text = "Start GroundSeg"
        rad = 12
        fg = "#008EFF"
        bc = "#008EFF"
        self.start = customtkinter.CTkButton(
                self,text=text,corner_radius=rad,fg_color=fg,border_color=bc,command=self.start_groundseg
                )

    def place_widgets(self):

        # Title
        self.main_title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        # RAM
        self.ram_title.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
        self.ram_label.place(relx=0.5, rely=0.22, anchor=tk.CENTER)
        self.ram_dm.place(relx=0.15, rely=0.22, anchor=tk.CENTER)
        self.ram_d5.place(relx=0.25, rely=0.22, anchor=tk.CENTER)
        self.ram_d1.place(relx=0.35, rely=0.22, anchor=tk.CENTER)
        self.ram_i1.place(relx=0.65, rely=0.22, anchor=tk.CENTER)
        self.ram_i5.place(relx=0.75, rely=0.22, anchor=tk.CENTER)
        self.ram_im.place(relx=0.85, rely=0.22, anchor=tk.CENTER)

        # CPU
        self.cpu_title.place(relx=0.5, rely=0.32, anchor=tk.CENTER)
        self.cpu_label.place(relx=0.5, rely=0.39, anchor=tk.CENTER)
        self.cpu_dm.place(relx=0.15, rely=0.39, anchor=tk.CENTER)
        self.cpu_d5.place(relx=0.25, rely=0.39, anchor=tk.CENTER)
        self.cpu_d1.place(relx=0.35, rely=0.39, anchor=tk.CENTER)
        self.cpu_i1.place(relx=0.65, rely=0.39, anchor=tk.CENTER)
        self.cpu_i5.place(relx=0.75, rely=0.39, anchor=tk.CENTER)
        self.cpu_im.place(relx=0.85, rely=0.39, anchor=tk.CENTER)

        # HDD
        self.hdd_title.place(relx=0.5, rely=0.49, anchor=tk.CENTER)
        self.hdd_label.place(relx=0.5, rely=0.56, anchor=tk.CENTER)
        self.hdd_dm.place(relx=0.15, rely=0.56, anchor=tk.CENTER)
        self.hdd_d10.place(relx=0.25, rely=0.56, anchor=tk.CENTER)
        self.hdd_d1.place(relx=0.35, rely=0.56, anchor=tk.CENTER)
        self.hdd_i1.place(relx=0.65, rely=0.56, anchor=tk.CENTER)
        self.hdd_i10.place(relx=0.75, rely=0.56, anchor=tk.CENTER)
        self.hdd_im.place(relx=0.85, rely=0.56, anchor=tk.CENTER)

        # Default
        self.defaults_title.place(relx=0.5, rely=0.68, anchor=tk.CENTER)
        self.reset_ram.place(relx=0.3, rely=0.75, anchor=tk.CENTER)
        self.reset_cpu.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        self.reset_hdd.place(relx=0.7, rely=0.75, anchor=tk.CENTER)

        # Launch
        self.start.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def configure_ram_dec(self, state):
        self.ram_d1.configure(state=state)
        self.ram_d5.configure(state=state)
        self.ram_dm.configure(state=state)

    def configure_ram_inc(self, state):
        self.ram_i1.configure(state=state)
        self.ram_i5.configure(state=state)
        self.ram_im.configure(state=state)

    def configure_cpu_dec(self, state):
        self.cpu_d1.configure(state=state)
        self.cpu_d5.configure(state=state)
        self.cpu_dm.configure(state=state)

    def configure_cpu_inc(self, state):
        self.cpu_i1.configure(state=state)
        self.cpu_i5.configure(state=state)
        self.cpu_im.configure(state=state)

    def configure_hdd_dec(self, state):
        self.hdd_d1.configure(state=state)
        self.hdd_d10.configure(state=state)
        self.hdd_dm.configure(state=state)

    def configure_hdd_inc(self, state):
        self.hdd_i1.configure(state=state)
        self.hdd_i10.configure(state=state)
        self.hdd_im.configure(state=state)

    # Start GroundSeg
    def start_groundseg(self):
        with open(self.config_file, "w") as f:
            json.dump({"ram":self.ram,"cpu":self.cpu,"hdd":self.hdd}, f, indent = 4)
            f.close()

        print("Starting GroundSeg")
        print(f"ram: {self.ram}")
        print(f"cpu: {self.cpu}")
        print(f"hdd: {self.hdd}")
        print("start qemu")
        # insert qemu command here

    # Change Ram value
    def set_ram(self, change, v):
        if change == 'inc':
            self.ram = self.ram + v # increment ram
            self.configure_ram_dec('normal') # set dec buttons to normal
        elif change == 'dec':
            self.ram = self.ram - v # decrement ram
            self.configure_ram_inc('normal') # set inc buttons to normal

        if self.ram >= self.total_ram - 1:
            # ram maxed out
            self.ram = self.total_ram - 1
            self.configure_ram_inc('disabled')
        elif self.ram <= self.min_ram:
            # ram is at minimum
            self.ram = self.min_ram
            self.configure_ram_dec('disabled')

        self.ram_label.configure(text=f"{self.ram}/{self.total_ram - 1} GB")
        self.place_widgets()

    # Change CPU value
    def set_cpu(self, change, v):
        if change == 'inc':
            self.cpu = self.cpu + v # increment ram
            self.configure_cpu_dec('normal') # set dec buttons to normal
        elif change == 'dec':
            self.cpu = self.cpu - v # decrement ram
            self.configure_cpu_inc('normal') # set inc buttons to normal

        if self.cpu >= self.total_cpu:
            # ram maxed out
            self.cpu = self.total_cpu
            self.configure_cpu_inc('disabled')
        elif self.cpu <= self.min_cpu:
            # cpu is at minimum
            self.cpu = self.min_cpu
            self.configure_cpu_dec('disabled')

        self.cpu_label.configure(text=f"{self.cpu}/{self.total_cpu} cores")
        self.place_widgets()

    # Change HDD value
    def set_hdd(self, change, v):
        if change == 'inc':
            self.hdd = self.hdd + v # increment ram
            self.configure_hdd_dec('normal') # set dec buttons to normal
        elif change == 'dec':
            self.hdd = self.hdd - v # decrement ram
            self.configure_hdd_inc('normal') # set inc buttons to normal

        if self.hdd >= self.free_hdd:
            # ram maxed out
            self.hdd = self.free_hdd
            self.configure_hdd_inc('disabled')
        elif self.hdd <= self.min_hdd:
            # hdd is at minimum
            self.hdd = self.min_hdd
            self.configure_hdd_dec('disabled')

        self.hdd_label.configure(text=f"{self.hdd}/{self.free_hdd} GB")
        self.place_widgets()

    def ram_to_default(self):
        self.ram = self.default_ram
        self.ram_label.configure(text=f"{self.ram}/{self.total_ram - 1} GB")
        self.place_widgets()

    def cpu_to_default(self):
        self.cpu = self.default_cpu
        self.cpu_label.configure(text=f"{self.cpu}/{self.total_cpu} cores")
        self.place_widgets()

    def hdd_to_default(self):
        self.hdd = self.default_hdd
        self.hdd_label.configure(text=f"{self.hdd}/{self.free_hdd} GB")
        self.place_widgets()

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        threading.Thread(target=self.switch_pages, daemon=True).start()

    def switch_pages(self):

        # Pages
        install_page = InstallPage(self)
        installing_page = InstallingPage(self)
        launcher_page = LauncherPage(self)
        fix_page = FixPage(self)
        fixing_page = FixingPage(self)

        # Main container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Stacking pages on top of each other
        install_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        installing_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        launcher_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        fixing_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        fix_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # Infinite loop that decides which page is shown
        while True:
            if u.shown == 'installing':
                installing_page.show()
            elif u.shown == 'install':
                install_page.show()
            elif u.shown == 'launcher':
                launcher_page.show()
            elif u.shown == 'fixing':
                fixing_page.show()
            else:
                fix_page.show()

            sleep(0.1)

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    root = customtkinter.CTk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("640x480")
    root.title("GroundSeg Launcher")
    root.mainloop()
