+++
Description = "Setting up Self-Hosted Website Analytics"
Date = 2021-03-19T20:08:47-05:00
PublishDate = 2021-03-19T20:08:47-05:00 # this is the datetime for the when the epsiode was published. This will default to Date if it is not set. Example is "2016-04-25T04:09:45-05:00"
title = "Shynet- The Self-Hosted Analytics Platform"
#blog_banner = ""
blog_image = "img/episode/default.jpg"
images = ["img/episode/default-social.jpg"]
#Author = ""
#aliases = ["/##"]
draft=true
+++
### What is Shynet?
A few weeks ago I was browsing the subreddit [/r/selfhosted](www.reddit.com/r/selfhosted) and came across a cool post about an application called [Shynet](https://github.com/milesmcc/shynet). It is a self-hosted web analytics tool and looks REALLY cool. I've used [Google Analytics](https://analytics.google.com) in the past but I don't run a commercial site and SEO doesn't really matter to me so if I can just see some traffic data, that's good enough for me! Castanet (the Hugo theme for the site) does support Google Analytics, but if I can use a non-Google tool, I'm all in!
Here is how the project describes themselves:
>There are a lot of web analytics tools. Unfortunately, most of them come with the following caveats:
>
>* They require handing all of your visitors' info to a third-party company
>* They use cookies to track visitors across sessions, so you need to have those annoying cookie notices
>* They collect so much personal data that even the NSA is jealous
>* They are closed source and/or expensive, often with limited data portability
>* They are hard to use
>
> Shynet has none of these caveats. You host it yourself, so the data is yours. It works without cookies, so you don't need any intrusive cookie notices. It collects just enough data to be useful, but not enough to be creepy. It's open source and intended to be self-hosted. And you may even find the interface easy to use. 

### Installation
Shynet has great [documentation](https://github.com/milesmcc/shynet/blob/master/GUIDE.md#installation) if you are already familiar with how to use docker. I initially tried to run this on my Pi but found out that they do not have an arm64 image. I do have a secondary computer that is x86 that I run a few docker containers on so I figured I would give it a go on that.

After cloning the repo, I modified the files according to the instructions. I was a little uneasy at the possibility of having TWO reverse proxies since SWAG gets all my incoming traffic and that Shynet uses nginx as well, but I figured I would see what happens. I set it up without ssl just to try to make things easier at first.

Everything went smoothly! I was able to log into the dashboard of Shynet just fine but there was one weird thing I noticed.

<img src="https:linuxlemming.com/img/blog/shynet/shynetdash.png" width=100 height=100/>