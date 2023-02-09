import music_tag
from pathlib import Path
import re
import json
import re
from os.path import exists
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
done_files_path = "./done_files.json"


def tag_music_files_in_path(playlist_path: Path, do_all=False):
    compatible_files_list = []
    with open(done_files_path, "r") as done_files_f_r:
        done_files = json.load(done_files_f_r)
    with open(playlist_path, mode='r', encoding="utf8") as playlist_f:
        playlist_f = list(playlist_f)
        for x in range(0, len(playlist_f)):
            playlist_f[x] = playlist_f[x].replace('\n', '')
        for file_str in playlist_f:
            file_ext = re.findall(r'(?<=\.)\w*$', file_str)[0].lower()
            # print("file extension: " + file_ext)
            if file_ext in ext_list :
                compatible_files_list.append(file_str)

    for compat_file in compatible_files_list:
        if do_all or compat_file not in done_files:
            try:
                print(compat_file)
            except UnicodeError as e:
                print("Found unicode error for file name")
            # print(dir_path / file)
            try:
                f = music_tag.load_file(Path(compat_file))
                # print(f['genre'])
                # print(type(f['genre']))
                print(f['genre'].values)
                if do_all or ('Bigbag' not in f['genre'].values and 'Bigbag' not in str(f['genre'].values)):
                    print("Bigbag missing")
                    genre = str(f['genre']).replace(",",";").split(";")
                    new_genre = ["Bigbag"]
                    for x in range(0, len(genre)):
                        genre[x] = genre[x].strip(" ;'/][<>")
                        if genre[x] != '' and genre[x] not in new_genre:
                            new_genre.append(genre[x])
                    f['genre'] = ";".join(new_genre)
                    f.save()
                    print(f['genre'])
                if compat_file not in done_files:
                    done_files.append(compat_file)
            except AttributeError as e:
                print("Attribute error, probably an embedded picture")
                print(str(e))
            except Exception as e:
                print(type(e))
                print(str(e))

    files_removed_from_bigbag = []
    for done_file in done_files:
        if done_file not in compatible_files_list:
            files_removed_from_bigbag.append(done_file)
    for file_to_be_removed in files_removed_from_bigbag:
        file_to_be_removed_path = Path(file_to_be_removed)
        if file_to_be_removed_path.is_file():
            music_f = music_tag.load_file(file_to_be_removed_path)
            music_f["genre"] = str(music_f['genre']).replace(',', ';').replace('; Bigbag', '') + '; Xigbag'
            music_f.save()
        else:
            print("File does not exist: " + file_to_be_removed)
        done_files.remove(file_to_be_removed)
        print("removed Bigbag genre from: " + file_to_be_removed)
    with open(done_files_path, "w") as done_files_f_w:
        json.dump(done_files, done_files_f_w)



def test_a_file(music_file_path: str, do_all=False):
        file_ext = re.findall(r'(?<=\.)\w*$', music_file_path)[0].lower()
        # print("file extension: " + file_ext)
        if file_ext in ext_list:
            print(music_file_path + ": " + file_ext)
            # print(dir_path / file)
            f = music_tag.load_file(Path(music_file_path))
            print(f['genre'])
            # print(type(f['genre']))
            if do_all or 'Bigbag' not in f['genre'].values:
                print("Bigbag missing")
                print(f['genre'])
                f['genre'] = str(f['genre']) + ', Bigbag'
                f.save()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # test_a_file("C:\\Users\\sathy\\Music\\01 Donna Lee.mp3")
    tag_music_files_in_path(Path("C:\\Users\\sathy\\Music\\MusicBee\\Playlists\\Meesta\\BigBag2.m3u"), do_all=True)
    print("Completed")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


