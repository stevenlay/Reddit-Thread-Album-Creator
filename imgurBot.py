from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import praw
import sys
from imgurpython import ImgurClient 
import lib.config 
import requests

LIMIT = 5
HREF_SIZE = 6
BUFFER_SIZE = 2

client_id = lib.config.client_id
client_secret = lib.config.client_secret
client_user = lib.config.client_user
client_password = lib.config.client_password
client = ImgurClient(client_id, client_secret)

auth_url = (client.get_auth_url('pin'))
print(auth_url)
driver = webdriver.Chrome()
driver.get(auth_url)

user = driver.find_element_by_xpath('//*[@id="username"]')
user.clear()
password = driver.find_element_by_xpath('//*[@id="password"]')
password.clear()
user.send_keys(client_user)
password.send_keys(client_password)

creds = client.authorize(input("Pin: "), 'pin')
client.set_user_auth(creds['access_token'], creds['refresh_token'])


#bot
reddit = praw.Reddit("imgurAlbum")
submission = reddit.submission(url="%s" % sys.argv[1])
title_and_link = submission.title + " - " + submission.url
print(title_and_link)
albumConfig = {
    'title': submission.title,
    'description': sys.argv[1],
    'ids': ["jaqIcKk", "ZLfpBd2"]
}

album = client.create_album(albumConfig)
print(album["id"])

submission.comment_sort = "top"
submission.comments.replace_more(limit=0)

img_cfg = {
    'album': album["id"]
}

image = client.upload_from_url(submission.url, config=img_cfg, anon=False)



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
    tag = ("(%d) " % top_level_comment.score + "\"" + description + "\" - " + top_level_comment.author.name)
    print(tag)
    if "/a/" in link:
        album_id = link[len("https://imgur.com/a/"):]
        direct_img = client.get_album_images(album_id)
        if len(direct_img) == 1:
            imgur_img = direct_img[0].link
            link = imgur_img
        print(link)

    COUNTER += 1
    
    photoConfig = {
            'album': deletehash,
            'description': tag,
    }

    image = client.upload_from_url(link, config=photoConfig, anon=True)

print("https://imgur.com/a/" + album["id"])
