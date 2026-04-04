"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}\n")

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
    print("=" * 80)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n🎵 TOP 5 RECOMMENDATIONS (Score out of 10.0):\n")
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{i}. {song['title'].upper()}")
        print(f"   Artist: {song['artist']}")
        print(f"   Score: {score:.2f}/10.0")
        print(f"   Why: {explanation}")
        print()


if __name__ == "__main__":
    main()
