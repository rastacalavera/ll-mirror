+++
Description = "The pains that go with learning how to do something on your own and finally finding (limited) success. Blog photo from [Backdoor Survival on Flickr](https://www.flickr.com/photos/backdoorsurvival/7019634849/in/photolist-bGisT4-7YV4zG-bnCNEQ-at9con-dARur2-dBYisw-oT7t1E-dAT37J-6rtuia-oLXSfZ-37S2CG-aRuWUe-kDQwg4-roDfpm-boj58R-kDQw9a-7VZucT-8rsm94-6JxPZU-yGpo4-9kfA9U-bJGd9-dAhpow-dAkE95-2czD39E-24vBWdY-8FipaZ-5XicUA-82yXVc-dARF94-dAuRXn-dAwJ5K-dAKJf1-5vRA8n-px5YU4-qvv6Gj-KdQHf-aQS4Wp-kDQwek-t9whUW-b67Ej-bo1SLp-9LCooV-eer58m-eer5aJ-dAQBfD-8vMd4G-dXu9Bp-9mkb6h-5iJeQd)."
Date = 2021-02-26T13:42:00-06:00
PublishDate = 2021-02-26T13:42:00-06:00 # this is the datetime for the when the epsiode was published. This will default to Date if it is not set. Example is "2016-04-25T04:09:45-05:00"
title = "Website Woes"
#blog_banner = ""
blog_image = "img/episode/website_woes.jpg"
images = ["img/episode/website_woes.jpg"]
#Author = ""
#aliases = ["/##"]
+++
### Ignorance Is Not Bliss- Have Some Grit When Using Git
I think I was a little over ambitious with this project. I am fine using git in a terminal but when working with markdown files, I like to have a preview pane so I chose to try to do everything in VSCode.
Installing the app wasn't an issue, but I had a lot to learn in terms of using it with github and gitlab.
This was mistake #1, better the devil you know when trying something new I guess. I now have VSCode working as intended and feel pretty confident when pushing to the main linuxlemming repository.I run KDE and there was an issue with token authentication and I had to install gnome keyring in order to get things to play nice. 

I REALLY struggled getting the website in a functional state and being new to VSCode certainly didn't help. At one point I accidently tried to push changes to a repo I had forked from **(woops)** and when I made and committed changes and pushed to my own repo, I wasn't seeing the expected changes on the gitlab site. 

I think I need to still figuring out pulling/rebase or something because when there are conflicts I am completely lost on how to properly fix them. I still have **A LOT** to learn with git.

### Error: Unable to locate config file or config directory. Perhaps you need to create a new site.

I am still very confused about the finer details of Hugo. I spent hours building, modifying and nuking site after site, repo after repo, desperately trying to figure out what the heck I was doing wrong. 
After a few hours of sleep I came up with a systematic approach.
1. Get the theme I wanted working first.
    - Clone the repo from [Arrested DevOps](https://github.com/arresteddevops/ado-hugo)
    - Make a new hugo site 
    - Throw everything from the working clone into the new site and verify that Hugo will serve it
    - Throw my files into the the new site one at a time and fix things as they break.

While that looks pretty straight forward, it sure as heck wasn't when I started. See ado-devops uses a theme called [castanet](https://github.com/mattstratton/castanet) which is what I found first. I just wanted that and thought (still am not sure) that it could be used as a standalone item. A bit hiccup I had though was that outside of the "exampleSite" there was just all this **extra stuff**. I have no idea what any of it does, but it is important. Trying to run `hugo server` outside of the exampleSite didn't work (that made sense to me) but when I put all my own stuff in and started tweaking things got weird and I was getting module errors and had to put a copy of the *castanet* folder in my home folder to get it to work. This was one of those cases where I should have just stopped and done other things and wait for that **AH HA!** moment when you randomly think of a possible solution, but I was being stubborn. I wanted to figure this out!

To someone who knows Hugo well, I am sure that all of this makes sense, but for a beginner like myself, I was making some misguided choices.

So here is what I've learned:
- Castanet is a theme only. The example site is provided just to show you what it looks like and to play with to see what stuff does. DO NOT USE THIS THINKING THAT YOU CAN MODIFY IT AND PUSH TO GITLAB.
- Ado-hugo is the site **WITH** that castanet theme.
- LEAVE CASTANET ALONE! The exampleSite can be deleted but don't mess with anything else.
- Modify or replace all the stuff in Ado-hugo (which in my case I previously made in castanet so I just pulled everything over).

### DNS Headache

I recently decided to purchase my domain of `linuxlemming.com` from [register4less](https://register4less.com) after hearing about it on [The Ask Noah Show](https://asknoahshow.com). They seem like a good company but there user interface is like taking a trip back to 2002. I needed to have my domain pointing to my gitlab page so I was following gitlab's [documentation](https://docs.gitlab.com/ee/user/project/pages/custom_domains_ssl_tls_certification/) but was getting confused again and was super fatigued by this whole process. I hopped into the matrix room for Ask Noah and awesome community member [rwaltr](https://discourse.destinationlinux.network/u/rwaltr/summary) helped me get things sorted. After my website was verified, I have two urls:
- The gitlab page- https://rastacalavera.gitlab.io/linuxlemming
- My Domain page- https://linuxlemming.com/
The gitlab page url works fine but the domain one only loads the main page and 404s on everything else. Searching seemed to lead me to that I might have to wait 24-48 hours and then everything will work. I hope that is the case. . . otherwise I'll be popping into the gitlab forums next to try to trouble shoot the issue.

### baseURL and Extra Stuff

Now that the site is up, more things don't work! HOORAY!

So here is the main issue, If my baseURL is set to different options, the theme breaks but the links all go to the correct location or the theme works but none of the links move accordingly. Here it is laid out:

#### baseurl= "https://rastacalavera.gitlab.io/linuxlemming/" 
* Theme works
* gitlab page url works fine, all links work
* linuxlemming.com landing pages works with theme
* none of the links work. All have an extra `/linuxlemming/`

### baseurl= "https://www.linuxlemming.com/"
* gitlab page loads but there is no theme
    * none of the links work, they all 404. 
    * after the main "rastacalavera.gitlab.io/" there is no "/linuxlemming/"
* linuxlemming.com loads but there is no theme
    * all links work
```
#baseurl = "http://localhost:1313"
#baseurl = "https:www.linuxlemming.com/"
baseurl = "https://rastacalavera.gitlab.io/linuxlemming/"
#relativeURLs = true
languageCode = "en-us"
title = "The Linux Lemming"
theme = "castanet"
googleAnalytics = ""
paginate = "9"
buildFuture = true

[taxonomies]
  category = "categories"
  series = "series"
  tag = "tags"

[permalinks]
  page = "../..:filename/"
  about = "../..:filename/"
  episode = "../..:filename/"
```
### Light at the End of the Tunnel
I had tried everything and was out of my depth. I wasn't sure where to turn next. GitLab community support forums? A group from DLN or JB? My problem was pretty unique to me and it seemed like a big ask to jump in a random public group asking for help.

I had previously posted an issue on the [castanet github page](https://github.com/mattstratton/castanet) and the developer, [Matt Stratton](https://github.com/mattstratton) was super friendly and quick to respond! I figured it was worth another shot to open an issue and detail everything that I had tried. 

Well, Matt returned and again was super helpful and friendly! Together we solved the issue and also fixed a larger setting in the theme that may benefit others in the future! If felt really good to close issue [342](https://github.com/mattstratton/castanet/issues/342) not only because it solved my problem but because I had a great community interaction. I really hope I can contribute back to the project by helping to close some of the "chore" issues for him. 

My interaction with Matt just reaffirmed how great open source can be. To get hands on with the actual dev and have a positive interaction is priceless. I'm sure most of his [Arrested DevOps Podcast](https://www.arresteddevops.com/) is over my head, but I'll be sure to give it a listen and if it sounds interesting, you should too!

If you want to see some of our fixes in detail, check out the [issue tracker on his page](https://github.com/mattstratton/castanet/issues/342) or my commit history on [GitLab](https://gitlab.com/rastacalavera/linuxlemming/-/commits/master)