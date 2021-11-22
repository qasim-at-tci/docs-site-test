import json
import os
import copy
import fileinput
import re

jsonToParse = input('Specify JSON file (cleaned up to be a list of dicts): ')

# grab working directory
startDir = input('Specify local content directory: ')
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
def attachmentChangeMove(oldPath, dirpath, newDirAtt, name):

    attNameSearch = '\(.*?attachments/[-/\w]*/([-\w]*[?.]\w*)?\)' #need to grab img name from start match
    newAttDir = startDir.replace('content\\', '') + 'static\\attachments' + newDirAtt.replace('/', os.sep)
    with fileinput.input(os.path.join(dirpath, name), inplace=True, backup='', encoding="utf-8") as file:
        for line in file:
            oldAttDir = ''
            if re.search(attNameSearch,line) != None:
                matched = re.search(attNameSearch,line)
                lastIndex = matched.end()
                oldAttDir = matched.group().strip('()')
                attName = matched.group(1)
                os.makedirs((newAttDir+name[:-(len(exten))]), exist_ok=True)
                fileInOldDir = os.path.exists(oldPath + '\\' + oldAttDir.replace('/', os.sep))
                if oldAttDir.find('attachments') > 1:
                    insert = matched.group()
                elif name == "_index.md":
                    insert = '(/attachments' + newDirAtt + '/' + attName + ')' + line[lastIndex:]
                    if fileInOldDir is True:
                        os.replace(oldPath + '\\' + oldAttDir.replace('/', os.sep), newAttDir + attName)
                else:
                    insert = '(/attachments' + newDirAtt + name[:-(len(exten))] + '/' + attName + ')' + line[lastIndex:]
                    if fileInOldDir is True:
                        os.replace(oldPath + '\\' + oldAttDir.replace('/', os.sep), newAttDir + name[:-(len(exten))] + '\\' + attName)
                line = re.sub(r''+attNameSearch,insert,line.rstrip())
            print(line, end='')


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
        elif (item["i"] == "index") and ("m" not in item):
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
                    item["newDir"] = categoryChecker["d"]
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
                    os.replace(startDir + dirpath + '\\' + name, newDir + '_index.md')
                    attachmentChangeMove((startDir + dirpath), newDir, itemGrab["newDir"], '_index.md')
                else:
                    #move file
                    os.replace(startDir + dirpath + '\\' + name, newDir + name)
                    attachmentChangeMove((startDir + dirpath), newDir, itemGrab["newDir"], name)

# What will be logged
logname = baseParent["u"].strip("/") + '-json-log.log'
catName = baseParent["u"].strip("/") + '-json-cat.log'






# Write results to logfile
with open(logname, 'w') as logfile:
    logfile.write(results)
with open(catName, 'w') as catfile:
    catfile.write(categories)