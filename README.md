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

### Upload a song

`POST {API_PREFIX}/songs/upload` requires a bearer token and multipart form data:

- `title`: song title
- `artist_id`: ID of an existing artist
- `song_file`: audio file
- `cover_image`: image file

The audio is uploaded to the configured songs bucket using its original filename.
The cover image is uploaded to the configured bucket under `images/`, using its
original filename.
A successful request returns the created song record.

<h2>Tables</h2>

<img width="968" height="464" alt="image" src="https://github.com/user-attachments/assets/745e3a40-a0bf-4702-bb53-b2c090746ea8" />
