import sys, os, re, json

def get_xml_file(files):
    res = list()
    for file in files:
        if file.endswith(".xml"):
            res.append(file)
            #break
    return res

def save_object(obj, filename):
    with open(filename, 'w') as outfile:
        json.dump(obj, outfile)

def put_json_in_this_directory(apis_json):
    save_object(apis_json, "template_result.json")

if __name__ == '__main__':
    if len(sys.argv)>1:
        directory_path = sys.argv[1]
        if os.path.isdir(directory_path) and os.path.exists(directory_path):
            files = os.listdir(directory_path)
            if files and len(files)>0:
                xml_files = get_xml_file(files)
                apis_info = get_list_of_template_info(directory_path, xml_files)
                put_json_in_this_directory(apis_info)
            else:
                print("There are not any file in this directory")
        else:
            print("Argument is not a valid directory path")
    else:
        print("There are not arguments")