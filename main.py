import music_tag
from pathlib import Path
import json
import re

import logging

from Config import AppConfig
import setup

BIGBAG = "Bigbag"

ext_list = [
    "aac",
    "aiff",
    "dsf",
    "flac",
    "m4a",
    "mp3",
    "ogg",
    "opus",
    "wav",
    "wv"
]


def tag_music_files_in_path(playlist_path: Path, do_all=False):
    compatible_files_list = []
    with open(setup.done_files_path, "r") as done_files_f_r:
        done_files = json.load(done_files_f_r)
    with open(playlist_path, mode='r', encoding="utf8") as playlist_f:
        playlist_f = list(playlist_f)
        for x in range(0, len(playlist_f)):
            playlist_f[x] = playlist_f[x].replace('\n', '')
        for file_str in playlist_f:
            file_ext = re.findall(r'(?<=\.)\w*$', file_str)[0].lower()
            # logging.debug("file extension: " + file_ext)
            if file_ext in ext_list:
                compatible_files_list.append(file_str)

    for compat_file in compatible_files_list:
        # apply Bigbag genre
        if do_all or compat_file not in done_files:
            try:
                logging.debug(compat_file)
            except UnicodeError as e:
                logging.debug("Found unicode error for file name")
            # logging.debug(dir_path / file)
            try:
                f = music_tag.load_file(Path(compat_file))
                logging.debug(f['genre'].values)
                if do_all or ('Bigbag' not in f['genre'].values and 'Bigbag' not in str(f['genre'].values)):
                    logging.debug("Bigbag missing")
                    apply_genre(f, "Bigbag")
                    logging.debug(f['genre'])
                if compat_file not in done_files:
                    done_files.append(compat_file)
            except AttributeError as e:
                logging.debug("Attribute error, probably an embedded picture")
                logging.debug(str(e))
            except Exception as e:
                logging.debug(type(e))
                logging.debug(str(e))

    files_removed_from_bigbag = []
    for done_file in done_files:
        if done_file not in compatible_files_list:
            files_removed_from_bigbag.append(done_file)
    #Remove Bigbag Genre, add Xigbag
    for file_to_be_removed in files_removed_from_bigbag:
        file_to_be_removed_path = Path(file_to_be_removed)
        if file_to_be_removed_path.is_file():
            music_f = music_tag.load_file(file_to_be_removed_path)
            apply_genre(music_f, "Xigbag", "Bigbag")
        else:
            logging.debug("File does not exist: " + file_to_be_removed)
        done_files.remove(file_to_be_removed)
        logging.debug("removed Bigbag genre from: " + file_to_be_removed)
    with open(setup.done_files_path, "w") as done_files_f_w:
        json.dump(done_files, done_files_f_w)


def apply_genre(f, new_genre_str, remove_genre=None):
    genre = str(f['genre']).replace(",", ";").split(";")
    new_genre = [new_genre_str]
    for x in range(0, len(genre)):
        genre[x] = genre[x].strip(" ;'/][<>")
        if genre[x] != '' and genre[x] not in new_genre and genre[x] != remove_genre:
            new_genre.append(genre[x])
    f['genre'] = ";".join(new_genre)
    f.save()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tag_music_files_in_path(setup.playlist_path, do_all=AppConfig.App.DO_ALL)
    logging.debug("Completed")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
