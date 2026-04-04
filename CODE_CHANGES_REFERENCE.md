"""
QUICK REFERENCE: WEIGHT SHIFT CHANGES APPLIED
═══════════════════════════════════════════════════════════════════════════════

This file shows exactly what was changed in recommender.py

═══════════════════════════════════════════════════════════════════════════════
CHANGE #1: OOP Implementation (_score_song_with_breakdown, Lines 78-91)
═══════════════════════════════════════════════════════════════════════════════

BEFORE:
───────
        # Genre match: +2.0
        if song.genre in preferred_genres:
            genre_points = 2.0
            total_score += genre_points
            reasons.append(f"genre match (+{genre_points:.1f})")

        # Mood match: +1.0
        if song.mood in preferred_moods:
            mood_points = 1.0
            total_score += mood_points
            reasons.append(f"mood match (+{mood_points:.1f})")

        # Energy closeness: up to +2.0
        energy_closeness = self._closeness(song.energy, user.target_energy, 0.35)
        energy_points = energy_closeness * 2.0


AFTER:
──────
        # Genre match: +1.0  ← CHANGED
        if song.genre in preferred_genres:
            genre_points = 1.0  ← CHANGED
            total_score += genre_points
            reasons.append(f"genre match (+{genre_points:.1f})")

        # Mood match: +1.0
        if song.mood in preferred_moods:
            mood_points = 1.0
            total_score += mood_points
            reasons.append(f"mood match (+{mood_points:.1f})")

        # Energy closeness: up to +4.0  ← CHANGED
        energy_closeness = self._closeness(song.energy, user.target_energy, 0.35)
        energy_points = energy_closeness * 4.0  ← CHANGED


═══════════════════════════════════════════════════════════════════════════════
CHANGE #2: Functional Implementation (_score_song_functional, Lines 213-227)
═══════════════════════════════════════════════════════════════════════════════

BEFORE:
───────
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

    # Energy closeness: up to +2.0
    energy_closeness = _closeness(song["energy"], target_energy, float(user_prefs.get("energy_range", 0.35)))
    energy_points = energy_closeness * 2.0


AFTER:
──────
    # Genre match: +1.0  ← CHANGED
    if song["genre"] in preferred_genres:
        genre_points = 1.0  ← CHANGED
        total_score += genre_points
        reasons.append(f"genre match (+{genre_points:.1f})")

    # Mood match: +1.0
    if song["mood"] in preferred_moods:
        mood_points = 1.0
        total_score += mood_points
        reasons.append(f"mood match (+{mood_points:.1f})")

    # Energy closeness: up to +4.0  ← CHANGED
    energy_closeness = _closeness(song["energy"], target_energy, float(user_prefs.get("energy_range", 0.35)))
    energy_points = energy_closeness * 4.0  ← CHANGED


═══════════════════════════════════════════════════════════════════════════════
IMPACT SUMMARY
═══════════════════════════════════════════════════════════════════════════════

CHANGED ITEMS:
  ✓ Genre match points:      2.0 → 1.0      (HALF)
  ✓ Energy points multiplier: 2.0 → 4.0     (DOUBLE)  
  ✓ Maximum possible score:   10.3 → 11.3   (+1.0)
  ✓ Genre importance:         19% → 9%
  ✓ Energy importance:        19% → 35%

UNCHANGED ITEMS:
  • Mood match: Still +1.0
  • Tempo/Valence/Danceability/Acousticness: Unchanged
  • Crescendo proxy: Unchanged
  • Acoustic preference bonus: Still +0.3
  • All other logic: Unchanged


═══════════════════════════════════════════════════════════════════════════════
REVERTING THE CHANGES
═══════════════════════════════════════════════════════════════════════════════

If you want to go back to the original weights, change:

Line ~78 (OOP):        genre_points = 1.0  →  genre_points = 2.0
Line ~84 (OOP):        energy_points = energy_closeness * 4.0  →  energy_closeness * 2.0
Line ~213 (Functional):genre_points = 1.0  →  genre_points = 2.0
Line ~227 (Functional):energy_points = energy_closeness * 4.0  →  energy_closeness * 2.0


═════════════════════════════════════════════════════════════════════════════════
TEST RESULTS
═════════════════════════════════════════════════════════════════════════════════

With these changes applied:

Command:  python -m src.main
Status:   ✓ Works
Output:   Top 5 recommendations show higher energy-focused scores

Command:  python -m src.system_evaluation
Status:   ✓ Works
Key Finding: "Sad Pop Music" profile now recommends sad music first ✅


═════════════════════════════════════════════════════════════════════════════════
NEXT EXPERIMENT IDEAS
═════════════════════════════════════════════════════════════════════════════════

Try these weight combinations to find the sweet spot:

OPTION 1: Balanced Middle Ground
  Genre:  2.0 → 1.5
  Energy: 2.0 → 3.0
  Reason: Compromise between current and new

OPTION 2: Mood-First Tuning
  Genre:  2.0 → 1.0
  Mood:   1.0 → 1.5
  Energy: 2.0 → 4.0
  Reason: Emphasize emotional matching over genre

OPTION 3: Adaptive Weighting (Most Complex)
  If query contains emotional descriptors (sad, chill, etc):
    Use G=1.0, E=4.0 (current)
  Else (just genre query):
    Use G=2.0, E=2.0 (original)
  Reason: Different behavior for different query types


═════════════════════════════════════════════════════════════════════════════════
"""
