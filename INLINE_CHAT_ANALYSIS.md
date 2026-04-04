"""
INLINE CHAT ANALYSIS: Why "Sad Pop Music" Recommends Happy Pop
================================================================

SCENARIO: User Profile "Sad Pop Music"
- Wants: pop genre + sad mood + low valence (0.2)
- Energy: 0.7

RESULT #1 - Sunrise City (scores 6.08/10) ✓ TOP MATCH
  Song attributes: genre=pop, mood=HAPPY, valence=0.84
  Breakdown:
    ✓ Genre match: +2.0  (user wanted pop, got pop)
    ✗ Mood match: +0     (user wanted sad, got HAPPY - NO BONUS, NO PENALTY!)
    ✓ Energy alignment: +1.31
    ✓ Tempo match: +0.66
    ✓ Danceability fit: +1.11
    ✓ Acousticness fit: +0.56
    ✓ Crescendo vibe: +0.43
    ─────────────────────
    TOTAL: 6.08/10

RESULT #2 - Neon Sidewalk Cipher (scores 5.67/10)
  Song attributes: genre=hip-hop, mood=GRITTY, valence=0.42
  Breakdown:
    ✗ Genre match: +0    (user wanted pop, got hip-hop)
    ✗ Mood match: +0     (user wanted sad, got gritty)
    ✓ Energy alignment: +1.89
    ✓ Tempo match: +1.08
    ✓ Valence fit: +0.37  (valence 0.42 is closer to target 0.2 than 0.84!)
    ✓ Danceability fit: +1.33
    ✓ Acousticness fit: +0.62
    ✓ Crescendo vibe: +0.39
    ─────────────────────
    TOTAL: 5.67/10

KEY INSIGHT:
─────────────
Sunrise City wins despite:
  • Having OPPOSITE mood (happy vs. sad) ← This feels wrong!
  • Having OPPOSITE valence (0.84 vs. target 0.2) ← This is off!
  
Why? Because:
  • Genre match bonus: +2.0 is FIXED and powerful
  • Mood not matching → No penalty, just no bonus
  • Numeric mismatches only reduce partial points
  
WEIGHT HIERARCHY REVEALED:
─────────────────────────
Genre match (+2.0):        Dominant force
Mood match (+1.0):         Only matters FOR MATCHES
Energy closeness (+2.0):   Strong secondary
Valence closeness (+1.0):  Weak tertiary
Mood mismatch penalty:     ZERO (no guardrail!)

CONCLUSION:
───────────
The genre weight is so strong that it "captures" all songs of that genre
REGARDLESS of their emotional properties (mood, valence).

A user asking for "sad pop" gets the HAPPIEST pop song in the database
because no mood/valence penalty exists for mismatches.
"""
