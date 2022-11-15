from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import json
import time
import re
from GAuth import GAuth

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

class YouTubeApi:

    def __init__(self, gauth: GAuth) -> None:
        self.service = build('youtube', 'v3', credentials=gauth.get_creds())

    def execute(self, request):
        try:
            data = request.execute();
            return data

        except HttpError as error:
            print(F'An error occurred: {error}')

        return None

    def get_videos(self, channel_id, parts):
        return self.execute(self.service.channels().list(part=parts, id=channel_id))

    def get_my_videos(self):
        # TODO loop more than 100 videos
        return self.execute(self.service.search().list(
                part="snippet",
                forMine=True,
                maxResults=100,
                type="video"
        ))

    def get_comments(self, videoId, parts): 
        return self.execute(self.service.commentThreads().list(part=parts, videoId=videoId))

    def get_replies(self, parentId):
        return self.execute(self.service.comments().list(
        part="id,snippet",
        maxResults=100,
        parentId=parentId
    ))

    def reject_comment(self, commentId, banAuthor=False):
        return self.execute(self.service.comments().setModerationStatus(
                id=commentId,
                moderationStatus="rejected",
                banAuthor=banAuthor
        ))

    def delete_block_or_ban(self, BANNED_USERNAME_KEYWORDS, BLOCKED_USERNAME_KEYWORDS, BLOCKED_COMMENT_KEYWORDS):
        videos_data = self.get_my_videos()
        print(videos_data)
        for video in videos_data.get("items"):
            video_id = video.get("id").get("videoId")
            print (f"Video Id {video_id}")
            comments = self.get_comments(video_id, "snippet,replies,id",)
            print(f"Comments: {comments}")
            # comments.list with id if there are replies.
            if comments == None:
                continue

            comments = comments.get("items")
            
            for comment in comments:
                snippet = comment.get("snippet")
                if "topLevelComment" in snippet:
                    top_comment = snippet.get("topLevelComment")
                    comment_id = top_comment.get("id")
                    print(f"Comment id: {comment_id}")
                    snippet = top_comment.get("snippet")
                    author = snippet.get("authorDisplayName")
                    text = snippet.get("textDisplay")
                    print(f"Author: {author}")
                    print(f"Text: {text}")
                else:
                    comment_id = comment.get("id")
                    text = snippet.get("textDisplay")
                    author = snippet.get("authorDisplayName")
                    print(f"comment_id = {comment_id}\n author = {author}\n text = {text}")


                should_delete = False
                should_ban = False

                if "replies" in comment:
                    replies = self.get_replies(comment_id).get("items")
                    comments += replies

                for blocked_comment in BLOCKED_COMMENT_KEYWORDS:
                    if re.search(blocked_comment, text, re.IGNORECASE):
                        should_delete = True
                        break
                        

                for blocked_username in BLOCKED_USERNAME_KEYWORDS:
                    if should_delete or re.search(blocked_username, author, re.IGNORECASE):
                        should_delete = True
                        break    
                
                for banned_username in BANNED_USERNAME_KEYWORDS:
                    if  re.search(banned_username, author, re.IGNORECASE):
                        should_ban = True
                        break
                
                if should_delete or should_ban:
                    print(f"should_delete = {should_delete}\n should_ban = {should_ban}\n author = {author}\n text = {text}")
                    self.reject_comment(comment_id, should_ban)


# this is the main section for this code.
if __name__ == '__main__':
    # Set banned user names here such as "message me at", "whatsapp", "telent"
    BANNED_USERNAME_KEYWORDS = []
    # This is similar to above but it doens't ban them from your channel it just blocks them.
    BLOCKED_USERNAME_KEYWORDS = []
    # This blocks users based on their comments as well.
    BLOCKED_COMMENT_KEYWORDS = []

    auth = GAuth.default()
    youtube_client = YouTubeApi(auth)
    videos_data = youtube_client.delete_block_or_ban(BANNED_USERNAME_KEYWORDS, BLOCKED_USERNAME_KEYWORDS, BLOCKED_COMMENT_KEYWORDS)
