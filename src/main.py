"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from textwrap import wrap

from src.recommender import load_songs, recommend_songs


def print_recommendation_table(recommendations) -> None:
    """Print recommendations as a simple ASCII table with reasons."""
    col_rank = 4
    col_title = 22
    col_artist = 16
    col_score = 7
    col_reason = 62

    sep = (
        "+"
        + "-" * (col_rank + 2)
        + "+"
        + "-" * (col_title + 2)
        + "+"
        + "-" * (col_artist + 2)
        + "+"
        + "-" * (col_score + 2)
        + "+"
        + "-" * (col_reason + 2)
        + "+"
    )

    print(sep)
    print(
        f"| {'#':<{col_rank}} | {'Title':<{col_title}} | {'Artist':<{col_artist}} | {'Score':<{col_score}} | {'Reason':<{col_reason}} |"
    )
    print(sep)

    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        reason_lines = wrap(explanation, width=col_reason) or [""]

        print(
            f"| {str(i):<{col_rank}} | {song['title'][:col_title]:<{col_title}} | {song['artist'][:col_artist]:<{col_artist}} | {f'{score:.2f}':<{col_score}} | {reason_lines[0]:<{col_reason}} |"
        )
        for line in reason_lines[1:]:
            print(
                f"| {'':<{col_rank}} | {'':<{col_title}} | {'':<{col_artist}} | {'':<{col_score}} | {line:<{col_reason}} |"
            )
        print(sep)


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}\n")

    # Switch ranking behavior here:
    # "balanced", "genre_first", "mood_first", "energy_focused"
    ranking_mode = "balanced"
    ranking_modes = ["balanced", "genre_first", "mood_first", "energy_focused"]

    user_profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
        "Late-Night Synthwave": {"genre": "synthwave", "mood": "moody", "energy": 0.7},
        "Focus Flow": {"genre": "lofi", "mood": "focused", "energy": 0.4},
        "Warm Up Workout": {"genre": "house", "mood": "euphoric", "energy": 0.9},
    }

    # Starter example profile: pop + happy + energetic
    user_prefs = user_profiles["High-Energy Pop"]
    print(f"User Profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print(f"Ranking mode: {ranking_mode}")
    print("=" * 80)

    recommendations = recommend_songs(user_prefs, songs, k=5, mode=ranking_mode)

    print("\n🎵 TOP 5 RECOMMENDATIONS (ASCII SUMMARY TABLE):\n")
    print_recommendation_table(recommendations)

    print("\n🔁 MODE COMPARISON (Top 3 per strategy)\n")
    for mode in ranking_modes:
        print(f"[{mode}]")
        mode_recommendations = recommend_songs(user_prefs, songs, k=3, mode=mode)
        for i, rec in enumerate(mode_recommendations, 1):
            song, score, _explanation = rec
            print(f"  {i}. {song['title']} ({score:.2f}) - {song['artist']} [{song['genre']}/{song['mood']}]")
        print()


if __name__ == "__main__":
    main()
