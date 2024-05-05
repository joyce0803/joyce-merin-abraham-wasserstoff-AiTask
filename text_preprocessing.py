from bs4 import BeautifulSoup
import html
import re


def remove_html_tags(text):
    return BeautifulSoup(text, "html.parser").get_text()

def decode_html_entities(text):
    return html.unescape(text)

def clean_text(text):
    # Remove new lines and tabs
    text = re.sub(r'[\t\n\r]+', ' ', text)
    # Remove any other non-printable characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text

def preprocess_text(text):
    text = remove_html_tags(text)
    text = decode_html_entities(text)
    text = clean_text(text)
    return text

