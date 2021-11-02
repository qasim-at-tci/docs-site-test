dictList=[{'name': 'Mark', 'place': 'Amersfoort'}, {'name': 'Natasa', 'place': 'Rijswijk'}]
print (dictList)

dicts = [
    { "name": "Tom", "age": 10 },
    { "name": "Mark", "age": 5 },
    { "name": "Pam", "age": 7 },
    { "name": "Dick", "age": 12 }
]
print (dicts)
print(next(item for item in dicts if item["name"] == "Pam"))
print(next(item for item in dicts if item["name"] == "Pam")['age'])