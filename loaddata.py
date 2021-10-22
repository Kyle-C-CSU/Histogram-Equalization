import pickle
dbfile = open('examplePickle', 'rb')     
db = pickle.load(dbfile)
for keys in db:
    print(keys, '=>', db[keys])
dbfile.close()