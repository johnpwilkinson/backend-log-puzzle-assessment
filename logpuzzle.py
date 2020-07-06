#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse
import shutil

def get_terminal_columns():
    return shutil.get_terminal_size().columns

def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    # exatracts host_name from file_name
    host = filename[re.search(r"_(.*?)", filename).span()[1]:]
    urlz = []
    # 
    with open(filename, "r") as f:
        for line in f:
            matches = re.findall(r'GET \S+ HTTP', line)
            # gets the urls that have 'puzzle' in them and are unique
            for match in matches:
                if match[5:-5] not in urlz and "puzzle" in match:
                    urlz.append(match[5:-5])
            # sorts alphabetically
            urlz.sort(key=lambda x: x[-8:-4])
            
    urlz = list(map(lambda each: "http://"+host + "/" + each, urlz))
    return urlz



def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # container for images
    res_list = []
    # if dest_dir doesnt exist, then make it
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
        # using enumerate to give each url an index
    for i, each in enumerate(img_urls):
        print(f"Downloading image {i+1} of {len(img_urls)}")
        # sets file name for each, retrieves and added file with name convention to list
        file_name = dest_dir + "/img" + str(i) + each[-4:]
        urllib.request.urlretrieve(each, file_name)
        res_list.append("img" + str(i) + each[-4:])
        # opens your destination dir and appends an <img> tag for corresponding img url
    with open(dest_dir + "/index.html", 'a') as f:
        f.write('<html><body>\n')
        for url in res_list:
            f.write(f'<img src={url}>')
        f.write("</body></html>")
        # prints output to the width of the console with instructions for user
    width = get_terminal_columns()
    print("/" * width)
    print(f"check out {dest_dir} and open index.html in chrome to see the image".center(width))
    print("/" * width)


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
