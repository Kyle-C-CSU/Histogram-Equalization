import pickle
import cv2
img = cv2.imread("fuji.png")
db = {}
db["img"] = img
# for reading also binary mode is important
dbfile = open('examplePickle', 'wb')     
db = pickle.dump(db,dbfile)

dbfile.close()