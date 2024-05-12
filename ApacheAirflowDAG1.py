from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import requests
from bs4 import BeautifulSoup
import re

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    return links

def extract_article_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []
    for article in soup.find_all('article'):
        title_tag = article.find('h2')
        title = title_tag.text.strip() if title_tag else "No title available"
        
        description_tag = article.find('p')
        description = description_tag.text.strip() if description_tag else "No description available"
        
        articles.append({'title': title, 'description': description})
    return articles

def preprocess_text(text):
    text = re.sub('<[^<]+?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

def DawnArticleProcessed(**kwargs):
    dawn_articles = kwargs['ti'].xcom_pull(task_ids='extract_dawn_articles')
    dawn_articles_processed = [{'title': preprocess_text(article['title']), 
                                'description': preprocess_text(article['description'])} 
                               for article in dawn_articles]
    return dawn_articles_processed
    
def BBCArticleProcessed(**kwargs):
    bbc_articles = kwargs['ti'].xcom_pull(task_ids='extract_bbc_articles')
    bbc_articles_processed = [{'title': preprocess_text(article['title']), 
                               'description': preprocess_text(article['description'])} 
                              for article in bbc_articles]
    return bbc_articles_processed

def store_processed_data(**kwargs):
    dawn_articles_processed = kwargs['ti'].xcom_pull(task_ids='process_dawn_articles')
    bbc_articles_processed = kwargs['ti'].xcom_pull(task_ids='process_bbc_articles')
    
    with open('/path/to/dawn_processed_data.txt', 'w', encoding='utf-8') as file:
        for article in dawn_articles_processed:
            file.write(f"Title: {article['title']}\nDescription: {article['description']}\n\n")
    
    with open('/path/to/bbc_processed_data.txt', 'w', encoding='utf-8') as file:
        for article in bbc_articles_processed:
            file.write(f"Title: {article['title']}\nDescription: {article['description']}\n\n")

with DAG(
    'data_extraction_transformation_storage',
    default_args=default_args,
    description='Automate data extraction, transformation, and storage',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['data_extraction', 'data_transformation', 'data_storage'],
) as dag:

    extract_dawn_articles = PythonOperator(
        task_id='extract_dawn_articles',
        python_callable=extract_article_info,
        op_kwargs={'url': 'https://www.dawn.com/'}
    )

    extract_bbc_articles = PythonOperator(
        task_id='extract_bbc_articles',
        python_callable=extract_article_info,
        op_kwargs={'url': 'https://www.bbc.com/'}
    )

    process_dawn_articles = PythonOperator(
        task_id='process_dawn_articles',
        python_callable=DawnArticleProcessed,
        provide_context=True
    )

    process_bbc_articles = PythonOperator(
        task_id='process_bbc_articles',
        python_callable=BBCArticleProcessed,
        provide_context=True
    )

    store_processed_data = PythonOperator(
        task_id='store_processed_data',
        python_callable=store_processed_data,
        provide_context=True
    )

    extract_dawn_articles >> process_dawn_articles >> store_processed_data
    extract_bbc_articles >> process_bbc_articles >> store_processed_data
