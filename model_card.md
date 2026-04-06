# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

  
Example: **VibeFinder 1.0**  

I named my model VibeCompass 1.0. I chose that name because my recommender tries to guide a listener toward songs that match their current taste direction, not just their genre label. The name also fits the way I built the project: I kept adjusting the scoring logic until it pointed more reliably toward the kind of music I wanted it to surface.

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

I designed this recommender to generate a short ranked list of songs from a small local catalog. It is meant to suggest songs that fit a user profile based on genre, mood, energy, and more detailed preferences like popularity or decade. I assume the user is giving me a simple taste profile rather than a full listening history, so I treat the input like a snapshot of what they want right now.

This is for classroom exploration, not real-world personalization at scale. I used it to study how ranking systems behave, how weights change the output, and how quickly a recommender can become biased if one feature dominates too much.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

I compare each song against the user's preferences and give it points for how well it matches. I started with the starter features like genre, mood, energy, tempo, valence, danceability, and acousticness, then I expanded the system with popularity, release decade, mood tags, lyrical density, and production quality. That made the recommender feel much less like a one-dimensional filter and more like a ranking model with several layers of meaning.

My scoring logic is a mix of direct matches and closeness scores. A genre or mood match gives a simple point boost, while numeric features are scored by how close the song is to the user's target. I also added strategy modes such as balanced, genre_first, mood_first, and energy_focused so I could intentionally change the recommendation style instead of hard-coding one behavior forever. On top of that, I added diversity penalties so the same artist or genre does not keep taking over the top results.

The biggest change from the starter logic is that I made the system explainable and configurable. I return reason strings for each song, I use multiple feature types, and I let the ranking behavior shift depending on the mode. That gave me a better way to test the recommender because I could see exactly why a song scored well.

I also documented the flow in a Mermaid diagram and made the CLI output a readable ASCII table so the process is easy to follow from input to ranked output. That helped me connect the math in the code with the way I present the results in terminal.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

My catalog currently has 18 songs. The starter version had a much smaller and simpler dataset, so I expanded the CSV and added more song metadata to support richer scoring. The catalog now includes pop, lofi, rock, ambient, jazz, synthwave, hip-hop, r&b, country, afrobeats, classical, reggaeton, house, and blues, along with moods like happy, chill, intense, moody, nostalgic, euphoric, and melancholic.

I added new attributes like popularity, release decade, mood tags, lyrical density, and production quality. I did that because I wanted the model to reflect more than just genre and energy. Even with those improvements, the dataset is still small, so many real tastes are missing and some genres or moods only appear once or twice. That means the recommender can still be useful for experimentation, but it cannot represent the full diversity of actual music listening.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

My system works well for users whose preferences are fairly clear. For example, High-Energy Pop, Chill Lofi, Deep Intense Rock, and Warm Up Workout all produced results that made sense to me because the score logic matched the kind of song the user seemed to want. I also think it works well when the user profile is internally consistent, such as high energy plus upbeat or low energy plus calm.

One pattern I captured correctly is that numeric closeness matters. When a song is close to the user's target energy, tempo, or valence, it usually rises in the list even if it does not have a perfect genre match. I also saw that the strategy modes change the flavor of the ranking in a controlled way, which made it easier for me to compare outputs and reason about behavior.

Some results matched my intuition very well. For example, Sunrise City felt like a good top result for a happy pop listener, and Midnight Coding felt reasonable for a chill lofi listener. Those cases reassured me that the recommender can feel believable when the scoring logic and the user profile point in the same direction.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

My biggest limitation is that I still only have a small catalog, so the model cannot represent the full range of real listening tastes. I also do not use lyrics, language, artist reputation over time, or session history, so the recommender is making decisions from a limited surface-level snapshot. That means it can miss subtle intent that a real music app might understand better.

I saw a real bias risk when one feature weight became too strong. For example, if energy is too heavily weighted, the recommender can keep promoting energetic songs even for users who asked for something calmer or more emotionally specific. That can create a filter bubble where a narrow style shows up too often. I also think the dataset itself is biased by coverage, because the catalog is not balanced evenly across all genres and moods.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested multiple everyday profiles and edge-case profiles. My everyday profiles included High-Energy Pop, Chill Lofi, Deep Intense Rock, Focus Flow, and Warm Up Workout. My edge cases included Sad Pop Music, High Energy + Sad, Non-Danceable House, 200 BPM Acoustic Jazz, and Impossible Preference. I used those on purpose because I wanted to see how the recommender handled normal tastes versus conflicting tastes.

I looked at the top 5 results for each profile and checked whether the songs felt like a believable match. I also compared recommendations across strategy modes so I could see how the same profile changed when I switched from balanced to genre_first or energy_focused. One thing that surprised me was how strongly the same song could move up or down when I changed a single weight, which showed me how sensitive ranking systems are to scoring assumptions.

I also ran a logic experiment where I changed the balance between genre and energy. That experiment helped me see that the recommender is not just outputting songs; it is encoding a decision about what matters most. I used tests and terminal runs to make sure the model still behaved correctly after each change.

I also compared the outputs from my different strategy modes and used the top-k diversity reranking step to see whether the final list felt less repetitive. That gave me a clearer view of the difference between ranking quality and list quality.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

If I keep developing this model, I would first expand the dataset so the recommender has more variety to learn from. I would add more songs across underrepresented genres and moods, because the current catalog is still too small to support broad recommendations. I would also keep improving the diversity penalty so the final top-k results are less repetitive when the same artist or genre keeps appearing.

I would also like to improve the explanation system. Right now, the reason strings are helpful, but I think I could make the output even clearer by summarizing which features mattered most for the final rank. Another future improvement would be to make the ranking mode more user-configurable, so someone could choose strict genre matching, mood-first matching, or an exploratory mode depending on what kind of recommendation session they want.

## Challenge Implementation Summary

### Challenge 1: Add Advanced Song Features with Agent Mode
I implemented this challenge by expanding `data/songs.csv` and updating parsing plus scoring logic in `src/recommender.py`. I added at least five advanced attributes: popularity (0-100), release decade, mood tags, lyrical density, and production quality. I then introduced math-based scoring rules for each one, including closeness scoring for numeric fields and overlap scoring for mood tags. This made the ranking less dependent on only genre and mood and allowed era, detail, and style signals to influence outcomes in a measurable way.

### Challenge 2: Create Multiple Scoring Modes
I implemented multiple ranking strategies in `src/recommender.py` using a simple strategy-style structure so modes stay modular and easy to extend. The modes I added were balanced, genre_first, mood_first, and energy_focused. I exposed mode switching in `src/main.py`, which allowed me to compare how the same profile produces different results depending on recommendation philosophy. This made experimentation and debugging much more structured than a single fixed scorer.

### Challenge 3: Diversity and Fairness Logic
I implemented a diversity penalty during top-k selection so repeated artists and genres are less likely to dominate the final list. The reranking step computes an adjusted score by subtracting repeat penalties when an artist or genre already appears in selected recommendations. In plain terms, the rule follows adjusted_score = base_score - artist_repeat_penalty - genre_repeat_penalty. This gave me better list variety while preserving relevance.

### Challenge 4: Visual Summary Table
I improved terminal readability by adding an ASCII summary table in `src/main.py` that shows title, artist, score, and reason text. I also wrapped long reason strings so explanations remain readable rather than collapsing into one long line. This made the recommender much easier to validate because I could inspect scores and explanations in one clean view.

### Challenge 5: System Evaluation and Stress Testing
I implemented an explicit evaluation pass with normal, adversarial, and contradictory user profiles to test robustness. I used scenarios like Sad Pop Music, High Energy + Sad, and Impossible Preference to verify the model still returns the nearest compromise rather than failing. I also validated behavior with `pytest -q` and repeated CLI runs to confirm that feature additions, strategy modes, and diversity reranking continued to work together correctly.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps

My biggest learning moment was realizing that recommender systems are really about design choices, not just code. A small scoring change can move a song from first place to third place, and that showed me how sensitive ranking systems are to weight decisions. I started thinking of the recommender less like a toy and more like a policy engine that decides what counts as relevant.

The Mermaid flowchart and ASCII table helped me turn that idea into something I could explain visually and in the terminal. I found it easier to reason about the system when I could see both the data flow and the final reasons for each recommendation.

Using AI tools helped me move faster when I was brainstorming profiles, testing edge cases, and drafting explanations. I still had to double-check the AI output by running the code and reading the actual recommendation results, because the AI could suggest ideas that sounded right but did not always match the behavior I wanted. That was especially important when I was debugging scoring and comparing outputs across profiles.

What surprised me most was how a simple point-based algorithm can still feel like a real recommendation system. Even though the logic is basic, the outputs feel personal when the top results line up with the user's mood and energy. At the same time, that is also where the risk lives: if one score is too dominant, the system can create a hidden bias without looking obviously wrong.

If I extended this project, I would add more songs, stronger diversity controls, and user-facing settings that let someone choose between strict genre matching and mood-first matching. I would also want to improve the explanations so the user can understand not only which song won, but also why the system preferred that song over the others.


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
