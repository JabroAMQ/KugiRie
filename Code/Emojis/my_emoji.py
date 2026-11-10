import discord

class MyEmoji:
    """Custom discord emoji with extra information that the bot needs."""
    def __init__(self, emoji: discord.Emoji, row: int):
        self._emoji = emoji
        self._row = row

    @property
    def row(self) -> int:
        """The row that the emoji belongs to."""
        return self._row

    @row.setter
    def row(self, row : int) -> None:
        self._row = row

    @property
    def emoji(self) -> discord.Emoji:
        """The custom discord emoji."""
        return self._emoji

    @property
    def id(self) -> int:
        """The id of the custom discord emoji."""
        return self._emoji.id

    @property
    def name(self) -> str:
        """The name of the custom discord emoji."""
        return self._emoji.name
    
    def __repr__(self) -> str:
        return str(self.emoji)

    def __key(self) -> int:
        return self.id
    
    def __hash__(self) -> int:
        return hash(self.__key())
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MyEmoji):
            return NotImplemented
        
        return self.__key() == other.__key()
        
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, MyEmoji):
            return NotImplemented
        
        if self.row == other.row:
            return self.name.lower() < other.name.lower()
        
        return self.row < other.row
