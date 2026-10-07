# Hungarian SecList

Hungarian-language wordlists for security testing: password cracking, username enumeration, content discovery and fuzzing against Hungarian targets. Think of it as a Hungarian companion to [SecLists](https://github.com/danielmiessler/SecLists).

**[Magyar leírás lent ↓](#magyar)**

## Lists

| File | Entries | Contents |
|---|---:|---|
| `hungarian-words.txt` | 96,378 | Hungarian dictionary headwords (lowercase), checked against Hunspell hu_HU and a 4.4M-form corpus |
| `hungarian-proper-nouns.txt` | 14,782 | Place names (Hungary and historical Hungary), surnames, geographic names, institutions, brands |
| `hungarian-numbers.txt` | 6,801 | Number words: cardinals, ordinals, fractions, multiplicatives, collectives, distributives (spelling per AkH. 12) |
| `hungarian-passwords.txt` | 2,564 | Passwords Hungarians realistically use: names, cities, football clubs, food, swear words + year/digit suffixes, accented and unaccented twins, common PINs |
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

## Usage

Accented characters (`á é í ó ö ő ú ü ű`) are kept. Many real-world Hungarian passwords are typed without them, so generate unaccented variants when needed:

```sh
# strip accents
iconv -f utf-8 -t ascii//TRANSLIT hungarian-words.txt | sort -u > hungarian-words-ascii.txt

# hashcat: dictionary + rules
hashcat -m 0 hashes.txt hungarian-passwords.txt -r rules/best64.rule

# combine names with years
hashcat -a 6 -m 0 hashes.txt names-male.txt '?d?d?d?d'

# content discovery
ffuf -u https://target.hu/FUZZ -w hungarian-words.txt
```

Multi-word entries (titles, phrases) contain spaces; strip them (`tr -d ' '`) for password candidates.

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
| `hungarian-passwords.txt` | Magyarok által valóban használt jelszavak: nevek, városok, focicsapatok, ételek, káromkodások + évszám/szám végződések, ékezetes és ékezet nélküli párok, gyakori PIN-ek |
| `names-female.txt`, `names-male.txt` | Női és férfi utónevek |
| `names-romani.txt` | Magyarországi roma közösségekben gyakori utónevek, becenevek és vezetéknevek |
| `nicknames-female.txt`, `nicknames-male.txt` | Becenevek |
| `hungarian-slang-2026.txt` | Mai magyar szleng: ifjúsági, gamer, chat, vulgáris |
| `hunglish-mix.txt` | Magyar–angol keverék kifejezések és hibrid igék |
| `hungarian-books.txt` | Magyarul ismert könyvek, versek, regények címei |
| `hungarian-movie-titles.txt` | Magyar filmek és sorozatok, valamint külföldi filmek magyar címen |

Minden fájl UTF-8 (NFC), LF sorvégű, soronként egy bejegyzés, duplikátum nélkül, magyar ábécérendben.

Az ékezetek megmaradtak. Ékezet nélküli változathoz: `iconv -f utf-8 -t ascii//TRANSLIT`.

### Jogi nyilatkozat

Kizárólag engedélyezett biztonsági tesztelésre, kutatásra és oktatásra. A felhasználó felel azért, hogy jogosult legyen a tesztelt rendszerek vizsgálatára.

### Licenc

[MIT](LICENSE)
