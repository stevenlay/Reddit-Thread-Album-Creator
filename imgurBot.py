import praw
import sys
from imgurpython import ImgurClient 
import lib.config 
import requests

LIMIT = 10
HREF_SIZE = 6
BUFFER_SIZE = 2

client_id = lib.config.client_id
client_secret = lib.config.client_secret
client_user = lib.config.client_user
client_password = lib.config.client_password
client = ImgurClient(client_id, client_secret)

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
     
    description_start = comment_text.find(link) + len(link) + BUFFER_SIZE
    description_end = comment_text.find("</a", description_start)
    description = comment_text[description_start:description_end]
    print("(%d) " % top_level_comment.score + "\"" + description + "\" - " + top_level_comment.author.name)

    if "/a/" in link:
        album_id = link[len("https://imgur.com/a/"):]
        direct_img = client.get_album_images(album_id)
        if len(direct_img) == 1:
            imgur_img = direct_img[0].link
            print(imgur_img)
    else: 
        print(link)

    COUNTER += 1

