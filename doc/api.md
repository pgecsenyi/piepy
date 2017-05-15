# PiEPy: API

## Maintenance

    GET /categories

Lists available categories.

    GET /rebuild

Rebuilds media database, updates information.

    GET /search/<string:search_string>

Searches among the titles.

    GET /status

Provides status information, such as uptime or synchronization status.

    GET /sync

Updates the media database without deleting it. Indexes new files and removes obsolete entries. Supposed to be faster than a full reset and a bit less precise in the same time. Every now and then doing a full reset is recommended.

## Audio

    GET /audio/albums

Get audio albums.

    GET /audio/albums?artist=<int:artist_id>

Get audio albums for the given artist.

    GET /audio/artists

Get audio artists.

    GET /audio/tracks

Get audio tracks.

    GET /audio/tracks?album=<int:album_id>

Get audio albums for the given album.

    GET /audio/player/<string:action>

Apply forward, fast forward, pause, stop, rewind, fast rewind, volume down, volume up, faster or slower operations on the audio player.

    GET /audio/player/play/<int:track_id>

Plays the track with the given ID.

    GET /audio/player/play?id=<int:id>&audioout=<string>

Plays the audio file with the given ID (if there is any item with the specified ID). This URL also specifies the audio output of the device to use: this value can be either `analog` or `digital`. Note however that this is only kind of a recommendation and currently works with _omxplayer_ only, _VLC_ does ignore this parameter.

## Image

    GET /image/albums

Lists all albums.

    GET /image/viewer/next

Jumps to the next image.

    GET /image/viewer/previous

Jumps to the previous image.

    GET /image/viewer/stop

Stops slideshow.

    GET /image/viewer/view/<int:id_album>

Starts slideshow.

    GET /image/viewer/zoom-in

Increases zoom.

    GET /image/viewer/zoom-out

Decreases zoom.

## Video

    GET /video/details/<int:id_title>

Returns details for the given ID (if there is any item with the specified ID).

    GET /video/languages

Lists all available languages (lists each language that has at least one corresponding video file).

    GET /video/player/faster

Instructs player to play video faster.

    GET /video/player/fastforward

Jumps forward 10 minutes in time.

    GET /video/player/fastrewind

Jumps backward 10 minutes in time.

    GET /video/player/forward

Jumps forward 30 seconds in time.

    GET /video/player/pause

Pauses player.

    GET /video/player/play/<int:id>

Plays the video file with the given ID (if there is any item with the specified ID).

    GET /video/player/play?id=<int:id>&audioout=<string:audio_output>

Plays the video file with the given ID (if there is any item with the specified ID). This URL also specifies the audio output of the device to use: this value can be either `analog` or `digital`. Note however that this is only kind of a recommendation and currently works with omxplayer only, VLC does ignore this parameter.

    GET /video/player/play?id=<int:id>&subtitle=<int:id_subtitle>

Plays the video file with the given ID (if there is any item with the specified ID) and with the given subtitle (if there is any subtitle with the specified ID).

    GET /video/player/play?id=<int:id>&subtitle=<int:id_subtitle>&audioout=<string:audio_output>

Plays the video file with the given ID (if there is any item with the specified ID) and with the given subtitle (if there is any subtitle with the specified ID). This URL also specifies the audio output of the device to use: this value can be either `analog` or `digital`. Note however that this is only kind of a recommendation and currently works with omxplayer only, VLC does ignore this parameter.

    GET /video/player/rewind

Jumps backward 30 seconds in time.

    GET /video/player/slower

Instructs player to play video slower.

    GET /video/player/stop

Stops playing.

    GET /video/player/volumedown

Lowers volume a bit.

    GET /video/player/volumeup

Raises volume a bit.

    GET /video/qualities

Lists all available qualities (lists each quality that has at least one corresponding video file).

    GET /video/titles

Lists all available titles.

    GET /video/titles?language=<int:id_language>

Lists all titles that are available on the language identified by `id_language`.

    GET /video/titles?language=<int:id_language>&parent=<int:id_parent>

Lists all titles that are available on the language identified by `id_language` and have the parent `id_parent`.

    GET /video/titles?language=<int:id_language>&quality=<int:id_quality>

Lists all titles that are available on the language identified by `id_language` and their quality matches the quality specified by `id_quality`.

    GET /video/titles?language=<int:id_language>&subtitle=<int:id_language>

Lists all titles that are available on the language identified by `id_language` and have a subtitle of the given language.

    GET /video/titles?language=<int:id_language>&parent=<int:id_parent>&quality=<int:id_quality>

Lists all titles that are available on the language identified by `id_language`, have the parent `id_parent` and their quality matches the quality specified by `id_quality`.

    GET /video/titles?parent=<int:id_parent>

Lists all titles that have the parent `id_parent`.

    GET /video/titles?parent=<int:id_parent>&quality=<int:id_quality>

Lists all titles that have the parent `id_parent` and the quality `id_quality`.

    GET /video/titles?parent=<int:id_parent>&quality=<int:id_quality>&subtitle=<int:id_language>

Lists all titles that have the parent `id_parent` and the quality `id_quality` and have a subtitle of the given language.

    GET /video/titles?parent=<int:id_parent>&subtitle=<int:id_language>

Lists all titles that have the parent `id_parent` and have a subtitle of the given language.

    GET /video/titles?quality=<int:id_quality>

Lists all titles whose quality matches the quality specified by `id_quality`.

    GET /video/titles?quality=<int:id_quality>&subtitle=<int:id_language>

Lists all titles that are available in the given quality and have a subtitle of the given language.

    GET /video/titles?subtitle=<int:id_language>

Lists all titles for which a subtitle is available on the given language.

## Playlist

    PUT /playlist/add

Adds a playlist to the database.
Parameters: { title, tracks: [ { category_id, file_id }, ... ] }

    PUT /playlist/add_track

Adds a track to a playlist in the database.
Parameters: { playlist_id, number_after, track: { category_id, file_id } }

    POST /playlist/move_track

Changes the number of the given track in the given playlist.
Parameters: { playlist_id, number_to_move, number_after }

    DELETE /playlist/delete/<id>

Deletes the playlist specified by <id>.

    DELETE /playlist/delete_track/<int:id>

Deletes the playlist item specified by <id> from the current playlist.

    GET /playlist/all

Lists all playlists.

    GET /playlist/current

Lists the playlist that is currently played.

    GET /playlist/<id>

Provides informations about the playlist given by <id>.

    GET /playlist/next

Jumps to the next track on the playlist.

    GET /playlist/play/<int:id>

Starts playing of the given playlist.

    GET /playlist/previous

Jumps to the previous track on the playlist.

    GET /playlist/stop

Stops playing.
