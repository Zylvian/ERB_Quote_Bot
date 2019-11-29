import os
import time

import praw
from prawcore import PrawcoreException
from utils import Util
import logging as log


class RedditBot:

    def __init__(self):
        self.LOCK_FILE = 'lockfile.lock'

        log.basicConfig(
            filename='bot_logging.log',
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=log.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')

        self.util = Util()
        self.bot_name = "ERB_Quote_Bot"

    def _comment_responder(self):
        reddit = praw.Reddit('bot2')

        subreddit_name = self.util.get_subs()

        subreddit = reddit.subreddit("+".join(subreddit_name))

        for comment in subreddit.stream.comments(skip_existing=True):

            if os.path.isfile(self.LOCK_FILE):

                # Parse the comment
                text = comment.body.encode(encoding="utf-8", errors="strict")

                if isinstance(text, (bytes, bytearray)):
                    text = text.decode("utf-8")

                # Gets next lyric or is None.
                next_lyric = self.util.get_next_lyric(text)

                is_self = str(comment.author.name) == str(self.bot_name)

                # If a triggerword is in the string...

                log.info("In response to {} I got {}, and the user posting is {}".format(text, next_lyric, str(comment.author.name)))

                if next_lyric and not is_self:
                    response_string = next_lyric

                    try:
                        comment.reply(response_string)
                    except praw.exceptions.APIException as e:
                        log.info(str(e))
                        log.info("Ratelimit probably, we try another time")

            else:
                return

    def run(self):
        with open(self.LOCK_FILE, 'w'): pass
        print("Lock file made (presumably)")
        log.info("STARTED")
        # remove to kill

        self.run_cont()

    def run_cont(self):

        try:
            self._comment_responder()
        except PrawcoreException as e:
            log.info(e)
            log.info("Sleeping for 1 minute...")
            time.sleep(60)
            self.run_cont()
        except KeyboardInterrupt:
            raise
        except UnicodeEncodeError as e:
            log.info(e)
            log.info("The unicode errors are back.")
            time.sleep(10)
            self.run_cont()
        except Exception as e:
            log.info(e)
            log.info("Something random happened, sleeping for 10 sec.")
            time.sleep(10)
            self.run_cont()


if __name__ == '__main__':
    RedditBot().run()
