import tkinter as tk
import customtkinter
import threading
import psutil
import os

from utils import Utils
from time import sleep

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
       label = customtkinter.CTkLabel(self,
                                      text="GroundSeg is missing required files",
                                      height=240
                                      )
       # Fix button
       button = customtkinter.CTkButton(self,
                                        text="Fix",
                                        corner_radius=12,
                                        fg_color="#008EFF",
                                        border_color="#008EFF",
                                        command=fix_groundseg)

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

        to_gb = 2**30
        self.total_ram = int(psutil.virtual_memory().total / to_gb) #GB
        total_cpu = int(os.cpu_count())
        free_hdd = int(psutil.disk_usage('/').free / to_gb) #GB

        # default amount 80%
        self.ram = int(self.total_ram * 0.8) #GB
        self.cpu = int(total_cpu * 0.8)
        self.hdd = int(free_hdd * 0.8) #GB

        # button states
        self.ram_hep = 'normal'
        self.ram_lus = 'normal'

        def set_ram(change, v):

            if change == 'inc':
                self.ram = self.ram + v
                # If inc called, set all decrement buttons to normal
                self.ram_dec_button_one.configure(state='normal')
                self.ram_dec_button_five.configure(state='normal')
                self.ram_min_button.configure(state='normal')

            elif change == 'dec':
                # if dec is called, set all increment buttons to normal
                self.ram = self.ram - v
                self.ram_inc_button_one.configure(state='normal')
                self.ram_inc_button_five.configure(state='normal')
                self.ram_max_button.configure(state='normal')

            if self.ram >= self.total_ram - 1:
                self.ram = self.total_ram - 1
                # if already at max, set increment buttons to disabled
                self.ram_inc_button_one.configure(state='disabled')
                self.ram_inc_button_five.configure(state='disabled')
                self.ram_max_button.configure(state='disabled')

            elif self.ram <= 4:
                self.ram = 4
                # if already at min, set decrement buttons to disabled
                self.ram_dec_button_one.configure(state='disabled')
                self.ram_dec_button_five.configure(state='disabled')
                self.ram_min_button.configure(state='disabled')

            self.ram_label.configure(text=f"RAM - {self.ram}/{self.total_ram - 1} GB")

            self.ram_min_button.place(relx=0.14, rely=0.2, anchor=tk.CENTER)
            self.ram_dec_button_five.place(relx=0.25, rely=0.2, anchor=tk.CENTER)
            self.ram_dec_button_one.place(relx=0.35, rely=0.2, anchor=tk.CENTER)
            self.ram_inc_button_one.place(relx=0.65, rely=0.2, anchor=tk.CENTER)
            self.ram_inc_button_five.place(relx=0.75, rely=0.2, anchor=tk.CENTER)
            self.ram_max_button.place(relx=0.86, rely=0.2, anchor=tk.CENTER)

        def start_groundseg(ram,cpu,hdd):
            print("Starting GroundSeg")
            print(f"ram: {ram}")
            print(f"cpu: {cpu}")
            print(f"hdd: {hdd}")
            # insert qemu command here

        # Alloc labels
        self.title_label = customtkinter.CTkLabel(self, text="Resource Allocation")
        self.ram_label = customtkinter.CTkLabel(self, text=f"RAM - {self.ram}/{self.total_ram - 1} GB")
        #cpu_label = customtkinter.CTkLabel(self, text="CPU cores allocation")
        #hdd_label = customtkinter.CTkLabel(self, text="Storage allocation")

        self.ram_dec_button_one = customtkinter.CTkButton(self,
                                                          text="-1",
                                                          width=12,
                                                          corner_radius=12,
                                                          fg_color="#008EFF",
                                                          border_color="008EFF",
                                                          state=self.ram_hep,
                                                          command=lambda: set_ram('dec',1)
                                                          )

        self.ram_dec_button_five = customtkinter.CTkButton(self,
                                                           text="-5",
                                                           width=12,
                                                           corner_radius=12,
                                                           fg_color="#008EFF",
                                                           border_color="008EFF",
                                                           state=self.ram_hep,
                                                           command=lambda: set_ram('dec',5)
                                                           )

        self.ram_inc_button_one = customtkinter.CTkButton(self,
                                                          text="+1",
                                                          width=12,
                                                          corner_radius=12,
                                                          fg_color="#008EFF",
                                                          border_color="008EFF",
                                                          state=self.ram_lus,
                                                          command=lambda: set_ram('inc',1)
                                                          )

        self.ram_inc_button_five = customtkinter.CTkButton(self,
                                                           text="+5",
                                                           width=12,
                                                           corner_radius=12,
                                                           fg_color="#008EFF",
                                                           border_color="008EFF",
                                                           state=self.ram_lus,
                                                           command=lambda: set_ram('inc',5)
                                                           )

        self.ram_min_button = customtkinter.CTkButton(self,
                                                      text="Min",
                                                      width=12,
                                                      corner_radius=12,
                                                      fg_color="#008EFF",
                                                      border_color="008EFF",
                                                      state=self.ram_hep,
                                                      command=lambda: set_ram('dec',999999)
                                                      )

        self.ram_max_button = customtkinter.CTkButton(self,
                                                      text="Max",
                                                      width=12,
                                                      corner_radius=12,
                                                      fg_color="#008EFF",
                                                      border_color="008EFF",
                                                      state=self.ram_hep,
                                                      command=lambda: set_ram('inc',999999)
                                                      )

        # Start button
        self.start_button = customtkinter.CTkButton(self,
                                               text="Start GroundSeg",
                                               corner_radius=12,
                                               fg_color="#008EFF",
                                               border_color="#008EFF",
                                               command=lambda: start_groundseg(self.ram,cpu,hdd)
                                               )

        # Title
        self.title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # RAM
        self.ram_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.ram_min_button.place(relx=0.14, rely=0.2, anchor=tk.CENTER)
        self.ram_dec_button_five.place(relx=0.25, rely=0.2, anchor=tk.CENTER)
        self.ram_dec_button_one.place(relx=0.35, rely=0.2, anchor=tk.CENTER)
        self.ram_inc_button_one.place(relx=0.65, rely=0.2, anchor=tk.CENTER)
        self.ram_inc_button_five.place(relx=0.75, rely=0.2, anchor=tk.CENTER)
        self.ram_max_button.place(relx=0.86, rely=0.2, anchor=tk.CENTER)

        # Launch
        self.start_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

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
    root.wm_geometry("480x320")
    root.title("GroundSeg Launcher")
    root.mainloop()
