from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Optional advanced preferences used by the functional recipe.
    preferred_genres: Optional[List[str]] = None
    preferred_moods: Optional[List[str]] = None
    target_tempo_bpm: float = 100.0
    target_valence: float = 0.6
    target_danceability: float = 0.7
    target_acousticness: float = 0.4
    weight_genre: float = 0.20
    weight_mood: float = 0.24
    weight_energy: float = 0.18
    weight_tempo: float = 0.12
    weight_valence: float = 0.10
    weight_danceability: float = 0.10
    weight_acousticness: float = 0.03
    weight_crescendo: float = 0.03

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _closeness(value: float, target: float, scale: float) -> float:
        if scale <= 0:
            return 0.0
        return max(0.0, 1.0 - min(abs(value - target) / scale, 1.0))

    @staticmethod
    def _crescendo_proxy(song: Song) -> float:
        # Proxy for build-and-release feel: danceability + energetic drive + low acousticness.
        return (
            0.45 * song.danceability
            + 0.35 * min(song.energy / 0.85, 1.0)
            + 0.20 * (1.0 - song.acousticness)
        )

    def _score_song_with_breakdown(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a song and return both its numeric score and reasons."""
        preferred_genres = user.preferred_genres or [user.favorite_genre]
        preferred_moods = user.preferred_moods or [user.favorite_mood]
        reasons: List[str] = []
        total_score = 0.0

        # Genre match: +1.0
        if song.genre in preferred_genres:
            genre_points = 1.0
            total_score += genre_points
            reasons.append(f"genre match (+{genre_points:.1f})")

        # Mood match: +1.0
        if song.mood in preferred_moods:
            mood_points = 1.0
            total_score += mood_points
            reasons.append(f"mood match (+{mood_points:.1f})")

        # Energy closeness: up to +4.0
        energy_closeness = self._closeness(song.energy, user.target_energy, 0.35)
        energy_points = energy_closeness * 4.0
        if energy_points > 0.05:
            total_score += energy_points
            reasons.append(f"energy alignment (+{energy_points:.2f})")

        # Tempo closeness: up to +1.2
        tempo_closeness = self._closeness(song.tempo_bpm, user.target_tempo_bpm, 40.0)
        tempo_points = tempo_closeness * 1.2
        if tempo_points > 0.05:
            total_score += tempo_points
            reasons.append(f"tempo match (+{tempo_points:.2f})")

        # Valence closeness: up to +1.0
        valence_closeness = self._closeness(song.valence, user.target_valence, 0.35)
        valence_points = valence_closeness * 1.0
        if valence_points > 0.05:
            total_score += valence_points
            reasons.append(f"valence fit (+{valence_points:.2f})")

        # Danceability closeness: up to +1.5
        dance_closeness = self._closeness(song.danceability, user.target_danceability, 0.35)
        dance_points = dance_closeness * 1.5
        if dance_points > 0.05:
            total_score += dance_points
            reasons.append(f"danceability fit (+{dance_points:.2f})")

        # Acousticness closeness: up to +0.8
        acoustic_closeness = self._closeness(song.acousticness, user.target_acousticness, 0.40)
        acoustic_points = acoustic_closeness * 0.8
        if acoustic_points > 0.05:
            total_score += acoustic_points
            reasons.append(f"acousticness fit (+{acoustic_points:.2f})")

        # Crescendo proxy: up to +0.5
        crescendo = self._crescendo_proxy(song)
        crescendo_points = crescendo * 0.5
        if crescendo_points > 0.05:
            total_score += crescendo_points
            reasons.append(f"crescendo vibe (+{crescendo_points:.2f})")

        # Bonus for acoustic preference
        if user.likes_acoustic:
            acoustic_bonus = song.acousticness * 0.3
            if acoustic_bonus > 0.05:
                total_score += acoustic_bonus
                reasons.append(f"acoustic preference (+{acoustic_bonus:.2f})")

        if not reasons:
            reasons.append("minimal match")

        return total_score, reasons

    def _score_song(self, user: UserProfile, song: Song) -> float:
        """Wrapper for backward compatibility; returns just the score."""
        score, _ = self._score_song_with_breakdown(user, song)
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(
            self.songs,
            key=lambda s: (
                self._score_song(user, s),
                1.0 if s.mood == user.favorite_mood else 0.0,
                self._closeness(s.tempo_bpm, user.target_tempo_bpm, 40.0),
            ),
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score_song_with_breakdown(user, song)
        reason_text = ", ".join(reasons)
        return f"{song.title} scores {score:.1f}/10.0 because: {reason_text}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def _score_song_functional(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    """Score a song and return both its numeric score and reasons."""
    preferred_genres = user_prefs.get("preferred_genres")
    if preferred_genres is None and user_prefs.get("genre") is not None:
        preferred_genres = [user_prefs["genre"]]
    preferred_genres = preferred_genres or []

    preferred_moods = user_prefs.get("preferred_moods")
    if preferred_moods is None and user_prefs.get("mood") is not None:
        preferred_moods = [user_prefs["mood"]]
    preferred_moods = preferred_moods or []

    target_energy = float(user_prefs.get("energy", 0.6))
    target_tempo = float(user_prefs.get("tempo_bpm", 100.0))
    target_valence = float(user_prefs.get("valence", 0.6))
    target_danceability = float(user_prefs.get("danceability", 0.7))
    target_acousticness = float(user_prefs.get("acousticness", 0.4))

    reasons: List[str] = []
    total_score = 0.0

    # Genre match: +1.0
    if song["genre"] in preferred_genres:
        genre_points = 1.0
        total_score += genre_points
        reasons.append(f"genre match (+{genre_points:.1f})")

    # Mood match: +1.0
    if song["mood"] in preferred_moods:
        mood_points = 1.0
        total_score += mood_points
        reasons.append(f"mood match (+{mood_points:.1f})")

    # Energy closeness: up to +4.0
    energy_closeness = _closeness(song["energy"], target_energy, float(user_prefs.get("energy_range", 0.35)))
    energy_points = energy_closeness * 4.0
    if energy_points > 0.05:
        total_score += energy_points
        reasons.append(f"energy alignment (+{energy_points:.2f})")

    # Tempo closeness: up to +1.2
    tempo_closeness = _closeness(song["tempo_bpm"], target_tempo, float(user_prefs.get("tempo_range", 40.0)))
    tempo_points = tempo_closeness * 1.2
    if tempo_points > 0.05:
        total_score += tempo_points
        reasons.append(f"tempo match (+{tempo_points:.2f})")

    # Valence closeness: up to +1.0
    valence_closeness = _closeness(song["valence"], target_valence, float(user_prefs.get("valence_range", 0.35)))
    valence_points = valence_closeness * 1.0
    if valence_points > 0.05:
        total_score += valence_points
        reasons.append(f"valence fit (+{valence_points:.2f})")

    # Danceability closeness: up to +1.5
    dance_closeness = _closeness(song["danceability"], target_danceability, float(user_prefs.get("danceability_range", 0.35)))
    dance_points = dance_closeness * 1.5
    if dance_points > 0.05:
        total_score += dance_points
        reasons.append(f"danceability fit (+{dance_points:.2f})")

    # Acousticness closeness: up to +0.8
    acoustic_closeness = _closeness(song["acousticness"], target_acousticness, float(user_prefs.get("acousticness_range", 0.40)))
    acoustic_points = acoustic_closeness * 0.8
    if acoustic_points > 0.05:
        total_score += acoustic_points
        reasons.append(f"acousticness fit (+{acoustic_points:.2f})")

    # Crescendo proxy: up to +0.5
    crescendo = _crescendo_proxy(song)
    crescendo_points = crescendo * 0.5
    if crescendo_points > 0.05:
        total_score += crescendo_points
        reasons.append(f"crescendo vibe (+{crescendo_points:.2f})")

    if not reasons:
        reasons.append("minimal match")

    return total_score, reasons


def _closeness(value: float, target: float, scale: float) -> float:
    """Return a 0-to-1 closeness score for a numeric feature."""
    if scale <= 0:
        return 0.0
    return max(0.0, 1.0 - min(abs(value - target) / scale, 1.0))


def _crescendo_proxy(song: Dict) -> float:
    """Estimate a build-and-release vibe from existing song features."""
    return (
        0.45 * song["danceability"]
        + 0.35 * min(song["energy"] / 0.85, 1.0)
        + 0.20 * (1.0 - song["acousticness"])
    )


def _passes_guardrails(user_prefs: Dict, song: Dict) -> bool:
    """Filter out songs that are too far from the user's comfort range."""
    danceability_floor = user_prefs.get("danceability_floor")
    if danceability_floor is not None and song["danceability"] < float(danceability_floor):
        return False

    tempo_tolerance = float(user_prefs.get("tempo_tolerance", 60.0))
    if "tempo_bpm" in user_prefs and abs(song["tempo_bpm"] - float(user_prefs["tempo_bpm"])) > tempo_tolerance:
        return False

    energy_tolerance = float(user_prefs.get("energy_tolerance", 0.5))
    if "energy" in user_prefs and abs(song["energy"] - float(user_prefs["energy"])) > energy_tolerance:
        return False

    return True

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return the top-k with explanations."""
    scored: List[Tuple[Dict, float, str, str]] = []
    for song in songs:
        if not _passes_guardrails(user_prefs, song):
            continue

        score, reasons = _score_song_functional(song, user_prefs)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation, song["artist"]))

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # Prefer artist variety when selecting top-k
    selected: List[Tuple[Dict, float, str]] = []
    used_artists = set()
    for song, score, explanation, artist in scored:
        if len(selected) >= k:
            break
        if artist not in used_artists:
            selected.append((song, score, explanation))
            used_artists.add(artist)

    # Fill remaining slots if needed
    if len(selected) < k:
        selected_ids = {s[0]["id"] for s in selected}
        for song, score, explanation, artist in scored:
            if len(selected) >= k:
                break
            if song["id"] not in selected_ids:
                selected.append((song, score, explanation))
                selected_ids.add(song["id"])

    return selected
