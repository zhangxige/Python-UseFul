# coding: utf-8
import time
import threading


# Thread-safe dictionary implementation
class ThreadSafeDict:
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)
        self._lock = threading.Lock()

    def __len__(self):
        with self._lock:
            return len(self._dict)

    def __getitem__(self, key):
        with self._lock:
            return self._dict[key]

    def __setitem__(self, key, value):
        with self._lock:
            self._dict[key] = value

    def __delitem__(self, key):
        with self._lock:
            del self._dict[key]

    def __contains__(self, key):
        with self._lock:
            return key in self._dict

    def get(self, key, default=None):
        with self._lock:
            return self._dict.get(key, default)

    def setdefault(self, key, default=None):
        with self._lock:
            return self._dict.setdefault(key, default)


# Thread-safe list implementation
class ThreadSafeList:
    def __init__(self, *args):
        self._list = list(*args)
        self._lock = threading.Lock()

    def append(self, item):
        with self._lock:
            self._list.append(item)

    def extend(self, iterable):
        with self._lock:
            self._list.extend(iterable)

    def __getitem__(self, index):
        with self._lock:
            return self._list[index]

    def __len__(self):
        with self._lock:
            return len(self._list)

    def __iter__(self):
        with self._lock:
            return iter(self._list)

    def __delitem__(self, index):
        with self._lock:
            del self._list[index]

    def __contains__(self, item):
        with self._lock:
            return item in self._list
        
    def clear(self):
        with self._lock:
            self._list.clear()

    def index(self, item):
        with self._lock:
            return self._list.index(item)
        
    def pop(self, index=-1):
        with self._lock:
            return self._list.pop(index)
    
    def remove(self, item):
        with self._lock:
            self._list.remove(item)

    def sort(self, key=None, reverse=False):
        with self._lock:
            self._list.sort(key=key, reverse=reverse)

    def reverse(self):
        with self._lock:
            self._list.reverse()


# Thread control class for managing thread states
class ThreadContrl:
    def __init__(self):
        self._event = threading.Event()

    def run(self):
        self._event.set()
        for _ in range(10):
            if not self._event.is_set():
                break
            print("Thread is running...")
            time.sleep(10)

    def stop(self):
        self._event.clear()

    def restart(self):
        self.stop()
        self.run()

    def hangup(self):
        self._event.wait()

    def is_running(self):
        return self._event.is_set()


# Example usage of ThreadSafeDict
if __name__ == "__main__":
    ts_dict = ThreadSafeDict()
    ts_dict['key1'] = 'value1'
    print(ts_dict['key1'])  # Output: value1
    ts_dict['key2'] = 'value2'
    print(len(ts_dict))  # Output: 2
    if 'key1' in ts_dict:
        print("key1 exists")
    del ts_dict['key1']
    print(ts_dict.get('key1', 'default'))  # Output: default
    print(ts_dict.get('key2'))  # Output: value2
