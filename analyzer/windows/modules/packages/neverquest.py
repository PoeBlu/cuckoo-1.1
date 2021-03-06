# Copyright (C) 2010-2014 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.common.abstracts import Package
from lib.api.process import Process
from lib.common.exceptions import CuckooPackageError
from lib.api.utils import Utils
import time
import os

class NeverQuest(Package):
    """NeverQuest analysis package."""

    def run_ie(self):
        time.sleep(30)
        iexplore = os.path.join(os.getenv("ProgramFiles"), "Internet Explorer", "iexplore.exe")
        ie = Process()
        if not ie.execute(path=iexplore, args="\"https://www.yahoo.com/\"", suspended=False):
             raise CuckooPackageError("Unable to execute initial Internet "
                                         "Explorer process, analysis aborted")
        return None

    def start(self, path):
        free = self.options.get("free", False)
        args = self.options.get("arguments", None)
        dll = self.options.get("dll", None)
        gw = self.options.get("setgw",None)
                

        u = Utils()
        if gw:
           u.set_default_gw(gw)

        suspended = True

        if free:
            suspended = False

        p = Process()
        if not p.execute(path=path, args=args, suspended=suspended):
            raise CuckooPackageError("Unable to execute initial process, "
                                     "analysis aborted")

        if not free and suspended:
            p.inject(dll)
            p.resume()
            self.run_ie()
            p.close()
            return p.pid
        else:
            self.run_ie()
            return None

    def check(self):
        return True

    def finish(self):
        if self.options.get("procmemdump", False):
            for pid in self.pids:
                p = Process(pid=pid)
                p.dump_memory()

        return True
