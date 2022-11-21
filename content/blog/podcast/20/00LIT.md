+++
Description = "Trying to document: How to implement the Live Item Tag in the RSS feed; How to get a server to handle the live stream; How to send the audio to the live stream; How to ping the index to let everyone know that [The Lemming is Lit](https://cautiouslycurious.com/listen/linux_lemming/radio.mp3)"
Date = 2022-11-18T15:26:53-06:00
PublishDate = 2022-11-18T15:26:53-06:00 # this is the datetime for the when the epsiode was published. This will default to Date if it is not set. Example is "2016-04-25T04:09:45-05:00"
title = "Let's Get LIT"
#blog_banner = ""
blog_image = "img/host/calaveraJP.jpeg"
images = ["img/episode/default-social.jpg"]
Author = "rastacalavera"
#aliases = ["/##"]
series = ["Podcasting 2.0"]
tags = ["Podcasting 2.0", "Podcast Namespace", "Enhancements", "Features"]
+++
I have been loving the Live notifications from [Podverse](podverse.fm) that let you know when a podcast you follow is doing a live stream. The only show that supports it currently that I listen to is the Podcasting 2.0 Show but I think more content creators will support it in the future. I think it is a bit burdensome to wrap your head around it, but I think I have figured out the basic steps. 

## Going LIT
* Get a server that will allow you to broadcast a live stream
    * There is probably an easier approach but I've chosen the self hosted option and am using [Azuracast](https://www.azuracast.com/) as the software stack to make this possible.
* Get software that will allow you to send audio to your live stream server
    * I have chosen to use [MIXXX](https://mixxx.org/) because it came pre-installed on my system and it seems pretty straight forward to use.
* Add the LIT tag to the RSS
    * ~~I am not sure if this is done at the individual episode level or further in the chain, still need to figure this one out.~~
    * It appears that this needs to live outside of the item tag so this would have to be something that is in the default params of the theme.
* Publish RSS with the updated LIT tag **and** send off a Podping to update the index.
    * I am still learning about Podping but I believe that this is the mechanism that can quickly update the [Podcast Index](https://podcastindex.org/) which will then trickle down to the apps to let listeners know that your podcast is live.

## Coding

I have a tinker [branch](https://gitlab.com/rastacalavera/linuxlemming/-/blob/lit2) of my site where I kind of test different things out.

So I've added these pieces below into the `episode.rss.xml` of Castanet 
```
    <podcast:liveItem> status={{ .Site.Params.show_live_status }} start="{{ .Site.Params.show_live_start }}" end="{{ .Site.Params.show_live_end }}"
      <title>Linux Lemming Live Stream</title>
      <enclosure url="https://cautiouslycurious.com/listen/linux_lemming/radio.mp3" type= "audio/mpeg" length="16000" />
      <podcast:contentLink href="https://cautiouslycurious.com/listen/linux_lemming/radio.mp3">Listen Live!</podcast:contentLink> 
    </podcast:liveItem>
```
I don't have a `GUID` in there which might be an issue. . . not entirely sure. I also had to kind of guess on the `length` for the enclosure because Azuracast is streaming at 128kbps so I used a [converter](https://www.gbmb.org/kbit-to-bytes) to get it into bytes.


 In the `config.toml` of the site I also added these params that could be called by the rss generator:
```
show_live_status = "\"ended\"" #pending/live/ended
show_live_start = "2022-11-22T20:30:00-06:00" #need to convert, https://dencode.com/en/date/iso8601
show_live_end = "2022-11-22T22:00:00-06:00" #need to convert, https://dencode.com/en/date/iso8601
```

I had to use a [date converter](https://dencode.com/en/date/iso8601) to get a ISO8601 Date that seemed to match the required format.


These all seemed to checkout so I added them into the main branch of the project without doing a PR. I didn't want to re-learn how to cherry pick a commit and it was just easier to copy and paste things over after I knew it wouldn't break it.

So in theory, I should be good to go! Once I get all the streaming stuff connected, I fire off a python script to notify podping and then a notification should go out to apps. Maybe I'll try getting LIT this week!