
import os
import random

import discord

from Code.Emojis.controller import Emojis_Controller
from Code.Utilities.read_yaml import load_yaml_content

class Easter_Eggs:
    _instance = None
    def __new__(cls) -> 'Easter_Eggs':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance

    def _set_data(self) -> None:
        yaml_route = os.path.join('Config', 'probs.yaml')
        probs_data = load_yaml_content(yaml_route=yaml_route)
        self.reaction_prob = probs_data['reaction']

    async def check(self, message: discord.Message):
        try:
            await self._emotes_get(message)
            if random.random() < self.reaction_prob:
                await self._emotes_react(message)

        except discord.errors.Forbidden:
            pass

    async def _emotes_get(self, message: discord.Message):
        emotes = Emojis_Controller().get_emojis_in_message(message.content)
        if emotes:
            await message.reply(emotes, allowed_mentions=discord.AllowedMentions.none())

    async def _emotes_react(self, message: discord.Message):
        await message.add_reaction(Emojis_Controller().get_random_emoji())