#!/usr/bin/env python3

"""
Kickstart iso creater
Create a smaller ISO that only includes
packages defined in a kickastart file.
Also includes the kickstart file and boots with it

Psudo code:
- Check prerequisites

- Parse kickstart file
  * get defined packages
  * ungroup multilayer groups

  






Notes:
  dnf download --resolve --alldeps --destdir=packages "firefox"
"""

import subprocess
import sys

def subprocesswrapper(*command):
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"subprocess {command} returned code {result.returncode}")
    return result.stdout

class main:
    def __init__(self):
        self.ks_file = "ks.cfg"
        self.packages = list()

    def get_package_list(self):
        is_in_packages = False
        for line in open(self.ks_file, "r").readlines():
            #print(line.strip())
            if "%packages" in line:
                is_in_packages = True
            elif is_in_packages:
                if "%end" in line:
                    break
                elif line.strip():
                    self.packages.append(line.strip())
    
    def split_groups(self):
        for package in self.packages:
            if package.startswith("@^"):
                mandatory = False
                for line in subprocesswrapper("dnf", "group", "info", package.strip("@^")).splitlines():
                    if "Mandatory Groups:" in line:
                        mandatory = True
                    elif mandatory:
                        if "Optional Groups:" in line:
                            break
                        print(line.strip())

                

    def test(self):
        self.get_package_list()
        self.split_groups()

if __name__ == "__main__":
    main().test()