import pickle

with open("system_pickles/data_reset.pkl", "rb") as file:
    data_good = pickle.load(file)


print(data_good)