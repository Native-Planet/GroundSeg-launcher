import customtkinter as ct
import webbrowser
import socket
import json
import subprocess
import psutil
import json
import os
import time
from threading import Thread
from resize import ResizeImage


class InstallPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)
        def install_groundseg():
            Thread(target=master.u.install_groundseg, daemon=True).start()
            master.switch_frame('installing')

        # Title
        l_text = "GroundSeg is not detected on your device."
        lbl = ct.CTkLabel(self,text=l_text, font=(None, 16))

        # Install button
        b_text = "Install GroundSeg"
        b_rad = 100
        #c = "#008EFF"
        c = "#FFFFFF"
        cmd = install_groundseg
        btn = ct.CTkButton(self,
                           text=b_text,
                           corner_radius=b_rad,
                           border_color=c,
                           border_width=2,
                           width=240,
                           border_spacing=12,
                           fg_color="transparent",
                           hover_color=c,
                           command=cmd)

        # Pack
        lbl.place(relx=0.5, rely=0.4, anchor=ct.CENTER)
        btn.place(relx=0.5, rely=0.6, anchor=ct.CENTER)

class FixPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)
        def fix_groundseg():
            Thread(target=master.u.fix_groundseg, daemon=True).start()
            master.switch_frame('fixing')

        # Title
        l_text = "GroundSeg is missing required files"
        lbl = ct.CTkLabel(self,text=l_text, font=(None, 16))

        # Install button
        b_text = "Repair"
        b_rad = 100
        c = "#FFFFFF"
        cmd = fix_groundseg
        btn = ct.CTkButton(self,
                           text=b_text,
                           corner_radius=b_rad,
                           border_color=c,
                           border_width=2,
                           width=240,
                           border_spacing=12,
                           fg_color="transparent",
                           hover_color=c,
                           command=cmd)

        # Pack
        lbl.place(relx=0.5, rely=0.4, anchor=ct.CENTER)
        btn.place(relx=0.5, rely=0.6, anchor=ct.CENTER)

class InstallingPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)
        l_text = "GroundSeg is installing..."
        p_text = "Please be patient"
        lbl = ct.CTkLabel(self,text=l_text, font=(None, 14))
        p_lbl = ct.CTkLabel(self,text=p_text, font=(None, 10))
        lbl.place(relx=0.5, rely=0.4, anchor=ct.CENTER)
        p_lbl.place(relx=0.5, rely=0.6, anchor=ct.CENTER)

class FixingPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)
        l_text = "GroundSeg is repairing..."
        p_text = "Please be patient"
        lbl = ct.CTkLabel(self,text=l_text, font=(None, 14))
        p_lbl = ct.CTkLabel(self,text=p_text, font=(None, 10))
        lbl.place(relx=0.5, rely=0.4, anchor=ct.CENTER)
        p_lbl.place(relx=0.5, rely=0.6, anchor=ct.CENTER)

class LaunchingPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)
        l_text = "GroundSeg is starting"
        p_text = "Please be patient"
        lbl = ct.CTkLabel(self,text=l_text, font=(None, 14))
        p_lbl = ct.CTkLabel(self,text=p_text, font=(None, 10))
        lbl.place(relx=0.5, rely=0.4, anchor=ct.CENTER)
        p_lbl.place(relx=0.5, rely=0.6, anchor=ct.CENTER)

class Control(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)

        self.config_file = f"{master.u.install_dir}/launcher.json"
        self.make_buttons(master)
        self.place_buttons()

    def make_buttons(self,master):
        self.restart = self.control_button("Restart GroundSeg", "#F5CA7B", lambda: self.restart_vm(master))
        self.stop = self.control_button("Stop GroundSeg", "#F47174", lambda: self.stop_vm(master))
        self.open = ct.CTkButton(self, text="Open Web UI", command=self.open_groundseg,
                                 fg_color="#008EFF",text_color="#FFFFFF",border_spacing=8,
                                 font=(None,16),width=480,corner_radius=16,
                                 height=36)

    def control_button(self,text,color,cmd):
        return ct.CTkButton(self,text=text,command=cmd,
                            fg_color="transparent",border_spacing=6, 
                            text_color=color,border_color=color,
                            font=(None,14), border_width=1,width=240,
                            corner_radius=20,hover_color="#FFFFFF")

    def place_buttons(self):
        self.restart.place(relx=0.3,rely=0.3,anchor=ct.CENTER)
        self.stop.place(relx=0.7,rely=0.3,anchor=ct.CENTER)
        self.open.place(relx=0.5,rely=0.6,anchor=ct.CENTER)

    def prompt_password(self, master):
        self.start_groundseg(master)

    def restart_vm(self,master):
        with open(self.config_file) as f:
            cfg = json.load(f)
            self.ram = cfg['ram']
            self.cpu = cfg['cpu']
            f.close()

        # Pop up
        dialog = ct.CTkInputDialog(text="Admin Password:", title="Password")
        self.password = dialog.get_input()
        # Stop command
        cat = f"$(echo $(echo {self.password} | sudo -S cat {master.u.install_dir}/pid))"
        subprocess.run(f"echo {self.password} | sudo -S kill {cat}", shell=True)
        time.sleep(3)
        # Start command
        vm_bin = f"{master.u.install_dir}/qemu-binaries/qemu-system-x86_64"
        vm_img = f"{master.u.install_dir}/groundseg.qcow2"
        pid = f"{master.u.install_dir}/pid"
        ports = ''.join(map(lambda x: f',hostfwd=tcp::{x}-:{x}',range(8081,8100)))
        cmd = ' '.join(['echo',self.password,'|','sudo','-S',
                       vm_bin,vm_img,'-smp',str(self.cpu),'-m',f"{self.ram}G",
                       '-nic','user,hostfwd=tcp::80-:80,hostfwd=tcp::27016-:27016' + ports,
                       '-accel','hvf','-display','none', '-pidfile', pid,'-daemonize'])
        subprocess.Popen(cmd,shell=True)
        # Switch frame
        master.switch_frame('launching')

    def stop_vm(self,master):
        dialog = ct.CTkInputDialog(text="Admin Password:", title="Password")
        self.password = dialog.get_input()
        cat = f"$(echo $(echo {self.password} | sudo -S cat {master.u.install_dir}/pid))"
        subprocess.run(f"echo {self.password} | sudo -S kill {cat}", shell=True)
        master.switch_frame('launcher')
    
    def open_groundseg(self):
        webbrowser.open(f"http://{socket.gethostname()}.local")


class LauncherPage(ct.CTkFrame):
    def __init__(self, master):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=master.w_width, height=master.w_height)

        # initialize variables
        self.load_values(master)
        # make bottom panel buttons
        self.make_buttons(master)
        # default to basic menu
        self.to_basic()
        # place start button
        self.start_btn.place(relx=0.8,rely=0.9,anchor=ct.CENTER)

    def make_buttons(self, master):
        white="#FFFFFF"
        blue="#008EFF"
        # Switch between advanced and basic menus
        self.tab_btn = ct.CTkButton(self,fg_color='transparent',
                                    border_color=white,
                                    width=180,
                                    border_width=1,
                                    corner_radius=12,
                                    border_spacing=4,
                                    hover_color=white)
        # Start GroundSeg VM
        self.start_btn = ct.CTkButton(self,fg_color=blue,
                                      text="Start GroundSeg",
                                      width=200,
                                      corner_radius=20,
                                      border_spacing=6,
                                      hover_color=white,
                                      command=lambda: self.prompt_password(master))
    def to_basic(self):
        self.tab_btn.configure(text='Go to Advanced Menu',command=self.to_adv)
        self.tab_btn.place(relx=0.2,rely=0.9,anchor=ct.CENTER)
        self.visible_page = BasicPage(self,self.content_width,self.content_height)
        self.visible_page.place(relx=0.5,rely=0,anchor=ct.N)
        
    def to_adv(self):
        self.tab_btn.configure(text='Back to Basic Menu',command=self.to_basic)
        self.tab_btn.place(relx=0.2,rely=0.9,anchor=ct.CENTER)
        self.visible_page = AdvancedPage(self,self.content_width,self.content_height)
        self.visible_page.place(relx=0.5,rely=0,anchor=ct.N)

    def prompt_password(self, master):
        dialog = ct.CTkInputDialog(text="Admin Password:", title="Password")
        master.password = dialog.get_input()
        self.start_groundseg(master)

    # Start GroundSeg
    def start_groundseg(self, master):
        rz_res = self.resize.set_size(self.default_hdd)
        if rz_res[0]:
            with open(self.config_file, "w") as f:
                json.dump({"ram":self.ram,"cpu":self.cpu}, f, indent = 4)
                f.close()

            # qemu command
            vm_bin = f"{master.u.install_dir}/qemu-binaries/qemu-system-x86_64"
            vm_img = f"{master.u.install_dir}/groundseg.qcow2"
            pid = f"{master.u.install_dir}/pid"
            ports = ''.join(map(lambda x: f',hostfwd=tcp::{x}-:{x}',range(8081,8100)))
            cmd = ' '.join(['echo',master.password,'|','sudo','-S',
                            vm_bin,vm_img,'-smp',str(self.cpu),'-m',f"{self.ram}G",
                            '-nic','user,hostfwd=tcp::80-:80,hostfwd=tcp::27016-:27016' + ports,
                            '-accel','hvf','-pidfile', pid,'-daemonize','-display','none'])
            subprocess.Popen(cmd,shell=True)
            master.switch_frame('launching')
        else:
            print(f"ERROR STARTING QEMU: {rz_res[1]}")

    def load_values(self, master):

        # Size of menu frame
        self.content_width = master.w_width
        self.content_height = master.w_height * 0.85

        # convert bytes to gigabytes
        gb = 2**30
        cfg = {}

        # config file
        self.config_file = f"{master.u.install_dir}/launcher.json"

        # init resize class
        self.resize = ResizeImage(f"{master.u.install_dir}/groundseg.qcow2")

        # resources available
        self.total_ram = int(psutil.virtual_memory().total / gb) #GB
        self.total_cpu = int(os.cpu_count())
        self.free_hdd = int(psutil.disk_usage('/').free / gb) #GB

        # preset settings
        # ram
        self.low_ram = int(self.total_ram * 0.4) #GB
        self.mid_ram = int(self.total_ram * 0.6) #GB
        self.default_ram = int(self.total_ram * 0.8) #GB

        # cpu
        self.low_cpu = int(self.total_cpu * 0.4)
        self.mid_cpu = int(self.total_cpu * 0.6)
        self.default_cpu = int(self.total_cpu * 0.8)

        # hdd
        self.default_hdd = int(self.free_hdd * 0.8) #GB

        try:
            with open(self.config_file) as f:
                cfg = f.json.load()
                self.ram = cfg['ram']
                self.cpu = cfg['cpu']
                f.close()
        except:
            self.ram = self.default_ram
            self.cpu = self.default_cpu

class BasicPage(ct.CTkFrame):
    def __init__(self, master, width, height):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=width, height=height)

        self.make_widgets(master)
        self.place_widgets()
        
    def make_widgets(self, master):
        self.ram_title = ct.CTkLabel(self, text="Maximum RAM Usage")
        self.ram_label = ct.CTkLabel(self, text=f"{master.ram} GB", font=(None,16))
        self.cpu_title = ct.CTkLabel(self, text="Maximum CPU Usage")
        self.cpu_label = ct.CTkLabel(self, text=f"{master.cpu} cores", font=(None,16))
        self.hdd_title = ct.CTkLabel(self, text="Maximum GroundSeg VM Storage Allowed")
        self.hdd_label = ct.CTkLabel(self, text=f"{master.default_hdd} GB", font=(None,16))
        self.usage_title = ct.CTkLabel(self, text="Current GroundSeg VM Storage Used")
        self.usage_label = ct.CTkLabel(self, text=f"{master.resize.usage()[1]} GB", font=(None,16))

    def place_widgets(self):
        # RAM
        self.ram_title.place(relx=0.5, rely=0.2, anchor=ct.CENTER)
        self.ram_label.place(relx=0.5, rely=0.27, anchor=ct.CENTER)
        # CPU
        self.cpu_title.place(relx=0.5, rely=0.37, anchor=ct.CENTER)
        self.cpu_label.place(relx=0.5, rely=0.44, anchor=ct.CENTER)
        # HDD
        self.hdd_title.place(relx=0.5, rely=0.54, anchor=ct.CENTER)
        self.hdd_label.place(relx=0.5, rely=0.61, anchor=ct.CENTER)
        # Real Usage
        self.usage_title.place(relx=0.5, rely=0.71, anchor=ct.CENTER)
        self.usage_label.place(relx=0.5, rely=0.78, anchor=ct.CENTER)

class AdvancedPage(ct.CTkFrame):
    def __init__(self, master, width, height):
        ct.CTkFrame.__init__(self, master, fg_color="transparent", width=width, height=height)

        self.make_widgets(master)
        self.place_widgets()

    def make_widgets(self, master):
        self.ram_title = ct.CTkLabel(self, text="Maximum RAM Usage (GB)")
        self.cpu_title = ct.CTkLabel(self, text="Maximum CPU Usage (Cores)")
        self.hdd_title = ct.CTkLabel(self, text="Maximum GroundSeg VM Storage Allowed")
        self.hdd_label = ct.CTkLabel(self, text=f"{master.default_hdd} GB", font=(None,16))
        self.usage_title = ct.CTkLabel(self, text="Current GroundSeg VM Storage Used")
        self.usage_label = ct.CTkLabel(self, text=f"{master.resize.usage()[1]} GB", font=(None,16))
        
        self.ram_select(master)
        self.cpu_select(master)

    def ram_select(self, master):
        white = "#ffffff"
        def set_ram(v):
            master.ram = int(v)

        vals = list(map(str, list(range(4,master.total_ram))))
        shown_val = ct.StringVar(value=str(master.default_ram))
        self.ram_sel = ct.CTkComboBox(self,command=set_ram)
        self.ram_sel.configure(variable=shown_val, values=vals)

    def cpu_select(self, master):
        def set_cpu(v):
            master.cpu = int(v)

        vals = list(map(str , list(range(1,master.total_cpu + 1))))
        shown_val = ct.StringVar(value=str(master.default_cpu))
        self.cpu_sel = ct.CTkComboBox(self,command=set_cpu)
        self.cpu_sel.configure(variable=shown_val, values=vals)

    def place_widgets(self):
        # RAM
        self.ram_title.place(relx=0.5, rely=0.2, anchor=ct.CENTER)
        self.ram_sel.place(relx=0.5, rely=0.27, anchor=ct.CENTER)
        # CPU
        self.cpu_title.place(relx=0.5, rely=0.37, anchor=ct.CENTER)
        self.cpu_sel.place(relx=0.5, rely=0.44, anchor=ct.CENTER)
        # HDD
        self.hdd_title.place(relx=0.5, rely=0.54, anchor=ct.CENTER)
        self.hdd_label.place(relx=0.5, rely=0.61, anchor=ct.CENTER)
        # Real Usage
        self.usage_title.place(relx=0.5, rely=0.71, anchor=ct.CENTER)
        self.usage_label.place(relx=0.5, rely=0.78, anchor=ct.CENTER)
