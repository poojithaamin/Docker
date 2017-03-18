import sys
import yaml, json
from flask import Flask
from github import Github


app = Flask(__name__)

g = Github()
flag = 0
arg1=sys.argv[1]
result = arg1.rpartition('github.com/')[2]
repo1 = g.get_repo(result)
print repo1.name


@app.route('/v1/<filename>')
def hello(filename):
    global flag
    flag = 0
    #get the url input file name and ext
    file_ext = filename.rpartition('.')[2]
    file_name = filename.rpartition('.')[0]
    #parse the file list in the repo
    for i in repo1.get_contents('/'):
        #if the file name matches, check further for extension
        if i.name.rpartition('.')[0] == file_name:
            flag = 1
            #if file ext is .yml and is same as input file ext
            if i.name.endswith('.yml') and i.name.rpartition('.')[2] == file_ext:
                return repo1.get_file_contents(i.name).decoded_content
            #if file ext is .json and and is same as input file ext    
            elif i.name.endswith('.json') and i.name.rpartition('.')[2] == file_ext:
                return repo1.get_file_contents(i.name).decoded_content
            #if file ext is .yml and input file ext is .json, then convert to yml file to json format    
            elif i.name.endswith('.yml') and file_ext == 'json':
                return json.dumps(yaml.load(repo1.get_file_contents(i.name).decoded_content), sort_keys=True, indent=2)
            #return file not found    
            else:
                flag = 0
    #return file not found
    if flag == 0:
        return "Error : File doesn't exist"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
