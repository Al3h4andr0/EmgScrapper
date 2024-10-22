import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page you want to scrape
url = """https://www.emag.ro/search/aspirator%20nazal%20bebelusi?ref=effective_search"""

# Send a GET request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find product containers (update the selector based on actual HTML structure)
    products = soup.find_all('div', class_='card-item')

    # Create a list to store product data
    product_list = []

    for product in products:
        title = product.find('h2', class_='card-v2-title-wrapper').text.strip() if product.find('h2', class_='card-v2-title-wrapper') else None
        price = product.find('p', class_='product-new-price').text.strip() if product.find('p', class_='product-new-price') else None
        super_pret = product.find('span', class_='card-v2-badge-cmp badge commercial-badge').contents[0] if product.find('span', class_='card-v2-badge-cmp badge commercial-badge') else None
        rating = product.find('span', class_='average-rating semibold').contents[0] if product.find('span', class_='average-rating semibold') else None
        no_reviews = product.find('span', class_='visible-xs-inline-block').contents[0].split('(', maxsplit=1)[1].split(')', maxsplit=1)[0] if product.find('span', class_='visible-xs-inline-block') else None

        # Append product data to the list
        product_list.append({
            'Title': title,
            'Price': price,
            'Super Pret': super_pret,
            'Rating': rating,
            'Reviews': no_reviews,
        })

    # Create a DataFrame
    df = pd.DataFrame(product_list)

    # Save to Excel
    df.to_excel('emag_products.xlsx', index=False)
    print("Data saved to emag_products.xlsx")

else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
