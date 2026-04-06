# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name
I named my model VibeCompass 1.0.
I chose this name because my system tries to guide a user toward songs that match their current vibe.

## 2. Intended Use
I built this model for classroom learning and experimentation.
Its job is to suggest a small top-k list (usually 3 to 5 songs) from a small local catalog.
I use it to understand how recommendation behavior changes when I change scoring rules.
I did not build it for production music personalization, safety-critical decisions, or identity-level profiling.

## 3. How It Works (Short Explanation)
I compare each song against a user profile and compute a total score.
I award points for genre and mood alignment.
I then add closeness points for numeric traits (energy, tempo, valence, danceability, acousticness).
I also score advanced attributes I added (popularity, release decade, mood tags, lyrical density, production quality).
After base scoring, I apply a selected strategy mode (balanced, genre_first, mood_first, energy_focused).
Then I rerank top candidates with diversity penalties so repeated artists and genres are less likely to dominate.
Each recommendation includes reason strings so I can explain exactly why it ranked where it did.

## 4. Data
My dataset currently has 18 songs.
The starter version had fewer songs and simpler attributes, so I expanded both volume and depth.
Each song now includes:
- Base fields: genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- Advanced fields: popularity, release_decade, mood_tags, lyrical_density, production_quality

What is still missing:
- lyric meaning and language context
- regional/cultural metadata
- long-tail genre coverage
- user history over time

Because the catalog is small, my model can overfit to a few strong tracks.

## 5. Strengths
I can explain every recommendation because my score is transparent and reason-based.
My strategy modes allow me to intentionally shift behavior rather than hiding logic in one hard-coded formula.
My edge-case evaluation script makes it easy to test contradictory user profiles.
My diversity reranking step improves list variety compared with pure score sorting.
The full pipeline is easy to run from terminal, so iteration speed is high.

## 6. Limitations and Bias
My strongest limitation is data coverage.
With only 18 songs, some user intents are underrepresented, so the model may return compromise matches instead of true matches.
I also observed feature dominance effects: when energy influence is high, energetic songs are repeatedly favored across unrelated profiles.
This can create a filter-bubble pattern where users see similar high-energy tracks even when their mood intent differs.
My fairness logic (diversity penalties) helps variety, but it does not solve representation bias in the underlying catalog.

## 7. Evaluation
I used three layers of evaluation:

1) Baseline profile checks:
I started with a pop/happy profile and confirmed top results felt reasonable and explanations matched score components.

2) Diverse profile testing:
I tested profiles like High-Energy Pop, Chill Lofi, Deep Intense Rock, and Warm Up Workout to ensure the model separates user tastes.

3) Adversarial stress testing:
I ran profiles such as Sad Pop Music, High Energy + Sad, Non-Danceable House, and Impossible Preference.
This exposed where the model prioritizes one feature over another and where contradictory preferences force compromise.

I also compared outputs across strategy modes and verified all code paths with unit tests and CLI runs.

## 8. Future Work
If I keep developing this project, I would prioritize:
1. Expanding and balancing the catalog (more genres, moods, and decades).
2. Improving diversity/fairness reranking with stronger constraints and optional novelty boosts.
3. Adding user-facing controls so people can choose strict genre matching, mood-first matching, or exploratory mode.

I would also add better score calibration so confidence values are easier to interpret.

## 9. Personal Reflection
My biggest learning moment was realizing how sensitive ranking is to small scoring changes.
I used AI tools to move faster in brainstorming, refactoring, and writing, but I had to validate each major suggestion by running tests and checking real outputs.
What surprised me is that even simple additive scoring can feel like a personalized recommender when the feature choices and explanations are coherent.
At the same time, this project taught me that "feels right" is not enough; I need systematic evaluation for bias, edge cases, and diversity.
If I continue, I will focus on stronger data quality, fairer ranking behavior, and clearer control over recommendation intent.
