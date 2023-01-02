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

#Original Directions
#An episode requires five files in total. The naming convention for those files is simply
#the number of the episode with three digits and leading zeroes (e.g. 000.xyz, 001.xyz, 002.xyz, etc.).
# First, you need a cover art image for the episode. The cover art images are located in
# the coverArt directory and in the PNG format (coverArt/XXX.png). A resolution of
# 1400 x 1400 pixels is recommended for the most podcasting platforms.
# The other files must be located in the _episodes_src/ directory:

# I want to reduce this down since Castanet solves everything except for the generation of chapters
# into the mp3 file itself.
#Still need to reference the art, metadata json and the chapters

#changed folder structure to match my repo organization
DATA_SRC_DIR = "./static/files/"
OUTPUT_DIR = "./static/files/"
SHOW_METADATA = {
    "title": "The Linux Lemming Podcast",
    "genre": "Podcast",
    "url": "https://linuxlemming.com",
    "author": "Rastacalavera",
    "email": "rastacalavera@protonmail.com",
    "subtitle": "Your long subtitle."
}

DATE_INPUT_FORMAT = "%Y-%m-%d %H:%M"
DATE_BLOG_FORMAT = "%Y-%m-%d %H:%M:00 +0100"
DATE_PODLOVE_FORMAT = "%Y-%m-%dT%H:%M:00+01:00"


# -- slugify episode titles ---------------------------------

def slugify(text):
    text = (text.replace("Ä", "Ae")
            .replace("Ö", "Oe")
            .replace("Ü", "Ue")
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
            .replace(" ", "_"))

    return re.sub(r"[^\w\-]", "", text)

class Episode(object):
    def __init__(self, mp3File):
        self.mp3File = mp3File
        self.number = int(os.path.basename(mp3File)[:-4])

        self._readJson()

        self.audiofile = eyed3.load(mp3File)
        self.chapters = list(self._readChapters())
        # added an "e" to adhere to my naming convention
        self.outputFilenameWithoutExtension = "e%03d" % (self.number)
        # original
        # self.outputFilenameWithoutExtension = "%03d_-_%s" % (self.number, slugify(self.title))
#        self._readMarkdown()

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
#    def _readMarkdown(self):
#        fileName = self.mp3File[:-3] + "md"
#        with open(fileName) as f:
#            self.showNotesMarkdown = f.read()
#            self.showNotesPlain = unmark(self.showNotesMarkdown)

    def writePodloveJson(self):
        global SHOW_METADATA
        duration = self.getDuration()
        metadata = {
            "version": "1.2.0",
            "chapters": []
        }

        for chapter in self.chapters:
            metadata["chapters"].append(
                {
                    # "start": chapter.start,
                    "startTime": (int(chapter.start)),
                    "title": chapter.title,
                    "url": "",
                    "img": ""
                })

        with open(OUTPUT_DIR + self.outputFilenameWithoutExtension + ".json", "w") as f:
            json.dump(metadata, f, ensure_ascii=False)  # write utf-8

    def _readChapters(self):
        fileName = self.mp3File[:-3] + "chapters"
        with open(fileName) as f:
            for line in f.readlines():
                elements = line.split("\t")
                yield Chapter(elements[2].strip(), float(elements[0]), float(elements[1]))

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
#        audiofile.tag.comments.set(self.showNotesPlain)
#        audiofile.tag.lyrics.set(self.showNotesPlain)
        audiofile.tag.images.set(type_=3,
                                 mime_type="image/png",
                                 description=SHOW_METADATA["title"],
                                 img_data=open("./static/files/%03d.png" % self.number, 'rb').read())

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

class Chapter(object):
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end

def readFiles(srcDir):

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
#    Path(MARKDOWN_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    episodes = []
    for mp3File in sorted(glob.glob(DATA_SRC_DIR + "*.mp3")):
        episode = Episode(mp3File)
        episodes.append(episode)

#        print(episode.number, episode.title, episode.date)
        episode.writeMp3Metadata()
#        episode.writeBlogEntry()
        episode.writePodloveJson()
#        episode.addToFeed(fg)

readFiles("./static/files/")
