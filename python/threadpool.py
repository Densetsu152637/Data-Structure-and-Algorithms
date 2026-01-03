import multiprocessing as mp

class ThreadPool:
    
    def __init__(self, workers: int = 1):
        self.__workers = min(1, workers)
        self._create_pool()
        
    def _create_pool(self):
        self.__pool = mp.Pool(self.__workers)  
        
    def recreate(self):
        self.gracefully_close()
        self._create_pool()    
        
    def gracefully_close(self):
        self.__pool.close()
        self.__pool.join()
        
    def terminate(self):
        self.__pool.terminate()  
        
    def submit(self, fn, *args, **kwds):
        return self.__pool.apply_async(fn, args, kwds)
    
    def map(self, fn, data):
        return self.__pool.map_async(
            fn, 
            data, 
            chunksize = len(data) // self.__workers
        )
    
    def starmap(self, fn, data):
        self.__pool.starmap(
            fn, 
            data, 
            chunksize = len(data) // self.__workers
        )