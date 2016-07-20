import sys, os, re

def get_xml_file(files):
    res = list()
    for file in files:
        if file.endswith(".xml"):
            res.append(file)
            #break
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

def get_name(match):
    name = re.search("name=\"(.*?)\"", match)
    return name.group(1)

def get_context(match):
    context = re.search("context=\"(.*?)\"", match)
    return context.group(1)

def remove_internal_if_exists(value):
    if "[INTERNAL]" in value:
        return value.replace("[INTERNAL] ","")
    else:
        return value

def get_resources(match):
    res = list()
    resources = re.findall("<resource .*?>(.*?)</resource>", match)
    for resource in resources:
        uri_match = re.search("value=\"\[API\](.*?)\"", resource)
        if uri_match:
            value = uri_match.group(1)
            uri = remove_internal_if_exists(value)
            res.append(uri)
    return res

def extract_info(api_content):
    res = {
        'name':'',
        'context':'',
        'resources':[],
        'templates':{},
        'sequences':{},
        'registers':{},
        'stores':{}
    }

    #matches = re.search("(<api )(.*?)(name=\"(.*?)\")(.*?)(context=\"(.*?)\")",api_content)
    matches = re.search("<api (.*?)>(.*?)</api>", api_content)
    if matches:
        res['name'] = get_name(matches.group(1))
        res['context'] = get_context(matches.group(1))
        res['resources'] = get_resources(matches.group(2))
        print(res)
    return res

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

