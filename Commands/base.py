import os
from abc import ABC, abstractmethod

import discord

from Code.Utilities.read_yaml import load_yaml_content

class Commands(ABC):

    def __init__(self) -> None:
        yaml_route = os.path.join('Config', 'moderation.yaml')
        moderation_data = load_yaml_content(yaml_route=yaml_route)
        self.OWNER_ID = moderation_data['owner_id']

    def is_user_owner(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.OWNER_ID
    
    @abstractmethod
    def load_commands(self, client: discord.Client) -> None:
        pass