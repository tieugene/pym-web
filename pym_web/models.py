"""Model for ToDo entries"""
# 1. std
from typing import Iterator, Callable
import datetime
# 3. locla
from pym_core.base.data import Store, StoreList, Entry, EntryList
# from pym_core.todo import enums as core_enums
from pym_core.todo.data import TodoStore, store_list, entry_list  # TodoVObj
from pym_core.todo import enums as core_enums
import enums
from settings import Cfg

_e_closed = {core_enums.EStatus.Completed, core_enums.EStatus.Cancelled}
_today = datetime.date.today()
_tomorrow = _today + datetime.timedelta(days=1)


# Base
class EntryModel(object):
    _data: EntryList

    def items(self) -> Iterator[Entry]:
        return self._data.items()

    def size(self) -> int:
        return self._data.size()

    def item_get(self, i: int) -> Entry:  # R
        return self._data.entry_get(i)


class EntryProxyModel(object):
    """Sort/filter proxy model"""
    _entry_model: EntryModel
    _filter_cb: Callable

    def __init__(self, entries: EntryModel):
        self._entry_model = entries
        self._filter_cb = self._filt_all

    def setSourceModel(self, m):
        ...

    def setFilterCB(self, cb: Callable = None):
        """Set filter callback
        Callback = f(Entry) -> bool (True == accept)
        """
        self._filter_cb = cb

    @staticmethod
    def _filt_all(_: Entry) -> bool:
        return True

    def items(self) -> Iterator[Entry]:
        for entry in self._entry_model.items():
            if entry.store.active:
                if not self._filter_cb or self._filter_cb(entry):
                    yield entry


class StoreModel(object):
    """
    rowCount()
    data(row, col)
    setData(row, col, data)
    item_add()
    item_get(idx)
    ?item_upd()
    item_del(idx)
    :todo: items() -> Iterator
    """
    _set_group: enums.SetGroup
    item_cls: type
    _data: StoreList
    _entry_model: EntryModel

    def __init__(self, entries: EntryModel):
        self._entry_model = entries

    def items(self) -> Iterator[Store]:
        return self._data.items()

    def size(self) -> int:
        return self._data.size()

    def item_add(self, item: Store):
        self._data.store_add(item)
        self.save_self()

    def item_get(self, i: int) -> Store:
        return self._data.store_get(i)

    def item_del(self, i: int):
        self._data.store_del(i)
        self.save_self()

    def load_self(self):
        """Load _data from settings"""
        if data := Cfg.get(self._set_group, 'store'):
            self._data.from_list(data)

    def load_entries(self):
        """Load _data from settings"""
        self._data.load_entries()

    def save_self(self):
        """Save _data to settings"""
        Cfg.set(self._set_group, 'store', self._data.to_list())


# ToDo
class TodoEntryModel(EntryModel):
    """todo: collect categories/locations on load"""

    def __init__(self):
        self._data = entry_list


class TodoEntryProxyModel(EntryProxyModel):

    def __init__(self, entries: TodoEntryModel):
        super().__init__(entries)

    def switchFilter(self, fn: int):
        """Switch filter
        :param fn: filter num (0+)
        """
        self.setFilterCB((
                             self._filt_all,
                             self.__filt_closed,
                             self.__filt_opened,
                             self.__filt_today,
                             self.__filt_tomorrow
                         )[fn])

    @staticmethod
    def __filt_closed(entry: Entry) -> bool:
        return entry.vobj.get_Status() in _e_closed

    @staticmethod
    def __filt_opened(entry: Entry) -> bool:
        return entry.vobj.get_Status() not in _e_closed

    @staticmethod
    def __filt_today(entry: Entry) -> bool:
        vobj = entry.vobj
        due = vobj.get_Due_as_date()
        return\
            (vobj.get_Status() not in _e_closed)\
            and (due is not None)\
            and (due <= _today)

    @staticmethod
    def __filt_tomorrow(entry: Entry) -> bool:
        vobj = entry.vobj
        due = vobj.get_Due_as_date()
        return\
            (vobj.get_Status() not in _e_closed)\
            and (due is not None)\
            and (due == _tomorrow)


class TodoStoreModel(StoreModel):
    item_cls = TodoStore

    def __init__(self, entries: TodoEntryModel):
        super().__init__(entries)
        self._set_group = enums.SetGroup.ToDo
        self._data = store_list

    def select(self):
        """Helper for form SelectField"""
        return [(i, s.name) for i, s in enumerate(self._data.items())]  # empty on start
        # for i, s in enumerate(self._data.items()):
        #    yield i, s.name


todo_entry_model = TodoEntryModel()
todo_store_model = TodoStoreModel(todo_entry_model)
todo_proxy_model = TodoEntryProxyModel(todo_entry_model)
