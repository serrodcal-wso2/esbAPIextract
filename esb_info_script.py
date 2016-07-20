import sys, os, re, json

def get_xml_file(files):
    res = list()
    for file in files:
        if file.endswith(".xml"):
            res.append(file)
            break
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

def get_templates_by_resource(resource):
    templates_matches = re.findall("<call-template target=\"(.*?)\"\/?>", resource)
    return templates_matches

def get_sequences_by_resource(resource):
    sequences_matches = re.findall("<sequence key=\"(.*?)\"\/?>", resource)
    return sequences_matches

def get_resources(match):
    res_resources = list()
    res_templates_by_resource = list()
    res_sequences_by_resource = list()
    resources = re.findall("<resource .*?>(.*?)</resource>", match)
    for resource in resources:
        uri_match = re.search("value=\"\[API\](.*?)\"", resource)
        if uri_match:
            value = uri_match.group(1)
            uri = remove_internal_if_exists(value)
            res_resources.append(uri)
        #TODO: poner un control, para si las listas son vacias, no anada nada al diccionario
        res_templates_by_resource.append(get_templates_by_resource(resource))
        res_sequences_by_resource.append(get_sequences_by_resource(resource))
    return (res_resources, res_templates_by_resource, res_sequences_by_resource)

def extract_info(api_content):
    res = {
        'name':'',
        'context':'',
        'resources':[],
        'templates':{},
        'sequences':{},
        'registers':{},
        'stores':{},
        'processors':{}
    }

    #matches = re.search("(<api )(.*?)(name=\"(.*?)\")(.*?)(context=\"(.*?)\")",api_content)
    matches = re.search("<api (.*?)>(.*?)</api>", api_content)
    if matches:
        res['name'] = get_name(matches.group(1))
        res['context'] = get_context(matches.group(1))
        ttuple = get_resources(matches.group(2))
        res['resources'] = ttuple[0]
        template_dict = dict()
        sequence_dict = dict()
        for i in range(0, len(ttuple[0])):
            template_dict[ttuple[0][i]] = list(set(ttuple[1][i]))
            sequence_dict[ttuple[0][i]] = list(set(ttuple[2][i]))
        res['templates'] = template_dict
        res['sequences'] = sequence_dict
        #print(res)
    return res

def save_object(obj, filename):
    with open(filename, 'w') as outfile:
        json.dump(obj, outfile)

def put_json_in_this_directory(apis_json):
    save_object(apis_json, "result.json")

if __name__ == '__main__':
    if len(sys.argv)>1:
        directory_path = sys.argv[1]
        if os.path.isdir(directory_path) and os.path.exists(directory_path):
            files = os.listdir(directory_path)
            if files and len(files)>0:
                xml_files = get_xml_file(files)
                apis_info = get_list_of_api_info(directory_path, xml_files)

                put_json_in_this_directory(apis_info)
            else:
                print("There are not any file in this directory")
        else:
            print("Argument is not a valid directory path")
    else:
        print("There are not arguments")