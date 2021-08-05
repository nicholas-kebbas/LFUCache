from collections import OrderedDict
from collections import defaultdict
import sys


# Generate a LFU Cache to maintain in memory cache
class LFUCache:
    def __init__(self, capacity=0):
        # map key to frequency
        self.key_frequency = {}

        # map frequency to dict of keys
        self.frequency_keys = defaultdict(OrderedDict)

        self.min_frequency = None
        self.capacity = capacity
        self.size = 0

    # Add a search term into the Cache
    def put(self, key: str, value: str) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_frequency:
            frequency = self.key_frequency[key]
            self.frequency_keys[frequency][key] = value
            self.get(key)
            # prevent memory leak
        else:
            self.key_frequency[key] = 1
            self.frequency_keys[1][key] = value
            self.min_frequency = 1

        # calculate size and remove if we need to
        while self.capacity < self.calculate_size():
            # remove Least Frequently Used Key
            delete_key, delete_val = self.frequency_keys[self.min_frequency].popitem(last=False)
            del self.key_frequency[delete_key]

    def calculate_size(self):
        self.size = sys.getsizeof(self.frequency_keys)
        return self.size

    def is_present(self, key) -> bool:
        if key in self.frequency_keys:
            return True
        return False

    # Retrieve a search term. If not there return None
    def get(self, key: str) -> str or None:
        if key not in self.key_frequency:
            return None
        # use frequency to find it in frequency_keys mapping
        frequency = self.key_frequency[key]
        value = self.frequency_keys[frequency][key]
        del self.frequency_keys[frequency][key]
        if frequency not in self.frequency_keys:
            if frequency == self.min_frequency:
                self.min_frequency += 1
            del self.frequency_keys[frequency]

        self.key_frequency[key] = frequency + 1
        self.frequency_keys[frequency+1][key] = value
        # prevent memory leak
        if not self.frequency_keys[frequency]:
            del self.frequency_keys[frequency]
        return value




