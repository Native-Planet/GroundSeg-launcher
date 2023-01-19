import customtkinter as ct
import time
from pages import InstallPage, InstallingPage, FixPage, LauncherPage, Control
from utils import Utils
from threading import Thread


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
        self.current_frame = None
        self.switch_frame(self.make_valid_frame())

    def make_valid_frame(self):
        valid = self.u.valid_page()
        # do background stuff here
        return valid[0]

    def switch_frame(self, page):
        if self.current_frame:
            self.current_frame(self).destroy()

        if page == 'install':
            self.current_frame = InstallPage

        if page == 'fix':
            self.current_frame = FixPage

        if page == 'installing':
            self.current_frame = InstallingPage
            self.u.installing = True

        if page == 'launcher':
            self.current_frame = LauncherPage

        if page == 'control':
            self.current_frame = Control

        self.current_frame(self).place(relx=0.5, rely=0.5, anchor=ct.CENTER)

        Thread(target=self.check_installing, daemon=True).start()

    def check_installing(self):
        if self.u.installing:
            while self.u.installing:
                time.sleep(0.1)

            self.switch_frame(self.make_valid_frame())

if __name__ == "__main__":
    ct.set_appearance_mode("dark")
    app = MainApp()
    app.mainloop()
