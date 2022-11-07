import requests
import json
import os.path

url = "https://bg.annapurnapost.com/api/search"
news_topic = "दुर्घटना"
file_name = f"{news_topic}.json"
page_to_fetch = 1  # initial

try:
    with open(file_name, 'r') as file:
        saved_news = json.load(file)
except:
    saved_news = {"fetched_upto": 0, "articles": []}


while True:
    """the below if statement helps to detect whether to fetch from first page 
    or to begin from where it ended on last code execution"""
    if (saved_news["fetched_upto"] != 0):
        page_to_fetch = saved_news["fetched_upto"] + 1
    response = requests.get(
        url=url, params={'title': news_topic, 'page': page_to_fetch}).json()
    # below if statement to handle zero articles found
    if (response["data"]["count"] == 0):
        print("news not found in this topic")
    # task to gather necessary info begins here
    else:
        articles_to_save = []  # each article to be appended in this list
        # iterating through each news article of specific page
        for each_news in response["data"]["items"]:
            # using news variable to collect only title and content field only
            news = {"title": each_news["title"],
                    "content": each_news["content"]}
            articles_to_save.append(news)
        # adding new articles to json file
        saved_news["articles"] += articles_to_save
        # updating fetched page info of json file
        saved_news["fetched_upto"] = page_to_fetch
        # printing few items to know news extracting status
        print("fetched upto page: " + str(page_to_fetch))
        print("remaining pages:" +
              str((response["data"]["totalPage"]) - page_to_fetch))

        # next time needs to fetch next page, so increased its value
        page_to_fetch += 1
    saved_news["total_page"] = response["data"]["totalPage"]
    # to stop while loop once articles of all pages are saved
    if (page_to_fetch > response["data"]["totalPage"]):
        print("Saved all the available articles")
        break

    # saving the above updated values of json file at the end
    with open(file_name, 'w') as file:
        json.dump(saved_news, file)
