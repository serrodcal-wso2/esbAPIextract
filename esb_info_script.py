import sys, os

def get_xml_file(files):
    res = list()
    for file in files:
        if file.endswith(".xml"):
            res.append(file)
    return res

def get_file_content_into_string(directory, file):
    data = ""
    full_path = directory + "/" + file
    with open(full_path, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return data

def get_list_of_api_info(directory, xml_files):
    apis_info = list()
    for api_file in xml_files:
        file_content = get_file_content_into_string(directory, api_file)
        api_info = extract_info(file_content)
        apis_info.append(api_info)
    return apis_info

def extract_info(api_content):
    return None

def parse_info_to_json(apis_info):
    return None

def put_json_in_this_directory(apis_json):
    var = None

if __name__ == '__main__':
    if len(sys.argv)>1:
        directory_path = sys.argv[1]
        if os.path.isdir(directory_path) and os.path.exists(directory_path):
            files = os.listdir(directory_path)
            if files and len(files)>0:
                xml_files = get_xml_file(files)
                apis_info = get_list_of_api_info(directory_path, xml_files)
                apis_json = parse_info_to_json(apis_info)
                put_json_in_this_directory(apis_json)
            else:
                print("There are not any file in this directory")
        else:
            print("Argument is not a valid directory path")
    else:
        print("There are not arguments")

