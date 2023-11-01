import re
import sys

import openai
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

from config import settings

openai.api_key = settings.openai_api_key


def summarize_text(user_text):
    # Create a conversation with a system message and user message
    conversation = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant that can summarize text. Please summarize the following text:",
        },
        {"role": "user", "content": user_text},
    ]

    # Generate a response using ChatCompletions API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conversation  # Choose the appropriate model
    )
    return response


def summarize_comment(user_text):
    # Create a conversation with a system message and user message
    conversation = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant that summarizes comments from discussion forums. Please provide a concise summary of the following comment and the sentiment expressed.",
        },
        {"role": "user", "content": user_text},
    ]

    # Generate a response using ChatCompletions API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conversation  # Choose the appropriate model
    )
    return response


def summarize_summaries(full_sum):
    # Create a conversation with a system message and user message
    conversation = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant that summarizes summaries of proposals and the comments from their discussion forums. Please provide a concise summary of the following proposal and the general thoughts and sentiment expressed in the discussion.",
        },
        {"role": "user", "content": full_sum},
    ]

    # Generate a response using ChatCompletions API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conversation  # Choose the appropriate model
    )
    return response


def get_md_table(table):
    table_data = []
    for row in table.find_all("tr"):
        row_data = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
        table_data.append(row_data)
    markdown_table = tabulate(table_data, tablefmt="pipe", headers="firstrow")
    return markdown_table


def get_list(element_list):
    return element_list.get_text().rstrip("\n").replace("\n", "\n* ")


def get_ordered_list(element_list):
    text = element_list.get_text()
    text = re.sub(r"\n+", "\n", text)
    return text.rstrip("\n").replace("\n", "\n1. ")


def get_text(elements):
    # remove images
    [
        i.decompose()
        for d in elements
        for i in d.find_all("div", class_="lightbox-wrapper")
    ]
    output = []
    for element in elements:
        output_l = ""
        for line in element:
            if line.name == "ul":
                output_l += get_list(line) + "\n"
            elif line.name == "ol":
                output_l += get_ordered_list(line) + "\n"
            elif hasattr(line, "attrs") and line.attrs.get("class") == ["md-table"]:
                output_l += get_md_table(line) + "\n"
            else:
                if line.name is not None:
                    output_l += line.get_text() + "\n"
        output.append(output_l)
    return output


def summarize_proposal(url):
    website = requests.get(url)
    soup = BeautifulSoup(website.text, "html.parser")
    article_body = soup.find_all("div", class_="post", itemprop="articleBody")
    discussion = soup.find_all("div", class_="post", itemprop="text")
    prop_sum = summarize_text(get_text(article_body)[0]).choices[0].message.content
    com_sum = ""
    for comment in get_text(discussion):
        com_sum += summarize_comment(comment).choices[0].message.content + "\n~~~\n"
    full_sum = f"Proposal Summary: {prop_sum}.\n Discussion Summaries: {com_sum}"
    discussion_sum = summarize_summaries(full_sum).choices[0].message.content
    return prop_sum, discussion_sum


if __name__ == "__main__":
    proposal_summary, discussion_summary = summarize_proposal(sys.argv[1])
    print(
        f"Proposal Summary:\n{proposal_summary}\n\nDiscussion Summary:\n{discussion_summary}"
    )
