import os

from Code.Anilist.Users.user import User
from Code.Utilities.read_yaml import load_yaml_content

class Users:

    _instance = None
    def __new__(cls) -> 'Users':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance

    def _set_data(self) -> None:
        yaml_route = os.path.join('Config', 'users.yaml')
        users_data = load_yaml_content(yaml_route=yaml_route)
        self.users_data = {
            int(discord_id): User(
                discord_id=int(discord_id),
                anilist_id=info['anilist_id'],
                anilist_name=info['anilist_name']
            )
            for discord_id, info in users_data['users'].items()
        }

    def get_user_name(self, discord_id: int) -> str | None:
        """Return the user name for a given discord_id, or None if not found."""
        user = self.users_data.get(discord_id)
        return user.anilist_name if user else None

    def get_all_users_names(self) -> list[str]:
        return [user.anilist_name for user in self.users_data.values()]

    def get_users_data(self) -> list[User]:
        """Return a list of all stored users."""
        return list(self.users_data.values())