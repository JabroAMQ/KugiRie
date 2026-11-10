import os
import importlib

import discord

from Code.Utilities.error_handler import print_exception
from Code.Anilist.controller import Controller
from Code.Emojis.controller import Emojis_Controller
from Code.Others.easter_eggs import Easter_Eggs

def load_app_commands(client: discord.Client):
    """
    Load all the `discord.app_commands` commands found in the `./Commands/Commands` subdirectory dynamically.\n
    Parameters:
    -----------
    - `client`: `discord.Client`
        The Discord Client to load commands into.
    """
    # importing inside function to avoid circular import error
    from Commands.base import Commands

    command_directory_path = os.path.join('Commands', 'Commands')

    for root, _, files in os.walk(command_directory_path):
        files = [file for file in files if file.endswith('.py')]
        
        for file in files:
            module_path = os.path.relpath(os.path.join(root, file))
            module_name = module_path[:-3].replace(os.path.sep, '.')
            
            try:
                module = importlib.import_module(module_name)
                class_name = f'{module_name.split(".")[-1].capitalize()}_Commands'

                if hasattr(module, class_name):
                    command_class = getattr(module, class_name)
                    if issubclass(command_class, Commands):
                        command_class().load_commands(client)
                    else:
                        print(f'Class {class_name} in module {module_name} does not inherit from Commands base class')
                
                else:
                    print(f'Invalid class name ({class_name}) in module {module_name} (check capitalizations in `class_name`)')

            except ImportError as error:
                print(f'Failed to import module {module_name}')
                print_exception(error)


async def load_controllers(client: discord.Client):
    """Auxiliar function to load the singleton controllers so that delay is not introduced when they are first needed."""
    # Saving the references is not needed
    Controller()
    Easter_Eggs()
    Emojis_Controller(client)