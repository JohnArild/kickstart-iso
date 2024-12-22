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
  dnf group install --downloadonly --downloaddir=packages graphical-server-environment

  dnf install anaconda anaconda-widgets kexec-tools-anaconda-addon anaconda-install-env-deps

  createrepo output
  mkisofs -o rocky8-custom.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T output
"""

import subprocess
import sys

def subprocesswrapper(*command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1)
    # Print stdout and stderr in real-time
    try:
        for line in process.stdout:
            print(line, end="")
        for line in iter(process.stderr.readline, ""):
            print(line, end="", file=sys.stderr)
    except KeyboardInterrupt:
        process.terminate()
        raise

    # Wait for the process to finish and get the exit code
    process.wait()
    if process.returncode != 0:
        raise RuntimeError(f"Error Code {process.returncode} from command: {command}")

class main:
    def __init__(self):
        self.ks_file = "ks.cfg"
        self.packagesdir = "packages"
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
 
    def download(self):
        for line in self.packages:
            if line.startswith("@^"):
                group = line.replace("@^", "")
                print(f"Downloading Group {group}")
                #subprocesswrapper(f"dnf group install -y --downloadonly --downloaddir=packages {group}")
                subprocesswrapper("dnf", 
                                  "group", 
                                  "install", 
                                  "-y", 
                                  "--downloadonly",  
                                  f"--downloaddir={self.packagesdir}", 
                                  group)
            else:
                print(f"Downloading Package: {line}")
                subprocesswrapper("dnf", 
                                  "download", 
                                  "--resolve", 
                                  "--alldeps", 
                                  f"--destdir={self.packagesdir}", 
                                  line)                

    def test(self):
        self.get_package_list()
        self.download()
        print("Done!")

if __name__ == "__main__":
    main().test()