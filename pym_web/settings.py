"""Config (settings) handler"""
# 1. std
from typing import Any
import os.path
import json
# 3. local
from pym_core import exc
import enums


class Cfg:
    """Static class to handle config"""
    __data: dict
    __path: str
    __loaded: bool

    @staticmethod
    def __chk_setup():
        if not Cfg.__path:
            raise exc.EntryLoadError("Cfg path not set")

    @staticmethod
    def __load():
        """Load settings"""
        Cfg.__chk_setup()
        if os.path.isfile(Cfg.__path):
            with open(Cfg.__path, 'rt') as ifile:
                Cfg.__data = json.load(ifile)

    @staticmethod
    def __save():
        """Save settings"""
        Cfg.__chk_setup()
        with open(Cfg.__path, 'wt') as ofile:
            json.dump(Cfg.__data, ofile, indent=1)

    @staticmethod
    def __try_load():
        """Load setting on demand"""
        if not Cfg.__loaded:
            Cfg.__load()
            Cfg.__loaded = True

    @staticmethod
    def setup(path: str):
        """Set file path"""
        Cfg.__data = dict()
        Cfg.__path = path
        Cfg.__loaded = False

    @staticmethod
    def get(group: enums.SetGroup, key: str) -> Any:
        # TODO: default values are caller's problem
        Cfg.__try_load()
        if group.value in Cfg.__data:
            return Cfg.__data[group.value].get(key)

    @staticmethod
    def set(group: enums.SetGroup, key: str, val: Any):
        if group.value not in Cfg.__data:
            Cfg.__data[group.value] = dict()
        Cfg.__data[group.value][key] = val
        Cfg.__save()
