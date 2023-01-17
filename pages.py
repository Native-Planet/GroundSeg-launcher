import customtkinter as ct
import psutil
import json
import os
from threading import Thread
from resize import ResizeImage

class InstallPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)
        def install_groundseg():
            Thread(target=master.u.install_groundseg, daemon=True).start()
            master.switch_frame('installing')

        # Title
        l_text = "GroundSeg is not installed"
        lbl = ct.CTkLabel(self,text=l_text)

        # Install button
        b_text = "Install"
        b_rad = 12
        c = "#008EFF"
        cmd = install_groundseg
        btn = ct.CTkButton(self,text=b_text,corner_radius=b_rad,border_color=c,fg_color=c,command=cmd)

        # Pack
        lbl.place(relx=0.5, rely=0.4, anchor=ct.CENTER)
        btn.place(relx=0.5, rely=0.6, anchor=ct.CENTER)

class FixPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)
        def fix_groundseg():
            Thread(target=master.u.fix_groundseg, daemon=True).start()

        # Title
        l_text = "GroundSeg is missing required files"
        lbl = ct.CTkLabel(self,text=l_text)

        # Install button
        b_text = "Fix"
        b_rad = 12
        c = "#008EFF"
        cmd = fix_groundseg
        btn = ct.CTkButton(self,text=b_text,corner_radius=b_rad,border_color=c,fg_color=c,command=cmd)

        # Pack
        lbl.place(relx=0.5, rely=0.4, anchor=ct.CENTER)
        btn.place(relx=0.5, rely=0.6, anchor=ct.CENTER)

class InstallingPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)
        l_text = "Please be patient while we install GroundSeg..."
        lbl = ct.CTkLabel(self,text=l_text)
        lbl.place(relx=0.5, rely=0.5, anchor=ct.CENTER)

class LauncherPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)

        self.master = master
        self.w_width = master.w_width
        self.w_height = master.w_height * 0.85

        self.tab = 'simple'
        self.make_buttons()
        self.place_buttons()
        self.place_page('simple',self.master)

    def set_simple(self):
        if self.tab != 'simple':
            self.btn_smp.configure(border_color="#0077BB", fg_color="#0077BB",state='disabled')
            self.btn_adv.configure(border_color="#008EFF", fg_color="#008EFF",state='normal')
            self.tab = 'simple'

        self.place_buttons()
        self.place_page(self.tab,self.master)

    def set_advanced(self):
        if self.tab != 'advanced':
            self.btn_adv.configure(border_color="#0077BB", fg_color="#0077BB",state='disabled')
            self.btn_smp.configure(border_color="#008EFF", fg_color="#008EFF",state='normal')
            self.tab = 'advanced'

        self.place_buttons()
        self.place_page(self.tab,self.master)

    def place_buttons(self):
        self.btn_smp.place(relx=0.38,rely=0.05,anchor=ct.CENTER)
        self.btn_adv.place(relx=0.62,rely=0.05,anchor=ct.CENTER)


    def make_buttons(self):
        smp_text = "Simple"
        adv_text = "Advanced"
        b_rad = 12
        c = "#008EFF"
        d = "#0077BB"
        smp_cmd = self.set_simple
        adv_cmd = self.set_advanced

        self.btn_smp = ct.CTkButton(self,
                                    text=smp_text,
                                    corner_radius=b_rad,
                                    border_color=c,
                                    fg_color=c,
                                    state='disabled',
                                    command=smp_cmd
                                    )
        self.btn_adv = ct.CTkButton(self,
                                    text=adv_text,
                                    corner_radius=b_rad,
                                    border_color=d,
                                    fg_color=d,
                                    command=adv_cmd
                                    )

    
    def make_pages(self,master):
        self.advanced_page = AdvancedPage(self, master)
        self.simple_page = SimplePage(self, master)

    def place_page(self,page,master):
        self.make_pages(master)
        if page == 'simple':
            self.advanced_page.destroy()
            self.simple_page.place(relx=0.5,rely=0.52,anchor=ct.CENTER)
        if page == 'advanced':
            self.simple_page.destroy()
            self.advanced_page.place(relx=0.5,rely=0.52,anchor=ct.CENTER)

class SimplePage(ct.CTkFrame):
    def __init__(self, master, grandmaster):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)
        ct.CTkLabel(self, text="simple page placeholder").place(relx=0.5,rely=0.5,anchor=ct.CENTER)

class AdvancedPage(ct.CTkFrame):
    def __init__(self, master, grandmaster):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)

        self.load_values(grandmaster)
        self.make_labels()
        self.make_ram_buttons()
        self.make_cpu_buttons()
        self.make_hdd_buttons()
        self.make_reset_buttons()
        self.make_start_button()
        self.place_widgets()

    # Default values
    def load_values(self,grandmaster):

        # convert bytes to gigabytes
        gb = 2**30
        cfg = {}

        # config file
        self.config_file = f"{grandmaster.u.install_dir}/launcher.json"

        # init resize class
        self.resize = ResizeImage(f"{grandmaster.u.install_dir}/groundseg.qcow2")

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

        return ct.CTkButton(self,
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
        self.main_title = ct.CTkLabel(self, text="Advanced Virtual Machine Settings", font=(None,16))
        self.ram_title = ct.CTkLabel(self, text="RAM")
        self.ram_label = ct.CTkLabel(self, text=f"{self.ram}/{self.total_ram - 1} GB")
        self.cpu_title = ct.CTkLabel(self, text="CPU")
        self.cpu_label = ct.CTkLabel(self, text=f"{self.cpu}/{self.total_cpu} cores")
        self.hdd_title = ct.CTkLabel(self, text="Maximum Disk Usage (Piers and s3 buckets)")
        self.hdd_label = ct.CTkLabel(self, text=f"{self.hdd}/{self.free_hdd} GB")
        self.defaults_title = ct.CTkLabel(self, text="Reset To Default Settings")

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
        self.start = ct.CTkButton(
                self,text=text,corner_radius=rad,fg_color=fg,border_color=bc,command=self.hdd_checker
                )

    def place_widgets(self):

        # Title
        self.main_title.place(relx=0.5, rely=0.05, anchor=ct.CENTER)

        # RAM
        self.ram_title.place(relx=0.5, rely=0.15, anchor=ct.CENTER)
        self.ram_label.place(relx=0.5, rely=0.22, anchor=ct.CENTER)
        self.ram_dm.place(relx=0.15, rely=0.22, anchor=ct.CENTER)
        self.ram_d5.place(relx=0.25, rely=0.22, anchor=ct.CENTER)
        self.ram_d1.place(relx=0.35, rely=0.22, anchor=ct.CENTER)
        self.ram_i1.place(relx=0.65, rely=0.22, anchor=ct.CENTER)
        self.ram_i5.place(relx=0.75, rely=0.22, anchor=ct.CENTER)
        self.ram_im.place(relx=0.85, rely=0.22, anchor=ct.CENTER)

        # CPU
        self.cpu_title.place(relx=0.5, rely=0.32, anchor=ct.CENTER)
        self.cpu_label.place(relx=0.5, rely=0.39, anchor=ct.CENTER)
        self.cpu_dm.place(relx=0.15, rely=0.39, anchor=ct.CENTER)
        self.cpu_d5.place(relx=0.25, rely=0.39, anchor=ct.CENTER)
        self.cpu_d1.place(relx=0.35, rely=0.39, anchor=ct.CENTER)
        self.cpu_i1.place(relx=0.65, rely=0.39, anchor=ct.CENTER)
        self.cpu_i5.place(relx=0.75, rely=0.39, anchor=ct.CENTER)
        self.cpu_im.place(relx=0.85, rely=0.39, anchor=ct.CENTER)

        # HDD
        self.hdd_title.place(relx=0.5, rely=0.49, anchor=ct.CENTER)
        self.hdd_label.place(relx=0.5, rely=0.56, anchor=ct.CENTER)
        self.hdd_dm.place(relx=0.15, rely=0.56, anchor=ct.CENTER)
        self.hdd_d10.place(relx=0.25, rely=0.56, anchor=ct.CENTER)
        self.hdd_d1.place(relx=0.35, rely=0.56, anchor=ct.CENTER)
        self.hdd_i1.place(relx=0.65, rely=0.56, anchor=ct.CENTER)
        self.hdd_i10.place(relx=0.75, rely=0.56, anchor=ct.CENTER)
        self.hdd_im.place(relx=0.85, rely=0.56, anchor=ct.CENTER)

        # Default
        self.defaults_title.place(relx=0.5, rely=0.68, anchor=ct.CENTER)
        self.reset_ram.place(relx=0.3, rely=0.75, anchor=ct.CENTER)
        self.reset_cpu.place(relx=0.5, rely=0.75, anchor=ct.CENTER)
        self.reset_hdd.place(relx=0.7, rely=0.75, anchor=ct.CENTER)

        # Launch
        self.start.place(relx=0.5, rely=0.9, anchor=ct.CENTER)

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

    def hdd_checker(self):
        resize_res = self.resize.resize(self.hdd)
        if resize_res[0]:
            self.start_groundseg()
        elif resize_res[1]:
            print(f"ERROR RESIZING: {resize_res[1]}")
        else:
            self.shrink_popup()
            # user wants to shrink
            # popup warning
            # use self.resize.force_resize()
            # start groundseg

    def shrink_popup(self):
        window = ct.CTkToplevel(self)
        window.geometry("400x200")
        window.title("Alert!")

        def force_start():
            fr_res = self.resize.force_resize(self.hdd)
            if fr_res[0]:
                self.start_groundseg()
            else:
                print(f"FORCE RESIZE ERROR: {fr_res}")
            window.destroy()

        warning = f"Shrink maximum disk usage from {self.resize.qc_gibs} GB to {self.hdd} GB?"
        warning_label = ct.CTkLabel(window, text=warning)

        usage_text = f"Current Usage: {self.resize.usage()[1]}"
        usage_label = ct.CTkLabel(window, text=usage_text)

        b_text = "Yes, please continue and launch GroundSeg"
        b_rad = 12
        c = "#008EFF"
        cmd = force_start
        w_button = ct.CTkButton(window,text=b_text,corner_radius=b_rad,border_color=c,fg_color=c,command=cmd)

        warning_label.place(relx=0.5,rely=0.2,anchor=ct.CENTER)
        usage_label.place(relx=0.5,rely=0.5,anchor=ct.CENTER)
        w_button.place(relx=0.5,rely=0.8,anchor=ct.CENTER)


    # Start GroundSeg
    def start_groundseg(self):

        with open(self.config_file, "w") as f:
            json.dump({"ram":self.ram,"cpu":self.cpu,"hdd":self.hdd}, f, indent = 4)
            f.close()

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
