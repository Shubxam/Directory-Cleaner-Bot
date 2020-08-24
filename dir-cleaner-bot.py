##TODO
##-Implement other ways of sorting: modification date/first-letter/..
# since we're working w/ os functionalities like moving files, we import os
import os
#The argparse module makes it easy for us to accept custom command line arguments for our programs.
import argparse
#regEx module for searching patterns in files.
import re

#adding description for our program
parser = argparse.ArgumentParser(
    description='Clean up directory and arrange files into folders by their type.'
)

#customizing --path argument
parser.add_argument('--path', type=str, default='.', help='Directory path to be cleaned.')

#parse the arguments given by parser and extract the path.
args = parser.parse_args()
path = args.path

print(f'Cleaning up {path}')

#returns a list with all files and folders present in path
dir_content = os.listdir(path)

#uses list comprehension to iterate through every file/directory in dir_content and returns a list w/ absolute path to each item
path_dir_content = [os.path.join(path, doc) for doc in dir_content]

#iterates through every file and checks whether is a file or directory and adds to respective folder.
folder = [doc for doc in path_dir_content if os.path.isdir(doc)]
file = [doc for doc in path_dir_content if os.path.isfile(doc)]

#counters to keep track of files moved and folders created to avoid duplication.
moved = []
# created_folders = []

print(f'Cleaning up {len(file)} of {len(dir_content)} elements.')

for doc in file:
    if doc in moved:
        print(f'{doc} already present')
        continue
    #seperating filepath/filename and .extension
    file_path,file_ext = os.path.splitext(doc)
    #hidden file returns file_ext='' thus length 0.
    if len(file_ext) == 0:
        print(f'Hidden file : {doc} \n leaving untouched.')
        continue
    if doc not in moved:
        #creating directory path name using file extension excluding '/'
        destination_dir = os.path.join(path, file_ext[1:])
        #If folder for extension doesn't already exist, make one.
        if not os.path.exists(destination_dir):
            print(f'created directory {destination_dir}')
            os.mkdir(destination_dir)
        # print(f'moving file {doc}')
        #extracting filename.extension from full-name.
        filename = re.findall(r'\/[\w+\.\s\-\_\(\)\+\@]*\.[\w+]*', doc)
        try:
            #rename function moves file from source to destination
            #second argument of join removes trailing '/' from file-name
            os.rename(doc, os.path.join(destination_dir, filename[-1][1:]))
            moved.append(doc)
        except IndexError:
            print(f'Can\'t parse file-name : {doc}' )
print(f'moved {len(moved)} files')