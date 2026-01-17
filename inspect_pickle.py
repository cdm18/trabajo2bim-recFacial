import pickle
data = pickle.loads(open("encodings.pickle", "rb").read())
print(set(data["names"]))
