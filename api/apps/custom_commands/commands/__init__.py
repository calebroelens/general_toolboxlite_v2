import traceback
import uuid
from abc import ABC, abstractstaticmethod, abstractmethod, abstractproperty
import os
from importlib import util

from core.odoo.client import OdooClient


class BaseCommand(ABC):

    commands = []

    def __init__(self, client: OdooClient):
        self.__client = client
        self.__identifier = str(uuid.uuid4())

    def __init_subclass__(cls, **kwargs):
        cls.commands.append(cls)

    @staticmethod
    @abstractmethod
    def run(client: OdooClient):
        pass



# Loader

def load_command(command_directory: str):
    name = os.path.split(command_directory)[-1]
    spec = util.spec_from_file_location(name, command_directory)
    command = util.module_from_spec(spec)
    spec.loader.exec_module(command)
    return command


path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

for fname in os.listdir(dirpath):
    # Load only "real modules"
    if not fname.startswith('.') and not fname.startswith('__') and fname.endswith('.py'):
        try:
            load_command(os.path.join(dirpath, fname))
        except Exception:
            traceback.print_exc()

