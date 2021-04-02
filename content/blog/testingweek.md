+++
Description = "Participation in the 21.04 Ubuntu Image Test"
Date = 2021-04-01T14:54:33-05:00
PublishDate = 2021-03-31T14:54:33-05:00 # this is the datetime for the when the epsiode was published. This will default to Date if it is not set. Example is "2016-04-25T04:09:45-05:00"
title = "Helping the Hippo"
#blog_banner = ""
blog_image = "img/episode/e04/e04.png"
images = ["img/episode/e04/e04.png"]
#Author = ""
#aliases = ["/##"]
draft= false #set to false to publish
+++
### Ubuntu 21.04 Testing Week
Oh boy! What an oppertunity! I just heard from many different podcasts about the beta test week for Ubuntu 21.04. I have never participated in an event like this before so I am grateful that something like this exists.

Alan Pope recently made a [forum post](https://discourse.ubuntu.com/t/ubuntu-21-04-testing-week/21519) about the event that includes [documentation for new testers](https://wiki.ubuntu.com/QATeam/Overview/NewTesters). It's about an hour investment to learn the process of how to conduct the tests. 

I watched Alan's videos on how to do it and then logged into my account and got started.

### Using Virtual Images
I don't have spare hardware at the moment so I decided to do all the testing in virtual box. I haven't used virtual box that much, but the process was pretty straight forward. 

1. Download the ISO(s) that you want to test. I did Kbuntu and Kylin because they still had tests that needed to be done in the live environment. I am familiar with Kbuntu and have heard of Kylin but never tried it.
2. Open Virtual box and create a new environment.

<p style="text-align:center;"><img src="https://linuxlemming.com/img/episode/e04/new.png" width="500" height="100"/>

3. Setup the virtual environment for Linux and Ubuntu

<p style="text-align:center;"><img src="https://linuxlemming.com/img/episode/e04/type.png" width="300" height="200"/>

4. Allocate the memory for ram. I have 32GB so I gave mine around 8GB of ram
<p style="text-align:center;"><img src="https://linuxlemming.com/img/episode/e04/memory.png" width="300" height="200"/>

5. I did not provide any disk space for the machine since this will be running a live environment only.

<p style="text-align:center;"><img src="https://linuxlemming.com/img/episode/e04/nodisk.png" width="300" height="200"/>

6. Mount the ISO in the virtual environment

<p style="text-align:center;"><img src="https://linuxlemming.com/img/episode/e04/iso.png" width="300" height="200"/>

7. Change the settings to recognize it as a live environment

<p style="text-align:center;"><img src="https://linuxlemming.com/img/episode/e04/live.png" width="400" height="200"/>

Now I was ready to follow the checklist and submit any bugs that I came across! I found only a small "bug" in Kbuntu where the language menu was not in the described place. Kylin on the other hand had LOTS of screen tearing when I was using apps.
<h2 style="text-align:center;"> Kbuntu </h2>  
<p style="text-align:center;"><img src="https://linuxlemming.com/img/episode/e04/kbuntu.png" width="600" height="100"/>
<h2 style="text-align:center;"> Kylin </h2> 
<p style="text-align:center;"><img src="https://linuxlemming.com/img/episode/e04/kylin.png" width="600" height="100"/>

I imagine that the next steps involve a Conical employee to verify my findings. Hopefully I'll find more time to test more but it felt good to contribute to this effort.