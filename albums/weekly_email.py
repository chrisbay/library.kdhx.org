import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django_cron import CronJobBase, Schedule

from albums.models import Album


def get_week_endpoints():
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    return (start_date, end_date)


def weekly_email_msg():
    start_date, end_date = get_week_endpoints()
    albums = list(Album.objects.filter(created__date__gt=start_date))
    args = {
        'albums': sorted(albums, key=lambda x: (x.genre.label, x.artist.display_name)),
        'start_date': start_date,
        'end_date': end_date
    }
    return render_to_string('albums/weekly_email.jinja', args)


class SendMail(CronJobBase):

    RUN_EVERY_MINS = 1440 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'albums.weekly_email.SendMail'

    def do(self):
        start_date, end_date = get_week_endpoints()
        msg = weekly_email_msg()
        report_url = 'https://library.kdhx.org'+reverse("albums:weekly-email")
        send_mail(
            "New in the KDHX music library from {} to {}".format(start_date, end_date),
            report_url,
            'christopherbay@gmail.com',
            ['chris@chrisbay.net'],
            fail_silently=False,
            html_message=msg
        )