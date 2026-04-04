"""
SYSTEM EVALUATION: Adversarial & Edge Case Testing
====================================================
This script tests the recommender system with "adversarial" profiles designed to 
expose edge cases, contradictions, and potential weaknesses in the scoring logic.

Insights Being Tested:
- Conflicting preferences (high energy + sad mood)
- Extreme values (0.0 or 1.0 across dimensions)
- Normalization edge cases
- Preference conflicts that may "trick" scoring
"""

from src.recommender import load_songs, _score_song_functional
from typing import List, Dict, Tuple

def create_adversarial_profiles() -> Dict[str, Dict]:
    """Create test profiles designed to expose edge cases and contradictions."""
    
    profiles = {
        # 1. CONFLICTING ENERGY & MOOD
        "High Energy + Sad": {
            "genre": "rock",
            "mood": "sad",
            "energy": 0.9,  # Very high energy
            # Sad mood typically expects low energy - contradiction!
            "preferred_moods": ["sad"],
            "preferred_genres": ["rock"],
            "tempo_bpm": 120,
            "valence": 0.2,  # Low valence (sad)
            "danceability": 0.8,  # But high danceability (contradictory)
            "acousticness": 0.4,
        },
        
        # 2. ACOUSTIC CONTRADICTION
        "Electric Rock + High Acousticness": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "preferred_moods": ["intense"],
            "preferred_genres": ["rock"],
            "acousticness": 0.9,  # Very acoustic
            "tempo_bpm": 150,  # Fast rock tempo
            "valence": 0.5,
            "danceability": 0.7,
        },
        
        # 3. EXTREME ENERGY BOUNDARIES
        "Minimal Energy (0.0)": {
            "genre": "ambient",
            "mood": "chill",
            "energy": 0.0,  # Absolute minimum - edge case!
            "preferred_moods": ["chill"],
            "preferred_genres": ["ambient"],
            "tempo_bpm": 40,
            "valence": 0.3,
            "danceability": 0.3,
            "acousticness": 0.7,
        },
        
        # 4. MAXIMUM ENERGY BOUNDARY
        "Maximum Energy (1.0)": {
            "genre": "house",
            "mood": "euphoric",
            "energy": 1.0,  # Absolute maximum
            "preferred_moods": ["euphoric"],
            "preferred_genres": ["house"],
            "tempo_bpm": 200,
            "danceability": 1.0,
            "valence": 0.9,
            "acousticness": 0.0,
        },
        
        # 5. ULTRA-HIGH TEMPO + ACOUSTIC
        "200 BPM Acoustic Jazz": {
            "genre": "jazz",
            "mood": "relaxed",
            "energy": 0.3,  # Relaxed, but...
            "preferred_moods": ["relaxed"],
            "preferred_genres": ["jazz"],
            "tempo_bpm": 200,  # Way too fast for jazz/relaxed
            "acousticness": 0.95,
            "valence": 0.6,
            "danceability": 0.3,
        },
        
        # 6. DANCEABILITY PARADOX
        "Non-Danceable House": {
            "genre": "house",
            "mood": "euphoric",
            "energy": 0.8,
            "preferred_moods": ["euphoric"],
            "preferred_genres": ["house"],
            "danceability": 0.1,  # Very low danceability (house is for dancing!)
            "tempo_bpm": 120,
            "valence": 0.8,
            "acousticness": 0.2,
        },
        
        # 7. VALENCE MISMATCH
        "Sad Pop Music": {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.7,
            "preferred_moods": ["sad"],
            "preferred_genres": ["pop"],
            "valence": 0.2,  # Very sad (contradicts pop's typical happiness)
            "tempo_bpm": 100,
            "danceability": 0.7,
            "acousticness": 0.3,
        },
        
        # 8. ALL EXTREMES
        "Impossible Preference": {
            "genre": "synthwave",
            "mood": "moody",
            "energy": 0.5,
            "preferred_moods": ["moody"],
            "preferred_genres": ["synthwave"],
            "tempo_bpm": 220,
            "valence": 0.1,  # Very sad
            "danceability": 0.95,  # But highly danceable
            "acousticness": 0.05,  # Very electric/synthetic
        },
    }
    
    return profiles


def run_adversarial_evaluation(songs: List[Dict], profiles: Dict[str, Dict]) -> None:
    """Run the recommender on each adversarial profile and show results."""
    
    print("\n" + "=" * 90)
    print("🔬 SYSTEM EVALUATION: ADVERSARIAL PROFILE TESTING")
    print("=" * 90)
    print("\nTesting recommender scoring logic with edge cases and contradictions...\n")
    
    for profile_name, user_profile in profiles.items():
        print("\n" + "─" * 90)
        print(f"🎭 PROFILE: {profile_name}")
        print("─" * 90)
        
        # Show what makes this profile adversarial
        print(f"  Energy Target: {user_profile.get('energy', 0.6):.2f}")
        print(f"  Mood Preference: {user_profile.get('preferred_moods', [user_profile.get('mood', 'unknown')])}")
        print(f"  Genre Preference: {user_profile.get('preferred_genres', [user_profile.get('genre', 'unknown')])}")
        print(f"  Tempo Target: {user_profile.get('tempo_bpm', 100):.0f} BPM")
        print(f"  Valence Target: {user_profile.get('valence', 0.6):.2f}")
        print(f"  Danceability Target: {user_profile.get('danceability', 0.7):.2f}")
        print(f"  Acousticness Target: {user_profile.get('acousticness', 0.4):.2f}")
        
        # Score and rank all songs
        scored_songs = []
        for song in songs:
            score, reasons = _score_song_functional(song, user_profile)
            scored_songs.append((song, score, reasons))
        
        # Sort by score descending
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Show top 5
        print(f"\n  🎵 TOP 5 RECOMMENDATIONS:\n")
        for rank, (song, score, reasons) in enumerate(scored_songs[:5], 1):
            print(f"    {rank}. [{score:5.2f}/10] {song['title']}")
            print(f"       Artist: {song['artist']} | Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"       Energy: {song['energy']:.2f} | Tempo: {song['tempo_bpm']:.0f} BPM | Valence: {song['valence']:.2f}")
            reasons_str = " • ".join(reasons) if reasons else "No strong matches"
            print(f"       Why: {reasons_str}\n")
        
        # Identify potential "tricks" or anomalies
        top_score = scored_songs[0][1]
        if top_score < 2.0:
            print(f"  ⚠️  WARNING: Very low recommendation scores (max: {top_score:.2f}/10)")
            print(f"     This profile may be impossible to satisfy!\n")
        elif len(set(s[0]['genre'] for s in scored_songs[:5])) == 1:
            print(f"  ℹ️  INFO: All top 5 are same genre (possible over-weighting of genre)\n")
        else:
            print()


def main():
    """Run system evaluation."""
    songs = load_songs("data/songs.csv")
    print(f"\n📊 Loaded {len(songs)} songs from database")
    
    adversarial_profiles = create_adversarial_profiles()
    run_adversarial_evaluation(songs, adversarial_profiles)
    
    print("\n" + "=" * 90)
    print("✅ EVALUATION COMPLETE")
    print("=" * 90)
    print("\nKey Questions to Consider:")
    print("  • Did any profile expose scoring bugs or unexpected behavior?")
    print("  • Are contradictory preferences handled gracefully?")
    print("  • Do extreme values (0.0, 1.0) cause any issues?")
    print("  • Are weights balanced appropriately for edge cases?")
    print("  • Should certain preference combinations be rejected?")
    print()


if __name__ == "__main__":
    main()
