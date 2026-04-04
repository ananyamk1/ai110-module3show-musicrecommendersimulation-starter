# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

One weakness I observed is an energy-driven filter bubble: because energy alignment is weighted strongly, songs with similar energy repeatedly rise to the top even when mood or genre intent is less aligned. This can bias recommendations toward users whose preferences are near the dataset's mid-to-high energy range, while users asking for low-energy but emotionally specific music may get less precise results. The default guardrails are broad enough to let many candidates pass, so the energy score often becomes the dominant ranking signal instead of a balanced one. In experiments like "Sad Pop Music," this made results feel directionally better on energy but sometimes less faithful to the user's explicit genre request.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested the recommender with both everyday profiles (like High-Energy Pop, Chill Lofi, and Warm Up Workout) and adversarial profiles (like "Sad Pop Music," "High Energy + Sad," and "Impossible Preference"). I looked at the top 5 songs for each profile and checked whether the results felt musically reasonable for a real listener, not just mathematically high-scoring. One surprise was that songs like "Gym Hero" and "Sunrise City" kept appearing for users who asked for "Happy Pop," because those tracks score well on energy and danceability and get an extra boost from genre alignment. Another surprise was that contradictory profiles (for example, sad mood + very high energy) still produced stable recommendations, but the system sometimes prioritized energy fit over emotional tone. This evaluation helped me see that the outputs are often sensible, but they can still drift toward energetic tracks when user preferences conflict.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
