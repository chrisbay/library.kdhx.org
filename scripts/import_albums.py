from albums.models import Album, Artist, RecordLabel, MediaType, Genre, Location
from data.models import AlbumImport, GenreImport
from django.db.models import ObjectDoesNotExist
from datetime import datetime
import csv
import sys
import traceback


TEST_MODE = True
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
            csv_reader = csv.reader(file, dialect=csv.unix_dialect, quoting=csv.QUOTE_NONE, escapechar='\\')

            # Skip header row
            next(csv_reader)

            row_count = 0
            for row in csv_reader:

                if TEST_MODE:
                    row_count += 1
                    if row_count > TEST_MAX:
                        break

                # Columns in imported data
                # [0] ID
                # [1] ArtistFirst
                # [2] ArtistLast
                # [3] FileUnder
                # [4] Title
                # [5] DateIn
                # [6] LabelName
                # [7] GenreID
                # [9] Media
                # [13] MIA (location)

                # Don't create duplicate entries
                existing_album_import_res = AlbumImport.objects.filter(orig_id=int(row[0]))
                if len(existing_album_import_res):
                    existing_album_import = existing_album_import_res[0]
                    print("Album with orig_id={0} and new_id={1} has already been imported"
                          .format(existing_album_import.orig_id, existing_album_import.new_id))
                    continue

                title = row[4].title()

                csv_artist_first = row[1].strip().title()
                csv_artist_last = row[2].strip().title()
                csv_file_under = row[3].strip()
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

                csv_labels = row[6].split('/')
                csv_labels = [x.strip() for x in csv_labels]
                labels = []
                if len(csv_labels):
                    for csv_label in csv_labels:
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

                csv_genre_id = int(row[7])

                # Combine world beat/folk genres
                if 15 <= csv_genre_id <= 21:
                    csv_genre_id = csv_genre_id + 14
                elif csv_genre_id == 36:
                    csv_genre_id = 37

                if csv_genre_id not in orig_genre_values:
                    print("Skipping import of album with unknown genre: {0}".format(csv_genre_id))
                    continue

                genre_import = GenreImport.objects.get(orig_id=int(row[7]))
                genre = Genre.objects.get(pk=genre_import.new_id)

                csv_location = row[13].strip().title()
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
                        created = datetime(csv_created_parts[0], csv_created_parts[1], csv_created_parts[2])
                    except ValueError: # Set created to now for invalid dates
                        created = datetime.now()
                else:
                    created = datetime.now()

                album = Album.objects.create(title=title, artist=artist, media=media_obj,
                              genre=genre, location=location, created=created)
                album.labels = labels
                album.save()
                AlbumImport.objects.create(orig_id=int(row[0]), new_id=album.id)
    except:
        print('{0} - {1}'.format(sys.exc_info()[0], sys.exc_info()[1]))
        tb = sys.exc_info()[2]
        traceback.print_tb(tb)
