+++
Description = "I was able to migrate my old Linkace containers from a backup on my NAS!!"
Date = 2022-11-17T15:22:11-06:00
PublishDate = 2022-11-17T15:22:11-06:00 # this is the datetime for the when the epsiode was published. This will default to Date if it is not set. Example is "2016-04-25T04:09:45-05:00"
title = "Link Ace"
#blog_banner = "img/blog/apps/linkace/linkace.jpg"
blog_image = "img/blog/apps/linkace/linkace.jpg"
images = ["img/episode/default-social.jpg"]
Author = "rastacalavera"
#aliases = ["/##"]
series = ["selfhosted Apps"]
tags = ["selfhosted","selfhosting","archive","docker","open source","bookmark archive","2-factor"]
+++
# What is Linkace?
Linkace provides a way to archive a website, add tags to the website archive, add website archives to organized lists and present all this information to the user using a private or public dashboard! To see a more concise list of features, you should checkout the page features[^1] because the creator can explain everything better than my summarization.

## How to Setup Linkace?
There are two options when setting up Linkace; the simple option[^2] or the advanced option[^3]. The main difference between the two is how the app is served and the database backend it connects too as well. The creator recommends that if you have full control of your system to use the advanced feature and if you are limited to your environment, then the simple approach should be used.

I personally chose to go the simple route because I was just testing the application, but maybe down the line I will migrate to the advanced setup.

To get the needed files from GitHub onto my server, I first made a folder and then entered it.
 
`mkdir linkace && cd linkace`
 
Then grabbed the files using
  
`wget https://github.com/Kovah/LinkAce/releases/download/v1.10.5/linkace-v1.10.5-docker-simple.zip`

and finally unzipped the folders using `unzip`.

This leaves you with the `docker-compose` file and the `.env` file that you can customize as needed.

In my instance, I run all my apps behind SWAG so I needed to add the external network connection by putting a bit of code at the end of the `docker-compose` file that looks like this:
```
networks:
  default:
    name: swag
    external: true
```

I hit a snag with permission issues with the containers trying to reference by `.env` file and I am not sure if I needed to include a `PUID` `PGID` value in the environment but I just ended up using `chmod 777 .env` when the containers were down and when I brought them back up, everything seemed to be working just fine.

## 2-Factor Auth??
As I was setting this up for the blog, I saw that there was a setting to enable 2-Factor authentication. I have never tried this so I gave it a whirl and it worked great! It generates a QR code that can be scanned by a password manager, like [bitwarden](https://bitwarden.com/linux), and then it generates a 6 digit code that you have to enter after putting in your normal login credentials. 

Now I couldn't get the scan QR code feature to work, but I was able to enter the token in manually and low and behold it was seamless! So now I have 2-Factor auth on a self-hosted application!

## Email tie in?
The documentation is great but things get a little weird when it comes to email. I've struggled using Gmail in the past and using tokens and doing weird calls in the container terminal but this project didn't really explain the steps for this and there wasn't much chatter in their community spaces[^4].

## Worth Checking Out!!
I think Linkace is a really cool project and recommend you give it a whirl!


## Links
[^1]:[Project Features](https://www.linkace.org/about/)
[^2]:[Simple Setup with Docker](https://www.linkace.org/docs/v1/setup/setup-with-docker/simple/)
[^3]:[Advanced Setup with Docker](https://www.linkace.org/docs/v1/setup/setup-with-docker/advanced/)
[^4]:[GitHub Discussions](https://github.com/Kovah/LinkAce/discussions)

[Project Website](https://www.linkace.org/)

[Support the Project](https://www.linkace.org/support/)