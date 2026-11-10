from Code.Anilist.Users.catalog import Users

class Anime:
    """Represents an anime entry in the catalog."""

    def __init__(self, media_id: int, media_title: str, media_status: str):
    
        self.media_id = media_id
        self.media_status = media_status
        self.media_title = media_title
        self.users_data: dict[int, dict[str, int|str]] = {}
        """
        users_data = {
            discord_id_1: {
                'score': score_1,
                'status': status_1,
                'progress': progress_1,
            },
        }
        """

    def add_user_data(self, discord_id: int, score: int, status: str, progress: int) -> None:
        """Add user data to the anime entry."""
        self.users_data[discord_id] = {
            'score': score,
            'status': status,
            'progress': progress,
        }

    def represent_users_data(self) -> str:
        """Return a string contaning, for each existing status, the list of users (names) that have that status, along with their scores."""
        ORDERED_STATUSES = ["CURRENT", "REPEATING", "COMPLETED", "PAUSED", "DROPPED", "PLANNING"]
        # Temporary list of tuples to be able to sort the users by their names
        status_dict: dict[str, int, list[tuple[str, str]]] = {status: [] for status in ORDERED_STATUSES}

        # Split the users by their anime status
        for user_id, user_data in self.users_data.items():
            user_status = user_data['status']
            user_name = Users().get_user_name(user_id)
            user_score = user_data['score']

            # Add the progress if the anime is not in completed or ptw
            if user_status in {"CURRENT", "REPEATING", "PAUSED", "DROPPED", }:
                user_progress = user_data['progress']
                content = f"{user_name} [{user_progress}] **{user_score}**" if user_score else f"{user_name} [{user_progress}]"    
            else:
                content = f"{user_name} **{user_score}**" if user_score else f"{user_name}"

            status_dict[user_status].append((user_name, user_score, content))

        result = ""
        for status, users in status_dict.items():
            if users:
                sorted_users = sorted(users, key=lambda x: (-x[1], x[0].lower()))
                formatted_users = [user[2] for user in sorted_users]
                result += f"**{status.capitalize()}:** {(' | ').join(formatted_users)}\n"

        # Add the users that doesn't have the anime in their list (Not-On-List)
        not_on_list_users = []
        for user in Users().get_users_data():
            if user.discord_id not in self.users_data:
                not_on_list_users.append(user.anilist_name)

        if not_on_list_users:
            not_on_list_users.sort(key=lambda x: x.lower())
            result += f"**Not On List:** {(' | ').join(not_on_list_users)}"

        return result


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Anime):
            return NotImplemented
        return self.media_id == other.media_id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Anime):
            return NotImplemented
        return self.media_id < other.media_id