import os
import random

import discord

from Code.Emojis.my_emoji import MyEmoji
from Code.Emojis.kugiroll import Kugiroll
from Code.Utilities.read_yaml import load_yaml_content
from Code.Utilities.error_handler import error_handler_decorator

class Emojis_Controller:
    _instance = None
    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data(*args)
        return cls._instance
    
    def _set_data(self, client: discord.Client) -> None:
        # Get the emoji data
        yaml_route = os.path.join('Config', 'emojis.yaml')
        emojis_data = load_yaml_content(yaml_route=yaml_route)
        
        self.emojis: dict[str, MyEmoji] = {}
        self.emojis_by_row: dict[int, list[str]] = {i: [] for i in range(1, 6)}

        for id, data in emojis_data['emojis'].items():
            discord_emoji = client.get_emoji(id)
            my_emoji = MyEmoji(discord_emoji, data['row'])

            self.emojis[data['name']] = my_emoji
            self.emojis_by_row[my_emoji.row].append(str(my_emoji))

        # Get the rolls probs
        yaml_route = os.path.join('Config', 'probs.yaml')
        probs_data = load_yaml_content(yaml_route=yaml_route)
        kugiroll_data = probs_data['kugiroll']

        self.max_rolls = kugiroll_data['max_rolls']
        self.row_probs = [kugiroll_data[f'row_{i}'] for i in range(1, 6)]


    def get_emoji(self, name: str) -> str:
        e = self.emojis.get(name)
        return str(e) if e is not None else ''

    def get_emojis_in_message(self, message_content: str) -> str:
        sorted_emoji_list = sorted(list(self.emojis.values()))
        return ''.join([str(emoji) for emoji in sorted_emoji_list if emoji.name.lower() in message_content.lower()])

    def get_random_emoji(self) -> str:
        e = random.choice(list(self.emojis.values()))
        return str(e)


    @error_handler_decorator()
    async def print_all_emojis(self, interaction: discord.Interaction):
        emojis = '\n'.join([' '.join(self.emojis_by_row[row]) for row in range(1, 6)])
        await interaction.response.send_message(content=emojis)

    async def kugiroll(self, message: discord.Message):
        # Check if the message ask for a kugiroll
        word_list = message.content.lower().split(' ')
        if word_list[0] != '$p' and word_list[0] != '$pokemon':
            return

        # Check the amount of rolls desired
        rolls = 1
        if len(word_list) > 1 and word_list[1].isnumeric() and int(word_list[1]) > 1:
            rolls = int(word_list[1])

        if rolls > self.max_rolls:
            await message.channel.send(f'Tranquilízate {message.author.name}! El número máximo permitido es {self.max_rolls}')
            return

        # Do the rolls
        match rolls:
            case 1:
                result = Kugiroll.single_kugiroll(self.emojis_by_row, self.row_probs)
                await message.channel.send(result)
            case _:
                result = Kugiroll.multiple_kugiroll(self.emojis_by_row, rolls, self.row_probs)
                await message.channel.send(f'{message.author.name}, has conseguido:\n\n{result}')