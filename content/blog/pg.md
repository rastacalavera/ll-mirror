+++
Description = "Setting Up a Self-Hosted Podcast Generator"
Date = 2021-03-18T19:42:30-05:00
PublishDate = 2021-03-18T19:42:30-05:00 # this is the datetime for the when the epsiode was published. This will default to Date if it is not set. Example is "2016-04-25T04:09:45-05:00"
title = "Self-Hosted Podcast Generator"
#blog_banner = ""
blog_image = "img/episode/default.jpg"
images = ["img/episode/default-social.jpg"]
#Author = ""
#aliases = ["/##"]
+++
### Moving from Gitlab to Podcast Generator
A few years ago, a friend and I had what I would call a "hobby cast". We would put together show ideas, meet up once a week and record a 30-60 minute show. It was a lot of fun and I used the open source software [Podcast Generator](www.podcastgenerator.net) to publish it in iTunes so our friends could subscribe and listen.

I remember the installation process being really easy so I figured I would go a head and try to get it up and running for the Linux Lemming. I considered self-hosting it locally using [docker](https://hub.docker.com/r/vonproteus/podcast-generator) and that went fine at first, but then I decided against it if more than 5 people actually start paying attention to this project.

### Linode Woes and Vague Documentation
I figured I would get a $5 VPS to run the software and went with Linode since a lot of the JB community is using their service now. It was an absolute headache. I don't want to knock the service and would still recommend them to other people but in terms of getting up and running quickly, it did not function as expected. 

Their base Ubuntu 20.04.3 image was similar to my experience on the [Raspberry Pi 4](/blog/e02/) where adding users was a pain, setting default shells was a pain, it was overall just a hassle. Then on top of that, after I got everything setup how I wanted it to, I couldn't get the software to run as expected.

Granted, getting the software to run was a two fold issue.
1. The documentation from Podcast Generator consists of this:
>
    1. Download the latest version of Podcast Generator;
    2. Unzip the zip package containing the script;
    3. Upload the resulting files and folders to your web server;
    4. Point your web browser to the URL corresponding to the location where Podcast Generator files were uploaded (e.g. http://mypodcastsite.com/podcastgen). You will be redirected automatically to the 3-step setup wizard;
    5. Log-in into Podcast Generator administration area and start publishing your podcast.
>
**That's it**, five steps. Simple right? Well, if you are already familiar with setting up a LAMP stack, and administrating apache then sure it would be simple. If it's something you've done once a few years ago, good luck. After tons of searching, I stumbled onto this [open issue](https://github.com/PodcastGenerator/PodcastGenerator/issues/272) from 2020 which kind of helped but I still wasn't able to get past the welcome screen. A user from that thread, j-atoms, put together some [documentation](https://github.com/j-atoms/Podcast-Generator-Ubuntu-install-notes/blob/master/install-notes) which I think could be cleaned up and merged into the main project. I don't see the main project doing that though, because they kind of want people to purchase a hosted instance from their [partner](https://rss.com/blog/how-to-create-an-rss-feed-for-a-podcast/). The pricing was hard to find for them, if you have a university account, you can get their service for $5.99 USD but if you're a private party, it's $12.99 USD. They do offer free accounts for non-profits too which is pretty cool. 

So what now? Pay the $12.99 or keep searching?

### Let's Try Digital Ocean
I figured maybe I had done something horribly wrong on my Linode and I had already blown it away five or so times so I figured I might as well try [Digital Ocean](www.digitalocean.com) and see if I get different results.

I've used DO a lot in the past and when I spun up their LAMP stack for $5.99 USD (BTW, you don't need a LAMP stack for this server but it saves you the step of having to download apache and PHP) and it had the user creation I am use to! Strange that their image did and Linode didn't. . . .

Now before I found the j-atoms documentation as mentioned earlier, I was using Digital Ocean's [documentation](https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-16-04) on how to setup apache. Linode also had [documentation](https://www.linode.com/docs/guides/how-to-install-apache-web-server-debian-10/) but their LAMP uses Debian 9 Buster and the guide is about how to install it from scratch on Ubuntu so the disconnect was just too much for me. The DO documentation was straight forward **but** I still had the same issue in the end.

### Back to Git Hub
So what do I do now? I went back to the source to try to get help. I commented on the j-atoms thread and got no response. I figured I could [open an new](https://github.com/PodcastGenerator/PodcastGenerator/issues/405) *"Help Wanted"* issue on their tracker and see if anyone could help. Well I was waiting for reply, I went back and re-read the j-atoms thread and noticed something that I had over looked previously.User emilengler had been the first to reply and below their main point, included an extra little thing about packages that I had missed.
>After this please install these packages sudo apt install php-gettext php-xml
If php-gettext is not available, try to not install it. Maybe it is not required on Ubuntu
>
**WHAT?!?**
Are these two things not included in a standard LAMP install?!? I figured I might as well give it a go and see what happens.

The `php-gettext` package was not available. When I tried to `apt install php-xml` it gave me the option to install it. I was floored. After installing the package, everything worked as expected.
You'd think Podcast Generator would include that little piece of information in their five step installation.

<img src="https://tenor.com/view/facepalm-really-stressed-mad-angry-gif-16109475" />

### Up and Running
Well, it's all up now. I eventually I'll be serving my podcast files from [this site](rss.linuxlemming.com) rather than hosting them through gitlab. I am thinking I may try and contribute this back upstream using j-atoms work as a jumping off point as well.