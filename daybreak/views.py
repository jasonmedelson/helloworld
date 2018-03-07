from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
# Create your views here.

def index(request):
    return render(
        request,
        './index.html'
    )

def search(request):
    if 'q' in request.GET:
        parse = request.GET['q']
        sort = parse.split("https")
        num = len(sort)
        links = []
        names = []
        like = []
        retweet = []
        tweets=[]
        date=[]
        allinfo=[]
        for link in range(1,num):
            url = "https"
            try:
                url+=sort[link]
                links.append(url)
                # req = urlreq.urlopen(url)
                url = url[:len(url)-2]
                req = requests.get(url, verify=False)
                soup = BeautifulSoup(req.content)
                name = soup.find_all("span", {"class": "username"})
                name= name[4].text.strip()
                name = name[1:]
                names.append(name)

                tweet = soup.find_all("p", {"class": "TweetTextSize--jumbo"})
                tweet = tweet[0].text.strip()
                tweets.append(tweet)

                try:
                    retweets = soup.find_all("a", {"class": "request-retweeted-popup"})
                    retweets = retweets[0].text.strip()
                    retweets = retweets.split(" ")
                    retweets = retweets[0]
                    retweets = int(retweets.replace(",", ""))
                    retweet.append(retweets)
                except:
                    retweets = 0
                    retweet.append(retweets)

                try:
                    likes = soup.find_all("a", {"class": "request-favorited-popup"})
                    likes = likes[0].text.strip()
                    likes = likes.split(" ")
                    likes = likes[0]
                    likes = int(likes.replace(",", ""))
                    like.append(likes)
                except:
                    likes = 0
                    like.append(likes)

                timestamp = soup.find_all("span", {"class": "metadata"})
                timestamp = timestamp[0].text.strip()
                timestamp = timestamp.split("- ")
                timestamp = timestamp[1]
                try:
                    timestamp = timestamp.split("from")
                    timestamp = timestamp[0].strip()
                    date.append(timestamp)
                except:
                    timestamp = timestamp
                    date.append(timestamp)
            except:
                names.append(" ")
                like.append(0)
                retweet.append(0)
                tweets.append(" ")
                date.append(" ")

    else:
        message = 'You submitted an empty form.'
        return HttpResponse(message)
    for i in range(num-1):
        allinfo.append(date[i])
        allinfo.append(names[i])
        allinfo.append(links[i])
        allinfo.append(retweet[i])
        allinfo.append(like[i])
        allinfo.append(tweets[i])
    zipped = zip(date,names,links,retweet,like,tweets)
    return render(
        request,
        'data.html',
        context={'names': names, 'likes': like,
                 'retweets': retweet, 'tweets': tweets, "zipped":zipped,
                 'dates': date, "items":num,"links":links, "fulldata": allinfo},
    )

# def search(request):
#     if 'q' in request.GET:
#         message = 'You searched for: %r' % request.GET['q']
#     else:
#         message = 'You submitted an empty form.'
#     return HttpResponse(message)
