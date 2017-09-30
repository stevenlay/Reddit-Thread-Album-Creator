import praw
import sys



reddit = praw.Reddit("imgurAlbum")
subreddit = sys.argv[1]
print(subreddit)
