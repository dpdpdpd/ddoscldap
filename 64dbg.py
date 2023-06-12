import dnfile, sys, os
def Main():
    if(len(sys.argv) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print("Description: Creates x64dbg script for setting breakpoints on defined ImplMap (PInvoke) methods of .NET executable")
        print(f"Usage: {os.path.basename(sys.argv[0])} <filepath>\n")
        sys.exit()
    file_path = sys.argv[1]
    script_path = file_path + "_x64dbg.txt"
    dn_file = dnfile.dnPE(file_path)
    if(dn_file.net is None or dn_file.net.metadata is None):
        print(f"{sys.argv[1]} is NOT a .NET executable !!!\n")
        sys.exit()
    if(dn_file.net.mdtables.ImplMap is None):
        print(f".NET executable '{sys.argv[1]}' has NO ImplMap !!!\n")
        sys.exit()
    # Getting all ImplMap methods and module scope
    implmap_table = dn_file.net.mdtables.ImplMap.rows
    implmap_modules = []
    implmap_methods = []
    [implmap_modules.append(row.ImportScope.row.Name.lower().replace(".dll", "")) for row in implmap_table if (row.ImportScope.row.Name.lower().replace(".dll", "") not in implmap_modules)]
    [implmap_methods.append(row.ImportName) for row in implmap_table if (row.ImportName not in implmap_methods)]
    # Creation of x64dbg script
    x64dbg_script = "; Replace charset depending APIs - ex. CreateProcess -> CreateProcessA or CreateProcessW !!!\n"
    for module in implmap_modules:
        x64dbg_script += f"loadlib {module}\n"
    for method in implmap_methods:
        x64dbg_script += f"SetBPX {method}\n"
    with open(script_path, "wt",encoding="utf-8") as f_scr:f_scr.write(x64dbg_script)
    print(f"x64dbg script created: '{script_path}'")
if __name__ == '__main__':
    Main()