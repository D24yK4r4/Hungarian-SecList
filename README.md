# Hungarian SecList

Hungarian-language wordlists for security testing: password cracking, username enumeration, content discovery and fuzzing against Hungarian targets. Think of it as a Hungarian companion to [SecLists](https://github.com/danielmiessler/SecLists).

**[Magyar leírás lent ↓](#magyar)**

## Lists

| File | Entries | Contents |
|---|---:|---|
| `hungarian-words.txt` | 96,378 | Hungarian dictionary headwords (lowercase), checked against Hunspell hu_HU and a 4.4M-form corpus |
| `hungarian-proper-nouns.txt` | 14,782 | Place names (Hungary and historical Hungary), surnames, geographic names, institutions, brands |
| `hungarian-numbers.txt` | 6,801 | Number words: cardinals, ordinals, fractions, multiplicatives, collectives, distributives (spelling per AkH. 12) |
| `hungarian-passwords.txt` | 7,033 | Passwords Hungarians realistically use: names, cities, football clubs, food, endearments, swear words + year/digit suffixes, accented and unaccented twins, common PINs. Hand-built, **not** sourced from any breach |
| `names-female.txt` | 2,691 | Female given names (official registrable list style) |
| `names-male.txt` | 2,015 | Male given names |
| `names-romani.txt` | 293 | Given names, nicknames and surnames common among Hungarian Roma communities |
| `nicknames-female.txt` | 180 | Female diminutives / nicknames (becenevek) |
| `nicknames-male.txt` | 196 | Male diminutives / nicknames |
| `hungarian-slang-2026.txt` | 893 | Contemporary Hungarian slang: youth, gamer, chat, vulgar |
| `hunglish-mix.txt` | 576 | Hungarian–English code-mixed phrases and hybrid verbs (`lájkolom`, `overthinkelem`, `callban vagyok`) |
| `hungarian-books.txt` | 721 | Book, poem and novel titles known in Hungary (Hungarian titles) |
| `hungarian-movie-titles.txt` | 802 | Hungarian films/series and foreign films under their Hungarian release titles |

All files are UTF-8 (NFC), LF line endings, one entry per line, no duplicates, sorted in Hungarian collation (`LC_ALL=hu_HU.UTF-8 sort`).

Pre-stripped, accent-free copies of the biggest lists live in [`ascii/`](ascii/); a hashcat rule set is in [`rules/hungarian.rule`](rules/hungarian.rule); the generators and the validator are in [`scripts/`](scripts/).

## Usage

Accented characters (`á é í ó ö ő ú ü ű`) are kept. Many real-world Hungarian passwords are typed without them. Ready-made unaccented copies of the main lists are in [`ascii/`](ascii/); to strip accents from any list yourself:

```sh
# accent-free copy (handles ő/ű, which iconv//TRANSLIT often mangles)
python3 scripts/strip-accents.py hungarian-words.txt ascii/hungarian-words.txt

# iconv works too, but ONLY under a UTF-8 locale — in a C/POSIX locale it
# emits "?" for every accented letter:
LC_ALL=en_US.UTF-8 iconv -f utf-8 -t ascii//TRANSLIT hungarian-words.txt | sort -u

# hashcat: dictionary + the bundled Hungarian rule set
hashcat -m 0 hashes.txt hungarian-passwords.txt -r rules/hungarian.rule

# combine names with years
hashcat -a 6 -m 0 hashes.txt names-male.txt '?d?d?d?d'

# username candidates for account enumeration (kovacs.janos, jkovacs, ...)
python3 scripts/usernames.py --limit-given 50 > usernames.txt

# content discovery
ffuf -u https://target.hu/FUZZ -w hungarian-words.txt
```

Multi-word entries (titles, phrases) contain spaces; strip them (`tr -d ' '`) for password candidates.

## Maintenance

The lists are regenerable and validated:

```sh
# one-time: install the Hungarian locale (Debian/Ubuntu)
sudo locale-gen hu_HU.UTF-8

# check every list: UTF-8, NFC, LF, no dupes, Hungarian sort order, README counts
python3 scripts/check.py

# normalize, dedupe and re-sort every list in place
python3 scripts/check.py --fix

# rebuild the password list from its base words (src/password-bases.txt)
python3 scripts/passwords.py src/password-bases.txt
```

CI runs `scripts/check.py` on every push and pull request (see
[`.github/workflows/check.yml`](.github/workflows/check.yml)).

## Legal

For authorized security testing, research and education only. You are responsible for having permission to test any system you use these lists against.

## License

[MIT](LICENSE)

---

<a name="magyar"></a>
## Magyar

Magyar nyelvű wordlistek biztonsági teszteléshez: jelszótörés, felhasználónév-enumeráció, tartalomfelderítés és fuzzing magyar célpontokon. A [SecLists](https://github.com/danielmiessler/SecLists) magyar kiegészítője.

### Listák

| Fájl | Tartalom |
|---|---|
| `hungarian-words.txt` | Magyar szótári szavak (kisbetűs), Hunspell hu_HU szótárral és korpusszal ellenőrizve |
| `hungarian-proper-nouns.txt` | Helynevek (Magyarország és a történelmi Magyarország), vezetéknevek, földrajzi nevek, intézmények, márkák |
| `hungarian-numbers.txt` | Számnevek: tő-, sor-, tört-, szorzó-, gyűjtő- és osztószámnevek (AkH. 12 szerint) |
| `hungarian-passwords.txt` | Magyarok által valószínűleg használt jelszavak: nevek, városok, focicsapatok, ételek, becézések, káromkodások + évszám/szám végződések, ékezetes és ékezet nélküli párok, gyakori PIN-ek. Kézzel összeállítva, **nem** valódi adatszivárgásból |
| `names-female.txt`, `names-male.txt` | Női és férfi utónevek |
| `names-romani.txt` | Magyarországi roma közösségekben gyakori utónevek, becenevek és vezetéknevek |
| `nicknames-female.txt`, `nicknames-male.txt` | Becenevek |
| `hungarian-slang-2026.txt` | Mai magyar szleng: ifjúsági, gamer, chat, vulgáris |
| `hunglish-mix.txt` | Magyar–angol keverék kifejezések és hibrid igék |
| `hungarian-books.txt` | Magyarul ismert könyvek, versek, regények címei |
| `hungarian-movie-titles.txt` | Magyar filmek és sorozatok, valamint külföldi filmek magyar címen |

Minden fájl UTF-8 (NFC), LF sorvégű, soronként egy bejegyzés, duplikátum nélkül, magyar ábécérendben.

Előre elkészített, ékezet nélküli változatok az [`ascii/`](ascii/) mappában; hashcat szabályfájl: [`rules/hungarian.rule`](rules/hungarian.rule); a generátorok és az ellenőrző a [`scripts/`](scripts/) mappában.

Az ékezetek megmaradtak. Ékezet nélküli változat: `python3 scripts/strip-accents.py bemenet.txt`. (Az `iconv -f utf-8 -t ascii//TRANSLIT` csak UTF-8 locale alatt működik, C/POSIX locale-ban minden ékezetes betűre `?`-et ad.)

### Karbantartás

```sh
sudo locale-gen hu_HU.UTF-8      # egyszer, a magyar locale-hoz
python3 scripts/check.py         # minden lista ellenőrzése (CI is ezt futtatja)
python3 scripts/check.py --fix   # normalizálás, duplikátumok törlése, újrarendezés
```

### Jogi nyilatkozat

Kizárólag engedélyezett biztonsági tesztelésre, kutatásra és oktatásra. A felhasználó felel azért, hogy jogosult legyen a tesztelt rendszerek vizsgálatára.

### Licenc

[MIT](LICENSE)
