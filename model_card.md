# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name
VibeCompass 1.0.

## 2. Intended Use
This model suggests 3 to 5 songs from a small catalog.
It is designed for classroom exploration of recommender logic.
It is useful for testing how profile choices and scoring rules affect ranking.
It is not designed for real-user personalization at scale.

## 3. How It Works (Short Explanation)
The model compares each song to a user profile.
It gives points for genre and mood matches.
It gives more points when numeric features are close to user targets.
It also scores advanced attributes like popularity, decade preference, mood tags, lyrical density, and production quality.
After scoring, it applies a selected strategy mode and then reranks with diversity penalties.

## 4. Data
The dataset has 18 songs in data/songs.csv.
Each row includes genre, mood, energy, tempo, valence, danceability, and acousticness.
I added advanced fields: popularity, release_decade, mood_tags, lyrical_density, and production_quality.
The catalog is still small, so many tastes are underrepresented.

## 5. Strengths
The model is easy to understand and debug.
Different user profiles produce visibly different outputs.
Strategy modes make behavior explainable (genre-first, mood-first, energy-focused).
The diversity penalty helps reduce repeated artists in top results.

## 6. Limitations and Bias
The small dataset creates repetition and limited coverage.
High-weight features can dominate and create filter-bubble behavior.
For example, energy-focused scoring can over-promote energetic songs across different users.
The model also lacks lyrical meaning, language, and cultural context.

## 7. Evaluation
I tested everyday profiles and edge-case profiles.
Examples include High-Energy Pop, Chill Lofi, Sad Pop Music, High Energy + Sad, and Impossible Preference.
I compared top results across strategy modes and checked whether changes made musical sense.
I also ran unit tests and adversarial evaluation scripts to confirm the system runs correctly.

## 8. Future Work
1. Expand the dataset with more songs, genres, and moods.
2. Improve diversity controls so top-k results are less repetitive.
3. Add user-facing controls for strict genre mode versus mood-first mode.

## 9. Personal Reflection
My biggest learning was that a small scoring change can strongly shift recommendations.
AI tools helped me move faster in brainstorming and implementation, but I still had to verify outputs with tests and terminal runs.
I was surprised that a simple scoring system can feel realistic when profile intent and ranking align.
If I continue this project, I would focus on richer data, better fairness checks, and clearer score explanations for users.
