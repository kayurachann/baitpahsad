"""Cho phép import sealwatch mà không cần torch/torchvision (chỉ dùng SRM và FLD ensemble, không dùng mạng nơ-ron)."""
import importlib.abc
import importlib.machinery
import sys
import types


class _Meta(type):
    def __getattr__(cls, name):
        return _gia(name)


def _gia(name):
    return _Meta(name, (), {"__init__": lambda self, *a, **k: None, "__call__": lambda self, *a, **k: None})


class _ModGia(types.ModuleType):
    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return _gia(name)


class _Tim(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, fullname, path, target=None):
        if fullname.split(".")[0] in ("torch", "torchvision"):
            return importlib.machinery.ModuleSpec(fullname, self, is_package=True)
        return None

    def create_module(self, spec):
        return _ModGia(spec.name)

    def exec_module(self, module):
        module.__path__ = []


sys.meta_path.insert(0, _Tim())
