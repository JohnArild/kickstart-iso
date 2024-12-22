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

"""

class main:
    def __init__(self):
        self.ks_file = "ks.cfg"
        self.packages = list()

    def get_packages(self):
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

    def test(self):
        self.get_packages()
        print(self.packages)

if __name__ == "__main__":
    main().test()