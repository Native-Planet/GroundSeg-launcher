import guestfs
import subprocess
import re
import socket

class ResizeImage:

## EXPOSED

    def __init__(self, img):
        self.img = img
        self.disk = "/dev/sda"
        self.part = "/dev/sda1"

    # Actual usage of the image
    def usage(self):
        try:
            output = subprocess.check_output(["qemu-img", "info", self.img])
            size = [x for x in output.decode("utf-8").split("\n") if "disk size" in x][0].split(':')[-1]
            return (True, size.strip().split(' ')[0])

        except Exception as e:
            return (False, e)

    # Increase size of filesystem if smaller than 80% of host free space
    def set_size(self, v):

        # get current usage
        us_res = self.usage()
        if not us_res[0]:
            return us_res

        # start guestfs
        gfs_res = self._start_gfs()
        if not gfs_res[0]:
            return gfs_res

        # set hostname
        h_res = self.set_hostname()
        if not h_res[0]:
            return h_res

        # get filesystem size
        fss_res = self._fs_size()
        if not fss_res[0]:
            return fss_res

        # resize filesystem
        if float(us_res[1]) < v:
            rfs_res = self._resize_fs(v)
            if not rfs_res[0]:
                return rfs_res

        # close image
        return self._close_fs()


## INTERNAL

    # start guestfs
    def _start_gfs(self):
        try:
            self.g = guestfs.GuestFS(python_return_dict=True)
        except Exception as e:
            return (False, e)
        try:
            self.g.add_drive_opts(self.img, format='qcow2', readonly = False)
        except Exception as e:
            return (False, e)
        try:
            self.g.launch()
        except Exception as e:
            return (False, e)
        return (True, None)
    # set hostname
    def set_hostname(self):
        try:
            self.g.mount(self.part,"/")
            self.g.write("/etc/hostname",socket.gethostname())
            self.g.umount_all()
            return (True, None)
        except Exception as e:
            return (False, e)

    def _fs_size(self):
        try:
            self.disk_bytes = self.g.blockdev_getsize64(self.disk)
        except Exception as e:
            return (False, e)
        try:
            self.disk_gibs = self.disk_bytes / (2**30)
        except Exception as e:
            return (False, e)
        try:
            self.in_bytes = self.g.blockdev_getsize64(self.part)
        except Exception as e:
            return (False, e)
        try:
            self.in_gibs = self.in_bytes / (2**30)
        except Exception as e:
            return (False, e)
        return (True, None)

    def _resize_fs(self,v):
        try:
            self.g.resize2fs_size(self.part, v * (2**30))
            return (True, None)
        except Exception as e:
            return (False, e)

    def _close_fs(self):
        try:
            self.g.shutdown()
        except Exception as e:
            return (False, e)
        try:
            self.g.close()
        except Exception as e:
            return (False, e)
        return (True, None)
