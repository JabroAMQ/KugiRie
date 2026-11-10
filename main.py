import os

import dotenv
import discord

from Commands.utilities import load_app_commands, load_controllers
from Code.Emojis.controller import Emojis_Controller
from Code.Others.easter_eggs import Easter_Eggs

class KugiRie(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.sync_commands = False
        self.tree = discord.app_commands.CommandTree(self)
        load_app_commands(self)

        @self.tree.error
        async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
            if isinstance(error, discord.app_commands.errors.CheckFailure):
                await interaction.response.send_message(content='You don\'t have permissions to use this command', ephemeral=True)
            else:
                # NOTE this should never be reached
                print('Unhandled app_commands top level error!')
                raise error

    async def setup_hook(self):
        if self.sync_commands:
            commands = await self.tree.sync()
            print(f'Synced {len(commands)} commands.')

    async def on_ready(self):
        await load_controllers(self)
        await self.change_presence(activity=discord.Game(name='$p'))
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        await Emojis_Controller().kugiroll(message)
        await Easter_Eggs().check(message)


dotenv.load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
client = KugiRie()
client.run(TOKEN)