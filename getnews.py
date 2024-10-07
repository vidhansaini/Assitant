import requests
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak out text
def speak_news(text):
    engine.say(text)
    engine.runAndWait()

# Function to fetch and display news based on country and category
def get_news(country, category):
    api_key = "5975c8377e2d4bf3aed1edef6deae45b"  # Replace with your NewsAPI key
    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        news_data = response.json()
        
        if news_data['status'] == 'ok':
            articles = news_data['articles'][:5]  # Fetch top 5 news articles
            if articles:
                for i, article in enumerate(articles):
                    title = article.get('title', 'No title available')
                    description = article.get('description', 'No description available')
                    
                    # Print and speak the news
                    print(f"News {i+1}: {title}")
                    print(f"Description: {description}\n")
                    speak_news(f"News {i+1}: {title}. {description}")
            else:
                speak_news(f"Sorry, no news found for {category} in {country}.")
        else:
            speak_news("There was an issue fetching the news.")
    
    except Exception as e:
        speak_news("An error occurred while trying to fetch the news.")
        print(f"Error: {e}")

# Example usage within Dexter or for testing
if __name__ == "__main__":
    country = input("Enter the country code (e.g., 'us' for USA, 'in' for India): ").strip()
    category = input("Enter the news category (e.g., 'sports', 'business', 'entertainment'): ").strip()
    get_news(country, category)
