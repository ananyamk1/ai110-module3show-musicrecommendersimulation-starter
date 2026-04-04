"""
WHY GENRE DOMINATES: The Scoring Architecture Problem
======================================================

QUESTION: Why does "Sad Pop Music" recommend "Sunrise City" (happy) instead of 
          "Neon Sidewalk Cipher" (gritty, closer to sad)?

ANSWER: The genre weight creates an "attractor" that overpowers mood/valence signals.

┌─ CURRENT SCORING LOGIC ─────────────────────────────────────────┐
│                                                                    │
│  # Genre match: +2.0                                             │
│  if song["genre"] in preferred_genres:                           │
│      total_score += 2.0  ← FIXED BONUS                           │
│                                                                    │
│  # Mood match: +1.0                                              │
│  if song["mood"] in preferred_moods:                             │
│      total_score += 1.0  ← ONLY IF EXACT MATCH                   │
│  # If mood doesn't match → NO POINTS, NO PENALTY                 │
│                                                                    │
│  # Valence (emotional tone): +1.0 MAX                            │
│  valence_closeness = _closeness(...)                             │
│  valence_points = valence_closeness * 1.0  ← CAN'T EXCEED +1.0   │
│                                                                    │
└────────────────────────────────────────────────────────────────┘

PRACTICAL IMPACT ON "SAD POP" SEARCH:
─────────────────────────────────────

Pop songs in dataset: [Sunrise City (happy), Generic_Pop_A (happy), ...]
Hip-hop songs:       [Neon Sidewalk Cipher (gritty), ...]

Algorithm logic:
  1. Filter all songs
  2. Score EVERY pop song with +2.0 bonus
  3. Score generic features on top
  4. Result: Highest-scoring pop song wins, regardless of mood!
  
Pop songs all get +2.0 start → They compete among themselves
Hip-hop songs get +0.0 from genre → They start behind
Even if hip-hop song has better mood match, the genre penalty is insurmountable

MATHEMATICAL PROOF:
──────────────────
Sunrise City: 2.0 (genre) + ... = 6.08
Cipher:       0.0 (genre) + 1.89 (energy) + 1.08 (tempo) + ... = 5.67

For Cipher to win over Sunrise City, it would need:
  (5.67 + 2.0) = 7.67 > 6.08
  
But there's no +2.0 available to songs outside the preferred genre!


THE REAL PROBLEM:
─────────────────
When a user says "sad pop", they might mean:
  A) Find me pop music that HAPPENS to be sad
  B) Find me sad music that HAPPENS to be pop

Current system assumes (A) and will ALWAYS recommend pop, even if
ALL pop songs are happy, over sad music in other genres.

This is why "Sad Pop Music" feels off - we're forcing the genre first,
then finding emotions within that constraint.
"""
