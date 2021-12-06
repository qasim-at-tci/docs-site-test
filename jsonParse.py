import json
import os
import copy
import fileinput
import re

jsonToParse = input('Specify JSON file (cleaned up to be a list of dicts): ')

# grab working directory
startDir = input('Specify FULL PATH to local content directory: ')
# change current working directory
os.chdir(startDir)
# print new working directory
print('\nCurrent working directory: ', os.getcwd(), end='\n')

# The top argument for walk
topdir = '.'
# The extension to search through
exten = '.md'

results = str()
categories = str()
myList = []
baseParent = []
childrenOfCategories = []
childrenOfParents = []
childrenOfParentsCopy = []
parents = []
catList = []
attLeftover = []
attList = []
attItems = str()

# returns dictionary item from a list of dictionaries
def nextItem(key, value, list_dicts):
    for item in list_dicts:
        if item[key] == value:
            return item

# returns dictionary item from a list of dictionaries & checks if directory is the same
def nextItemWithDirCheck(key, value, directory, list_dicts):
    for item in list_dicts:
        altPath = '.' + item["d"].replace('/', os.sep)
        altPathClean = altPath[:-1]
        if (item[key] == value) and (directory == altPathClean):
            return item

# moves attachment files to new locations and changes references to them in files
#only works for clean references, nothing above dir where the md file is
def attachmentChangeMove(oldPath, dirpath, newDirAtt, name):
    #pattern to find any 'attachment' between () in a line, will capture the last ) in line
    fullAttachmentRefSearch = '(?<=\])\(.*?attachments/(.*)?\)'
    #pattern to search against, does not capture + or extra . in names, still can get a false positive with 
    #multiple '![something](something)' in a single line
    attNameSearch = '(?<=\])\(.*?attachments([-/\w]*?)([-.\+\w= ]*)\)'
    logName = str()
    #define new dir for attachment
    newAttDir = startDir.replace('content\\', '') + 'static\\attachments' + newDirAtt.replace('/', os.sep)
    #go through .md file line by line
    with fileinput.input(os.path.join(dirpath, name), inplace=True, backup='', encoding="utf-8") as file:
        for line in file:
            oldAttDir = ''
            fullSearch = re.search(fullAttachmentRefSearch,line)
            strictSearch = re.search(attNameSearch,line)
            if fullSearch != None and strictSearch == None:
                entry = {"file": name, "path": dirpath, "line No.": fileinput.filelineno(), "match": fullSearch.group()}
                logName += 'FS %s\n' % entry
            #if there's a match to the strict pattern
            if strictSearch != None:
                matched = strictSearch
                entry = {"file": name, "path": dirpath, "line No.": fileinput.filelineno(), "match": matched.group()}
                lastIndex = matched.end()
                #should give back the old attachment path reference
                oldAttDir = matched.group().strip('()')
                #gives back the name of the attachment
                attName = matched.group(2)
                #check to make sure there still is a file in path, otherwise os.replace errors
                fileInOldDir = os.path.exists(oldPath + '\\' + oldAttDir.replace('/', os.sep))
                #excludes any results with more than './' preceding 'attachments'
                if oldAttDir.find('attachments') > 2:
                    insert = matched.group()
                    #saves the excluded to a list to run through later
                    attLeftover.append(entry)
                elif name == "_index.md":
                    insert = ('(/attachments' + newDirAtt + attName + ')' + line[lastIndex:]).replace('//', '/')
                    os.makedirs(newAttDir, exist_ok=True)
                    if fileInOldDir is True:
                        os.replace(oldPath + '\\' + oldAttDir.replace('/', os.sep), newAttDir + attName)
                        attList.append((newAttDir + attName).replace(os.sep, '/'))
                        logName += 'OK %s\n' % entry
                else:
                    insert = ('(/attachments' + newDirAtt + name[:-(len(exten))] + '/' + attName + ')' + line[lastIndex:]).replace('//', '/')
                    os.makedirs((newAttDir+name[:-(len(exten))]), exist_ok=True)
                    if fileInOldDir is True:
                        os.replace(oldPath + '\\' + oldAttDir.replace('/', os.sep), newAttDir + name[:-(len(exten))] + '\\' + attName)
                        attList.append((newAttDir + name[:-(len(exten))] + '\\' + attName).replace(os.sep, '/'))
                        logName += 'OK %s\n' % entry
                line = re.sub(r''+attNameSearch,insert,line.rstrip())
            print(line, end='')
    return logName

# JSON parsing
print("Started Reading JSON file")
with open(jsonToParse, "r") as read_file:
    #initial list of menu items, kept so we can debug 
    menuItems = json.load(read_file)
    #completely detatched copy of menuItems
    myList = copy.deepcopy(menuItems)

    #first loop to grab all items and create separate lists
    for item in myList:
        # grabs item that has a category tag as parent and adds to childrenOfCategories list
        if "c" in item:
            childrenOfCategories.append(item)
        # grabs item that has a parent tag, puts into parent list and adds to childrenOfParents list
        elif "p" in item:
            childrenOfParents.append(item)
            parents.append(item["p"])
        # grabs baseparent of all entries in json
        elif "m" in item:
            baseParent = item
        # grabs non baseParent index files - currently only category files
        elif item["i"] == "index":
            categories += '%s\n' % item["t"]
            catList.append(item)
            parents.append(item["t"])
        # grabs all categories and adds to catList and parents list
        else:
            categories += '%s\n' % item["t"]
            catList.append(item)
            parents.append(item["i"])

    #hardcopy of childrenOfParents list, original gets changed with every item update
    childrenOfParentsCopy = copy.deepcopy(childrenOfParents)

    #loop again to sort directory of each item
    for item in myList:
        #if item is not a parent to any page, it won't be _index, won't get a directory named after it
        if item["i"] not in parents:
            item["newDir"] = "/"
        #if it is a parent, it will be turned into _index and get a directory named after it
        else:
            item["newDir"] = "/" + item["i"] + "/"
            item["indexFlag"] = "true"
        #checks if item has a parent
        if "p" in item:
            parentChecker = nextItem("i", item["p"], childrenOfParentsCopy)
            #as long as item has a parent
            while parentChecker != None:
                #add parent name to dir path
                item["newDir"] = "/" + parentChecker["i"] + item["newDir"]
                #set parent
                item["p"] = parentChecker["p"]
                #grabs next parent, if there is one
                parentChecker = nextItem("i", item["p"], childrenOfParentsCopy)
            #checks if the next parent is a child of a category
            childOfCategoryChecker = nextItem("i", item["p"], childrenOfCategories)
            #if next parent is a child of a category
            if childOfCategoryChecker != None:
                #set parent to child of category
                item["p"] = childOfCategoryChecker["i"]
                #add child category name to dir path
                item["newDir"] = "/" + childOfCategoryChecker["i"] + item["newDir"]
            #checks if the next parent is a category
            categoryChecker = nextItem("t", childOfCategoryChecker["c"], catList)
            #if next parent is a category
            if categoryChecker != None:
                #for category items that are named index
                if categoryChecker["i"] == "index":
                    indexCat = categoryChecker["d"][len(baseParent["u"]):]
                    #set parent to category
                    item["p"] = indexCat
                    #add base directory and category to dir path
                    item["newDir"] = baseParent["u"] + indexCat + item["newDir"]
                else:
                    #set parent to category
                    item["p"] = categoryChecker["i"]
                    #add base directory and category to dir path
                    item["newDir"] = baseParent["u"] + categoryChecker["i"] + item["newDir"]
        #checks if item has a category as parent (for items with only category parents)
        elif "c" in item:
            categoryChecker = nextItem("t", item["c"], catList)
            #if next parent is a category
            if categoryChecker != None:
                #for category items that are named index
                if categoryChecker["i"] == "index":
                    indexCat = categoryChecker["d"][len(baseParent["u"]):]
                    #set parent to category
                    item["p"] = indexCat
                    #add base directory and category to dir path
                    item["newDir"] = categoryChecker["d"] + item["newDir"]
                else:
                    #set parent to category
                    item["p"] = categoryChecker["i"]
                    #add base directory and category to dir path
                    item["newDir"] = baseParent["u"] + categoryChecker["i"] + item["newDir"]
        #checks if item is baseParent
        elif "m" in item:
            #set dir path
            item["newDir"] = baseParent["u"]
            #add indexFlag
            item["indexFlag"] = "true"
        #for categories that are already index files
        elif item["t"] in parents:
            item["newDir"] = item["d"]
            item["indexFlag"] = "true"
        #for categories
        else:
            #set dir path for categories
            item["newDir"] = baseParent["u"] + item["i"] + "/"

        #save items to results
        results += '%s\n' % item

#prep baseParent directory to compare
dirBaseParent = '.' + baseParent["u"].replace('/', os.sep)
dirBaseParentClean = dirBaseParent[:-1]

#for all files in dir path
for dirpath, dirnames, allfiles in os.walk(topdir):
    for name in allfiles:
        #if name is lowercase with extension .md & path is same as baseParent
        #second check is used to exclude files outside of baseParent
        if name.lower().endswith(exten) and (dirpath[:len(dirBaseParentClean)] == dirBaseParentClean):
            #matches next item by name
            #makes sure it's right item name by comparing initial directory
            #with current directory of name file
            #there can't be 2 files in the same initial dir with the same name
            itemGrab = nextItemWithDirCheck("i", name[:-(len(exten))], dirpath, myList)
            att = ''
            #if the name exists in myList
            if itemGrab != None:
                #reverse / to \ in path
                altPath = itemGrab["newDir"].replace('/', os.sep)
                newDir = startDir + 'en\\docs' + altPath
                #make all levels of directories between supplied path of itemGrab and starting directory
                os.makedirs(newDir, exist_ok=True)
                #if file has indexFlag
                if "indexFlag" in itemGrab:
                    #move file and rename to _index.md
                    os.replace(startDir + dirpath + '\\' + name, newDir + '\\_index.md')
                    att = attachmentChangeMove((startDir + dirpath), newDir, itemGrab["newDir"], '_index.md')
                else:
                    #move file
                    os.replace(startDir + dirpath + '\\' + name, newDir + name)
                    att = attachmentChangeMove((startDir + dirpath), newDir, itemGrab["newDir"], name)
                attItems += att
        #for moving of any txt files, like MAPPING
        elif (name == "_MAPPING.txt") and (dirpath[:len(dirBaseParentClean)] == dirBaseParentClean):
            os.makedirs(startDir + 'en\\docs' + dirpath, exist_ok=True)
            os.replace(startDir + dirpath + '\\' + name, startDir + 'en\\docs' + dirpath + '\\' + name)

#for all files in dir path
for dirpath, dirnames, allfiles in os.walk(topdir):
    for name in allfiles:
        #moves any '.pptx','.xls','.xlsm','.xlsx','.jar' or '.json' attachment to static\attachments
        #separated into another full walk through dirs, to rule out moving files before a reference for them gets picked up in the first walk
        if (name.lower().endswith(('.pptx','.xls','.xlsm','.xlsx','.jar','.json')) and (dirpath[:len(dirBaseParentClean)] == dirBaseParentClean)):
            os.makedirs(startDir.replace('content\\', '') + 'static\\attachments' + dirpath.replace('attachments', ''), exist_ok=True)
            os.replace(startDir + dirpath + '\\' + name, startDir.replace('content\\', '') + 'static\\attachments' + dirpath.replace('attachments', '') + '\\' + name)

#last run throuh for attachments, to go through leftover list, for attachments outside of .md directory
for entry in attLeftover:
    with fileinput.input(os.path.join(entry["path"], entry["file"]), inplace=True, backup='', encoding="utf-8") as file:
        for line in file:
            if entry["line No."] == fileinput.filelineno():
                attNameSearch = '(?<=\])\((.*?)/attachments/([-/\w]*/([-\w=]*[?.]\w*))?\)'
                matched = re.search(attNameSearch,line)
                #if there's a match on the specified line continue to change reference
                if matched != None:
                    lastIndex = matched.end()
                    for attItem in attList:
                        if attItem.endswith(matched.group(2)):
                            newRef = attItem.split('attachments/', maxsplit=1)
                            insert = ('(/attachments/' + newRef[1] + ')' + line[lastIndex:]).replace('//', '/')
                            line = re.sub(r''+attNameSearch,insert,line.rstrip())
                            attItems += 'OK %s\n' % entry
                #otherwise add to json-att.log list
                else:
                    attItems += 'NO %s\n' % entry
            print(line, end='')

# What will be logged
logname = baseParent["u"].strip("/") + '-json-log.log'
catName = baseParent["u"].strip("/") + '-json-cat.log'
attName = baseParent["u"].strip("/") + '-json-att.log'

# Write results to logfile
with open(logname, 'w') as logfile:
    logfile.write(results)
#with open(catName, 'w') as catfile:
    #catfile.write(categories)
with open(attName, 'w') as attfile:
    attfile.write("FS - result of full search for any attachments reference in (), needs manual editing\nOK - reference updated and file moved\nNO - matched in 1st loop, no match in 2nd, needs manual editing\n")
    attfile.write(attItems)
