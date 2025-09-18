from typing import Any, Iterable

from .abstract import AbstractFlexible


class ChainedDefault(AbstractFlexible):
    NOT_DETERMINED = '__NOT_DETEMINED__'
    
    def __init__(self,
                 default: Any = None,
                 next_level_default: Any = NOT_DETERMINED,
                 iterable_default: Iterable | None = None):
        if iterable_default == None:
            iterable_default = []
        
        self._value = default
        self.__next_level_default = next_level_default
        self.__iterable_default = iterable_default
    
    def __getitem__(self, __key):
        next_level_default_determined = bool(self.__next_level_default != self.NOT_DETERMINED)
        if next_level_default_determined:
            return ChainedDefault(default=self.__next_level_default,
                                         iterable_default=self.__iterable_default)
        else:
            return ChainedDefault(default=self._value,
                                         iterable_default=self.__iterable_default)
    
    def _is_iterable(self):
        try:
            iter(self._value)
            return True
        except TypeError:
            return False
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self._value=val
    
    @property
    def iterable_value(self):
        if self._is_iterable():
            return self._value
        return self.__iterable_default
    
    @property
    def flexible_value(self):
        return ChainedDefault(default=self._value, iterable_default=self.__iterable_default)
    
    def __str__(self):
        return f'\nType: {type(self)} \nValue: {self._value}\n'
