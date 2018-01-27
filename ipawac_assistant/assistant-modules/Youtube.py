# -*- coding: utf-8-*-
import re
from client.plugins import youtube_controller
from client.plugins.utilities import diagnose
from client.plugins.utilities.vlcclient import VLCClient

WORDS = ["YOUTUBE"]


def handle(text, mic, speaker, profile, visionProcess):
    """
        Responds to user-input, typically speech text, by relaying the
        meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    if diagnose.check_executable('vlc'):
        vlc = VLCClient("127.0.0.1")
        vlc.connect()

    if re.search('YOUTUBE', text, re.IGNORECASE):
        if re.search(r'search', text, re.IGNORECASE):
            temp = re.search(" for (\w+)", text, re.IGNORECASE)
            word_1 = str(temp.group(1))
        elif re.search(r'play', text, re.IGNORECASE):
            temp = re.search("play (\w+)", text, re.IGNORECASE)
            word_1 = str(temp.group(1))

        videos = []
        options = {}
        options['q'] = word_1
        options['max_results'] = 2
        youtube_controller.youtube_search(options)

        # textToSearch= word_1
        # speaker.clean_and_say("Searching youtube for {} now..".format(word_1,))
        # query = urllib.parse.quote(textToSearch)
        # url = "https://www.youtube.com/results?search_query=" + query
        # results = requests.get(url)
        # results_parsed = BeautifulSoup(results.text, "html.parser")
        # for vid in results_parsed.findAll(attrs={'class':'yt-uix-tile-link'}):
        #     if not vid['href'].startswith("https://googleads.g.doubleclick.net/‌​"):
        #             vid_url = ('https://www.youtube.com' + vid['href'])
        #             # print (vid_url)
        #             # print (bool (vid_url.startswith('https://www.youtube.com/watch?v='))
        #             if (bool (vid_url.startswith('https://www.youtube.com/watch?v='))):
        #                 video = pafy.new(vid_url)
        #                 video = [video.title, video.duration,video.getbestaudio().url]
        #                 videos.append(video)
        # i=1
        # for video in videos:
        #     print ("{}.{}->{}".format(i,video[0],video[1]))
        #     i= i + 1
        #     vlc.add(video[2])

        # speaker.clean_and_say("Which video do you want to play?")
        # answer = mic.activeListen()
        # selected = videos [int(answer)-1]
        # speaker.clean_and_say("Playing")
        # if diagnose.check_executable('vlc'):
        #     print ("VLC player found, using it")
        #     print (selected[2])
        #     vlc = VLCClient("::1")
        #     vlc.connect()
        #     vlc.add("{}".format(selected[2]),)

    elif re.search('STOP', text, re.IGNORECASE):
        vlc.stop()

    elif re.search('pause', text, re.IGNORECASE):
        vlc.pause()

    elif re.search('play', text, re.IGNORECASE):
        vlc.play()

    elif re.search(r'next song\b', text, re.IGNORECASE):
        vlc.next()

    elif re.search(r'previous song\b', text, re.IGNORECASE):
        vlc.prev()

    elif re.search(r'(decrease|reduce|turn down|lower)', text, re.IGNORECASE):
        vlc.voldown(10)

    elif re.search(r'(increase|turn up)', text, re.IGNORECASE):
        vlc.volup(10)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(
        re.search(
            r'((play|search)|(music)|(song)|(volume))',
            text,
            re.IGNORECASE))
