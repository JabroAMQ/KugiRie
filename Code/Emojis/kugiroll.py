import random
import itertools

class Kugiroll:
    @staticmethod
    def raw_roll_generator(emojis_by_row: dict[int, list[str]], success_probs: list[float]):
        """
        Produces infinite raw simulation results.
        Returns a dict for each complete roll: { row: [emoji1, emoji2, emoji3] }
        """        
        while True:
            current_roll = {}
            for index, success_prob in enumerate(success_probs):
                row_number = index + 1
                row_emojis = emojis_by_row.get(row_number)
                
                if not row_emojis:
                    continue

                if random.random() <= success_prob:
                    e = random.choice(row_emojis)
                    current_roll[row_number] = [e, e, e]
                else:
                    current_roll[row_number] = random.choices(row_emojis, k=3)
                    
            yield current_roll

    @staticmethod
    def single_kugiroll(emojis_by_row: dict[int, list[str]], success_probs: list[float]) -> str:
        """Simulate a roll of 3 emojis per available row."""
        raw_roll = next(Kugiroll.raw_roll_generator(emojis_by_row, success_probs))
        roll_visual = []

        for row_number, chosen_emojis in sorted(raw_roll.items()):
            is_win = len(set(chosen_emojis)) == 1
            row_str = f"{''.join(chosen_emojis)}   {'🔔' if is_win else '❌'}"
            roll_visual.append(row_str)
            
        return '\n'.join(roll_visual)
    

    @staticmethod
    def multiple_kugiroll(emojis_by_row: dict[int, list[str]], number_of_rolls: int, success_probs: list[float]) -> str:
        """Returns a summary with the results of rolling `number_of_rolls` `single_kugiroll()`"""
        rolls_results: dict[int, dict[str, int]] = {
            row: {emoji: 0 for emoji in emojis} 
            for row, emojis in emojis_by_row.items()
        }

        # Roll n "single_kugiroll()"
        rolls_stream = Kugiroll.raw_roll_generator(emojis_by_row, success_probs)
        limited_rolls = itertools.islice(rolls_stream, number_of_rolls)

        # Process the results
        for raw_roll in limited_rolls:
            for row_number, chosen_emojis in raw_roll.items():
                if len(set(chosen_emojis)) == 1:
                    winning_emoji = chosen_emojis[0]
                    rolls_results[row_number][winning_emoji] += 1

        # Create the summary
        rolls_summary = []
        for row_number, row_dict in sorted(rolls_results.items()):
            row_summary = [f'{emoji} x{count}' for emoji, count in row_dict.items() if count > 0]
            if row_summary:
                rolls_summary.append(f'~ **Fila {row_number}:** ' + ', '.join(row_summary))

        return '\n'.join(rolls_summary)