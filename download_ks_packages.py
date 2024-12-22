#!/usr/bin/env python3

import subprocess
import sys

def subprocesswrapper(*command):
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = process.stdout.decode('utf-8')
    stderr = process.stderr.decode('utf-8')
    
    if stderr:
        print(stderr, file=sys.stderr)
    if process.returncode != 0:
        raise RuntimeError("subprocess {} returned code {}".format(command, process.returncode))
    
    return stdout

class main:
    def __init__(self, input_ks, output_dir):
        self.ks_file = input_ks
        self.output_dir = output_dir
        self.packages = list()
    
    def read_ks(self):
        is_in_packages = False
        for line in open(self.ks_file, "r"):
            if is_in_packages:
                if "%end" in line:
                    is_in_packages = False
                elif line:
                    self.packages.append(line.strip())
            elif "%packages" in line:
                is_in_packages = True
    
    def download_packages(self):
        counter = 0
        count_to = len(self.packages)
        for package in self.packages:
            counter += 1
            print(f"[{counter}/{count_to}] Downloading: {package}")
            subprocesswrapper("dnf", "download", "--resolve", "--alldeps", f"--destdir={self.output_dir}", package)

    def run(self):
        self.read_ks()
        self.download_packages()
    
if __name__ == "__main__":
    main("new_ks.cfg", "packages").run()