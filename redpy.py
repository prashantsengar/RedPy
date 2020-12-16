import requests as _requests
import os as _os
import random


class Redpy:

    def __init__(self, user_agent):
        """Enter a user agent"""
        # print("hello")
        self.user = user_agent
        self.json_data = None

    def download(self, subreddit, number=5, sort_option=None,
                 num_of_images=0, num_of_videos=0):
        """
        Download images and videos from given subreddit
        - subreddit: name of subreddit from where to download
        - number: number of media files to download
        - sort_option: sort the subreddit using 'hot','new','top'
        - num_of_images: number of images to be downloaded
        - num_of_videos: number of videos to be downloaded
        if num_of_images and num_of_videos are not given, then random
        numbers are used
        """
        if sort_option is None:
            sort_option = ''
        if ((not num_of_images) and (not num_of_videos)):
            num_of_images = random.randint(0, number)
            num_of_videos = number - num_of_images

        subreddit = subreddit.split('/')[-1] if "/" in subreddit else subreddit

        self.json_data = self._generateJSON(subreddit, sort_option)
        self.download_images(subreddit, num_of_images, sort_option)
        self.download_videos(subreddit, num_of_videos, sort_option)

    def download_images(self, subreddit, number=5, sort_option=None):
        """Downloads images from subreddit.
            subreddit="Name of subreddit"
            number=Number of images to be downloaded
            sort_option=new/hot/top
        """
        if sort_option is None:
            sort_option = ''
        subreddit = subreddit.split('/')[-1] if "/" in subreddit else subreddit

        if self.json_data is None:
            self.json_data = self._generateJSON(subreddit, sort_option)

        self._DownloadFiles(self._getImages(self.json_data, number))

    def _DownloadFiles(self, image_links):

        if not self.createFolder():
            print("Error creating folder")
            return

        index = 0  # used to name the files
        for image_link in image_links:
            image_link = image_link.replace('amp;', '')
            f = _requests.get(image_link)
            if f.status_code == 200:
                with open(_os.path.join(_os.getcwd(), "red_media",
                        f"{index}.jpg"), 'wb') as media_file:
                    for chunk in f.iter_content(100000):
                        media_file.write(chunk)
                print("Downloaded")
                index += 1
        print("Download complete")

    def _getImages(self, jsonfile, number_of_files):

        images = []  # contains links of images
        for index in range(number_of_files):
            try:
                images.append(jsonfile['data']['children'][index]['data']
                              ['preview']['images'][0]['source']['url'])
            except Exception as e:
                print("Exception: ", e)
        return images

    def download_videos(self, subreddit, number=5, sort_option=None):
        if sort_option is None:
            sort_option = ''
        """Downloads Videos from subreddit.
            subreddit="Name of subreddit"
            number=Number of videos to be downloaded
            sort_option=new/hot/top
        """
        subreddit = subreddit.split('/')[-1] if "/" in subreddit else subreddit

        if self.json_data is None:
            self.json_data = self._generateJSON(subreddit, sort_option)

        self._DownloadVideoFiles(self._getVideos(self.json_data, number))

    def _DownloadVideoFiles(self, video_links):

        if not self.createFolder():
            print("Error creating folder")
            return

        index = 0  # used to name the files
        for video_link in video_links:
            video_link = video_link.replace('amp;', '')
            f = _requests.get(video_link)

            if f.status_code == 200:
                with open(f'{_os.getcwd()}/red_media/{index}.mp4'
                          , 'wb') as media_file:
                    for chunk in f.iter_content(100000):
                        media_file.write(chunk)
                print("Downloaded")
                index += 1
        print("Download complete")

    def _getVideos(self, jsonfile, number_of_files):
        videos = []

        for i in range(number_of_files):
            try:
                videos.append(jsonfile['data']['children'][i]
                              ['data']['preview']
                              ['reddit_video_preview']['fallback_url'])
            except Exception as e:
                print("Exception: ", e)
        return videos

    def _generateJSON(self, subreddit, sort_option):
        self.url = 'https://www.reddit.com/r/' + \
            subreddit + '/' + sort_option + '.json'
        print(self.url)

#        session = _requests.Session()
#        session.headers.update({'User-Agent': self.user})
#        session.headers.update({'user-agent': 'lmao rofl@matapita.com'})

        res = _requests.get(self.url, headers={'user-agent': self.user})
        if res.status_code != 200:
            print("Could not download")
            print("Change the User-Agent header")
            raise Exception(f"Error Status Code: {res.status_code}")
        return res.json()

    @staticmethod
    def createFolder():
        try:
            red_media = _os.path.join(_os.getcwd(), 'red_media')
            if not _os.path.exists(red_media):
                _os.mkdir(red_media)
                return True
            return True
        except Exception as e:
            print(e)
            return False
