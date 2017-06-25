from classification.models import GenreLabel
from albums.models import Genre
from data.models import GenreLabelImport


def run():
    with open('scripts/csv/genre_labels.csv') as file:
        for line in file:
            # ID,SubCategory,rgb1,rgb2
            vals = line.split(',')
            genre = Genre.objects.get(label__exact=vals[1])
            if genre:
                genre_label = GenreLabel(genre=genre,
                                         color_left=vals[2],
                                         color_right=vals[3])
                genre_label.save()
                record = GenreLabelImport(orig_id=int(vals[0]),
                                          new_id=genre_label.id)
                record.save()
