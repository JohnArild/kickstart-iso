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
    def __init__(self, input_ks, output_ks):
        self.ks_file = input_ks
        self.ks_new_file = output_ks
        self.packages = set()
        self.new_ks = str()
    
    @staticmethod
    def has_group(packages):
        for package in packages:
            if "@^" in package:
                return True
        return False

    def ungroup(self):
        #Get list of packages in groups
        while self.has_group(self.packages):
            new_package_list = set()
            for package in self.packages:
                if "@^" in package:
                    group_info = subprocesswrapper("dnf", "group", "info", package.strip("@^"))
                    print(f"Ungrouping: {package.strip('@^')}")
                    for line in group_info.splitlines():
                        if ":" in line:
                            is_in_mandatory_group = False
                            is_in_mandatory_packages = False
                            if "Mandatory Groups:" in line:
                                is_in_mandatory_group = True
                            if "Mandatory Packages:" in line:
                                is_in_mandatory_packages = True
                        else:
                            if is_in_mandatory_group:
                                line = line.strip()
                                new_package_list.add(f"@^{line}")
                            if is_in_mandatory_packages:
                                line = line.strip()
                                new_package_list.add(line)
                else:
                    new_package_list.add(package)
            self.packages = new_package_list

    def create_new_ks(self):
        #Extract packages from kickstart file
        is_in_packages = False
        for line in open("ks.cfg", "r").readlines():
            if is_in_packages:
                if "%end" in line:
                    is_in_packages = False
                    self.new_ks += line
                elif line:
                    self.packages.add(line.strip())
            elif "%packages" in line:
                is_in_packages = True
                self.new_ks += line + "<insert_packages_here>\n"
            else:
                self.new_ks += line
        #Ungroup groups in package list
        self.ungroup()
        #Convert package set to alphabetic list as string
        package_list_text = str()
        for package in sorted(self.packages, key=str.casefold):
            package_list_text += package + "\n"
        #Insert package list into kickstart script
        self.new_ks = self.new_ks.replace("<insert_packages_here>", package_list_text)
    
    def save_ks(self):
        open(self.ks_new_file, "w").write(self.new_ks)

    def run(self):
        self.create_new_ks()
        self.save_ks()
        print("Done!")

if __name__ == "__main__":
    main("ks.cfg", "new_ks.cfg").run()