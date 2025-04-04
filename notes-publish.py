import ScriptingBridge
import json
import argparse
import re
import os

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

def export_note(note, output):
    lan = which_language(note)
    directory = f'{output}/{lan}'
    file_path = f'{directory}/{note.name()}.html'
    os.makedirs(directory, exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(note.body())

def export_note_meta(note, output):
    lan = which_language(note)
    directory = f'{output}/{lan}'
    file_path = f'{directory}/{note.name()}.json'
    os.makedirs(directory, exist_ok=True)
    with open(file_path, 'w') as file:
        meta = {
            "title": str(note.name()),
            "create_date": str(note.creationDate())
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
