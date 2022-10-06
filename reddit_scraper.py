#reddit client id: 9uSZazoC_zoxPOZwsb2lVw
#secret: Od8EJ3AEpEHSYbZ4MvVkbc8h_geidA

import praw

reddit_client_id = "9uSZazoC_zoxPOZwsb2lVw"
secret = "Od8EJ3AEpEHSYbZ4MvVkbc8h_geidA"
agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

reddit = praw.Reddit(client_id = reddit_client_id, client_secret = secret, user_agent = agent)

hot_posts = reddit.subreddit('OnlineDating').hot(limit=200)
# print(hot_posts[0])
total_posts = list()

for post in hot_posts:
    print(post.title)
    # print(vars(post)) # print all properties
    Title=post.title,
    Score = post.score,
    Number_Of_Comments = post.num_comments,
    Publish_Date = post.created,
    Link = post.permalink,
    data_set = {"Title":Title[0],"Score":Score[0],   "Number_Of_Comments":Number_Of_Comments[0],"Publish_Date":Publish_Date[0],"Link":'https://www.reddit.com'+Link[0]}
    total_posts.append(data_set)

print(total_posts[0])




