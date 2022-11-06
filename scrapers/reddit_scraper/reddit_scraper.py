import config
import praw
import pandas as pd
from psaw import PushshiftAPI


reddit = praw.Reddit(client_id = config.reddit_client_id, client_secret = config.secret, user_agent = config.agent)
api=PushshiftAPI(reddit)
subreddits=['tinder','tinderstories']
keywords=['rape','scam','molestation','robbed','attacked','assault','catfish','phishing','child']
total_posts = list()
for q in keywords:
    hot_posts = api.search_submissions(q=q,subreddit=subreddits)
    id_list=[thing.id for thing in hot_posts]
    new_id=[]
    for id in id_list:
        new_id.append('t3_'+id)
    # print(hot_posts[0])

    for post in reddit.info(new_id):
        #print(post.title)
        # print(vars(post)) # print all properties
        Title=post.title
        Score = post.score
        Number_Of_Comments = post.num_comments
        Publish_Date = post.created
        Link = post.permalink
        Content = post.selftext
        data_set = {"Title":Title,"Score":Score, "Number_Of_Comments":Number_Of_Comments,"Publish_Date":Publish_Date,"Content":Content,"Category":q}
        total_posts.append(data_set)

#print(total_posts[0])

#df=pd.DataFrame.from_records(total_posts)
df=pd.DataFrame.from_records(total_posts)