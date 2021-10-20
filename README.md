# jupyter-server
Automatska konfiguracija Jupyter servera za potrebe PFE letnjeg seminara za nove polaznike 2021. godine.

## Ključevi
U direktorijum `keys/` potrebno je da se nalaze dva fajla:

- `authorized_keys` sa javnim ključevima administratora servera na kojem se pokreće Jupyter server
- `id_ed25519` sa ključem koji je postavljen kao [deploy key](https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys) i koji se koristi za kloniranje privatnih Git repozitorijuma sa PFE organizacije.

## Korisnici
Napravite fajl pod nazivom `users.txt` i u njega stavite imena i prezimena svih polaznika, neošišanom latinicom. Zatim pokrenite `python users.py < users.txt` kako biste generisali `users.json` fajl sa njihovim imenima, prezimenima, korisničkim imenima i lozinkama koji se koristi za pravljenje njihovih naloga na serveru, kao i za prikazivanje punih imena u rezultatima na tabli.

Nakon generisanja dodajte korisnika `pfe` u `users.json` ručno. On će služiti kao administrator JupyterHub instance, i lozinka za tog korisnika će takođe biti lozinka za tablu sa rezultatima testova.

## Konfiguracija
Glavni deo servera podešava se kroz [Ansible](https://www.ansible.com/). Nakon što ste podesili parametre iznad, u `hosts.ini` podesite adresu servera koji podešavate i pokrenite:
```console
$ pip install -r requirements.txt
$ ANSIBLE_NOCOWS=1 ansible-playbook -i hosts.ini ./playbook.yml
```

## Napomene
- Ukoliko menjate `config/nginx/*.conf` fajlove, oni se **neće ažurirati na serveru** ukoliko već postoje. Ovo je zbog toga što se nakon postavljanja na server oni menjanju preko [Certbot](https://certbot.eff.org/), samo ukoliko Certbot već nije pokretan ranije (jer pokretanje više puta može da generiše više sertifikata, a Let's Encrypt ima ograničenje na broj sertifikata generisanih tokom dana).
    - Ukoliko želite da forsirate ažuriranje konfiguracije i generisanje sertifikata, iskomentarišite liniju sa `creates:` kod koraka za generisanje sertifikata, i `force: no` kod Nginx konfiguracionih fajlova koje želite da regenerišete u `playbook.yml`.
