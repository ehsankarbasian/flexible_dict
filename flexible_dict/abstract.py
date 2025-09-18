from __future__ import annotations
from typing import Any, Iterable

from abc import ABC, abstractmethod


class AbstractFlexible(ABC):
    
    @abstractmethod
    def __init__(self, default: Any, iterable_default: Iterable) -> None:
        pass
    
    @abstractmethod
    def _is_iterable(self) -> bool:
        pass
    
    @property
    @abstractmethod
    def value(self) -> Any:
        pass
    
    @value.setter
    @abstractmethod
    def value(self, val: Any):
        pass
    
    @property
    @abstractmethod
    def iterable_value(self) -> Iterable:
        pass
    
    @property
    @abstractmethod
    def flexible_value(self) -> AbstractFlexible:
        pass
