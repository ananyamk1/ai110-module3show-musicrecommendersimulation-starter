from typing import List, Dict, Tuple, Optional, Callable
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
    popularity: float = 50.0
    release_decade: int = 2020
    mood_tags: Optional[List[str]] = None
    lyrical_density: float = 0.5
    production_quality: float = 7.0

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
    target_popularity: float = 60.0
    preferred_decade: int = 2020
    preferred_mood_tags: Optional[List[str]] = None
    target_lyrical_density: float = 0.6
    target_production_quality: float = 7.5


def _adjacent_decade_bonus(song_decade: int, target_decade: int) -> float:
    """Reward exact decade matches and small bonus for adjacent decades."""
    if song_decade == target_decade:
        return 1.2
    if abs(song_decade - target_decade) == 10:
        return 0.4
    return 0.0

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

        # Popularity closeness: up to +2.5
        popularity_closeness = self._closeness(song.popularity, user.target_popularity, 25.0)
        popularity_points = popularity_closeness * 2.5
        if popularity_points > 0.05:
            total_score += popularity_points
            reasons.append(f"popularity fit (+{popularity_points:.2f})")

        # Release decade affinity: +1.2 exact, +0.4 adjacent
        decade_points = _adjacent_decade_bonus(song.release_decade, user.preferred_decade)
        if decade_points > 0.0:
            total_score += decade_points
            reasons.append(f"era preference (+{decade_points:.1f})")

        # Detailed mood tags: +0.4 per matching tag, up to +1.6
        song_tags = song.mood_tags or []
        preferred_tags = user.preferred_mood_tags or []
        tag_matches = len(set(song_tags).intersection(set(preferred_tags)))
        mood_tag_points = min(tag_matches * 0.4, 1.6)
        if mood_tag_points > 0.05:
            total_score += mood_tag_points
            reasons.append(f"mood-tag match (+{mood_tag_points:.2f})")

        # Lyrical density closeness: up to +1.0
        lyrical_closeness = self._closeness(song.lyrical_density, user.target_lyrical_density, 0.30)
        lyrical_points = lyrical_closeness * 1.0
        if lyrical_points > 0.05:
            total_score += lyrical_points
            reasons.append(f"lyrical fit (+{lyrical_points:.2f})")

        # Production quality closeness: up to +0.8
        quality_closeness = self._closeness(song.production_quality, user.target_production_quality, 2.5)
        quality_points = quality_closeness * 0.8
        if quality_points > 0.05:
            total_score += quality_points
            reasons.append(f"production fit (+{quality_points:.2f})")

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
                    "popularity": float(row.get("popularity", 50.0)),
                    "release_decade": int(row.get("release_decade", 2020)),
                    "mood_tags": row.get("mood_tags", "").split("|") if row.get("mood_tags") else [],
                    "lyrical_density": float(row.get("lyrical_density", 0.5)),
                    "production_quality": float(row.get("production_quality", 7.0)),
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
    target_popularity = float(user_prefs.get("target_popularity", 60.0))
    target_decade = int(user_prefs.get("preferred_decade", 2020))
    preferred_mood_tags = user_prefs.get("preferred_mood_tags", [])
    target_lyrical_density = float(user_prefs.get("target_lyrical_density", 0.6))
    target_production_quality = float(user_prefs.get("target_production_quality", 7.5))

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

    # Popularity closeness: up to +2.5
    popularity_closeness = _closeness(song.get("popularity", 50.0), target_popularity, 25.0)
    popularity_points = popularity_closeness * 2.5
    if popularity_points > 0.05:
        total_score += popularity_points
        reasons.append(f"popularity fit (+{popularity_points:.2f})")

    # Release decade affinity: +1.2 exact, +0.4 adjacent
    song_decade = int(song.get("release_decade", 2020))
    decade_points = _adjacent_decade_bonus(song_decade, target_decade)
    if decade_points > 0.0:
        total_score += decade_points
        reasons.append(f"era preference (+{decade_points:.1f})")

    # Detailed mood tags: +0.4 per matching tag, up to +1.6
    song_tags = song.get("mood_tags", [])
    tag_matches = len(set(song_tags).intersection(set(preferred_mood_tags)))
    mood_tag_points = min(tag_matches * 0.4, 1.6)
    if mood_tag_points > 0.05:
        total_score += mood_tag_points
        reasons.append(f"mood-tag match (+{mood_tag_points:.2f})")

    # Lyrical density closeness: up to +1.0
    lyrical_closeness = _closeness(song.get("lyrical_density", 0.5), target_lyrical_density, 0.30)
    lyrical_points = lyrical_closeness * 1.0
    if lyrical_points > 0.05:
        total_score += lyrical_points
        reasons.append(f"lyrical fit (+{lyrical_points:.2f})")

    # Production quality closeness: up to +0.8
    quality_closeness = _closeness(song.get("production_quality", 7.0), target_production_quality, 2.5)
    quality_points = quality_closeness * 0.8
    if quality_points > 0.05:
        total_score += quality_points
        reasons.append(f"production fit (+{quality_points:.2f})")

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


def _strategy_balanced(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """Default strategy: no extra directional bias."""
    return 0.0, ""


def _strategy_genre_first(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """Boost songs that match preferred genre(s)."""
    preferred_genres = user_prefs.get("preferred_genres")
    if preferred_genres is None and user_prefs.get("genre") is not None:
        preferred_genres = [user_prefs["genre"]]
    preferred_genres = preferred_genres or []

    if song["genre"] in preferred_genres:
        return 1.2, "strategy genre-first (+1.20)"
    return 0.0, ""


def _strategy_mood_first(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """Boost songs that match preferred mood(s)."""
    preferred_moods = user_prefs.get("preferred_moods")
    if preferred_moods is None and user_prefs.get("mood") is not None:
        preferred_moods = [user_prefs["mood"]]
    preferred_moods = preferred_moods or []

    if song["mood"] in preferred_moods:
        return 1.2, "strategy mood-first (+1.20)"
    return 0.0, ""


def _strategy_energy_focused(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """Strongly prioritize energy closeness."""
    target_energy = float(user_prefs.get("energy", 0.6))
    energy_closeness = _closeness(song["energy"], target_energy, float(user_prefs.get("energy_range", 0.35)))
    bonus = energy_closeness * 1.6
    if bonus > 0.05:
        return bonus, f"strategy energy-focused (+{bonus:.2f})"
    return 0.0, ""


RANKING_STRATEGIES: Dict[str, Callable[[Dict, Dict], Tuple[float, str]]] = {
    "balanced": _strategy_balanced,
    "genre_first": _strategy_genre_first,
    "mood_first": _strategy_mood_first,
    "energy_focused": _strategy_energy_focused,
}


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return the top-k with explanations."""
    strategy_fn = RANKING_STRATEGIES.get(mode, _strategy_balanced)
    artist_penalty = float(user_prefs.get("artist_diversity_penalty", 1.1))
    genre_penalty = float(user_prefs.get("genre_diversity_penalty", 0.35))
    apply_genre_penalty = bool(user_prefs.get("enable_genre_diversity_penalty", True))

    scored: List[Tuple[Dict, float, List[str], str, str]] = []
    for song in songs:
        if not _passes_guardrails(user_prefs, song):
            continue

        score, reasons = _score_song_functional(song, user_prefs)
        strategy_bonus, strategy_reason = strategy_fn(song, user_prefs)
        score += strategy_bonus
        if strategy_reason:
            reasons.append(strategy_reason)
        scored.append((song, score, reasons, song["artist"], song["genre"]))

    # First sort by base score, then rerank with diversity penalties.
    scored.sort(key=lambda x: x[1], reverse=True)

    selected: List[Tuple[Dict, float, str]] = []
    remaining = scored.copy()
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}

    while remaining and len(selected) < k:
        best_idx = 0
        best_adjusted = float("-inf")
        best_penalties = (0.0, 0.0)

        for idx, (song, base_score, _reasons, artist, genre) in enumerate(remaining):
            artist_dup_count = artist_counts.get(artist, 0)
            genre_dup_count = genre_counts.get(genre, 0)

            artist_div_penalty = artist_dup_count * artist_penalty
            genre_div_penalty = genre_dup_count * genre_penalty if apply_genre_penalty else 0.0
            adjusted_score = base_score - artist_div_penalty - genre_div_penalty

            if adjusted_score > best_adjusted:
                best_adjusted = adjusted_score
                best_idx = idx
                best_penalties = (artist_div_penalty, genre_div_penalty)

        song, base_score, reasons, artist, genre = remaining.pop(best_idx)
        artist_div_penalty, genre_div_penalty = best_penalties

        final_reasons = reasons.copy()
        if artist_div_penalty > 0:
            final_reasons.append(f"artist diversity penalty (-{artist_div_penalty:.2f})")
        if genre_div_penalty > 0:
            final_reasons.append(f"genre diversity penalty (-{genre_div_penalty:.2f})")

        selected.append((song, best_adjusted, ", ".join(final_reasons)))
        artist_counts[artist] = artist_counts.get(artist, 0) + 1
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    return selected
