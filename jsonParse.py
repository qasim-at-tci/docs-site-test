import json
import os
import fileinput
import pandas as pd
import copy

jsonToParse = input('Please specify JSON file: ')

#menuDict = {}

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

def nextParent(key, value, list_dicts):
    for item in list_dicts:
        if item[key] == value:
            return item


# JSON parsing and reformatting in menuDict
print("Started Reading JSON file")
with open(jsonToParse, "r") as read_file:
    menuItems = json.load(read_file)
    myList = copy.deepcopy(menuItems)
    baseParent = []
    childrenOfCategories = []
    childrenOfParents = []
    childrenOfParentsCopy = []
    parents = []
    catList = []
    menuDict = {}
    

    for item in myList:
        # grabs item that has a category tag as parent and adds to childrenOfCategories list
        if "c" in item:
            #item["d"] = item["c"] + "/"
            childrenOfCategories.append(item)#["i"])
        # grabs item that has a parent tag as parent and adds to childrenOfParents list
        elif "p" in item:
            #item["d"] = item["p"] + "/"
            childrenOfParents.append(item)#["i"])
            parents.append(item["p"])
        # grabs baseparent of all entries in json
        elif "m" in item:
            baseParent = item#["d"]
        # grabs all categories and adds to catList list
        else:
            categories += '%s\n' % item["i"]
            catList.append(item)#["i"])
            #item["d"] = item["d"] + item["i"] + "/"
        #results += '%s\n' % item

    childrenOfParentsCopy = copy.deepcopy(childrenOfParents)

    for item in childrenOfParents:
        
        if item["i"] not in parents:
            item["d"] = "/"
        else:
            item["d"] = "/" + item["i"] + "/"
        parentChecker = nextParent("i", item["p"], childrenOfParentsCopy)
        while parentChecker != None:
            #parentChecker = {"key": "value"}
            
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
    #print("menuDict: ", menuDict)
    #print(type(menuItems)) # to test

    # next step is to loop over children with parents, to

    # for item in menuItems:
    #     print(item)
    #     print("Page name: ", item["t"])
    #     if "c" in item:
    #         print("Category: ", item["c"])
    #         item["d"] = item["d"] + item["c"] + "/"
    #     if "p" in item:
    #         print("Parent: ", item["p"])
    #         item["d"] = item["d"] + item["p"] + "/"
    #     #menuDict[item["i"]] = item
    #     # Save to results string instead of printing
    #     results += '%s\n' % item
        #print(type(item))

    #print(type(menuItems)) # to test

# Write results to logfile
with open(logname, 'w') as logfile:
    logfile.write(results)
with open(catName, 'w') as catfile:
    catfile.write(categories)

    #still need to find a way to iterate over keys names to see if anyone has the same entry for p or c
    #to give them isParent=true -> will be the way to distinguish which file gets a name change
    #for key, value in menuDict.items():
        #print(key, ":", value)


    print("Done reading json file")


""" for dirpath, dirnames, allfiles in os.walk(topdir):
    for name in allfiles:
        if name.lower().endswith(exten):
            print('File: ', os.path.join(dirpath, name))  # Print Filename
            os.altsep = '/'
            altPath = dirpath.replace(os.sep, os.altsep)
            # for toplevel directory
            if dirpath == '.':
                with fileinput.input(os.path.join(dirpath, name), inplace=True, backup='') as file:
                    
            # for any directory within toplevel
            else:
                with fileinput.input(os.path.join(dirpath, name), inplace=True, backup='') as file:
                     """