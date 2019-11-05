from datetime import date, timedelta
import re
import orodja as o

vzorec = (
    r'<span class="chart-element__rank__number">(?P<mesto_na_lestvici>\d{1,3})</span>'
    r'\s+'
    r'<span.*</span>'
    r'\s+'
    r'</span>'
    r'\s+'
    r'<span.*>'
    r'\s+'
    r'<span class="chart-element__information__song text--truncate color--primary">(?P<naslov_pesmi>.+)</span>'
    r'\s+'
    r'<span class="chart-element__information__artist text--truncate color--secondary">(?P<ime_izvajalca>.+)</span>'
    r'\s+'
    r'<.+>'
    r'\s+'
    r'<span.*</span>'
    r'\s+'
    r'<span.*</span>'
    r'\s+'
    r'<span class="chart-element__information__delta__text text--peak">(?P<najvišje_mesto>\d{1,3}) Peak Rank</span>'
    r'\s+'
    r'<span class="chart-element__information__delta__text text--week">(?P<tednov_na_lestvici>\d+) Weeks on Chart</span>'
)

def vse_sobote_v_letu(year):
   d = date(year, 1, 1)                    # January 1st
   d += timedelta(days = 5 - d.weekday())  # First Sunday
   while d.year == year:
      yield d
      d += timedelta(days = 7)

for sobota in vse_sobote_v_letu(2018):
   url = f'https://www.billboard.com/charts/hot-100/{sobota}'
   ime_datoteke = f'billboard_{sobota}'
   o.shrani_spletno_stran(url, ime_datoteke)

with open('prebrano', 'w', encoding='utf-8') as p:
   for sobota in vse_sobote_v_letu(2018):
      datoteka = f'billboard_{sobota}'
      vsebina = o.vsebina_datoteke(datoteka)
      vsebina = vsebina.replace('&#039;','\'')
      vsebina = vsebina.replace('&amp;','&')
      for zadetek in re.finditer(vzorec, vsebina):
         p.write(str(zadetek.groupdict()))

pesmi = []

for sobota in vse_sobote_v_letu(2018):
   datoteka = f'billboard_{sobota}'
   vsebina = o.vsebina_datoteke(datoteka)
   vsebina = vsebina.replace('&#039;','\'')
   vsebina = vsebina.replace('&amp;','&')
   for zadetek in re.finditer(vzorec, vsebina):
      pesmi.append(zadetek.groupdict())

o.zapisi_json(pesmi,'billboard.json')
o.zapisi_csv(pesmi,['mesto_na_lestvici','naslov_pesmi','ime_izvajalca','najvišje_mesto','tednov_na_lestvici'],'billboard.csv')