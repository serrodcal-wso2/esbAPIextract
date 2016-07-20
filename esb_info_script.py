import sys, os

def get_xml_file(files):
    res = ()
    for file in files:
        if file.endswith(".xml"):
            res.append(file)
    return res

if __name__ == '__main__':
    if len(sys.argv)>1:
        directory_path = sys.argv[1]
        if os.path.isdir(directory_path) and os.path.exists(directory_path):
            files = os.listdir(directory_path)
            if files and len(files)>0:
                xml_files = get_xml_file(files)
            else:
                print("There are not any file in this directory")
        else:
            print("Argument is not a valid directory path")
    else:
        print("There are not arguments")

