import json
import re
import requests
import orodja

stevilo_del = 2994
del_na_stran = 10


start = 1

for start in range(1, stevilo_del, del_na_stran):
     url = (
      f'https://www.studentski-servis.com/index.php?t=prostaDela&page={start}&perPage={del_na_stran}'
     '&podjetje=&sort=1&workType=1&keyword=&urnaPostavkaMin=4.13&urnaPostavkaMax=20.00'
            )
     r = requests.get(url)

     vsebina = r.text

     with open(f'dela-{start}-{start + del_na_stran - 1}.html', 'w', encoding="utf-8") as f:
        f.write(vsebina)

#for start in range(1, stevilo_del, del_na_stran):
   # with open(f'dela-{start}-{start + del_na_stran - 1}.html') as f:
      #  vsebina = f.read()
    #for zadetek in re.finditer(vzorec_bloka, vsebina):
       # dela.append(zadetek.groupdict())
       # count += 1

#with open('dela.json', 'w') as f:
    #json.dump(dela, f, indent=2, ensure_ascii=True)


   # r'<span class="lokacija"><img src="?*"><strong>(?P<lokacija>.+?)</strong></span>'


count = 0   
dela = []


vzorec = re.compile(r'<span class="title">(?P<naslov>.+?)</span>.*?'
                    r'<strong>(?P<postavka_neto>[0-9]{1,2},[0-9]{1,2}).+?neto</strong>.*?'
                    r'<span class="lokacija">\n\s*<img src="resources/images/icons/icon_job_location.png" />\n\s+<strong>(?P<lokacija>.+?)</strong>\n{2}\s*</span>\n{2}\s*</div>\n{4}\s*<div class="col jobData">\n+\s+<div class="cols space20 cols1-3">.*?'
                    r'<div class="jobContent col">\n\n\s+<p>(?P<opis>.+?)</p>\n\n\s+<ul>\n\n\s+<li><strong>'
                    r'.+?t. prostih mest:</strong>\s(?P<prosta_mesta>[0-9]{1,2})\s<span class="spacer">.*?'
                    r'<li><strong>Trajanje:</strong>(?P<trajanje>.+?)\s<span class="spacer">.*?'
                    r'<li><strong>Delovnik:</strong>(?P<delovnik>.+?)<span class="spacer">.*?'
                    r'<li><strong>.*?ifra:</strong>\s(?P<sifra>\d{6})\s.*?'
                    r'<strong>Narava dela:</strong>(?P<narava_dela>.+?)</li>',
                    flags=re.DOTALL
                        )

                                 
                  
#<p>(?P<opis>.*)</p>\n*\s*<ul>\n*\s*<li><strong>

for start in range(1, stevilo_del, del_na_stran):
    with open(f'dela-{start}-{start + del_na_stran - 1}.html') as f:
        vsebina = f.read()
        for zadetek in re.finditer(vzorec, vsebina):
            dela.append(zadetek.groupdict())
            count += 1
       
print(dela)
print(count)


with open('dela.json', 'w') as f:
    json.dump(dela, f, indent=2, ensure_ascii=True)


