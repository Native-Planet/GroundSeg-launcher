import os
import time
import requests
import socket
from threading import Thread

import customtkinter as ct
import paramiko

# Classes
from pages import InstallPage, InstallingPage, FixPage, FixingPage, LaunchingPage, LauncherPage, Control
from utils import Utils

# Main class
class MainApp(ct.CTk):
    def __init__(self):
        ct.CTk.__init__(self)

        # Load utils class
        self.u = Utils()

        # Main Window
        self.w_width = 640
        self.w_height = 480
        self.geometry(f"{self.w_width}x{self.w_height}")
        self.title("GroundSeg Launcher")

        # Frame switcher
        self.launching = False
        self.current_frame = None
        if os.path.isfile(f"{self.u.install_dir}/pid"):
            page = 'control'
        else:
            page = self.make_valid_frame()
        self.switch_frame(page)

    def make_valid_frame(self):
        valid = self.u.valid_page()
        print(f"Missing packages: {valid[1]}")
        self.u.packages = valid[1]
        return valid[0]

    def switch_frame(self, page):
        print(page)
        if self.current_frame:
            self.current_frame(self).destroy()

        if page == 'install':
            self.current_frame = InstallPage

        if page == 'fix':
            self.current_frame = FixPage

        if page == 'installing':
            self.current_frame = InstallingPage
            self.u.installing = True

        if page == 'fixing':
            self.current_frame = FixingPage
            self.u.fixing = True

        if page == 'launching':
            self.launching = True
            self.current_frame = LaunchingPage

        if page == 'control' or os.path.isfile(f"{self.u.install_dir}/pid"):
            self.current_frame = Control

        if page == 'launcher':
            self.current_frame = LauncherPage


        self.current_frame(self).place(relx=0.5, rely=0.5, anchor=ct.CENTER)

        Thread(target=self.check_installing, daemon=True).start()
        Thread(target=self.check_fixing, daemon=True).start()
        Thread(target=self.check_launching, daemon=True).start()

    def check_installing(self):
        if self.u.installing:
            while self.u.installing:
                time.sleep(0.1)

            self.switch_frame(self.make_valid_frame())

    def check_fixing(self):
        if self.u.fixing:
            while self.u.fixing:
                time.sleep(0.1)

            self.switch_frame(self.make_valid_frame())

    def check_launching(self):
        if self.launching:
            while self.launching:
                addr = socket.gethostname()
                if not '.local' in addr:
                    addr = f"{addr}.local"
                name = addr[:-6]
                port=1723
                username='setname'
                password='setnamepass'
                cmd=f'sudo hostnamectl set-hostname {name}' 
                try:
                    r = requests.get(f"http://{addr}")
                    if r.status_code == 200:
                        # Set hostname
                        ssh=paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(addr,port,username,password)
                        ssh.exec_command(cmd) # first time won't work
                        time.sleep(3)
                        ssh.exec_command(cmd) # second time will

                        # Switch to launcher screen
                        self.launching = False
                        self.switch_frame('control')

                except Exception as e:
                    pass

if __name__ == "__main__":
    ct.set_appearance_mode("dark")
    app = MainApp()
    app.mainloop()
