from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import pprint

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
CSE_ID = os.getenv('CSE_ID')


def google_search(search_term, **kwargs):
	service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
	search_results = service.cse().list(q=search_term, cx=CSE_ID, **kwargs).execute()
	return search_results['items']




try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

def advanced_google_search(query):
	search_results = search(query, num=3, stop=3, pause=2)
	return search_results