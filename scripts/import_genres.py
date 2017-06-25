from albums.models import Genre
from data.models import GenreImport


def run():
    with open('scripts/csv/genre_labels.csv') as file:
        for line in file:
            # ID,SubCategory,rgb1,rgb2
            vals = line.split(',')
            genre = Genre(label=vals[1])
            genre.save()
            record = GenreImport(orig_id=int(vals[0]), new_id=genre.id)
            record.save()
