''' Modern Gaming AI Algorithms

This script extracts a Wikipedia article and finds the most relevant pages linked in the article.

Written by Job van der Zwaag

'''

import requests
import json
import time
import urllib.parse

#Input
topic_url = 'https://en.wikipedia.org/wiki/United_States'
number_of_pages = 10
print_information = False

#Get the topic from the url and make it readable
topic_name = topic_url.split("/")[-1]
topic_name_normal = topic_name.replace("_", " ")
topic_name_normal = urllib.parse.unquote(topic_name_normal)

if print_information:
    print("Finding pages about the topic: ", topic_name_normal)

#Get the first alinea from the Wikipedia page
topic_wiki_response = requests.get(topic_url)
topic_wiki_text = topic_wiki_response.text
topic_wiki_text_begin = topic_wiki_text.split('<div id="siteSub" class="noprint">From Wikipedia, the free encyclopedia</div>')[1]
topic_wiki_text_end = topic_wiki_text_begin.split('id="toc"')[0]

if print_information:
    print(topic_name_normal, " page received from Wikipedia.")

#Get the links from the text
topic_wiki_links_begin = topic_wiki_text_end.split('<a href="/wiki/')

linked_pages = []

#Check for every link if it is usable
for link in topic_wiki_links_begin:
    page_name_parts = link.split('"')

    page_name = page_name_parts[0]

    #No loops
    if page_name == topic_name:
        continue

    #Wikipedia main page
    if page_name == "Main_Page":
        continue

    #Lists are not very usefull
    if "List_of_" in page_name:
        continue

    #Disambiguation pages are useless
    if "disambiguation" in page_name:
        continue

    #Not a page but an paragraph on a page
    if "#" in page_name:
        continue

    #Some Wikipedia specific pages
    if "Wikipedia" in page_name:
        continue

    if "File:" in page_name:
        continue

    if "Special:" in page_name:
        continue
    
    if "Category:" in page_name:
        continue

    if "Help:" in page_name:
        continue

    if "Talk:" in page_name:
        continue

    if "Portal:" in page_name:
        continue

    #The first part before any link is not a page
    if "<div id=" in page_name:
        continue
    
    linked_pages.append(page_name)

if print_information:
    print("Normal links extracted from page. ", len(linked_pages), " links found.")

linked_pages_views = {}
relevant_pages = {}

#Get the pageviews for the linked pages
for linked_page in linked_pages[:200]:

    linked_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" + linked_page + "/monthly/20210401/20210430"

    pageviews = requests.get(linked_url, headers={"User-Agent":"TopicBot"})
    pageviews_text = json.loads(pageviews.text)

    if "items" in pageviews_text:
        linked_pages_views[linked_page] = pageviews_text["items"][0]["views"]

#Order the pages by view count
linked_pages_views_ordered = sorted(linked_pages_views.items(), key=lambda x: x[1], reverse=True)

if print_information:
    print("Looked at the number of views of the linked pages.")

index = 0
relevant_links = []

#We only need to check untill we have the amount of relevant pages we need
while len(relevant_pages) < number_of_pages and index < len(linked_pages_views_ordered):
    linked_page = linked_pages_views_ordered[index]
    linked_url = "https://en.wikipedia.org/wiki/" + linked_page[0]
    
    #Get the first alinea from the Wikipedia page
    linked_response = requests.get(linked_url)
    linked_text = linked_response.text
    linked_begin = linked_text.split('<div id="siteSub" class="noprint">From Wikipedia, the free encyclopedia</div>')[1]
    linked_end = linked_begin.split('id="toc"')[0]

    #If the topic is named in the text the page is really relevant
    if topic_name in linked_end or topic_name_normal in linked_end:
        relevant_pages[linked_page[0]] = linked_page[1]
        relevant_links.append(linked_url)

    index = index + 1

if print_information:
    print("Checked if the linked pages were actually relevant.")

if print_information:
    print("\nRelevant pages:")

    for relevant_page in relevant_pages.items():
        #Get the topic from the url and make it readable
        normal_name = relevant_page[0].replace("_", " ")
        normal_name = urllib.parse.unquote(normal_name)

        print(normal_name, ": ", relevant_page[1])

if print_information:
    print("\nRelevant links:")

print(relevant_links)




