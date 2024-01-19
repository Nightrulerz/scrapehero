from lxml import html
import requests
import csv

def product_service_data():
    """
    Extracts Products and Services data and write to CSV file
    """
    homepage_url = "https://www.nlm.nih.gov/"
    response_1 = get_response(homepage_url)
    parser_1 = html.fromstring(response_1.text)
    raw_url = parser_1.xpath('//a[text()="All Products and Services"]/@href')

    # Formatting the URL
    nlm_resources_url = f"https:{raw_url[0]}"
    response_2 = get_response(nlm_resources_url)
    parser_2 = html.fromstring(response_2.text)
    results = parser_2.xpath('//div[@class="record_box"]')

    full_data = []
    for result in results:
        resource_raw = result.xpath('.//a/@title')
        resource_url_raw = result.xpath('.//button/following::a[1]/@href')
        raw_description = result.xpath('.//text()[not(parent::a/@title)][not(parent::div[contains(@id,"description")])][not(parent::b)][not(parent::a[@target="_blank"])][not(parent::button)]')
        data = {
            "Resource": clean_data(resource_raw),
            "URL": clean_data(resource_url_raw),
            "Description": clean_data(raw_description)
        }
        full_data.append(data)
    keys = ["Resource","URL","Description"]
    saving_data(full_data, keys)


def saving_data(full_data, keys):
    """
    Writes scraped data to csv file
    
    Args:
        file_name: output file name
        full_data: list of scraped Products and Services data
    """
    with open('Products_and_Services.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        # full_data : is a list of dicts, we have created a list full_data and appended the data to it 
        dict_writer.writerows(full_data)


def get_response(url: str) -> requests.Response:
    """
    Retrieves html response by sending requests

    Args:
        url(str): Website URL

    Returns:
        requests.Response
    """
    headers  = {
        'Accept':('text/html,application/xhtml+xml,application/xml;q=0.9,'
        'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        }
    # Retrying 3 times if status code is not 200
    for retry in range(3):
        # Sending request
        response = requests.get(url, headers=headers)
        # Checking the response status code
        if response.status_code == 200:
            return response


def clean_data(list_element):
    '''
    The function cleans the list provided returns a string
    
    Args:
    list_element (list): List of strings

    '''
    if not list_element:
        return None
    text = ' '.join(' '.join(list_element).split()).strip()
    return None if not text.strip() else text.strip()


if __name__ == "__main__":
    product_service_data()
