# Model Card: VibeCompass 1.0

## Model Name
VibeCompass 1.0.
It recommends songs based on vibe and listening goals.

## Goal / Task
This recommender suggests songs a user might like.
It tries to match genre, mood, and music features like energy and tempo.
It returns the top ranked songs, not one perfect answer.

## Data Used
The dataset has 18 songs.
Each song includes genre, mood, energy, tempo, valence, danceability, and acousticness.
The catalog is small, so it cannot represent all music tastes.
Some genres and moods have only one or two songs.

## Algorithm Summary
Each song gets points for how well it matches user preferences.
Genre and mood can add bonus points.
Feature similarity adds more points when values are close to the user target.
Right now, energy has strong influence, so energetic songs can rank high often.
Then the system sorts songs by score and returns the top results.

## Observed Behavior / Biases
I saw an energy-centered pattern in many tests.
Songs with similar energy often beat songs with better emotional fit.
For example, songs like "Gym Hero" can appear often for "Happy Pop" style users because they are high energy and highly danceable.
The small dataset also creates repetition, so the same songs show up across different profiles.

## Evaluation Process
I tested everyday profiles like High-Energy Pop, Chill Lofi, and Warm Up Workout.
I also tested edge-case profiles like Sad Pop Music, High Energy + Sad, and Impossible Preference.
I compared top 5 outputs across profiles to see what changed and why.
I also ran a logic experiment by lowering genre weight and increasing energy weight.
That experiment showed clearer emotional matches in some cases, but weaker genre loyalty in others.

## Intended Use and Non-Intended Use
Intended use: classroom learning and basic recommender experiments.
It is good for understanding how weights and features affect ranking.
Non-intended use: real-world music personalization at scale.
It should not be used for high-stakes decisions or claims about user identity, mental health, or culture.

## Ideas for Improvement
1. Increase dataset size and balance genres and moods.
2. Add a small penalty for strong mood mismatch so happy songs do not dominate sad requests.
3. Add a diversity rule so top 5 results are less repetitive.

## Personal Reflection
My biggest learning moment was seeing how one weight change could totally change the top recommendation. I learned that recommender behavior is not just about data, it is also about design choices in scoring.

AI tools helped me move faster when generating test profiles, comparing outputs, and writing clear explanations. I still had to double-check AI suggestions by running the code and reading the actual ranking results in the terminal.

I was surprised that a simple point-based algorithm could still feel like a real recommendation system. Even basic rules made results that felt intuitive most of the time, which is both useful and a little risky when hidden biases are present.

If I extend this project, I would add a larger dataset, better diversity in the top 5, and adaptive weights based on user intent. I would also add clearer user controls so people can choose whether they want strict genre matching or mood-first matching.
