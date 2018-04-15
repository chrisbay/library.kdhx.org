from albums.models import Album, Artist, RecordLabel, MediaType, Genre, Location
from data.models import AlbumImport, GenreImport
from django.db.models import ObjectDoesNotExist
from django.utils.timezone import make_aware, now
from datetime import datetime
import csv
import sys
import traceback
import re


TEST_MODE = False
TEST_MAX = 500


def run():
    if TEST_MODE:
        Album.objects.all().delete()
        AlbumImport.objects.all().delete()
    try:

        various_artists_obj = Artist.objects.get(name='Various Artists')
        self_released_obj = RecordLabel.objects.get(name='Self')
        default_media_obj = MediaType.objects.get(label='CD')
        default_location = Location.objects.get(label='Library')
        orig_genre_values = [x.orig_id for x in GenreImport.objects.all()]

        with open('scripts/csv/music.csv') as file:
            csv_reader = csv.reader(file, dialect=csv.unix_dialect, escapechar='\\')

            # Skip header row
            next(csv_reader)

            row_count = 0
            for row in csv_reader:

                if TEST_MODE:
                    row_count += 1
                    if row_count > TEST_MAX:
                        break

                # Columns in imported data
                # [0] seq (ID)
                # [1] ArtistFirst
                # [2] ArtistLast
                # [3] FileUnder
                # [4] Title
                # [5] DateIn
                # [6] DateOut
                # [7] LabelKey
                # [8] LabelID
                # [9] LabelName
                # [10] ReportType
                # [11] GenreID
                # [12] Obsenity
                # [13] Media
                # [14] NumCopies
                # [15] Women
                # [16] GayLesbian
                # [17] Local
                # [18] OtherInterest
                # [19] MIA (location)
                # [20] stamp

                # Don't create duplicate entries
                existing_album_import_res = AlbumImport.objects.filter(orig_id=int(row[0]))
                if len(existing_album_import_res):
                    existing_album_import = existing_album_import_res[0]
                    print("Album with orig_id={0} and new_id={1} has already been imported"
                          .format(existing_album_import.orig_id, existing_album_import.new_id))
                    continue

                title = clean_text(row[4])

                csv_artist_first = clean_text(row[1])
                csv_artist_last = clean_text(row[2])
                csv_file_under = clean_text(row[3])
                if csv_file_under == '#':
                    artist = various_artists_obj
                elif row[1].strip() == '':
                    existing_artist = Artist.objects.filter(name__iexact=csv_artist_last)
                    if len(existing_artist) > 0:
                        artist = existing_artist[0]
                    else:
                        artist = Artist.objects.create(name=csv_artist_last)
                else:
                    existing_artist = Artist.objects.filter(last__iexact=csv_artist_last).filter(first__iexact=csv_artist_first)
                    if len(existing_artist):
                        artist = existing_artist[0]
                    else:
                        artist = Artist.objects.create(first=csv_artist_first, last=csv_artist_last)

                csv_labels = row[9].split('/')
                csv_labels = [x.strip() for x in csv_labels]
                labels = []
                if len(csv_labels):
                    for csv_label in csv_labels:
                        csv_label = clean_text(csv_label)
                        existing_label = RecordLabel.objects.filter(name__iexact=csv_label)
                        if len(existing_label) > 0:
                            labels.append(existing_label[0])
                        else:
                            new_label = RecordLabel.objects.create(name=csv_label)
                            labels.append(new_label)
                else:
                    labels.append(self_released_obj)

                existing_media = MediaType.objects.filter(label__iexact=row[9])
                if len(existing_media):
                    media_obj = existing_media[0]
                else:
                    media_obj = default_media_obj

                csv_genre_id = int(row[11])

                # Combine world beat/folk genres
                if 15 <= csv_genre_id <= 21:
                    csv_genre_id = csv_genre_id + 14
                elif csv_genre_id == 36:
                    csv_genre_id = 37

                if csv_genre_id not in orig_genre_values:
                    print("Skipping import of album with unknown genre: {0}".format(csv_genre_id))
                    continue

                genre_import = GenreImport.objects.get(orig_id=csv_genre_id)
                genre = Genre.objects.get(pk=genre_import.new_id)

                csv_location = clean_text(row[19])
                if csv_location == 'Gone Missing':
                    csv_location = 'Missing'
                try:
                    location = Location.objects.get(label=csv_location)
                except ObjectDoesNotExist:
                    location = default_location

                csv_created = row[5].strip()
                if len(csv_created):
                    csv_created_parts = [int(x) for x in csv_created.split('-')]
                    try:
                        created = make_aware(datetime(csv_created_parts[0], csv_created_parts[1], csv_created_parts[2]))
                    except ValueError: # Set created to now for invalid dates
                        created = now()
                else:
                    created = now()

                album = Album.objects.create(title=title, artist=artist, media=media_obj,
                              genre=genre, location=location, created=created)
                album.labels = labels
                album.save()
                AlbumImport.objects.create(orig_id=int(row[0]), new_id=album.id)
    except:
        print('{0} - {1}'.format(sys.exc_info()[0], sys.exc_info()[1]))
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)


def clean_text(text):
    text = str.replace(text, '&#039;', "'")
    p = re.compile('&amp;', re.I)
    text = p.sub('&', text)
    return text.strip().title()