import os,re,sys,argparse

def rename(original_path,id_pattern,newfilename_format):
    filenamelist = os.listdir(original_path)

    for filename in filenamelist:
        filepath = os.path.join(original_path,filename)
        if(os.path.isdir(filepath)):
            continue
        if(filename.startswith('.')):
            continue
        pattern = re.compile(id_pattern)
        match = pattern.search(filename)
        if(match):
            placeholder_count = newfilename_format.count('*')
            id = str(int(match.group(1))).zfill(placeholder_count)
            newfilename = re.sub('\*{' + str(placeholder_count) + '}',id,newfilename_format) + os.path.splitext(filename)[1]
            newfilepath = os.path.join(original_path,newfilename)
            os.rename(filepath,newfilepath)

try:
    rename(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit()
except Exception as ex:
    pass

parser = argparse.ArgumentParser()
parser.add_argument('--original_path', type=str, default = None)
parser.add_argument('--id_pattern', type=str, default = None)
parser.add_argument('--newfilename_format',type=str,default = None)
args = parser.parse_args()
rename(args.original_path,args.id_pattern,args.newfilename_format)