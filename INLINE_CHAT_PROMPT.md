"""
WHERE TO USE INLINE CHAT IN recommender.py
============================================

PROBLEM: Genre weight (+2.0) dominates mood weight (+1.0)
LOCATION: Lines 218-232 in src/recommender.py

The issue is in _score_song_functional():

    ┌─ SELECT THESE LINES AND ASK COPILOT: ─────────────────┐
    │                                                          │
    │  # Genre match: +2.0                                   │
    │  if song["genre"] in preferred_genres:                 │
    │      genre_points = 2.0                                │
    │      total_score += genre_points                       │
    │      reasons.append(f"genre match (+{genre_points})") │
    │                                                          │
    │  # Mood match: +1.0                                    │
    │  if song["mood"] in preferred_moods:                   │
    │      mood_points = 1.0                                 │
    │      total_score += mood_points                        │
    │      reasons.append(f"mood match (+{mood_points})")   │
    │                                                          │
    └──────────────────────────────────────────────────────┘

THEN ASK COPILOT:
─────────────────

"I'm using this profile to test: 
  {
    genre: 'pop',
    mood: 'sad', 
    energy: 0.7,
    valence: 0.2
  }
  
And I'm getting 'Sunrise City' (happy pop) as top recommendation.

Why does genre weight (+2.0) override mood weight (+1.0) so heavily?
What happens when genre matches but mood is opposite (happy vs sad)?
Should there be a penalty for mood mismatch, not just a bonus for match?"


EXPECTED INSIGHT FROM COPILOT:
──────────────────────────────

Copilot will explain that:

1. Genre match is a FIXED +2.0 bonus (13% of total 15.0 max)
2. Mood match is a FIXED +1.0 bonus (only if exact match, otherwise +0)
3. There's NO penalty for mood mismatch
4. So:
   - Any pop song starts at +2.0 minimum
   - Any non-pop song starts at +0.0
   - Non-pop would need massive numeric bonuses to catch up

5. "Sunrise City" wins because:
   - Pop ✓ → +2.0
   - Happy (not sad) → +0 (no penalty!)
   - High valence (not sad) → +0 (only bonus for closeness, diminishes)

6. "Neon Sidewalk Cipher" can't win because:
   - Hip-hop (not pop) → +0 absolute penalty!
   - Even with better mood/valence closeness, can't overcome genre filter


WHAT THIS REVEALS:
──────────────────

Your recommender has a HARD GENRE FILTER, softly implemented:
- Genre match is so heavily weighted
- That it acts as a constraint
- Mood/valence differences within genre are acceptable
- Mood/valence matches with different genre are unlikely to win

This is actually okay! Some apps do this deliberately.
But it should be documented or configurable.
"""
