from bs4 import BeautifulSoup

from django.template.loader import render_to_string

from .tasks import slack_post_message


def main_text_from_html(html):
    """
    Return text from the 'main' tag of some html
    Allows easier maintenance of email templates, since no separate .txt template is required
    """
    soup = BeautifulSoup(html, features="html.parser")
    main = soup.find("main")
    if not main:
        raise ValueError("Passed html does not include a 'main' element")
    return main.get_text()


def slack_post_templated_message(template, context=None):
    text = render_to_string(template, context)
    slack_post_message(text)
