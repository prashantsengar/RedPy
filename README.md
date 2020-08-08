# RedPy
A Python wrapper to download images from Reddit

## Installation

`pip3 install RedPy`

-- Or --

`git clone https://github.com/prashantsengar/RedPy`

`cd RedPy`


## Usage

In a Python shell

```python3
>>> from redpy import RedPy
# create an instance
# Creatinga an instance requires you to enter a user-agent. From the PRAW documentation
"A user agent is a unique identifier that helps Reddit determine the source of network requests. To use Reddit’s API, you need a unique and descriptive user agent. The recommended format is <platform>:<app ID>:<version string> (by u/<Reddit username>). For example, android:com.example.myredditapp:v1.2.3 (by u/kemitche). Read more about user agents at Reddit’s API wiki page."
>>> red = RedPy('web:redpy:v2.1 (by u/myusername)')

# Downloading requires a subreddit, and some other optional-arguments. 
# subreddit: the text after r/. For example, for r/pics, subreddit=pics
# number: The number of items to download
# sort_option: hot/top/new as per the Reddit sort options
# num_of_images: The number of images to download
# num_of_videos: The number of videos to download.
## if the above two arguments are not provided, the number of images and videos are downloaded at random.
>>> red.download(subreddit, number=5, sort_option=None,
                 num_of_images=0, num_of_videos=0)
                 
# Example
>>> red.download('pics', 5, top)

# Download 2 videos and 7 images
>>> red.download('funny', 9, top, num_of_videos=2)
```

# To-do
1. Other than downloading images, also return the download URLs of the media files
2. Make it system path independent
