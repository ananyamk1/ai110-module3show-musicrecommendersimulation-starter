# Reflection on Profile Pair Comparisons

## Pair 1: High-Energy Pop vs Chill Lofi
High-Energy Pop consistently pulls songs like "Sunrise City" and sometimes "Gym Hero" because those songs are upbeat, energetic, and easy to dance to. Chill Lofi shifts the list toward tracks like "Midnight Coding" and "Library Rain," which are slower and softer. This difference makes sense because one listener wants momentum and the other wants calm focus.

## Pair 2: Warm Up Workout vs Minimal Energy (0.0)
Warm Up Workout tends to favor high-energy tracks with faster tempo, since the profile is asking for motivation and movement. Minimal Energy (0.0) does the opposite and pulls more ambient or low-intensity songs like "Spacewalk Thoughts." This is a good sign because the recommender is clearly responding to opposite energy goals.

## Pair 3: Sad Pop Music vs High-Energy Pop
High-Energy Pop usually ranks bright, energetic pop songs at the top, which is expected. Sad Pop Music was more surprising: energetic songs can still appear high if they fit the energy target, even when their mood is happier than requested. In plain terms, this is why a song like "Gym Hero" can show up: it matches the "pop + high energy" part very strongly, so it can beat songs that are sadder but less energetic.

## Pair 4: Electric Rock + High Acousticness vs 200 BPM Acoustic Jazz
Electric Rock + High Acousticness still often returns rock/intense songs first, because strong genre and energy matches can outweigh unusual acoustic preferences. 200 BPM Acoustic Jazz also shows a mismatch pattern where genre/acoustic fit can still beat the unrealistic tempo request. This makes sense because the model tries to find the best compromise when user preferences conflict.

## Pair 5: Maximum Energy (1.0) vs Non-Danceable House
Maximum Energy (1.0) pushes very energetic songs to the top, even across multiple genres. Non-Danceable House asks for a strange combination, so the recommender still finds house/euphoric tracks but may include songs that are more danceable than the user asked for. That result is reasonable for this dataset because most house-like tracks are naturally high-energy and dance-friendly.

## Pair 6: High Energy + Sad vs Impossible Preference
High Energy + Sad can still return strong results because at least part of the request is realistic in the catalog. Impossible Preference produces lower-confidence matches because the requested combination is extreme and hard to satisfy at the same time. This makes sense: when no song is a perfect fit, the recommender picks the closest compromise rather than returning nothing.
