import os,re,sys,argparse

def rename(path,id_format,name_format):
    filenamelist = os.listdir(root_path)

    for filename in filenamelist:
        filepath = os.path.join(root_path,filename)
        if(os.path.isdir(filepath)):
            continue
        if(filename.startswith('.')):
            continue
        pattern = re.compile(id_format)
        match = pattern.search(filename)
        if(match):
            id = match.group(1)
            newfilename = newfilename_format.replace('*',id) + os.path.splitext(filename)[1]
            newfilepath = os.path.join(root_path,newfilename)
            os.rename(filepath,newfilepath)

try:
    root_path = sys.argv[1]
    id_format = sys.argv[2]
    newfilename_format = sys.argv[3]
    rename(root_path, id_format, newfilename_format)
    sys.exit()
except Exception as ex:
    pass

parser = argparse.ArgumentParser()
parser.add_argument('--root_path', type=str, default = None)
parser.add_argument('--id_format', type=str, default = None)
parser.add_argument('--newfilename_format',type=str,default = None)
args = parser.parse_args()
root_path = args.root_path
id_format = args.id_format
newfilename_format = args.newfilename_format

rename(root_path,id_format,newfilename_format)