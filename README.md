# 🎵 Music Recommender Simulation

## Project Summary
This project builds a small music recommender and explains how it works.
The system compares song features with a user profile and ranks songs by score.
I extended the starter version with advanced features, switchable ranking strategies, and diversity logic.
The goal is classroom learning, not production-grade personalization.

---

## How The System Works
This recommender is a content-based ranking system.
It scores each song against a user profile and returns the highest-ranked results.

### Song Features Used
- Base features: genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- Advanced features: popularity, release_decade, mood_tags, lyrical_density, production_quality

### User Preferences Used
- Base preferences: preferred genre, preferred mood, target energy
- Optional targets: tempo, valence, danceability, acousticness
- Advanced targets: target popularity, preferred decade, preferred mood tags, target lyrical density, target production quality
- Ranking mode: balanced, genre_first, mood_first, energy_focused
- Diversity controls: artist diversity penalty and optional genre diversity penalty

### Scoring Overview
1. Score categorical matches (genre and mood).
2. Score numeric closeness for energy, tempo, valence, danceability, and acousticness.
3. Add advanced feature scores:
   - popularity closeness
   - decade preference (exact/adjacent)
   - mood tag overlap
   - lyrical density closeness
   - production quality closeness
4. Apply mode-specific strategy bonus.
5. Build top-k results with diversity penalties to reduce repeated artists/genres.

### Strategy Modes
- `balanced`: no extra directional bonus
- `genre_first`: boosts songs in preferred genre
- `mood_first`: boosts songs in preferred mood
- `energy_focused`: boosts energy closeness more strongly

### Diversity Rule
When a song is considered for top-k selection, its adjusted score is:

adjusted_score = base_score - (artist_repeat_count × artist_penalty) - (genre_repeat_count × genre_penalty)

This makes repeated artists (and optionally repeated genres) less likely to dominate the final list.

---

## Getting Started

### Setup
1. Create a virtual environment (optional):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

```bash
pytest -q
```

---

## Experiments You Tried
I tested multiple profile types and compared ranking behavior:

- Everyday profiles: High-Energy Pop, Chill Lofi, Warm Up Workout
- Edge-case profiles: Sad Pop Music, High Energy + Sad, Impossible Preference
- Strategy comparison: balanced vs genre_first vs mood_first vs energy_focused
- Logic experiment: shifted weight emphasis from genre-heavy toward energy-heavy

### What Happened
- Strategy modes produced clearly different top-3 results.
- Energy-focused ranking consistently promoted high-energy songs.
- Mood-first ranking improved emotional alignment in several cases.
- Diversity penalties reduced repeated-artist dominance in top recommendations.

---

## Limitations and Risks
- The dataset is small (18 songs), so repetition is unavoidable.
- Some genres and moods are underrepresented.
- The system does not use lyrics, language, or cultural context.
- Strong weights can create filter-bubble behavior (for example, energy-heavy outputs).
- Scores can look confident even when user preferences are contradictory.

---

## Reflection
My biggest learning was that simple scoring choices can strongly change outputs.
A small weight or strategy change can move a song from rank 1 to rank 3.
That made it clear that recommender behavior is not only about data, but also about design decisions.

Using AI tools helped me move faster when brainstorming profiles, writing comparison logic, and debugging quickly.
I still had to verify every important suggestion by running tests and checking real terminal output.
I was surprised that even a simple point-based system can feel like a real recommender when results mostly match user intent.
If I extend this project, I would add a larger catalog, better calibration of scores, and stronger diversity controls.
