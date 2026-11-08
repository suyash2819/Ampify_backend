# Ampify_backend

Spotify Like App.


<h2> functional requirements - Features </h2>

1. user should be able to see the home page without sign up, but they should not be able to listen to any music
2. user should be able to sign up, redirect to sign in after sign up
3. user should be able to sign in
    3.a. User should be able to fill a survey on what he/she likes to listen (choose artist)
4. user should see the home page with the preferred choice in 3.a
5. user should be able to click on that choice and play the music
6. user should be able to search for a music
7. user can create playlists
8. user can like the songs
9. user can play from liked songs
10. Add songs into queue while playing the songs

non functional req - not needed rn
scalability - support 1L users
availability - music should be available, availability > consistency here

<h2>System Design</h2>

Include Redis, Messaging Queue / Pub Sub, Load Balancer/API Gateway as needed

<img width="1456" height="778" alt="image" src="https://github.com/user-attachments/assets/a6f1df8e-588f-453f-b645-927828e932a8" />


<h2>Apis</h2>

/user/signup - POST <br/>
/user/signin - POST <br/>
/getStaticData - GET <br/>
/userMusicData - POST, GET <br/>

### Submit play events

`POST {API_PREFIX}/events` requires a bearer token and accepts a JSON array of
play-ended events. The authenticated user's ID is taken from the token; clients
must not send `user_id`.

Each event includes `event_id`, `type` (`play_ended`), `track_id`, `started_at`
(ISO 8601 timestamp with timezone), `ms_played`, `track_duration_ms`,
`end_reason` (`finished`, `skipped`, `closed`, or `error`), and `source`
(`user` or `agent`). `context_type`, `context_id`, `session_id`,
`queue_instance_id`, `device`, and `app_version` are optional.

Event IDs already stored for that user are ignored, including duplicates within
the same request. The response reports the number of inserted and duplicate
events:

```json
{"inserted": 1, "duplicates": 1}
```

### Get personalized song suggestions

`GET {API_PREFIX}/songs/suggestions` requires a bearer token and returns up to
three songs. Recommendations use the user's recent play events and each song's
`mood`. Skipped songs and their moods are included as negative signals so the
model can avoid those tracks and moods; a previously skipped track cannot be
returned as a recommendation. Songs without a mood are not candidates. Set
`GROQ_KEY` to enable the language-model selection step.

### Upload a song

`POST {API_PREFIX}/songs/upload` requires a bearer token and multipart form data:

- `title`: song title
- `mood`: song mood used for personalized recommendations
- `artist_id`: ID of an existing artist
- `song_file`: audio file
- `cover_image`: image file

The audio is uploaded to the configured songs bucket using its original filename.
The cover image is uploaded to the configured bucket under `images/`, using its
original filename.
A successful request returns the created song record.

<h2>Tables</h2>

<img width="968" height="464" alt="image" src="https://github.com/user-attachments/assets/745e3a40-a0bf-4702-bb53-b2c090746ea8" />
