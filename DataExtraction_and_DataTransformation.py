import requests
from bs4 import BeautifulSoup
import re

#---------------------------------------------------------- DATA EXTRACTION -----------------------------------------------------------------------------------------
# Function to extract links from a webpage
def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    return links

# Function to extract titles and descriptions from articles on a webpage
def extract_article_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []
    for article in soup.find_all('article'):
        # Check if <h2> tag exists before trying to access its text
        title_tag = article.find('h2')
        title = title_tag.text.strip() if title_tag else "No title available"
        
        # Check if <p> tag exists before trying to access its text
        description_tag = article.find('p')
        description = description_tag.text.strip() if description_tag else "No description available"
        
        articles.append({'title': title, 'description': description})
    return articles

# --------------------------------------------------------- DATA TRANSFORMATION -----------------------------------------------------------

# pre-processing the text
def preprocess_text(text):
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', text)
    # Remove special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    return text

# Data Transformation
def DawnArticleProcessed(dawn_articles) :

 dawn_articles_processed = [{'title': preprocess_text(article['title']), 
                            'description': preprocess_text(article['description'])} 
                           for article in dawn_articles]
 return dawn_articles_processed


    
def BBCArticleProcessed(bbc_articles) :
 bbc_articles_processed = [{'title': preprocess_text(article['title']), 
                           'description': preprocess_text(article['description'])} 
                          for article in bbc_articles]
 return bbc_articles_processed




# URLs of dawn.com and BBC.com landing pages
dawn_url = 'https://www.dawn.com/'
bbc_url = 'https://www.bbc.com/'

# Extract links from dawn.com and BBC.com landing pages
dawn_links = extract_links(dawn_url)
bbc_links = extract_links(bbc_url)

# Extract titles and descriptions from articles on dawn.com and BBC.com homepages
dawn_articles = extract_article_info(dawn_url)
bbc_articles = extract_article_info(bbc_url)





# Data Transformation

dawn_articles_processed=DawnArticleProcessed(dawn_articles)
bbc_articles_processed=BBCArticleProcessed(bbc_articles)

print("Processed Dawn Articles:", dawn_articles_processed)
print("Processed BBC Articles:", bbc_articles_processed)


# ---------------------------- STORING THE PROCESSED DATA TO TXT FILES -------------------------------------------------------------
# Write processed Dawn data to dawn_processed_data.txt
with open('dawn_processed_data.txt', 'w', encoding='utf-8') as file:
    for article in dawn_articles_processed:
        file.write(f"Title: {article['title']}\nDescription: {article['description']}\n\n")

# Write processed BBC data to bbc_processed_data.txt
with open('bbc_processed_data.txt', 'w', encoding='utf-8') as file:
    for article in bbc_articles_processed:
        file.write(f"Title: {article['title']}\nDescription: {article['description']}\n\n")

print("Processed data written to dawn_processed_data.txt and bbc_processed_data.txt.")




