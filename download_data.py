import requests
import time
import csv
import json

# Replace with your TMDb API key
API_KEY = '044dd6a43c6eda579cce68b556c61251'
BASE_URL = 'https://api.themoviedb.org/3'

# Function to fetch data from TMDb API
def fetch_movies(page):
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&page={page}"
    response = requests.get(
        url,
        headers={
            'Content-Type': 'application/json',
            'Authentication':
            f'Bearer {API_KEY}'
        }
    )
    
    # Check for successful response
    if response.status_code != 200:
        print(f"Error: Unable to fetch page {page}. Status code: {response.status_code}")
        return None
    
    data = response.json()
    return data['results']

# Function to fetch 1000 movies
def get_1000_movies():
    all_movies = []
    page = 1
    while len(all_movies) < 1000:
        print(f"Fetching page {page}...")
        movies = fetch_movies(page)

        if not movies:
            break

        # Add the movies to the list
        all_movies.extend(movies)

        # Stop if we have 1000 or more movies
        if len(all_movies) >= 1000:
            break

        # Move to the next page
        page += 1

        # Adding a delay to avoid hitting rate limits
        time.sleep(1)

    # Truncate the list to exactly 1000 movies if necessary
    return all_movies[:1000]

# Save movies data to CSV file
def save_movies_to_csv(movies):
    with open('movies.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'summary', 'release_year', 'genres']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for movie in movies:
            genres = ", ".join([str(genre) for genre in movie.get('genre_ids', [])])
            writer.writerow({
                'title': movie['title'],
                'summary': movie.get('overview', 'No summary available'),
                'release_year': movie['release_date'][:4],  # Extract year from release_date
                'genres': genres
            })
    
    print("Movies data saved to movies.csv")

# Save movies data to JSON file
def save_movies_to_json(movies):
    # Open a file in write mode
    with open('movies.json', 'w', encoding='utf-8') as jsonfile:
        # Prepare the movie data to write as JSON
        json.dump(movies, jsonfile, ensure_ascii=False, indent=4)

    print("Movies data saved to movies.json")

# Main function to get movies and save to CSV
def main():
    # Fetch 1000 movies from TMDb
    print("Fetching movies...")
    movies = get_1000_movies()
    
    if len(movies) < 1000:
        print(f"Warning: Only {len(movies)} movies were fetched.")
    
    # Save the fetched movies to a CSV file
    save_movies_to_json(movies)

# Run the main function
if __name__ == "__main__":
    main()
