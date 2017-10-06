import praw
import sys
LIMIT = 5
HREF_SIZE = 6
BUFFER_SIZE = 2
#bot
reddit = praw.Reddit("imgurAlbum")
submission = reddit.submission(url="%s" % sys.argv[1])
submission.comment_sort = "top"
submission.comments.replace_more(limit=0)

COUNTER = 0
for top_level_comment in submission.comments:
        
    #stop once comment is reached
    if COUNTER == LIMIT:
        break
    if top_level_comment.body != "[deleted]":
       comment_text = top_level_comment.body_html
      
       #get image link posted
       image_start = comment_text.find("href=\"") + HREF_SIZE
       image_end = comment_text.find("\">", image_start)
       link = comment_text[image_start:image_end]
       print(link)
       
       #get description posted
       description_start = comment_text.find(link) + len(link) + BUFFER_SIZE
       description_end = comment_text.find("</a", description_start)
       description = comment_text[description_start:description_end]
       print("(%d) " % top_level_comment.score + top_level_comment.author.name + " -   " +  description)
        
    COUNTER += 1

