import json
import os
import fileinput
import copy

jsonToParse = input('Please specify JSON file: ')

# grab working directory
#startDir = input('Please specify directory: ')
# change current working directory
#os.chdir(startDir)
# print new working directory
#print('\nCurrent working directory: ', os.getcwd(), end='\n')

# The top argument for walk
topdir = '.'
# The extension to search through
exten = '.md'
# What will be logged
logname = 'json-log.log'
catName = 'json-cat.log'
results = str()
categories = str()

# returns dictionary item from a list of dictionaries
def nextParent(key, value, list_dicts):
    for item in list_dicts:
        if item[key] == value:
            return item


# JSON parsing
print("Started Reading JSON file")
with open(jsonToParse, "r") as read_file:
    #initial list of menu items, kept so we can debug 
    menuItems = json.load(read_file)
    #completely detatched copy of menuItems
    myList = copy.deepcopy(menuItems)
    #empty lists to populate later
    baseParent = []
    childrenOfCategories = []
    childrenOfParents = []
    childrenOfParentsCopy = []
    parents = []
    catList = []    

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
        # grabs all categories and adds to catList list
        else:
            categories += '%s\n' % item["i"]
            catList.append(item)

    #completely detatched copy of childrenOfParents
    childrenOfParentsCopy = copy.deepcopy(childrenOfParents)

    #start looping through items in childrenOfParents
    for item in childrenOfParents:
        
        if item["i"] not in parents:
            item["d"] = "/"
        else:
            item["d"] = "/" + item["i"] + "/"
        parentChecker = nextParent("i", item["p"], childrenOfParentsCopy)
        while parentChecker != None:
            if parentChecker["i"] not in parents:
                item["d"] = "/" + parentChecker["p"] + item["d"]
            else:
                item["d"] = "/" + parentChecker["i"] + item["d"]
            item["p"] = parentChecker["p"]
            parentChecker = nextParent("i", item["p"], childrenOfParentsCopy)
        childOfCategoryChecker = nextParent("i", item["p"], childrenOfCategories)
        if childOfCategoryChecker != None:
            item["p"] = childOfCategoryChecker["i"]
            item["d"] = "/" + childOfCategoryChecker["i"] + item["d"]
        categoryChecker = nextParent("t", childOfCategoryChecker["c"], catList)
        if categoryChecker != None:
            item["p"] = categoryChecker["i"]
            item["d"] = baseParent["d"] + categoryChecker["i"] + item["d"]

        results += '%s\n' % item

    print("Base parent: ", baseParent)
    print("Parents: ", parents)
    print("Children of categories: ",childrenOfCategories)
    print("Children of Parents: ", childrenOfParents)
    print("Category list: ", catList)

# Write results to logfile
with open(logname, 'w') as logfile:
    logfile.write(results)
with open(catName, 'w') as catfile:
    catfile.write(categories)