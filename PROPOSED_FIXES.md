"""
POTENTIAL FIXES: Balancing Genre vs. Mood Weight
================================================

CURRENT BEHAVIOR (Feels "Off"):
User: "sad pop"
System: Returns Sunrise City (happy pop) - highest scoring pop song

WHY: Genre match (+2.0) overrides mood preference

PROPOSED SOLUTIONS:
──────────────────

OPTION 1: Add Mood Penalty (Guardrail)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before (in recommender.py):
    if song["mood"] in preferred_moods:
        mood_points = 1.0
        total_score += mood_points
    # Mood mismatch → NO PENALTY

After:
    if song["mood"] in preferred_moods:
        mood_points = 1.0
        total_score += mood_points
    else:
        # NEW: Penalty for mood mismatch
        mood_penalty = 1.5  # penalize opposite mood
        total_score -= mood_penalty

Impact:
    Sunrise City: 2.0 (genre) + ... - 1.5 (sad mismatch) = 4.58 (lower!)
    Cipher:       0.0 (genre) + ... + 0 (gritty ≠ sad, but closer) = 5.67 (higher!)

Result: Happy pop loses to gritty hip-hop when sad preference exists!


OPTION 2: Reweight Genre to 1.5 (Less Dominant)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before:
    genre_points = 2.0

After:
    genre_points = 1.5  # DOWN from 2.0

Impact:
    Genre match: 1.5 (10% of total max)
    Mood is now competitive!

    Sunrise City: 1.5 (genre) + ... = 5.58
    Cipher:       0.0 (genre) + ... = 5.67  (closer match!)


OPTION 3: Use Valence Penalty (Emotional Mismatch)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Valence is the ACTUAL emotional tone (0=sad, 1=happy)

Before:
    valence_closeness = _closeness(song["valence"], target_valence, 0.35)
    valence_points = valence_closeness * 1.0  # Only bonus

After:
    valence_closeness = _closeness(song["valence"], target_valence, 0.35)
    valence_points = valence_closeness * 1.5  # MORE points for match
    if target_valence < 0.4:  # User wants sad
        if song["valence"] > 0.7:  # Song is very happy
            valence_points *= 0.5  # Reduce score 50%

Impact:
    Sunrise City has valence=0.84 (very happy) vs target=0.2 (very sad)
    → Penalty applied → Score reduced


OPTION 4: Composite Emotional Match (Best?)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Combine mood CATEGORY and valence DIMENSION:

    energy_match = _closeness(song["energy"], target, 0.35)
    valence_match = _closeness(song["valence"], target, 0.35)
    
    emotional_alignment = (energy_match + valence_match) / 2.0
    emotional_points = emotional_alignment * 1.5
    
    # If there's a mood MISMATCH on categorical level:
    if song["mood"] not in preferred_moods and target_valence set:
        # Use valence to rescue the score
        # But reduce genre bonus if emotional direction is very wrong
        if target_valence < 0.4 and song["valence"] > 0.7:
            total_score *= 0.85  # 15% penalty for happy/sad conflict

Impact:
    This creates a "soft" emotional alignment layer
    Genre still matters, but emotional direction is respected


TESTING THE FIXES:
─────────────────

Test against Profile 7 again:
    
    BEFORE:  Sunrise City (happy) = 6.08 ← WINS (feels off)
    AFTER:   Neon Sidewalk Cipher (gritty) = 5.67+ ← Should win (feels better)

Then rerun system_evaluation.py to see if other profiles are affected.


RECOMMENDATION FOR NEXT STEP:
────────────────────────────

1. Use Inline Chat on the genre/mood section in recommender.py
2. Ask: "Should we add a penalty for mood mismatch?"
3. Prototype OPTION 3 (valence penalty) - simplest change
4. Rerun system_evaluation.py
5. Compare before/after on the "Sad Pop Music" profile
"""
