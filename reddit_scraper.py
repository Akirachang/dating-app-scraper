import config
import praw
import pandas as pd

reddit = praw.Reddit(client_id = config.reddit_client_id, client_secret = config.secret, user_agent = config.agent)

hot_posts = reddit.subreddit('tinderstories').hot(limit=200)
# print(hot_posts[0])
total_posts = list()

for post in hot_posts:
    #print(post.title)
    # print(vars(post)) # print all properties
    Title=post.title
    Score = post.score
    Number_Of_Comments = post.num_comments
    Publish_Date = post.created
    Link = post.permalink
    Content = post.selftext
    data_set = {"Title":Title,"Score":Score, "Number_Of_Comments":Number_Of_Comments,"Publish_Date":Publish_Date,"Content":Content}
    total_posts.append(data_set)

#print(total_posts[0])

df=pd.DataFrame.from_records(total_posts)

df.to_csv('Reddit_HotPosts.csv', encoding='utf-8', index=False)



