from Code.Anilist.Animes.anime import Anime

class Animes:

    _instance = None
    def __new__(cls) -> 'Animes':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance

    def _set_data(self) -> None:
        self.anime_data: dict[int, Anime] = {}

    def add(self, media_data: dict) -> None:
        media_id: int = media_data['mediaId']
        media_title: str = media_data['title']
        media_status: str = media_data['mediaStatus']
        if media_id not in self.anime_data:
            self.anime_data[media_id] = Anime(media_id, media_title, media_status)

        user_discord_id: int = media_data['discordId']
        user_score: int = int(media_data['score']*10)
        user_status: str = media_data['userStatus']
        user_progress: int = media_data['progress']

        self.anime_data[media_id].add_user_data(user_discord_id, user_score, user_status, user_progress)

    def get_planned_list(self, discord_id: int) -> list[Anime]:
        planned_animes = []
        for anime in self.anime_data.values():
            if discord_id in anime.users_data and anime.users_data[discord_id]['status'] == 'PLANNING':
                planned_animes.append(anime)
        return planned_animes

    def get_anime(self, anime_id: int) -> Anime:
        return self.anime_data.get(anime_id)