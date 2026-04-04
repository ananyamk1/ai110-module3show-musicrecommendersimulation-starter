# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This recommender is a content-based ranking system. It compares each song in `data/songs.csv` to a user taste profile, computes a weighted score, and returns the highest-ranked songs.

### Finalized Algorithm Recipe

1. Input data
- Song features: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
- User profile: `preferred_genres`, `preferred_moods`, target numeric values, and feature weights

2. Optional guardrail filter
- Remove obvious mismatches before scoring, such as:
   - danceability below the user's beat floor
   - tempo outside the user's tolerance range
   - energy far from the user's target

3. Score numeric features by closeness
- For each numeric feature, reward closeness to the target (not simply high or low values):

$$
	ext{closeness} = 1 - \min\left(\frac{|x - t|}{r}, 1\right)
$$

- where $x$ is the song value, $t$ is the user target, and $r$ is the allowed range scale.
- Apply this to `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

4. Score categorical matches
- Genre score:
   - 1.0 if song genre is in `preferred_genres`
   - 0 otherwise
- Mood score:
   - 1.0 if song mood is in `preferred_moods`
   - 0 otherwise
- Mood can be weighted slightly higher than genre for vibe-focused matching.

5. Add a "crescendo vibe" proxy
- Because the dataset has no time-series audio progression, approximate buildup/peak feel as a weighted blend of:
   - higher `danceability`
   - moderate/high `energy`
   - lower `acousticness`
- This provides a boost for songs likely to feel like they build and release.

6. Weighted final score

$$
S = w_g s_g + w_m s_m + w_e s_e + w_t s_t + w_v s_v + w_d s_d + w_a s_a + w_c s_c
$$

- where:
   - $s_g, s_m$ are genre and mood match scores
   - $s_e, s_t, s_v, s_d, s_a$ are numeric closeness scores
   - $s_c$ is the crescendo proxy
   - weights are user-configurable and normalized

7. Ranking rule
- Score every remaining song
- Sort scores descending
- Return Top $K$ recommendations (for example Top 3 or Top 5)

8. Tie-break and variety
- If scores tie, prefer:
   - mood match first
   - then closest tempo match
   - then artist variety to avoid repeated artists in Top $K$

### Potential Bias Note

This system might over-prioritize the features with the largest weights (for example genre or mood), which can hide strong cross-genre songs that still match the user's overall vibe. It may also reflect the limited genre and mood coverage in the small CSV catalog.


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Default Pop/Happy Profile
Running the recommender with the default user profile (`genre: pop, mood: happy, energy: 0.8`) produces:

```
Loaded songs: 18

User Profile: genre=pop, mood=happy, energy=0.8
================================================================================

🎵 TOP 5 RECOMMENDATIONS (Score out of 10.0):

1. SUNRISE CITY
   Artist: Neon Echo
   Score: 7.76/10.0
   Why: genre match (+2.0), mood match (+1.0), energy alignment (+1.89), 
        tempo match (+0.66), valence fit (+0.31), danceability fit (+1.11), 
        acousticness fit (+0.36), crescendo vibe (+0.43)

2. ROOFTOP LIGHTS
   Artist: Indigo Parade
   Score: 5.74/10.0
   Why: mood match (+1.0), energy alignment (+1.77), tempo match (+0.48), 
        valence fit (+0.40), danceability fit (+0.99), acousticness fit (+0.70), 
        crescendo vibe (+0.41)

3. GYM HERO
   Artist: Max Pulse
   Score: 5.31/10.0
   Why: genre match (+2.0), energy alignment (+1.26), tempo match (+0.24), 
        valence fit (+0.51), danceability fit (+0.73), acousticness fit (+0.10), 
        crescendo vibe (+0.47)

4. NEON SIDEWALK CIPHER
   Artist: Nova Thread
   Score: 5.01/10.0
   Why: energy alignment (+1.31), tempo match (+1.08), valence fit (+0.49), 
        danceability fit (+1.33), acousticness fit (+0.42), crescendo vibe (+0.39)

5. PULSE OF LAGOS
   Artist: Kemi Ray
   Score: 4.57/10.0
   Why: energy alignment (+1.66), tempo match (+1.08), valence fit (+0.37), 
        danceability fit (+0.64), acousticness fit (+0.36), crescendo vibe (+0.46)
```

**Analysis**: The top recommendation (Sunrise City) earns the highest score because it matches on **all three primary criteria**: genre (pop), mood (happy), AND energy alignment (0.82 ≈ 0.8 target). The second-place song (Rooftop Lights) matches mood and energy well but is indie pop (not the exact genre match), illustrating how the scoring balances categorical matches with numeric closeness. GYM HERO has high energy but "intense" mood, showing how mood preference creates a trade-off.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

