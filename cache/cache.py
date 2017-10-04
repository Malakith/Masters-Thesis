import pickle


class Cache:
    def lookup(self, key):
        raise NotImplementedError("Should be implemented by concrete")

    def save(self, key, value):
        raise NotImplementedError("Should be implemented by concrete")


class NoneCache(Cache):
    def lookup(self, key):
        return None

    def save(self, key, value):
        return True


class FileCache(Cache):
    def __init__(self, filename):
        self.cache = {}
        if filename is None or filename == "":
            raise ValueError("filename should not be None or empty.")
        self.filename = filename
        with open(filename, "rb") as input_file:
            self.cache = pickle.load(input_file)

    def lookup(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            return None

    def save(self, key, value):
        self.cache[key] = value
        with open(self.filename, "wb") as output_file:
            pickle.dump(self.cache, output_file)