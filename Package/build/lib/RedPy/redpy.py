import requests as _requests
import os as _os
from fake_useragent import UserAgent
fav = 'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)'
ua = UserAgent(fallback = fav)

class Redpy:

    def __init__(self, user):
        """Enter a user agent"""
        print("hello")
        self.user = user

    def download(self, subreddit, number=5, sort_option=None):
        """Downloads images from subreddit.
            subreddit="Name of subreddit"
            number=Number of images to be downloaded
            sort_option=new/hot/top
        """
        subreddit.strip('/')
        if sort_option == None:
            sort_option = ''

        self.url = 'https://www.reddit.com/r/' + subreddit + '/'+  sort_option  +  '.json'
        print(self.url)

##        session = _requests.Session()
####        session.headers.update({'User-Agent': self.user})
##        session.headers.update({'user-agent': 'lmao rofl@matapita.com'})

        self.user = {'user-agent':self.user}
        res = _requests.get(self.url, headers=self.user)

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

        index = 0 #used to name the files
        for image_link in image_links:
            image_link = image_link.replace('amp;', '')
            f = _requests.get(image_link)

            if f.status_code==200:
                media_file = open(f'{_os.getcwd()}/red_media/{index}.jpg', 'wb')

                for chunk in f.iter_content(100000):
                    media_file.write(chunk)
                media_file.close()
                print("Downloaded")
                index+=1
        print("Download complete")
        global flag
        flag=1




    def _getImages(self, jsonfile, number_of_files):

        images = [] #contains links of images
        for index in range(number_of_files):
            try:
                images.append(jsonfile['data']['children'][index]['data']['preview']['images'][0]['source']['url'])
            except Exception as e:
                print(e)
        return images

    @staticmethod
    def createFolder():
        try:
            if not _os.path.exists(f'{_os.getcwd()}\\red_media'):
                _os.mkdir(f'{_os.getcwd()}\\red_media')
                return True
            return True
        except Exception as e:
            print(e)
            return False
