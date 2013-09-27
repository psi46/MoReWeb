import hashlib
import os

verbose = False
def get_python_file_list(rootdir):
    fileList =[]
    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.py'):
                fileList.append(os.path.join(root,file))
    return fileList

def hashfile(fileName, hasher, blocksize=65536):
    try:
        afile = open(fileName, "rb")
    except IOError:
        print ("Unable to open the file in readmode: [0]", fileName)
        return
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def md5(fileName):
    return hashfile(fileName,hashlib.md5())

def create_hash_list(fileList):
    hashlist = [(file,hashfile(file,hashlib.md5())) for file in fileList]
    return hashlist

def fill_hash_file(outputfile,hashlist):
    for i in hashlist:
        outputfile.write(str(i[0])+' '+(i[1])+'\n')

def create_hash_file_directory(filename,directory):
    fileList = get_python_file_list(directory)
    hashList = create_hash_list(fileList)
    fobj = open(filename, "w")
    fill_hash_file(fobj,hashList)
    fobj.close()

def compare_two_files(filename1,filename2):
    hash1 = md5(filename1)
    hash2 = md5(filename2)
    if verbose: print filename1 + ': ' + hash1
    if verbose: print filename2 + ': ' + hash2
    return hash1 ==hash2
