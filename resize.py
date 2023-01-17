import guestfs
import subprocess
import re

class ResizeImage:

## EXPOSED

    def __init__(self, img):
        self.img = img
        self.disk = "/dev/sda"
        self.part = "/dev/sda1"

    def resize(self, v):
        # get qcow2 size
        sz_res = self._qc_size()
        if not sz_res[0]:
            return sz_res
        
        # grow qcow2 size
        if self.qc_gibs > v: 
            return (False, None) # shrink, return False
        if self.qc_gibs < v:
            grow_res = self._qc_grow(v)
            if not grow_res[0]:
                return grow_res # grow error, return False with error

        # start guestfs
        gfs_res = self._start_gfs()
        if not gfs_res[0]:
            return gfs_res

        # get filesystem size
        fss_res = self._fs_size()
        if not fss_res[0]:
            return fss_res

        # resize partition
        prt_res = self._resize_part()
        if not prt_res[0]:
            return prt_res

        # resize filesystem
        rfs_res = self._resize_fs()
        if not rfs_res[0]:
            return rfs_res

        # close image
        return self._close_fs()


    def force_resize(self, v):
        # start guestfs
        gfs_res = self._start_gfs()
        if not gfs_res[0]:
            return gfs_res

        # get filesystem size
        fss_res = self._fs_size()
        if not fss_res[0]:
            return fss_res

        # shrink filesystem
        rfs_res = self._shrink_fs(v)
        if not rfs_res[0]:
            return rfs_res

        # shrink partition
        prt_res = self._shrink_part(v)
        if not prt_res[0]:
            return prt_res

        # close image
        cls_res = self._close_fs()
        if not cls_res[0]:
            return cls_res

        # shrink image
        return self._qc_shrink(v)

    def usage(self):
        try:
            output = subprocess.check_output(["qemu-img", "info", self.img])
            size = [x for x in output.decode("utf-8").split("\n") if "disk size" in x][0].split(':')[-1]
            return (True, size.strip())

        except Exception as e:
            return (False, e)


## INTERNAL

    # load virtual disk size
    def _qc_size(self):
        try:
            output = subprocess.check_output(["qemu-img", "info", self.img])
            line = [x for x in output.decode("utf-8").split("\n") if "virtual size" in x][0]
            self.qc_bytes = int(re.search(r'\((\d+)', line).group(1))
            self.qc_gibs = int(self.qc_bytes / (2**30))
            return (True, None)
        except Exception as e:
            return (False, e)

    # increase size of qcow2
    def _qc_grow(self,gib):
        cmd = ["qemu-img", "resize", self.img, f"{gib}G"]
        try:
            output = subprocess.check_output(cmd).decode("utf-8")
        except Exception as e:
            return (False, e)

        if output == 'Image resized.\n':
            return (True, None)
        else:
            return (False, output)

    def _qc_shrink(self,gib):
        cmd = ["qemu-img", "resize", "--shrink", self.img, f"{gib}G"]
        try:
            output = subprocess.check_output(cmd).decode("utf-8")
        except Exception as e:
            return (False, e)

        if output == 'Image resized.\n':
            return (True, None)
        else:
            return (False, output)

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

    def _resize_part(self):
        try:
            self.g.part_resize(self.disk, 1, int(self.disk_bytes/512) - 1)
            return (True, None)
        except Exception as e:
            return (False, e)

    def _resize_fs(self):
        try:
            self.g.resize2fs(self.part)
            return (True, None)
        except Exception as e:
            return (False, e)

    # No way to respond to the prompt
    def _shrink_part(self,v):
        try:
            self.g.part_resize(self.disk, 1, int(v * (2**30) / 512), 'yes')
            return (True, None)
        except Exception as e:
            return (False, e)

    def _shrink_fs(self,v):
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




#        if self.in_gibs > gib:
#            cmd = ["qemu-img", "resize", "--shrink", self.image_file, f"{gib}G"]
