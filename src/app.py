import tkinter as tk
import threading
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

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

class InstallPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

       def install_groundseg():
           threading.Thread(target=u.install_groundseg, daemon=True).start()

       # Title
       label = tk.Label(self, text="GroundSeg is not installed.")
       label.pack()

       # Install button
       button = tk.Button(self, text="Install", command=install_groundseg)
       button.pack()

class FixPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

       def fix_groundseg():
           to_fix = u.shown.split('-')[1]
           threading.Thread(target=u.fix_groundseg, args=(to_fix,), daemon=True).start()

       # Title
       label = tk.Label(self, text="GroundSeg is missing required files")
       label.pack()

       # Install button
       button = tk.Button(self, text="Fix", command=fix_groundseg)
       button.pack()

class InstallingPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Installing GroundSeg")
       # Progress bar?
       label.pack(side="top", fill="both", expand=True)

class FixingPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Fixing GroundSeg")
       # Progress bar?
       label.pack(side="top", fill="both", expand=True)

class LauncherPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="GroundSeg Launcher")
       label.pack(side="top", fill="both", expand=True)

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
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("480x320")
    root.mainloop()
