from textblob import TextBlob
import re

class Train:
    def __init__(self, df):
        self.df = df

    def clean_text(self):
        # Remove mention '@'
        self.df.tweet = self.df.tweet.apply(lambda x: re.sub('@[a-zA-Z0-9_]+', '', x))
    
        # Remove tag '#' but not the word
        self.df.tweet = self.df.tweet.apply(lambda x: re.sub('#', '', x))
        
        # Remove url
        self.df.tweet = self.df.tweet.apply(lambda x: re.sub('http[\S]+', '', x))
        
        # Remove contractions don't => dont  
        self.df.tweet = self.df.tweet.apply(lambda x: x.replace("'", ''))
        self.df.tweet = self.df.tweet.apply(lambda x: x.replace("’", ''))
        
        # Remove numbers
        self.df.tweet = self.df.tweet.apply(lambda x: re.sub('[0-9]\S+|[0-9]','' , x))
        
        # Filter words only     
        self.df.tweet = self.df.tweet.apply(lambda x: ' '.join(re.findall('[a-zA-Z]+', x)))
        
        # Strip 
        self.df.tweet = self.df.tweet.apply(lambda x: x.strip())

        # Remove 'amp'
        self.df.tweet = self.df.tweet.apply(lambda x: x.replace('amp', ''))
        
        # Capitalize
        self.df.tweet = self.df.tweet.apply(lambda x: x.capitalize())
        return self.df


    def language_processing(self):
            # Words correction 
            self.df.tweet = self.df.tweet.apply(lambda x: TextBlob(x).correct())
    
    def text_blob(self):
        self.df['polarity'] = self.df.tweet.apply(lambda x: TextBlob(x).sentiment.polarity)
        self.df['subjectivity'] = self.df.tweet.apply(lambda x: TextBlob(x).sentiment.subjectivity)
        return self.df

        
    def sentiment(self):
        def determine(x):
            if x < -0.25:
                return str(-1)
            elif x > 0.25:
                return str(1)
            else:
                return str(0)
            
        self.df['sentiment'] = self.df.polarity.apply(determine)
        return self.df
    
    def run_all(self):
        self.clean_text()
        self.text_blob()
        self.sentiment()
        
        return self.df