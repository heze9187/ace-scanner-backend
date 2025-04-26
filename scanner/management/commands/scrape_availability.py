# scanner/management/commands/scrape_availability.py
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from scanner.models import Court, CourtAvailability

class Command(BaseCommand):
    help = 'Scrape NYC Parks court availability and save into database'

    def handle(self, *args, **kwargs):
        courts = Court.objects.all()

        print(courts)

        # First, clear old availability
        CourtAvailability.objects.all().delete()

        for court in courts:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            r = requests.get(court.url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            tab_content = soup.find('div', class_='tab-content')
            print(tab_content)
            if not tab_content:
                continue

            for day_tab in tab_content:
                curr_date = day_tab.h3.string
                tbody = day_tab.table.tbody
                for trow in tbody:
                    curr_time = trow.find('strong').string
                    tds = trow.find_all('td', class_='status2')
                    if tds:
                        date_object = datetime.strptime(curr_date, "%A, %B %d, %Y").date()

                        # Save availability
                        CourtAvailability.objects.create(
                            court=court,
                            date=date_object,
                            time=curr_time
                        )

        self.stdout.write(self.style.SUCCESS('Scraping and saving done!'))