# jupyter-server
Automatska konfiguracija Jupyter servera za potrebe PFE kampova.

## Ključevi
U direktorijum `keys/` potrebno je da se nalaze dva fajla:

- `authorized_keys` sa javnim ključevima administratora servera na kojem se pokreće Jupyter server
- `id_ed25519` sa ključem koji je postavljen kao [deploy key](https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys) i koji se koristi za kloniranje privatnih Git repozitorijuma sa PFE organizacije.

## Korisnici
U direktorijumu `users` napravite fajl pod nazivom `users.txt` i u njega stavite imena i prezimena svih polaznika, neošišanom latinicom. Zatim pokrenite `users.py` iz tog direktorijuma kako biste generisali `users.json` fajl sa njihovim imenima, prezimenima, korisničkim imenima i lozinkama koji se koristi za pravljenje njihovih naloga na serveru, kao i za prikazivanje punih imena u rezultatima na tabli.

Nakon generisanja dodajte korisnika `pfe` u `users.json` ručno. On će služiti kao administrator JupyterHub instance, i lozinka za tog korisnika će takođe biti lozinka za tablu sa rezultatima testova.

Administrativni korisnik `pfe` ima mogućnost logovanja kao bilo koji drugi korisnik kroz *File > Hub Control Panel > Admin > Access Server*, a takođe može da pregleda (bez izmena) sve datoteke korisnika unutar `ADMINISTRATOR` direktorijuma u svom radnom prostoru.

### Distribucija lozinki
Postoje dva automatizovana načina da se polaznicima podele njihove JupyterHub lozinke: štampanjem na papiru ili preko Discord-a.

#### Štampanje kredencijala
Potrebno je u `users` direktorijumu pokrenuti `print_user_auth.py` skriptu, ona će izgenerisati `users.pdf` fajl koji je onda moguće odštampati i iseći kako bi se polaznicima podelili kredencijali.

#### Discord
Potrebno je napraviti `autodetection.json` fajl u `users` direktorijumu sa sledećom šemom:
```json
{
    "token": "",                    // Discord bot token
    "guild_id": 0,                  // ID PFE Discord servera
    "role_id": 0,                   // ID uloge u kojoj su polaznici za koje se organizuje kamp
    "message": "Kredencijali za JupyterHub su sledeći:\nKorisničko ime: `{username}`\nLozinka: `{password}`"
}
```
Nakon toga pokrenuti `users.py` opet (ili po prvi put) i on će pokušati da automatski detektuje koji nalog pripada kojem polazniku. Ukoliko za nekog polaznika ne uspe, proveriti da li je dobro postavljen nadimak na Discord ili ručno dodati u `users.json` kao `discord_id` polje sa Discord identifikatorom polaznika. Kad je to spremno, pokrenuti `send_user_auth.py` kako bi se polaznicima poslali kredencijali preko Discord DM.

### Arhiviranje korisničkih datoteka

Pozivom komande `jupyterhub_archive.sh` se u radni direktorijum arhiviraju svi JupyterHub podaci korisnika. Unutar `jupyterhub_YYYY-MM-DDTHH:MM:SS.zip` se nalaze zasebno arhivirani direktorijumi, gde je direktorijum svakog korisnika enkriptovan njegovom šifrom.

## Konfiguracija
Glavni deo servera podešava se kroz [Ansible](https://www.ansible.com/). Nakon što ste podesili parametre iznad, u `hosts.ini` podesite adresu servera koji podešavate i pokrenite:
```console
$ pip install -r requirements.txt
$ ANSIBLE_NOCOWS=1 ansible-playbook -i hosts.ini ./provision-server.yml
```

Nakon toga se u zavisnosti od tipa radionice pokreće:

- Za [opšti tip](#struktura-repozitorijuma-opšteg-tipa-radionica) radionice:
    ```console
    $ ANSIBLE_NOCOWS=1 ansible-playbook -i hosts.ini ./provision-generic.yml
    ```

- Za [Testbench](https://github.com/pfe-rs/jupyter-testbench) tip radionice:
    ```console
    $ ANSIBLE_NOCOWS=1 ansible-playbook -i hosts.ini ./provision-testbench.yml
    ```

## Napomene
- Ukoliko menjate `config/nginx/*.j2` fajlove, oni se **neće ažurirati na serveru** ukoliko već postoje. Ovo je zbog toga što se nakon postavljanja na server oni menjanju preko [Certbot](https://certbot.eff.org/), samo ukoliko Certbot već nije pokretan ranije (jer pokretanje više puta može da generiše više sertifikata, a Let's Encrypt ima ograničenje na broj sertifikata generisanih tokom dana).
- Ukoliko želite da forsirate ažuriranje konfiguracije i generisanje sertifikata, iskomentarišite liniju sa `creates:` kod koraka za generisanje sertifikata, i `force: no` kod Nginx konfiguracionih fajlova koje želite da regenerišete u `playbook.yml`.

### Struktura repozitorijuma opšteg tipa radionica

Repozitorijum za radionicu treba da bude struktuiran na sledeći način:
- `notebooks/`: sveske koje treba da se kopiraju u radni direktorijum svakog korisnika
- `dataset/`: svi podaci sa kojima korisnici treba da interaguju, imutabilno se linkuje u radni direktorijum svakog korisnika
- `packages/`: biblioteke napravljene za potrebe radionice (npr. [SauLib](https://github.com/pfe-rs/sau-radionica/tree/master/SauLib)) koje korisnici mogu da importuju
  - `setup.py`: meta-paket koji sadrži informacije o bibliotekama ([primer](https://github.com/pfe-rs/dos-radionica/blob/master/packages/setup.py))
- `LICENSE`: licenca pod kojom je kod objavljen, poželjno [MIT](https://mit-license.org/)
- `requirements.txt`: lista Python paketa (sa fiksiranom [minor](https://semver.org/#summary) verzijom) koji su neophodni za izvršavanje koda u sveskama
- `packages.txt`: lista sistemskih paketa koji su neophodni za izvršavanje koda u sveskama

```
├─ dataset/
│  ├─ signal_za_obradu.wav
│  ├─ podaci_za_treniranje.csv
│  └─ slika_za_obradu.png
├─ notebooks/
│  └─ Primer sveske.ipynb
├─ packages
│  ├─ setup.py
│  └─ biblioteka
│     └─ __init__.py
├─ LICENSE
├─ packages.txt
└─ requirements.txt
```
