from customtkinter import *

class App:
    _page = "install"
    .set_appearance_mode("dark")
root = tk.CTk()

root.geometry("640x480")
root.title("GroundSeg Launcher") #title


    def __init__(self, page):
        self._page = page


    root.mainloop()
