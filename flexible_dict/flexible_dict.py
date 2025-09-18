from typing import Any, Iterable

from .abstract import AbstractFlexible
from .chained_default import ChainedDefault


class FlexibleDict(AbstractFlexible, dict):
    
    def __init__(self,
                 input_dict: dict,
                 default: Any = None,
                 iterable_default: Iterable | None = None,
                 *args, **kwargs):
        if iterable_default == None:
            iterable_default = []
        
        iter(iterable_default)
        dict.__init__(self, *args, **kwargs)
        self.__value = self
        self.__default = default
        self.__iterable_default = iterable_default
        self.__load_dict(input_dict)
    
    
    def __load_dict(self, input_dict):
        is_input_dict = isinstance(input_dict, dict)
        if is_input_dict:
            for key, value in input_dict.items():
                super(FlexibleDict, self).__setitem__(key, value)
        return self
    
    def __setitem__(self, key, value):
        flexible_value = self.__generate_flexible_value(value)
        dict.__setitem__(self, key, flexible_value)
    
    def __getitem__(self, __key):
        if __key not in self.keys():
            self.__value = ChainedDefault(default=self.__default,
                                          iterable_default=self.__iterable_default)
        else:
            inline_value = super(FlexibleDict, self).__getitem__(__key)
            self.__value = self.__generate_flexible_value(inline_value)
        return self.__value
    
    def __generate_flexible_value(self, inline_value):
        is_inline_value_dict = isinstance(inline_value, dict)
        is_inline_value_flexible_dict = isinstance(inline_value, FlexibleDict)
        is_inline_value_subscriptable_default = isinstance(inline_value, ChainedDefault)
        
        if is_inline_value_flexible_dict or is_inline_value_subscriptable_default:
            flexible_value = inline_value
        elif is_inline_value_dict:
            flexible_value = FlexibleDict(input_dict=inline_value,
                                          default=self.__default,
                                          iterable_default=self.__iterable_default)
        else:
            flexible_value = ChainedDefault(default=inline_value, 
                                            next_level_default=self.__default,
                                            iterable_default=self.__iterable_default)
        return flexible_value
    
    def _is_iterable(self):
        try:
            iter(self.__value)
            return True
        except TypeError:
            return False
    
    @property
    def value(self):
        return dict(self.__value)
    
    # TODO: Create __value setter and test it too
    
    @property
    def iterable_value(self):
        if self._is_iterable():
            return dict(self.__value)
        return self.__iterable_default
    
    @property
    def flexible_value(self):
        return self.__value
    
    def __str__(self):
        return f'\nType: {type(self)} \nValue: {dict.__str__(self)}\n'
