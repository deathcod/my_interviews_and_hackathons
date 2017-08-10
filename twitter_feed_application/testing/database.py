from pymongo import MongoClient


class database(object):
    """docstring for database"""

    def __init__(self, database):
        client = MongoClient()
        self.db = client[database]

    def __get_all_doc(self, collection, where):
        collection = self.db[collection]
        return [i for i in collection.find(where)]

    def __get_first(self, collection, where):
        collection = self.db[collection]
        return collection.find_one(where)

    def __insert(self, collection, val):
        collection = self.db[collection]
        val['_id'] = collection.count() + 1
        collection.insert(val)
        pass

    def __delete(self, collection, where):
        collection = self.db[collection]
        collection.remove(where)
        pass

    def __update(self, collection, query, update):
        collection = self.db[collection]
        collection.update(query, {'$set': update})
        pass

    def store_user(self, user_credentials):
        post = dict()

        post['name'] = user_credentials['screen_name'].encode('utf-8', 'replace')
        post['OAUTH_TOKEN'] = user_credentials['oauth_token'].encode('utf-8', 'replace')
        post['OAUTH_SECRET_TOKEN'] = user_credentials['oauth_token_secret'].encode('utf-8', 'replace')
        self.__insert('users', post)
        pass

    # get user data
    def get_user(self, user_id=None, user_name=None):
        if user_id is not None:
            user = self.__get_first('users', {'_id': user_id})
        else:
            user = self.__get_first('users', {'name': user_name})

        return user

    #get vote status
    def get_vote_status(self, data, user_id):
        for i in data:
            vote = self.__get_first('vote', {'user_id': user_id, 'tweet_id': i['id_str']})
            if vote is None:
                i['status'] = "N"
            else:
                i['status'] = vote["status"]
        return data

    #count votes, views for a tweets
    def count_for_tweet(self, tweet):
        upvote = self.__get_all_doc('vote', {'tweet_id' : tweet['id_str'], 'status' : 'U'})
        if upvote is not None:
            tweet['upvote'] = len(upvote)

        downvote = self.__get_all_doc('vote', {'tweet_id': tweet['id_str'], 'status': 'D'})
        if downvote is not None:
            tweet['downvote'] = len(downvote)

        view_count = self.__get_first('tweet', {'tweet_id' : tweet['id_str']})
        if view_count is not None:
            tweet['view_count'] = view_count['count']

        return tweet

    # update user credentials
    def update_user(self, user_credentials=None, session_data=None):
        query = dict()
        update = dict()

        if user_credentials is not None:
            query['name'] = user_credentials['screen_name'].encode('utf-8', 'replace')
            update['OAUTH_TOKEN'] = user_credentials['oauth_token'].encode('utf-8', 'replace')
            update['OAUTH_SECRET_TOKEN'] = user_credentials['oauth_token_secret'].encode('utf-8', 'replace')

        else:
            query['_id'] = session_data['user_id']
            update['session_data'] = session_data['data'].encode('utf-8', 'replace')

        self.__update('users', query, update)
        pass

        return '{"remark": "successful"}'

    def update_views(self, data):

        tweet = self.__get_first('tweet', data)

        if tweet is None:
            data["count"] = 1
            self.__insert('tweet', data)

        else:
            query = {"tweet_id" : tweet["tweet_id"]}
            update = {"count" : tweet['count']+1}
            self.__update('tweet', query, update)

        return '{"remark" : "successful"}'
        pass

    def update_votes(self, data):
        vote = self.__get_first('vote', {"user_id": data["user_id"], "tweet_id" : data["tweet_id"]})
        if vote is None:
            self.__insert('vote', data)
        else:
            query = {"tweet_id": data["tweet_id"], "user_id" : data['user_id']}
            update = {"status" : data["status"]}
            self.__update('vote', query, update)
        pass

        return '{"remark": "successful"}'
