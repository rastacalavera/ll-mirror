import glob      # for listing files with pattern matching
import os.path   # for getting file size
import re        # regex for generating slugs for file names
import eyed3     # for reading and writing mp3 metadata
import json      # for reading metadata and writing podlove file
import markdown  # for creating plain text version of show notes for mp3 metadata
from io import StringIO  # also for un-markdowning
from eyed3.id3.tag import Tag
from shutil import copyfile
from datetime import datetime
import pytz  # timezones
from pathlib import Path
# from feedgen.feed import FeedGenerator  # for generating RSS feed


#need to find a way to better use these.
DATA_SRC_DIR = "/static/files/00test/" #"_episodes_src/"
MARKDOWN_OUTPUT_DIR = "/static/files/00out/"#"_episodes/"
OUTPUT_DIR = "/static/files/00out/"#"episodes/"
SHOW_METADATA = {
    "title": "The Linux Lemming",
    "genre": "Podcast",
    "url": "https:linuxlemming.com",
    "author": "Rastacalavera",
    "email": "rastacalavera@protonmail.com",
    "subtitle": "It's a show about software documentation, selfhosting and running with scissors."
}

DATE_INPUT_FORMAT = "%Y-%m-%d %H:%M"
DATE_BLOG_FORMAT = "%Y-%m-%d %H:%M:00 +0100"
DATE_PODLOVE_FORMAT = "%Y-%m-%dT%H:%M:00+01:00"

# I don't think this section is needed, don't need to generate an RSS from this script, castanet does that.
# def generateFeed():
#     global SHOW_METADATA
#     fg = FeedGenerator()
#     fg.load_extension('podcast')
#     fg.podcast.itunes_category('Technology', 'Leisure')
#     fg.podcast.itunes_author(SHOW_METADATA['author'])
#     fg.podcast.itunes_owner(SHOW_METADATA['author'], SHOW_METADATA['email'])
#     fg.podcast.itunes_explicit('clean')
#     fg.podcast.itunes_(SHOW_METADATA['subtitle'])
#     fg.podcast.itunes_summary(SHOW_METADATA['subtitle'])
#     fg.id(SHOW_METADATA['url'])
#     fg.title(SHOW_METADATA['title'])
#     fg.author({'name': SHOW_METADATA['author'], 'email': SHOW_METADATA['email']})
#     fg.link(href=SHOW_METADATA['url'], rel='alternate')
#     fg.logo(SHOW_METADATA['url'] + '/coverArt/000.png')
#     fg.subtitle(SHOW_METADATA['subtitle'])
#     fg.link(href=SHOW_METADATA['url'], rel='self')
#     fg.language('de')
#     fg.copyright('(c)2020')

#     return fg


# -- unmarkify ---------------------------------
def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
markdown.Markdown.output_formats["plain"] = unmark_element
__md = markdown.Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    return __md.convert(text)

#Used in the episode Class below.
# -- slugify episode titles ---------------------------------

# def slugify(text):
    text = (text.replace("Ä", "Ae")
            .replace("Ö", "Oe")
            .replace("Ü", "Ue")
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
            .replace(" ", "_"))

    return re.sub(r"[^\w\-]", "", text)

#THIS SEEMS IMPORTANT!!
class Episode(object):
    def __init__(self, mp3File):
        self.mp3File = mp3File
        self.number = int(os.path.basename(mp3File)[:-4])

        self._readJson()

        self.audiofile = eyed3.load(mp3File)
        self.chapters = list(self._readChapters())
        self.outputFilenameWithoutExtension = "%03d_-_%s" % (self.number, slugify(self.title)) #guess slugify is needed at this stage
        self._readMarkdown()

    def getFileSize(self):
        return os.path.getsize(self.mp3File)

    def getDuration(self):
        return self.audiofile.info.time_secs

    def _readJson(self):
        fileName = self.mp3File[:-3] + "json"
        with open(fileName) as f:
            metadata = json.load(f)

            self.title = metadata["title"]
            self.subtitle = metadata["subtitle"]
            self.summary = metadata["summary"] if "summary" in metadata else self.subtitle
            self.date = datetime.strptime(metadata["date"], DATE_INPUT_FORMAT)
            timezone = pytz.timezone('America/Chicago')
            self.date = timezone.localize(self.date)
            self.youtube = metadata["youtube"]

    def _readMarkdown(self):
        fileName = self.mp3File[:-3] + "md" # is this where it gets the mp3 name?
        with open(fileName) as f:
            self.showNotesMarkdown = f.read()
            self.showNotesPlain = unmark(self.showNotesMarkdown)

    def writePodloveJson(self):
        global SHOW_METADATA
        duration = self.getDuration()
        metadata = {
            "show": {
                "title": SHOW_METADATA['title'],
                "poster": "/static/files/coverart/"#"/coverArt/000.png", #is this dynamic or static?
                # "link": SHOW_METADATA["url"],
            },
            "title": self.title,
            "subtitle": self.subtitle,
            "summary": self.summary,
            "publicationDate": self.date.strftime(DATE_PODLOVE_FORMAT),
            "duration": "%02d:%02d:%02d.%03d" % (int(duration // 60 // 60), int(duration // 60), int(duration % 60), int((duration % 1) * 1000)),
            "poster": ("/static/files/coverart/%03d.png" % self.number), # ("/coverArt/%03d.png" % self.number)#this makes me think it is dynamic
            "link": "/episodes/" + self.outputFilenameWithoutExtension,
            "audio": [
                {
                    "url": "/" + self.targetMp3,
                    "size": str(self.getFileSize()),
                    "title": "MPEG Layer 3 Audio (mp3)",
                    "mimeType": "audio/mp3"
                },
            ],
            "chapters": []
        }

        for chapter in self.chapters:
            metadata["chapters"].append(
                {
                    # "start": chapter.start,
                    "start": "%02d:%02d:%02d.%03d" % (int(chapter.start // 60 // 60), int((chapter.start // 60) % 60), int(chapter.start % 60),
                                                      int((chapter.start % 1) * 1000)),
                    "title": chapter.title,
                    "href": "",
                    "image": ""
                })

        with open(OUTPUT_DIR + self.outputFilenameWithoutExtension + ".json", "w") as f:
            json.dump(metadata, f, ensure_ascii=False)  # write utf-8

    def _readChapters(self):
        fileName = self.mp3File[:-3] + "chapters"
        with open(fileName) as f:
            for line in f.readlines():
                elements = line.split("\t")
                yield Chapter(elements[2].strip(), float(elements[0]), float(elements[1]))
#THIS PROBABLY ISN'T NEEDED.
    def writeBlogEntry(self):
        global SHOW_METADATA
        with open(MARKDOWN_OUTPUT_DIR + self.outputFilenameWithoutExtension + ".markdown", "w") as f:
            # header
            f.write("---\n")
            f.write("layout:     episode\n")
            f.write("categories: podcast episode\n")
            f.write("mp3File:    %s.mp3\n" % self.outputFilenameWithoutExtension)
            f.write("podlove:    %s.json\n" % self.outputFilenameWithoutExtension)
            f.write("title:      %s\n" % repr(self.title))
            f.write("subtitle:   %s\n" % repr(self.subtitle))
            f.write("summary:    %s\n" % repr(self.summary))
            f.write("number:     %s\n" % self.number)
            f.write("cover:      /static/files/coverart/%03d.png\n" % self.number) #/coverArt/
            f.write("date:       %s\n" % self.date.strftime(DATE_BLOG_FORMAT))
            f.write("youtube:    %s\n" % self.youtube)
            f.write("---\n\n")

            # content
            f.write(self.showNotesMarkdown)

#THIS IS IMPORTANT
    def writeMp3Metadata(self):
        global SHOW_METADATA
        targetPath = OUTPUT_DIR + self.outputFilenameWithoutExtension + ".mp3"
        self.targetMp3 = targetPath
        copyfile(self.mp3File, targetPath)

        audiofile = eyed3.load(targetPath)
        # if audiofile.tag is None:
        audiofile.tag = Tag()
        audiofile.tag.title = self.title
        audiofile.tag.album = SHOW_METADATA["title"]
        audiofile.tag.artist = SHOW_METADATA["title"]
        audiofile.tag.genre = SHOW_METADATA["genre"]
        audiofile.tag.description = "description"
        audiofile.tag.comments.set(self.showNotesPlain)
        audiofile.tag.lyrics.set(self.showNotesPlain)
        audiofile.tag.images.set(type_=3,
                                 mime_type="image/png",
                                 description=SHOW_METADATA["title"],
                                 img_data=open("/static/files/coverart/%03d.png" % self.number, 'rb').read()) #./coverArt/

        i = 0
        chapterIds = []
        for chapter in self.chapters:
            chapterId = ("chp%d" % i).encode('utf-8')
            chap = audiofile.tag.chapters.set(chapterId,
                                              (chapter.start * 1000,
                                               chapter.end * 1000))  # seconds to milliseconds conversion
            chap.title = chapter.title
            chapterIds.append(chapterId)
            i += 1

        toc = "toc".encode('utf-8')
        audiofile.tag.table_of_contents.remove(toc)
        audiofile.tag.table_of_contents.set(toc,
                                            toplevel=True,
                                            child_ids=chapterIds,
                                            description="Table of Contents")

        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
#THIS PROBABLY ISN'T NEEDED
    def addToFeed(self, fg):
        global SHOW_METADATA
        absoluteMp3Url = "%s%s" % (SHOW_METADATA["url"], self.targetMp3)
        absoluteUrl = "%sepisodes/%s" % (SHOW_METADATA["url"], self.outputFilenameWithoutExtension)
        fe = fg.add_entry()
        fe.id(absoluteMp3Url)
        fe.title(self.title)
        fe.description(self.summary)
        fe.pubDate(self.date.strftime("%a, %d %b %Y %H:%M:%S +0001"))
        fe.link(href=absoluteUrl, rel="alternate")
        fe.enclosure(absoluteMp3Url, str(self.getFileSize()), 'audio/mpeg')
        duration = self.getDuration()
        fe.podcast.itunes_duration('%02d:%02d:%02d' % (int(duration // 60 // 60), int(duration // 60), int(duration % 60)))
        fe.podcast.itunes_image("%s/static/files/coverart/%03d.png" % (SHOW_METADATA["url"], self.number)) #coverArt/
        fe.podcast.itunes_summary(self.summary[:30] + (" [...]") if len(self.summary) > 30 else "")
        fe.podcast.itunes_subtitle(self.subtitle)
        fe.podcast.itunes_author(SHOW_METADATA['author'])
        fe.guid(permalink=True)


class Chapter(object):
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end

#THE LAST PART OF THIS PROBABLY ISN'T NEEDED
# def readFiles(srcDir):
#     fg = generateFeed()

#     Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
#     Path(MARKDOWN_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
#     episodes = []
#     for mp3File in sorted(glob.glob(DATA_SRC_DIR + "*.mp3")):
#         episode = Episode(mp3File)
#         episodes.append(episode)

#         # print(episode.number, episode.title, episode.date)
#         episode.writeMp3Metadata()
#         episode.writeBlogEntry()
#         episode.writePodloveJson()
#         # episode.addToFeed(fg)

#     fg.rss_file('podcast.xml', pretty=True)


# readFiles("/static/files/00test/") #./episodes_src/
