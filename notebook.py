#!/usr/bin/env python3
import os, sys, fnmatch

def Create(argv):
    def Usage():
        print("Usage:")
        print("notebook.py create <notebook_name>")

    if(len(argv) != 2):
        Usage()
        return
    if( argv[1] == "--help"):
        Usage()
        return

    notebook = argv[1]
    try:
        os.mkdir(notebook)
        fd = open(notebook + "/index.md" , "w")
        fd.write("# " + notebook + "\n")
        fd.close()
    except FileExistsError:
        print("A directory already exist with this name")

def AddModule(argv):
    def Usage():
        print("Usage:")
        print("notebook.py add_module <module_number> <module_name>")

    if(len(argv) != 3):
        Usage()
        return
    if( argv[1] == "--help"):
        Usage()
        return

    try:
        module_number = int(argv[1])
    except ValueError:
        Usage()
        return

    module_name = argv[2]
    module_name_expanded = "%20".join(module_name.split())


    try:
        os.mkdir(f"{module_number} {module_name}")
    except FileExistsError:
        print("This module already exists")
        exit(0)

    fd = open("index.md", "a")
    fd.write(f"{module_number}. [{module_name}]({module_number}%20{module_name_expanded}/{module_number}%20{module_name_expanded}.pdf)\n")
    fd.close()

def BuildModule(argv):
    cwd = os.getcwd()
    module_name = cwd.split("/")[-1]

    list_of_files = os.listdir(".")
    list_of_image = []
    for entry in list_of_files:
        if fnmatch.fnmatch(entry, "*.jpg"):
            list_of_image.append(entry)

    list_of_image.sort()

    convert_command = "convert"
    for img in list_of_image:
        convert_command += f" {img}"
    convert_command += " " +  "\ ".join(module_name.split()) + ".pdf"
    print(convert_command)
    os.system(convert_command)

def main():
    fun_mapping = { "create":Create,
                    "add_module":AddModule,
                    "build_module":BuildModule}
    def Usage():
        print("Usage:")
        funs = ", ".join(fun_mapping.keys())
        print(f"notebook.py [{funs}] ...")

    if(len(sys.argv) < 2):
        Usage()
        return
    if(sys.argv[1] == "--help"):
        Usage()
        return

    try:
        fun_mapping[sys.argv[1]](sys.argv[1:])
    except KeyError:
        Usage()
        return

if __name__ == "__main__":
    main()
