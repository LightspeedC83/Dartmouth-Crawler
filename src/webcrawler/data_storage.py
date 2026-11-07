import pickle
import os

def save_data(filename, to_store, overwrite=False):
    "pickles a python object into a file"
    if not os.path.isfile(filename) or overwrite: # if the file doesn't already exist or we overwrite anywas, we pickle!
        with open(filename, 'wb') as file:
            pickle.dump(to_store, file)
        print(f"data saved in `{filename}`")
        return True
    
    # otherwise we can't pickle
    print(f"Data NOT saved. A file `{filename}` already exists. ")
    return False    


def load_data(filename):
    """loads and returns a pickled python object from a file"""
    if not os.path.isfile(filename):
        print(f"couldn't load file `{filename}`")
        return None
    
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        if type(data) != type(set()):
            print("data loaded in was not of type set!")
        return data
    