import requests
from datetime import datetime, timedelta
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import json
import os
import time
load_dotenv()

keyword = os.getenv('keyword')
bearer_token = os.getenv('bearer_token')
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

class Twitter:
    
    def __init__(self,bearer_token,word) -> None:
        
        self.headers = {'Authorization': 'Bearer {}'.format(bearer_token),}
        self.keyword = word
        self.savefile = []
        self.temp = []
        self.scrape_textfile = []
        self.read_twitter_alert_file()
        try:os.mkdir('media')
        except:pass
            
    def get_my_id(self):
        # get author ID of twitter account who is using api keys.
        url = 'https://api.twitter.com/2/users/me'
        auth = OAuth1(consumer_key,consumer_secret,access_token,access_token_secret)
        res = requests.get(auth=auth,url=url)
        if res.status_code == 401:
            print(json.dumps(res.json(), indent=4, sort_keys=True))
            print('')
            print(' Invalid API credentials')
            print('')
            print('To get API KEYS, visit Twitter Developer. TwitterDev. https://developer.twitter.com/')
            print('')
            return False
        self.my_ID = res.json()['data']['id']
        
    def repost_tweet(self,tweet_id):

        auth = OAuth1(consumer_key,consumer_secret,access_token,access_token_secret)
        id = self.my_ID
        payload = {"tweet_id": str(tweet_id)}
        response = requests.post(auth=auth, url="https://api.twitter.com/2/users/{}/retweets".format(id), json=payload,headers={"Content-Type":"application/json"})
        try:
            data = response.json()['data']['retweeted']
            if data == True or data == 'true':
                print(json.dumps(response.json(), indent=4, sort_keys=True))
        except:
            payload = {'text':'based',
                       'quote_tweet_id':str(tweet_id)}
            url = 'https://api.twitter.com/2/tweets'
            response = requests.post(auth=auth,url=url,json=payload,headers={"Content-Type":"application/json"})
            print(json.dumps(response.json(), indent=4, sort_keys=True))

    def read_twitter_alert_file(self):
        try:
            twitter_alert_file = open('.\\save\\twitter_alerts.txt',encoding='UTF-8').read()
        except:
            with open('.\\save\\twitter_alerts.txt', mode='w', encoding='UTF-8') as file:
                file.write('')
                file.close()
            twitter_alert_file = open('.\\save\\twitter_alerts.txt',encoding='UTF-8',mode='r').read()
        
        if twitter_alert_file != '':
            dataFrame = json.loads(twitter_alert_file)
            for data in dataFrame:
                self.savefile.append(data)

    def saving(self):
        file_path = ".\\save\\twitter_alerts.txt"
        sorted_tweets = sorted(self.savefile, key=lambda x: (x['like'], 'media' in x), reverse=True)
        final_save = []
        for tweet in sorted_tweets:
            final_save.append(tweet)
        # Write the data to the text file with indentation
        with open(file_path, "w",encoding='UTF-8') as text_file:
            text_file.write(json.dumps(final_save, indent=4)) 
            
    def repost_top(self):
        
        # Repost the TOP 2 of the scrape tweets for the past 20 mins
        if self.temp != []:
            sorted_tweets = sorted(self.temp, key=lambda x: (x['like'], 'media' in x), reverse=True)
            tweeted = 0
            for tweet in sorted_tweets:
                if tweeted == 2:
                    break
                if tweet.get('media') != None:
                    self.repost_tweet(tweet.get('reply_to_tweet_id'))
                    tweeted += 1
                
    def scrape_word(self):
        
        based_word_list = []
        # Get the time from 10 minutes before to feed into twitter api filter.
        end_time = datetime.utcnow() - timedelta(minutes=20)
        end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # keyword = "based" scrape all tweets from 10 mins max is 450 tweet per 15 mins.
        params = {
            'query':self.keyword,
            'max_results':100,
            'end_time': end_time_str,
            'sort_order':'recency',
            'tweet.fields':'author_id,created_at,public_metrics,text',
            'expansions':"author_id,attachments.media_keys,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id",
            'media.fields':'media_key,url,public_metrics,variants,preview_image_url',
            'user.fields':'created_at,public_metrics,username,id,entities,name,url'
        }
    
        # Endpoint for searching tweets by keyword
        url = 'https://api.twitter.com/2/tweets/search/recent'
        
        
        # 5 requests only for every 20 mins total = 500 tweets only to matching the word for every 20 mins
        # 10,000 API limit per month 14 calls limit per hour. divide by 20 mins 4 calls every 20 mins
        
        tweet_limit = 0
        
        while True:
            if tweet_limit == 5:
                break
            res = requests.get(url,params=params,headers=self.headers)
            if 'UsageCapExceeded' in res.text:
                print(json.dumps(res.json(), indent=4, sort_keys=True))
                break
            data = res.json()
            try:
                next_token = data['meta']['next_token']
            except KeyError:break
            
            params['next_token'] = next_token

            try:
                print('Total tweets: ',len(data['data']))
                for tweet in data['data']:
                    ID = tweet['id']    
                    TEXT = tweet['text']
                    TEXT = TEXT.replace('\n','').strip()
                    created_at = tweet['created_at']
                    text_copy = TEXT
                    if len(TEXT) > 70:
                        TEXT = TEXT[:67] + '....'
                    else:
                        for n in range(71-len(TEXT)):
                            TEXT += ' '
                    
                    printed_text = f'Text: {TEXT} | ID: {ID} | Created: {created_at}'
                    if printed_text not in self.scrape_textfile:
                        self.scrape_textfile.append(printed_text)
                    print(printed_text)
                    text_split = text_copy.split(' ')
                    if len(text_split) == 2:
                        text_lower = text_split[1].lower()
                        if text_lower == self.keyword.lower():
                             based_word_list.append(ID)
                
                tweet_limit += 1
            except:
                break

        if based_word_list != []:
            based_word_list = list(set(based_word_list))
            based_word_list = based_word_list[:99]
            self.get_details(IDs=based_word_list)
        else:
            print('No found! []')
            
    def get_medias(self,IDs):

        IDs = ','.join(IDs)
        # get the media url
        params = {
            'ids':IDs,
            'expansions':"author_id,attachments.media_keys,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id",
            'media.fields':'media_key,url,public_metrics,variants,preview_image_url'
        }
        
        url = 'https://api.twitter.com/2/tweets?'
        res = requests.get(url,params=params,headers=self.headers)
        data = res.json()['data']
        medias = res.json()['includes']['media']
        
        save = []
        
        for json in data:
            
            id = json['id']
            attachments = json.get('attachments')
            if attachments == None:
                continue
            mediaKey = attachments['media_keys'][0]
            filename = ''
            
            for media in medias:
                media_key2 = media['media_key']
                if mediaKey == media_key2:
                    
                    type_ = media['type']
                    fileUrL = ''
                    if 'video' in type_:
                        fileUrL = media['variants'][0]['url']
                        
                    if 'photo' in type_:
                        fileUrL = media['url']

                    folder_exist = os.path.exists('.\\media')
                    if '.mp4' in fileUrL:
                        if fileUrL != '':
                            if folder_exist == True:
                                filename = '.\\media\\media_{}.mp4'.format(id)
                                resmedia = requests.get(fileUrL)
                                with open(filename,mode='wb+') as file:
                                    file.write(resmedia.content)
                                    file.close
            
                    if '.jpg' in fileUrL:
                        if fileUrL != '':
                            if folder_exist == True:
                                filename = '.\\media\\media_{}.jpg'.format(id)
                                resmedia = requests.get(fileUrL)
                                with open(filename,mode='wb+') as file:
                                    file.write(resmedia.content)
                                    file.close  

            dic = {}
            dic['id'] = id
            dic['filename'] = filename
            save.append(dic)
        
        return save
    
    def get_details(self,IDs):
        
        IDs = ','.join(IDs)
        
        params = {
            'ids':IDs,
            'tweet.fields':'author_id,created_at,public_metrics,text',
            'expansions':"author_id,attachments.media_keys,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id",
            'media.fields':'media_key,url,public_metrics,variants,preview_image_url'
        }
        
        url = 'https://api.twitter.com/2/tweets?'
        res = requests.get(url,params=params,headers=self.headers)
        save_temp = []
        medias = []
        
        json = res.json()
        datas = json['data']
        tweets = json['includes']['tweets']
        users = json['includes']['users']
        
        for dataItem in datas:
            referenced_tweets = dataItem.get('referenced_tweets')
            if referenced_tweets != None and 'replied_to' == referenced_tweets[0]['type'] or 'quoted' == referenced_tweets[0]['type']:
                typeTweet = referenced_tweets[0]['type']
                for tweet in tweets:
                    id = tweet['id']
                    if referenced_tweets[0]['id'] == id:
                        dic = self.get_details2(dataItem=dataItem,tweetItem=tweet,usersItem=users,typeTweet=typeTweet)
                        attachments = tweet.get('attachments')
                        if attachments != None:
                            medias.append(tweet['id'])
                        save_temp.append(dic)
            else:
                typeTweet = 'post'
                dic = self.get_details2(dataItem=dataItem,tweetItem=dataItem,usersItem=users,typeTweet=typeTweet)
                attachments = dataItem.get('attachments')
                if attachments != None:
                    medias.append(dataItem['id'])
                save_temp.append(dic)
        
        
        medias_result = []
        if medias != []:
            medias_result = self.get_medias(medias)
            
        for save_temp_item in save_temp:
            reply_to_tweet_id = save_temp_item['reply_to_tweet_id']
            for medias_item in medias_result:
                if reply_to_tweet_id == medias_item['id']:
                    save_temp_item['media'] = medias_item['filename']
        

            for k,v in save_temp_item.items():
                print(k,v,sep=' | ')
            self.savefile.append(save_temp_item)
            self.temp.append(save_temp_item)
        
        
    def get_details2(self,dataItem,tweetItem,usersItem,typeTweet):

        data = dataItem
        tweetID1 = ''
        tweetID2 = ''
        
        created_at1 = ''
        created_at2 = ''
        
        author_id1 = ''
        author_id2 = ''
        
        text1 = ''
        text2 = ''
        
        public_metrics1 = ''
        public_metrics2 = ''
        
        
        #-------------------------------------------------------
        
        
        author_id1 = data['author_id']
        created_at1 = data['created_at'].replace('T',' ')
        tweetID1 = data['id']
        public_metrics1 = data['public_metrics']
        text1 = data['text'].strip()
        
        #--------------------------------------------------------
        
        maintweet = tweetItem
        author_id2 = maintweet['author_id']
        created_at2 = maintweet['created_at'].replace('T',' ')
        tweetID2 = maintweet['id']
        public_metrics2 = maintweet['public_metrics']
        like = public_metrics2['like_count']
        quote_count = public_metrics2['quote_count']
        reply_count = public_metrics2['reply_count']
        retweet_count = public_metrics2['retweet_count']
        text2 = maintweet['text']
        
        user1 = ''
        user2 = ''
        
        for userRow in usersItem:
            idName = userRow['id']
            if author_id1 == idName:
                user1 = userRow['username']
            if author_id2 == idName:
                user2 = userRow['username']

        #--------------------------------------------------------
        dic = {}
        tweetURL = f'https://twitter.com/{user1}/status/{tweetID1}'
        tweetURL2 = f'https://twitter.com/{user2}/status/{tweetID2}'

        dic['type'] = typeTweet
        dic['author'] = user1
        dic['text'] = text1
        dic['author_id'] = author_id1
        dic['created_at'] = created_at1
        dic['tweet_id'] = tweetID1
        dic['tweet_url'] = tweetURL
        
        dic['reply_to_autor'] = user2
        dic['reply_to_text'] = text2
        dic['reply_to_autor_id'] = author_id2
        dic['reply_to_created_at'] = created_at2
        dic['reply_to_tweet_id'] = tweetID2
        dic['reply_to_tweet_url'] = tweetURL2
        dic['like'] = like
        dic['reply_count'] = reply_count
        dic['retweet_count'] = retweet_count
        dic['quote_count'] = quote_count
        
        return dic


def Twitter_Scraper():
    
    while True:
        
        # Script will run every 20 mins and post the top 2 with top like 
        
        twitter = Twitter(bearer_token=bearer_token,word=keyword) 
        creds = twitter.get_my_id()
        if creds == False:
            break
        twitter.scrape_word()
        twitter.repost_top()
        twitter.saving()
        print('sleep by (20 minutes) before run again.')
        time.sleep(1200)
        
        
if __name__ == '__main__':
    Twitter_Scraper()
    
