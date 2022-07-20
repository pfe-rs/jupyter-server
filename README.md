# jupyter-server
Automatska konfiguracija Jupyter servera za potrebe PFE kampova.

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
- `LICENSE`: licenca pod kojom je kod objavljen, poželjno [MIT](https://mit-license.org/)
- `requirements.txt`: lista Python paketa (sa fiksiranom [minor](https://semver.org/#summary) verzijom) koji su neophodni za izvršavanje koda u sveskama

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
└─ requirements.txt
```
