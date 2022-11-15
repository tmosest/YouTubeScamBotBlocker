# YouTubeScamBotBlocker

This repo can be used to block and ban users who post scam messages on accounts.

It uses V3 of the YouTube API to do so by:
    - Getting all video ids
    - Getting comment threads from videos ids.
    - Get inner comments using a comment api.
    - Compares the comment's author and text to the following list of key words in `./src/YouTubeApi.py` that need to be set by the user at the moment:
        ```
                BANNED_USERNAME_KEYWORDS = []
                BLOCKED_USERNAME_KEYWORDS = []
                BLOCKED_COMMENT_KEYWORDS = []
        ```
    - Use `setModerationStatus` to delete the comment if any words from `BLOCKED_USERNAME_KEYWORDS` are found in the `username` and `BLOCKED_COMMENT_KEYWORDS` for comments.
    - If the username contains anything from `BANNED_USERNAME_KEYWORDS` then they will get blocked from your channel as well.

## Setup

* Need to setup a OAuth Api in the Google Console. I'll explain that in the video. [Slack Overflow Answer](https://stackoverflow.com/questions/40136699/using-google-api-for-python-where-do-i-get-the-client-secrets-json-file-from)
* Need python3 to run this.
* Then clone or download this repo.
* Use pip3 to install the dependencies. `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
* Test run without blocking or banning with `python3 ./src/YouTubeApi.py` if there are no errors the project can be run.
* Update `BANNED_USERNAME_KEYWORDS = ['message me on', 'example2', 'example3']` at the bottom of `./src/YouTubeApi.py` to include keywords that should ban a user name.
* Update `BLOCKED_USERNAME_KEYWORDS = ['message me on', 'example2', 'example3']` to include keywords that should delete a user's comments without banning them.
* Update `BLOCKED_COMMENT_KEYWORDS = ['message me on', 'example2', 'example3']` to include keywords that should delete a user's comments without banning them based on comment content instead of user name.


## TODO
* Pagination. At the moment it will only do 100 videos and 100 comment threads with 100 inner comments at most.
* Create a global database for scammer names that could be used for multiple accounts. Using Google sheets API.
* `BANNED_COMMENT_KEYWORDS` for banning users based on comment strings instead of username strings?

## Notes
* I enjoy automating things and helping out. If you have a problem or manual task that can be automated reach out.
* Hopefullly YouTube will just add the ability to block bad user names on their own.