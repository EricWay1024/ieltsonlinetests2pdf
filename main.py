import requests
from bs4 import BeautifulSoup
import pdfkit
import time
import os
import re
from functools import partial
from urllib.parse import urljoin
import logging

def relative_to_absolute_urls(fragment, base_url):
    """Replace relative urls in a html fragment to absolute urls."""
    def srcrepl(base_url, match):
        absolute_link = urljoin(base_url, match.group(3))
        return "<" + match.group(1) + match.group(2) + "=" + "\"" + absolute_link + "\"" + match.group(4) + ">"
    p = re.compile(r"<(.*?)(src|href)=\"(?!http)(.*?)\"(.*?)>")
    absolute_fragment = p.sub(partial(srcrepl, base_url), fragment)
    return absolute_fragment

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://ieltsonlinetests.com/collection/ielts-mock-test-2022-january',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}

style = open('style.css').read()
template = """<!doctype html><html><head><style>{}</style><meta charset="utf-8">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>{}</body></html>"""

OUTPUT_DIR = "./res"
logging.basicConfig(level=logging.INFO)

try:
    os.makedirs(OUTPUT_DIR)
except FileExistsError:
    pass

def gen_pdf_for_test(test_name, output_file):
    """Generate a PDF file for the reading test of test_name from ieltsonlinetests.com."""

    response = requests.get(
        f'https://ieltsonlinetests.com/{test_name}', headers=headers)

    parsed_html = BeautifulSoup(response.text, 'html.parser')

    readings = parsed_html.find('div', {'class': 'split-right'})
    questions = parsed_html.find('div', {'class': 'split-left'})

    soup = BeautifulSoup("", 'html.parser')

    for i in [1, 2, 3]:
        r = readings.find('div', {'id': f'set-container-{i}'})
        q = questions.find('div', {'id': f'set-question-{i}'})
        soup.append(r)
        soup.append(q)

    new_html = template.format(style, str(soup))

    new_html = relative_to_absolute_urls(
        new_html, 'https://ieltsonlinetests.com/')

    # open('temp.html', 'w').write(new_html)
    pdfkit.from_string(new_html, output_file)


def fetch_name_list(name_list):
    for test_name in name_list:
        output_file = f'{OUTPUT_DIR}/{test_name}.pdf'
        if os.path.exists(output_file):
            logging.warning(f'File exists for {test_name}, skipping')
            continue
        try:
            gen_pdf_for_test(test_name, output_file)
        except KeyboardInterrupt:
            logging.error('Keyboard interruption, terminating')
            break
        except:
            logging.warning(f'Error encountered for {test_name}, skipping')
            continue
        logging.info(f'PDF generated for {test_name}')
        time.sleep(1.2)


if __name__ == '__main__':
    name_list_1 = [
        f'ielts-recent-mock-tests-volume-{v}-reading-practice-test-{p}' for v in range(1, 7) for p in range(1, 7)]

    months = ['january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december']

    name_list_2 = [f'ielts-practice-tests-plus-{v}-reading-practice-test-{p}' for v in range(1, 4) for p in range(1, 8)]
    name_list_3 = [f'ielts-practice-test-{v}-reading-practice-test-{p}' for v in range(1, 9) for p in range(1, 3)]
    
    name_list_4 = [f'ielts-mock-test-{year}-{month}-reading-practice-test-{num}' for year in [
        2020, 2021, 2022] for month in months for num in [1, 2]]
    
    fetch_name_list(name_list_1)
    fetch_name_list(name_list_2)
    fetch_name_list(name_list_3)
    fetch_name_list(name_list_4)
