from Code.Anilist.Animes.catalog import Animes
from Code.Anilist.Animes.anime import Anime
from Code.Anilist.Users.catalog import Users

def _get_planned_list(discord_id: int) -> list[Anime]:
    planned_list = Animes().get_planned_list(discord_id)

    if not planned_list:
        raise ValueError(f'No planned animes found for the user: {discord_id}.')

    return planned_list

def _get_anilist_name(discord_id: int) -> str:
    anilist_name = Users().get_user_name(discord_id)
    return anilist_name


def _extract_data(planned_list_1: list[Anime], planned_list_2: list[Anime], anilist_name_1: str, anilist_name_2: str) -> tuple[str, list[Anime]]:
    """Retrieve useful data from the two planned lists. Return the useful data as a string, and the shared animes between the two lists."""
    # Get the number of animes in each planned list
    num_animes_1 = len(planned_list_1)
    num_animes_2 = len(planned_list_2)

    # Get the shared animes between the two planned lists
    shared_animes: list[Anime] = []
    for anime_1 in planned_list_1:
        for anime_2 in planned_list_2:
            if anime_1 == anime_2:
                shared_animes.append(anime_1)
                break

    # Get the number of shared animes between the two planned lists
    num_shared_animes = len(shared_animes)

    # Get the percentage of shared animes between the two planned lists
    percentage_shared_1 = len(shared_animes) / num_animes_1 * 100 if num_animes_1 > 0 else 0
    percentage_shared_2 = len(shared_animes) / num_animes_2 * 100 if num_animes_2 > 0 else 0

    # Get the possibility of getting the same anime in a random roll of the two planned lists
    probability_same_anime = (
        num_shared_animes / (num_animes_1 * num_animes_2) * 100
        if num_animes_1 > 0 and num_animes_2 > 0
        else 0
    )

    # Get the possibility of getting an anime from planned_list_1 that is also in planned_list_2 in a random roll of planned_list_1 and vice versa
    # NOTE This is actually redundant with the percentage of shared animes, but it is more intuitive to understand for the user
    probability_anime_1_in_2 = (
        num_shared_animes / num_animes_1 * 100
        if num_animes_1 > 0
        else 0
    )
    probability_anime_2_in_1 = (
        num_shared_animes / num_animes_2 * 100
        if num_animes_2 > 0
        else 0
    )

    # Create the response message
    response = [
        f'- **{anilist_name_1}\'s ptw:** {num_animes_1} animes',
        f'- **{anilist_name_2}\'s ptw:** {num_animes_2} animes',
        f'- Shared: {num_shared_animes} animes',
        f'  - {percentage_shared_1:.4f}% of {anilist_name_1}\'s ptw list',
        f'  - {percentage_shared_2:.4f}% of {anilist_name_2}\'s ptw list',
        f'- `/random_planned` probabilities:',
        f'  - {anilist_name_1}\'s `/random_planned` anime result is in {anilist_name_2}\'s ptw: {probability_anime_2_in_1:.6f}%',
        f'  - {anilist_name_2}\'s `/random_planned` anime result is in {anilist_name_1}\'s ptw: {probability_anime_1_in_2:.6f}%',
        f'  - Getting the same anime: {probability_same_anime:.8f}%',
    ]
    response = '\n'.join(response)
    response = f'{response}\n\nShared animes:'
    return response, shared_animes

def _sort_animes(shared_animes: list[Anime]) -> list[str]:
    # Split the shared animes by status
    finished_list = []
    releasing_list = []
    not_yet_released_list = []
    cancelled_list = []

    for anime in sorted(shared_animes, key=lambda x: x.media_title.lower()):
        # NOTE harcodding for simplicity
        match anime.media_status:
            case 'FINISHED':
                finished_list.append(anime.media_title)
            case 'RELEASING':
                releasing_list.append(anime.media_title)
            case 'NOT_YET_RELEASED':
                not_yet_released_list.append(anime.media_title)
            case 'CANCELLED':
                cancelled_list.append(anime.media_title)

    # Join the sublists into a single string with the corresponding headers, if the sublists are not empty
    response = ''
    if finished_list:
        response += '************ FINISHED ************\n' + '\n'.join(anime for anime in finished_list) + '\n\n\n'
    if releasing_list:
        response += '************ RELEASING ************\n' + '\n'.join(anime for anime in releasing_list) + '\n\n\n'
    if not_yet_released_list:
        response += '************ NOT YET RELEASED ************\n' + '\n'.join(anime for anime in not_yet_released_list) + '\n\n\n'
    if cancelled_list:
        response += '************ CANCELLED ************\n' + '\n'.join(anime for anime in cancelled_list) + '\n\n\n'
    return response


def compare_ptw(discord_id_1: int, discord_id_2: int) -> tuple[str, str]:
    planned_list_1 = _get_planned_list(discord_id_1)
    anime_name_1 = _get_anilist_name(discord_id_1)

    planned_list_2 = _get_planned_list(discord_id_2)
    anime_name_2 = _get_anilist_name(discord_id_2)

    response, shared_animes = _extract_data(planned_list_1, planned_list_2, anime_name_1, anime_name_2)
    return response, _sort_animes(shared_animes)