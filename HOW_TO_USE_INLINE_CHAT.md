"""
STEP-BY-STEP: Using Inline Chat to Understand the "Off" Result
═══════════════════════════════════════════════════════════════

THE "OFF" RESULT:
─────────────────
Profile: "Sad Pop Music" 
  → Wants: pop + sad mood + low valence
  → Gets: Sunrise City (pop + HAPPY + high valence)
  → Feels: Like the system misunderstood the sad preference


STEP 1: Open the recommender scoring code
───────────────────────────────────────────

In VS Code:
  1. Open src/recommender.py
  2. Go to lines 214-232 (the _score_song_functional def)
  3. Find this section:
  
      # Genre match: +2.0
      if song["genre"] in preferred_genres:
          genre_points = 2.0
          total_score += genre_points
          reasons.append(f"genre match (+{genre_points:.1f})")

      # Mood match: +1.0
      if song["mood"] in preferred_moods:
          mood_points = 1.0
          total_score += mood_points
          reasons.append(f"mood match (+{mood_points:.1f})")


STEP 2: Select and Highlight This Code Block
───────────────────────────────────────────────

Highlight BOTH the genre and mood matching sections together.


STEP 3: Open Inline Chat
─────────────────────────

Mac:  ⌘ + I  (or keyboard shortcut)
Or:   Click the Copilot chat icon in the gutter


STEP 4: Paste This Question
────────────────────────────

"I'm debugging a recommendation system. When a user searches for 'sad pop',
they get 'Sunrise City' (happy pop with valence=0.84) instead of other 
sad music.

Looking at my scoring code:
- Genre match gives +2.0 IF genre matches
- Mood match gives +1.0 IF mood matches  
- There's NO penalty if mood is opposite

Why does a happy pop song rank higher than sad non-pop songs when the user
explicitly wants 'sad'? Is the genre weight too high relative to mood weight?"


STEP 5: Analyze Copilot's Response
───────────────────────────────────

Copilot will likely explain:

1) Genre (+2.0) = 13% of max score → Very high weight
2) Mood (+1.0) = 7% of max score → Lower weight
3) No mood penalty = asymmetric scoring (bonus for match, nothing for mismatch)
4) All pop songs get +2.0 baseline
5) Non-pop songs can't catch up unless they have huge numeric bonuses

Copilot might suggest:
  - Add a mood mismatch penalty
  - Reduce genre weight from 2.0 to 1.5
  - Increase mood weight from 1.0 to 1.5
  - Add valence-based penalty for emotional contradiction


STEP 6: Follow Up Question
──────────────────────────

"So if I wanted to recommend both happy pop AND sad pop when someone
searches for 'sad pop', what weight change would you suggest?
Should I penalize emotional mismatches, or reweight genre/mood?"


STEP 7: Implement the Fix (Optional)
─────────────────────────────────────

Based on Copilot's suggestion, modify recommender.py:

Option A (Simplest): Reduce genre weight
    genre_points = 1.5  # changed from 2.0

Option B (More nuanced): Add mood penalty
    if song["mood"] not in preferred_moods:
        total_score -= 1.0  # penalty for mood mismatch

Option C (Recommended): Increase valence importance for emotional queries
    if user wants sad (valence < 0.4) and song is very happy (valence > 0.7):
        total_score *= 0.85  # reduce by 15%


STEP 8: Retest with System Evaluation
──────────────────────────────────────

After making changes, run:
    python -m src.system_evaluation

Then compare:
    BEFORE:  "Sad Pop Music" → Sunrise City (6.08) - happy
    AFTER:   "Sad Pop Music" → ??? (should feel more sad)


KEY INSIGHT FROM ANALYSIS:
──────────────────────────

Your scoring has an IMPLICIT HARD GENRE FILTER:
  • Genre match is weighted so heavily
  • That it acts like a constraint
  • All pop songs compete among themselves
  • Non-pop songs almost never win
  • This means "sad pop" ALWAYS gets pop, even if all pop is happy

This might be INTENTIONAL (many music apps do this), but it should be:
  ✓ Documented
  ✓ Configurable  
  ✓ Or balanced better

SUMMARY OF SUPPORTING DOCS CREATED:
───────────────────────────────────

1. INLINE_CHAT_ANALYSIS.md        - What's off and why
2. SCORING_EXPLANATION.md         - How weights interact
3. INLINE_CHAT_PROMPT.md          - Exact question to ask  
4. PROPOSED_FIXES.md              - Options 1-4 with trade-offs
"""
