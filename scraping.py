#!/usr/bin/env python

import sys
import argparse
import requests
import re
from bs4 import BeautifulSoup


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('website',
                        help="website to be scraped")
    return parser


def scrape_web(args):
    url = args.website
    r = requests.get(url)
    websites = re.findall(
        'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', r.text)
    websites = set(websites)
    emails = re.findall(
        r'[\w\.-]+@[\w\.-]+', r.text)
    emails = set(emails)
    phone_numbers = re.findall(
        r'(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})', r.text)
    phone_numbers = set(phone_numbers)
    print("Emails:")
    for email in emails:
        print(email)

    print("Websites:")
    for site in websites:
        print(site)

    print("Phone Numbers:")
    for number in phone_numbers:
        print(number)


def find_rel_links(args):
    url = args.website
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    for link in soup.find_all('a'):
        print("In an <a> tags:", link.get('href'))
    for link in soup.find_all('img'):
        print("In an <img> tags:", link.get('src'))


def main(args):
    parser = create_parser()
    args = parser.parse_args()

    if not args:
        parser.print_usage()
        sys.exit(1)

    if args.website:
        scrape_web(args)
        find_rel_links(args)


if __name__ == '__main__':
    main(sys.argv[1:])
