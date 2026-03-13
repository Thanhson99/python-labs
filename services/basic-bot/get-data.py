import requests
from bs4 import BeautifulSoup

def get_programming_tutorial():
    url = "https://www.w3schools.com/python/"  # Basic Python learning page
    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract all lesson headings
        lessons = soup.find_all('div', class_='w3-panel w3-card-2 w3-white w3-round-large')
        for lesson in lessons:
            title = lesson.find('h2')
            if title:
                print(title.text.strip())
    else:
        print("Unable to access the website.")

# Run tutorial extraction
get_programming_tutorial()
