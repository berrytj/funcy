import inspect
from functools import partial


def _num_required_args(func):                                       
    """Copied from Toolz (https://github.com/pytoolz/toolz)."""
    try:                                                            
        spec = inspect.getargspec(func)                             
        if spec.varargs:                                            
            return None                                             
        num_defaults = len(spec.defaults) if spec.defaults else 0   
        return len(spec.args) - num_defaults                        
    except TypeError:                                               
        return None                                                 


class curry(object):
    """Copied from Toolz (https://github.com/pytoolz/toolz)."""
    def __init__(self, func, *args, **kwargs):                                  
        if not callable(func):                                                  
            raise TypeError("Input must be callable")                           
                                                                                
        # curry- or functools.partial-like object?  Unpack and merge arguments  
        if (hasattr(func, 'func') and hasattr(func, 'args')                     
                and hasattr(func, 'keywords')):                                 
            _kwargs = {}                                                        
            if func.keywords:                                                   
                _kwargs.update(func.keywords)                                   
            _kwargs.update(kwargs)                                              
            kwargs = _kwargs                                                    
            args = func.args + args                                             
            func = func.func                                                    
                                                                                
        if kwargs:                                                              
            self._partial = partial(func, *args, **kwargs)                      
        else:                                                                   
            self._partial = partial(func, *args)                                
                                                                                
        self.__doc__ = getattr(func, '__doc__', None)                           
        self.__name__ = getattr(func, '__name__', '<curry>')                    
                                                                                
    @property                                                                   
    def func(self):                                                             
        return self._partial.func                                               
                                                                                
    @property                                                                   
    def args(self):                                                             
        return self._partial.args                                               
                                                                                
    @property                                                                   
    def keywords(self):                                                         
        return self._partial.keywords                                           
                                                                                
    @property                                                                   
    def func_name(self):                                                        
        return self.__name__                                                    
                                                                                
    def __str__(self):                                                          
        return str(self.func)                                                   
                                                                                
    def __repr__(self):                                                         
        return repr(self.func)                                                  
    def __hash__(self):                                                         
        return hash((self.func, self.args,                                      
                     frozenset(self.keywords.items()) if self.keywords          
                     else None))                                                
                                                                                
    def __eq__(self, other):                                                    
        return (isinstance(other, curry) and self.func == other.func and        
                self.args == other.args and self.keywords == other.keywords)    
                                                                                
    def __ne__(self, other):                                                    
        return not self.__eq__(other)                                           
                                                                                
    def __call__(self, *args, **kwargs):                                        
        try:                                                                    
            return self._partial(*args, **kwargs)                               
        except TypeError:                                                       
            # If there was a genuine TypeError                                  
            required_args = _num_required_args(self.func)                       
            if (required_args is not None and                                   
                    len(args) + len(self.args) >= required_args):               
                raise                                                           
                                                                                
        return curry(self._partial, *args, **kwargs)                            
                                                                                
    # pickle protocol because functools.partial objects can't be pickled        
    def __getstate__(self):                                                     
        # dictoolz.keyfilter, I miss you!                                       
        userdict = tuple((k, v) for k, v in self.__dict__.items()               
                         if k != '_partial')                                    
        return self.func, self.args, self.keywords, userdict                    
                                                                                
    def __setstate__(self, state):                                              
        func, args, kwargs, userdict = state                                    
        self.__init__(func, *args, **(kwargs or {}))                            
        self.__dict__.update(userdict)                                          

