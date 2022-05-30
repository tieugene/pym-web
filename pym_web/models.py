"""Model for ToDo entries"""
from typing import Iterator

from pym_core.base.data import Store, StoreList, Entry, EntryList
# from pym_core.todo import enums as core_enums
from pym_core.todo.data import TodoStore, store_list, entry_list  # TodoVObj
import enums
from settings import Cfg


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

    def __init__(self, entries: EntryModel):
        self._entry_model = entries

    def setSourceModel(self, m):
        ...

    def items(self) -> Iterator[Entry]:
        for entry in self._entry_model.items():
            if entry.store.active:
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


class TodoStoreModel(StoreModel):
    item_cls = TodoStore

    def __init__(self, entries: TodoEntryModel):
        super().__init__(entries)
        self._set_group = enums.SetGroup.ToDo
        self._data = store_list


todo_entry_model = TodoEntryModel()
todo_store_model = TodoStoreModel(todo_entry_model)
todo_proxy_model = TodoEntryProxyModel(todo_entry_model)
