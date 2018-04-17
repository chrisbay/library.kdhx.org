from albums.models import RecordLabel, Album


def run(*args):
    from_label = RecordLabel.objects.get(id=args[0])
    to_label = RecordLabel.objects.get(id=args[1])
    to_merge = from_label.album_set.all()
    for album in to_merge:
        album.labels.remove(from_label)
        album.labels.add(to_label)
        album.save()
