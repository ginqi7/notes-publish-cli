import ScriptingBridge
import json
import argparse
import re
import os
from datetime import datetime
from tzlocal import get_localzone
from readability import Document
from bs4 import BeautifulSoup


def find_folder(app: ScriptingBridge.SBApplication, name: str):
    for folder in app.folders():
        if folder.name() == name:
            return folder


def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fff]')
    return bool(pattern.search(text))

def which_language(note):
    if contains_chinese(note.body()):
        return "zh"
    return "en"

def prettify_html(html):
    tree = BeautifulSoup(html, features="lxml")
    flag = True
    while flag:
        flag = False
        for x in tree.find_all():
            if (not x.contents) and len(x.get_text(strip=True)) == 0 and x.name not in ['img']:
                flag = True
                x.extract()

    return tree.prettify()


def export_note(note, output):
    lan = which_language(note)
    directory = f'{output}/{lan}'
    file_path = f'{directory}/{note.name()}.html'
    os.makedirs(directory, exist_ok=True)
    with open(file_path, 'w') as file:
        good_html = prettify_html(note.body())
        file.write(good_html)

def query_creation_date(html):
    pattern = r'>#(\d{4}-\d{2}-\d{2})<'
    matches = re.search(pattern, html)
    if matches:
        return matches.group(1)

def time_convert(time_str):
    # Parse the string into a datetime object (UTC time)
    utc_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S %z")

    # Retrieve the system timezone
    system_timezone = get_localzone()

    # Convert UTC time to system timezone time
    return str(utc_time.astimezone(system_timezone))

def export_note_meta(note, output):
    lan = which_language(note)
    directory = f'{output}/{lan}'
    file_path = f'{directory}/{note.name()}.json'
    os.makedirs(directory, exist_ok=True)
    creation_date = query_creation_date(note.body())
    if not creation_date:
        creation_date = time_convert(str(note.creationDate()))
    with open(file_path, 'w') as file:
        meta = {
            "title": str(note.name()),
            "create_date": creation_date
        }
        json.dump(meta, file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="A simple CLI for publishing MacOS Notes.")

    parser.add_argument("output", help="Output directory.")
    parser.add_argument("folder", help="MacOS Notes folder.")
    args = parser.parse_args()
    output = args.output
    folder = args.folder
    app = ScriptingBridge.SBApplication.alloc().initWithBundleIdentifier_("com.apple.Notes")
    folder = find_folder(app, folder)
    notes = folder.notes()
    for note in notes:
        print(f'Export {note.name()} to {output}')
        export_note(note, output)
        export_note_meta(note, output)

if __name__ == "__main__":
    main()
