import requests as _requests
import os as _os
import random


class Redpy:
    def __init__(self, user):
        """Enter a user agent"""
        print("hello")
        self.user = user

    def download(
        self, subreddit, number=5, sort_option=None, num_of_images=0, num_of_videos=0
    ):
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
        if (not num_of_images) and (not num_of_videos):
            num_of_images = random.randint(0, number)
            num_of_videos = number - num_of_images
        self.download_images(subreddit, num_of_images, sort_option)
        self.download_videos(subreddit, num_of_videos, sort_option)

    def download_images(self, subreddit, number=5, sort_option=None):
        """Downloads images from subreddit.
        subreddit="Name of subreddit"
        number=Number of images to be downloaded
        sort_option=new/hot/top
        """
        subreddit = subreddit.strip("/")
        if sort_option == None:
            sort_option = ""

        self.url = "https://www.reddit.com/r/" + subreddit + "/" + sort_option + ".json"
        print(self.url)

        ##        session = _requests.Session()
        ####        session.headers.update({'User-Agent': self.user})
        ##        session.headers.update({'user-agent': 'lmao rofl@matapita.com'})

        user = {"user-agent": self.user}
        res = _requests.get(self.url, headers=user)

        if res.status_code != 200:
            print("Could not download")
            print(res.status_code)
            return

        self._DownloadFiles(res.json(), number)

    def _DownloadFiles(self, jsonfile, number_of_files):
        image_links = self._getImages(jsonfile, number_of_files)

        if not self.createFolder():
            print("Error creating folder")
            return

        index = 0  # used to name the files
        for image_link in image_links:
            image_link = image_link.replace("amp;", "")
            f = _requests.get(image_link)

            if f.status_code == 200:
                media_file = open(f"{_os.getcwd()}/red_media/{index}.jpg", "wb")

                for chunk in f.iter_content(100000):
                    media_file.write(chunk)
                media_file.close()
                print("Downloaded")
                index += 1
        print("Download complete")
        global flag
        flag = 1

    def download_videos(self, subreddit, number=5, sort_option=None):
        """Downloads images from subreddit.
        subreddit="Name of subreddit"
        number=Number of images to be downloaded
        sort_option=new/hot/top
        """
        subreddit = subreddit.strip("/")
        if sort_option == None:
            sort_option = ""

        self.url = "https://www.reddit.com/r/" + subreddit + "/" + sort_option + ".json"
        print(self.url)

        user = {"user-agent": self.user}
        res = _requests.get(self.url, headers=user)

        if res.status_code != 200:
            print("Could not download")
            print(res.status_code)
            return
        self._DownloadVideoFiles(res.json(), number)

    def _DownloadVideoFiles(self, jsonfile, number_of_files):
        video_links = self._getVideos(jsonfile, number_of_files)

        if not self.createFolder():
            print("Error creating folder")
            return

        index = 0  # used to name the files
        for video_link in video_links:
            video_link = video_link.replace("amp;", "")
            f = _requests.get(video_link)

            if f.status_code == 200:
                media_file = open(f"{_os.getcwd()}/red_media/{index}.mp4", "wb")

                for chunk in f.iter_content(100000):
                    media_file.write(chunk)
                media_file.close()
                print("Downloaded")
                index += 1
        print("Download complete")
        global flag
        flag = 1

    def _getVideos(self, jsonfile, number_of_files):
        videos = []

        for i in range(number_of_files):
            try:
                videos.append(
                    jsonfile["data"]["children"][i]["data"]["preview"][
                        "reddit_video_preview"
                    ]["fallback_url"]
                )
            except Exception as e:
                print(e)
        return videos

    def _getImages(self, jsonfile, number_of_files):

        images = []  # contains links of images
        for index in range(number_of_files):
            try:
                images.append(
                    jsonfile["data"]["children"][index]["data"]["preview"]["images"][0][
                        "source"
                    ]["url"]
                )
            except Exception as e:
                print(e)
        return images

    @staticmethod
    def createFolder():
        try:
            if not _os.path.exists(f"{_os.getcwd()}\\red_media"):
                _os.mkdir(f"{_os.getcwd()}\\red_media")
                return True
            return True
        except Exception as e:
            print(e)
            return False


flag = 0

if __name__ == "__main__":
    import time

    while not flag:
        r = Redpy(f"lmao rofl@matapita.com")
        r.download(subreddit="pics", sort_option="top")
        time.sleep(3)
