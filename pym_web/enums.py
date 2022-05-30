# TODO: add Cfg enums: store, sort, filt, cols2show, colsorder
from enum import unique, IntEnum, Enum, auto


class SetGroup(Enum):
    """Config group"""
    Contacts = 'contacts'
    ToDo = 'todo'


class TodoSort(IntEnum):
    AsIs = auto()
    Name = auto()
    PrioDueName = auto()
