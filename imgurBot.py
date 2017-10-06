import praw
import sys


#bot
reddit = praw.Reddit("imgurAlbum")
submission = reddit.submission(url="%s" % sys.argv[1])
submission.comment_sort = "top"
submission.comments.replace_more(limit=0)
LIMIT = 5
COUNTER = 0

for top_level_comment in submission.comments:
    if COUNTER == LIMIT:
        break
    if top_level_comment.body != "[deleted]":
       comment_text = top_level_comment.body_html
       link = comment_text[comment_text.index("href=\"") + 6:comment_text.rindex("\">")]
       print((link))
    COUNTER += 1

