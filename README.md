# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

I built a music recommender that starts with a small CSV catalog and ranks songs based on how closely they match a user profile. I expanded the starter project into a more complete simulation by adding richer song metadata, multiple ranking strategies, and diversity reranking so the results are easier to explain and less repetitive. I used the project to study how recommendation systems turn simple rules into user-facing predictions, and I kept checking whether the results still felt believable as I changed the scoring logic. My version is intentionally small, but I tried to make it behave like a real recommender in the ways that matter for learning. I wanted to see how data shape, scoring weights, and reranking rules affect the final list, because those are the same kinds of tradeoffs that real recommendation systems make.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

I compare each song in `data/songs.csv` with a user profile and assign points for matches. I started with the obvious features like genre, mood, and energy, then I added more detailed features so the system could make a more nuanced choice. In my final version, I also included popularity, release decade, mood tags, lyrical density, and production quality so the scoring logic could reflect more than just a basic vibe check. My `UserProfile` stores both the user's main taste and optional deeper preferences. For example, I use a favorite genre and favorite mood, but I also allow targets for tempo, valence, danceability, acousticness, popularity, preferred decade, preferred mood tags, lyrical density, and production quality. I did this because I wanted the recommender to support both simple listeners and more specific listeners who care about details like "nostalgic" or "euphoric" tracks. The scoring process is layered. First I score categorical matches like genre and mood. Then I score numeric closeness by comparing each song value to the user's target using a bounded distance formula, so being close to the target matters more than just being large or small. After that, I add the advanced feature points, apply the current ranking strategy, and finally rerank the candidates with diversity penalties so one artist or one genre does not dominate the top list. I choose songs by scoring every track, sorting the full list, and then selecting the top-k results. In `main.py`, I also show a table of the recommendations with the reasons for each score, because I wanted the output to be easy to read and easy to debug. I also added a Mermaid flowchart in this section to show the path from user input to final ranking.

If I draw it as a simple flow, my design is:

User Preferences → Load Songs from CSV → Score Each Song → Apply Strategy Mode → Sort → Apply Diversity Penalty → Return Top K

The final algorithm recipe I used is:

1. Score genre and mood matches.
2. Score closeness for numeric features.
3. Add advanced feature scores.
4. Apply a ranking mode such as balanced, genre_first, mood_first, or energy_focused.
5. Rerank with artist and genre diversity penalties.
6. Return the top-k songs with explanations.

I expect the biggest bias risk to come from whichever feature gets the strongest weight. In my experiments, strong energy weighting made energetic songs rise across many profiles, even when the user asked for something calmer or more emotionally specific. That helped me see that recommendation logic can accidentally create a filter bubble if I do not balance the score carefully.

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

When I validated the project, I used `python -m src.main` to check the CLI output and `pytest -q` to make sure the core logic still passed tests after each major change. I also added `tests/conftest.py` so plain `pytest -q` works without needing a manual `PYTHONPATH` workaround.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

I ran the project like a sequence of controlled experiments. I started with the default High-Energy Pop profile so I had a baseline for what a "reasonable" recommendation looked like. Then I tested distinct profiles like Chill Lofi, Deep Intense Rock, Focus Flow, and Warm Up Workout to see whether the ranking shifted in a way that matched the user intent. I also tested edge-case profiles such as Sad Pop Music, High Energy + Sad, Non-Danceable House, 200 BPM Acoustic Jazz, and Impossible Preference. Those were important because they forced me to see what happens when a user asks for combinations that are hard to satisfy. I learned that my system does not crash or break in those cases; instead, it returns the closest compromise, which is exactly what I wanted to verify. I used a logic experiment to understand sensitivity. I shifted weight emphasis away from genre and toward energy and observed that the top-ranked songs changed noticeably. That experiment taught me that my recommender is not only describing songs; it is encoding a policy about what should matter most. I also built and tested multiple ranking strategies: balanced, genre_first, mood_first, and energy_focused. That let me compare how one user profile could produce different top results depending on the scoring philosophy. Finally, I added diversity penalties and checked whether the top-k list became less repetitive, especially when the same artist would otherwise appear too often.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

My recommender still has a small catalog, so I can only recommend from the songs that exist in the CSV. That means the system has very limited coverage and can only approximate a broader music taste. I also do not model lyrics, artist context, cultural meaning, or session history, so the recommendations are based on surface-level features. The biggest risk I saw was feature dominance. If one score component becomes too strong, the model can repeatedly favor songs with that feature even when the user asked for something different. For example, if energy is weighted too heavily, energetic songs can keep rising to the top across unrelated profiles. That is a useful behavior when energy is the real goal, but it becomes a bias problem if the user intended a calmer or more emotional list.
I also think the dataset itself creates bias. Because the catalog is small and some genres are represented more than others, the system has a natural tendency to favor the denser parts of the catalog. That means my recommender can look more confident than it really is.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

My biggest learning moment was realizing that recommendation systems are really about design choices, not just code. A small scoring change can move a song from first place to third place, and that showed me how sensitive ranking systems are to weight decisions. I started thinking of the recommender less like a toy and more like a policy engine that decides what "counts" as relevant. Using AI tools helped me move faster when I was brainstorming profiles, testing edge cases, and drafting explanations. I still had to double-check the AI output by running the code and reading the actual recommendation results, because the AI could suggest ideas that sounded right but did not always match the behavior I wanted. That was especially important when I was debugging scoring and comparing outputs across profiles. What surprised me most was how a simple point-based algorithm can still feel like a real recommendation system. Even though the logic is basic, the outputs feel personal when the top results line up with the user's mood and energy. At the same time, that is also where the risk lives: if one score is too dominant, the system can create a hidden bias without looking obviously wrong. Isf I extended this project, I would add more songs, stronger diversity controls, and user-facing settings that let someone choose between strict genre matching and mood-first matching. I would also want to improve the explanations so the user can understand not only which song won, but also why the system preferred that song over the others.


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
```

Human judgment still matters any time the recommender has to make a tradeoff that is not purely mathematical. In my system, the score can tell me which songs are closest to a profile, but it cannot decide whether a result actually feels appropriate, fair, or useful for the person asking. That judgment matters most when features conflict, when the catalog is sparse, or when one signal starts dominating the rest. I learned that a recommender can produce a ranking, but a person still has to decide whether that ranking is the right answer for the situation.