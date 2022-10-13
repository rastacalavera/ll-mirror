+++
title = ""

Description = "" #shows up next to the 

Date = {{ .Date }}

live_status = "pending" # need status of pending, live or ended

live_start = {{ .Date }} #A string representing an ISO8601 timestamp that denotes the time when the stream is intended to start.

live_end = {{ .Date }} #A string representing an ISO8601 timestamp that denotes the time when the stream is intended to end.

podcast_file = "###.mp3" # this MAY work for the enclosure

live_contentLink = #required to be present, to ensure that listeners have a fallback option in case their chosen app cannot play the given content stream directly.

podcast_bytes = "" # the length of the episode in bytes

episode_image = "img/episode/default.jpg"

images = ["img/episode/default-social.jpg"] #maybe only needed for webpage and not for RSS

explicit = "no" # values are "yes" or "no"

#guests = [] # The names of your guests, based on the filename without extension.
#sponsors = []
#episode = ""
#podcast_duration = "" #don't think this is needed
#media_override # if you want to use a specific URL for the audio file
+++
