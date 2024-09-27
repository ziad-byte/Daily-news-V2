import requests
from bs4 import BeautifulSoup
import json

# Function to fetch articles using tags from a JSON file
def fetch_articles(url, json_file):
    try:
        # Load the tag information from the JSON file
        with open(json_file, 'r') as file:
            tags = json.load(file)
        
        # Fetch and parse the webpage
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract the page name using the tag from the JSON file
        page_name_tag = tags.get('page_name', 'title')
        page_name = soup.find(page_name_tag).text.strip() if soup.find(page_name_tag) else 'No page name found'
        
        # Find all articles using the article tag from the JSON file
        article_tag = tags.get('article', 'article')
        articles = soup.find_all(article_tag)
        
        results = []
        
        for article in articles:
            # Extract the link, title, and description using the tags from the JSON file
            link_info = tags.get('link', {})
            link_tag = article.find(link_info.get('tag', 'a'), href=True)
            title_tag = article.find(tags.get('title', 'h3'))
            description_tag = article.find(tags.get('description', 'p'))
            
            link = link_tag[link_info.get('attribute', 'href')] if link_tag else 'No link found'
            title = title_tag.text.strip() if title_tag else 'No title found'
            description = description_tag.text.strip() if description_tag else 'No description found'
            
            # Create a dictionary to store the article data
            article_data = {
                "Page Name": page_name,
                "Link": link,
                "Title": title,
                "Description": description
            }
            results.append(article_data)
        
        # Print the results to the console
        for result in results:
            print(json.dumps(result, indent=4))
            print('-' * 40)
        
        # Optionally, write the results to a JSON file
        with open('articles_output.json', 'w') as outfile:
            json.dump(results, outfile, indent=4)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")

if __name__ == "__main__":
    url = "https://devblogs.microsoft.com/dotnet/category/aspnetcore/"
    json_file = 'tags.json'  # The JSON file with the tag structure
    fetch_articles(url, json_file)
