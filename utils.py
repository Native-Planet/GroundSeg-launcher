import os
import json
import time
import tarfile
import requests
from threading import Thread

class Utils:
    #install_dir = f'/Users/{os.environ["USER"]}/Documents/groundseg'
    install_dir = f'/home/nal/gsl_files'
    dl_addr = "https://2333367189d562c7da7650ec610d55a0.r2.cloudflarestorage.com/groundseg"

    installing = False
    fixing = False

    def check_qemu_binaries(self):
        return os.path.isdir(f"{self.install_dir}/qemu-binaries")

    def check_qemu_image(self):
        return os.path.isfile(f"{self.install_dir}/groundseg.qcow2")

    def valid_page(self):
        # List of uninstalled packages
        packages = []
        if not self.check_qemu_binaries():
            packages.append('qemu-bin')
        if not self.check_qemu_image():
            packages.append('image')

        # Valid page to display
        n = len(packages)
        page = 'launcher'
        if n == 2:
            page = 'install'
        elif n == 1:
            page = 'fix'
        elif n > 2:
            page = 'error'

        return (page, packages)

    def install_groundseg(self):
        self.incomplete = ['image','qemu-bin','qemu-src']
        print("Installing groundseg")

        # Start threads
        # groundseg image
        Thread(target=self.download_and_extract,
               args=(self.dl_addr, 'groundseg-img.tar.xz','image'),
               daemon=True
               ).start()

        # qemu binaries
        Thread(target=self.download_and_extract,
               args=(self.dl_addr, 'qemu-bin.tar.xz', 'qemu-bin'),
               daemon=True
               ).start()

        # qemu source code
        Thread(target=self.download_and_extract,
               args=(self.dl_addr, 'qemu-7.2.0.tar.xz', 'qemu-src'),
               daemon=True
               ).start()

        # switch displayed page when downloads are completed
        Thread(target=self.install_page_switch, daemon=True).start()

    def fix_groundseg(self):
        print("Repairing groundseg")
        self.incomplete = self.packages

        # Start threads
        if 'image' in self.incomplete:
            # groundseg image
            Thread(target=self.download_and_extract,
                   args=(self.dl_addr, 'groundseg-img.tar.xz','image'),
                   daemon=True
                   ).start()

        if 'qemu-bin' in self.incomplete:
            # qemu binaries
            Thread(target=self.download_and_extract,
                   args=(self.dl_addr, 'qemu-bin.tar.xz', 'qemu-bin'),
                   daemon=True
                   ).start()

            # qemu source code
        if 'qemu-src' in self.incomplete:
            Thread(target=self.download_and_extract,
                   args=("https://download.qemu.org/qemu-7.2.0.tar.xz", 'qemu-7.2.0.tar.xz', 'qemu-src'),
                   daemon=True
                   ).start()

        # switch displayed page when downloads are completed
        Thread(target=self.install_page_switch, daemon=True).start()

    def download_and_extract(self, url, dl_file, file_type):
        try:
            # Create directory
            os.makedirs(self.install_dir, exist_ok=True)

            def gs_print(msg):
                print(f"{file_type}: {msg}")

            # Delete file if exists
            try:
                gs_print(f"Deleting {dl_file}")
                os.remove(f"{self.install_dir}/{dl_file}")
            except:
                pass

            # Download the file
            gs_print(f"Downloading {dl_file}")

            r = requests.get(f"{url}/{dl_file}", stream=True)
            r.raise_for_status()

            with open(f"{self.install_dir}/{dl_file}", 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)

            # Extract the file
            gs_print(f"Extracting {dl_file}")
            with tarfile.open(f"{self.install_dir}/{dl_file}", mode='r:xz') as tar:
                tar.extractall(path=self.install_dir)

            # Remove tarball
            try:
                gs_print(f"Deleting {dl_file}")
                os.remove(f"{self.install_dir}/{dl_file}")
            except:
                pass

            # Set to complete
            self.incomplete.remove(file_type)
        except Exception as e:
            print(e)
            pass

    def install_page_switch(self):
        while True:
            if len(self.incomplete) < 1:
                print("Installation completed")
                self.installing = False
                self.fixing = False
                break
            time.sleep(0.1)
