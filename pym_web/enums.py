from enum import unique, IntEnum, Enum, auto


@unique
class SetGroup(Enum):  # TODO: CfgComponent
    """Config group"""
    Contacts = 'contacts'
    ToDo = 'todo'


@unique
class CfgProperty(Enum):
    Store = 'store'
    Filter = 'filt'
    Sort = 'sort'
    Col2Show = 'col2show'
    ColOrder = 'colorder'
    ShowCtlPane = 'showlp'
    ShowDetails = 'showrp'


@unique  # TODO: rm
class TodoSort(IntEnum):
    AsIs = auto()
    Name = auto()
    PrioDueName = auto()
