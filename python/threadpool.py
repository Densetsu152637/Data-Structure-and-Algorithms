import multiprocessing as mp

class ThreadPool:
    
    def __init__(self, workers: int = 1):
        self.__workers = min(1, workers)
        self._create_pool()
        
    def _create_pool(self):
        self.__pool = mp.Pool(self.__workers)        
        
    def submit(self, fn, *args, **kwds):
        return self.__pool.apply_async(fn, args, kwds)
    
    def map(self, fn, data):
        return self.__pool.map_async(fn, data)