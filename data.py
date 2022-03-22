import re
from datetime import datetime
from git import Object
import pandas as pd
import json

class Data:
    HASHTAGS = {'hashtags_count':{}, 'has_tags':0}
    MENTIONS = {'mentions_count':{}, 'has_mentions':0}

    def __init__(self, tweets):
        self.tweets = tweets

        # Reset the value, everytime the class being evoked
        Data.HASHTAGS['hashtags_count'] = {}
        Data.MENTIONS['mentions_count'] = {}
        Data.HASHTAGS['has_tags'] = 0
        Data.MENTIONS['has_mentions'] = 0

    @property
    def data_object(self):
        result = {'tweets':[]}
        for tweet in self.tweets:
            obj = {'id':tweet.id, 'user_id':tweet.user_id, 'date':tweet.datetime,
                   'username':tweet.username, 'name':tweet.name, 'tweet':tweet.tweet, 
                   'replies_count':tweet.replies_count, 'likes_count':tweet.likes_count, 
                   'retweets_count':tweet.retweets_count}
            result['tweets'].append(obj)
        result_json = json.dumps(result)
        return result_json

    def get_most_liked_tweet(self):
        most_liked = self.tweets[0]
        for tweet in self.tweets[1:]:
            if tweet.likes_count > most_liked.likes_count:
                most_liked = tweet
        return most_liked

    def get_most_retweeted_tweet(self):
        most_retweeted = self.tweets[0]
        for tweet in self.tweets[1:]:
            if tweet.retweets_count  > most_retweeted.retweets_count :
                most_retweeted = tweet
        return most_retweeted

    def get_most_replied_tweet(self):
        most_replied = self.tweets[0]
        for tweet in self.tweets[1:]:
            if tweet.replies_count  > most_replied.replies_count :
                most_replied = tweet
        return most_replied

    def count_tags(self):
        for item in self.tweets:
            tags = [x.lower() for x in re.findall(r'#(\w+)', item.tweet)]
            if tags: Data.HASHTAGS['has_tags'] += 1

            for tag in tags:
                if tag not in Data.HASHTAGS['hashtags_count']:
                    Data.HASHTAGS['hashtags_count'][tag] = 0
                Data.HASHTAGS['hashtags_count'][tag] += 1
        return Data.HASHTAGS['hashtags_count'], Data.HASHTAGS['has_tags']

    def count_mentions(self):
        for item in self.tweets:
            mentions = [x.lower() for x in re.findall(r'@(\w+)', item.tweet)]
            if mentions: Data.MENTIONS['has_mentions'] += 1

            for mention in mentions:
                if mention not in Data.MENTIONS['mentions_count']:
                    Data.MENTIONS['mentions_count'][mention] = 0
                Data.MENTIONS['mentions_count'][mention] += 1
        return Data.MENTIONS['mentions_count'], Data.MENTIONS['has_mentions']

    def get_dates(self):
        dates = list()
        for item in self.tweets:
            # Get all the dates
            date_str = f"{item.datetime.split(' ')[0]} {item.datetime.split(' ')[1]}"
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            dates.append(date_obj)
        return dates

    def get_tags_mentions_dataframes(self):
        tags_df = pd.DataFrame({'Hashtag':[x for x in Data.HASHTAGS["hashtags_count"].keys()], 
                                'Count':[x for x in Data.HASHTAGS["hashtags_count"].values()],
                                'Percentage':[(x / len(self.tweets) * 100) for x in Data.HASHTAGS["hashtags_count"].values()]
                                })
        tags_df.sort_values(by='Count', ascending=False, inplace=True)
        tags_df.reset_index(drop=True, inplace=True)

        mentions_df = pd.DataFrame({'Mention':[x for x in Data.MENTIONS["mentions_count"].keys()],
                                    'Count':[x for x in Data.MENTIONS["mentions_count"].values()],
                                    'Percentage':[(x / len(self.tweets) * 100) for x in Data.MENTIONS["mentions_count"].values()]
                                    })
        mentions_df.sort_values(by='Count', ascending=False, inplace=True)
        mentions_df.reset_index(drop=True, inplace=True)

        return tags_df, mentions_df

    
