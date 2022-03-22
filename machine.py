import twint 

class Machine:
    def __init__(self, params):
        self.params = params
        
    def run(self):
        config = twint.Config()
        config.Username = self.params.get('username')
        config.Search = self.params.get('key')
        config.Year = self.params.get('year_before')
        config.Since = f"{self.params.get('year_after')}-01-01"
        config.Store_object = True
        config.Limit = self.params.get('size')
        twint.output.clean_lists()
        twint.run.Search(config)

        self.tweets_as_objects = twint.output.tweets_list
        return self.tweets_as_objects



    def run2(self):
        config = twint.Config()
        config.Search = self.params.get('key')
        config.Year = self.params.get('year_before')
        config.Since = f"{self.params.get('year_after')}-01-01"
        config.Store_object = True
        config.Limit = self.params.get('size')
        twint.output.clean_lists()
        twint.run.Search(config)

        self.tweets_as_objects = twint.output.tweets_list
        return self.tweets_as_objects
