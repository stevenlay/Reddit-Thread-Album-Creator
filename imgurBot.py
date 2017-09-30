import praw
import sys


#bot
reddit = praw.Reddit("imgurAlbum")
submission = reddit.submission(url="%s" % sys.argv[1])
submission.comment_sort = "top"
submission.comments.replace_more(limit=0)

for top_level_comment in submission.comments:
    print(top_level_comment.body)

