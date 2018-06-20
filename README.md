# DirtyText # 
Searches for [ab]using of Unicode glyphs.

# Quick tour: #

## Common options: ##
- Read text directly from file: --file \<filename>
- Save modified text: --save \<file>
- Filter text: --filter
- Pipeline mode: -p/--pipeline

### Looks for ZERO-WIDTH characters: ###
    $> echo "This text‌‌‌‌‍‌‬‌‌‌‌‌‍‬‍‍ ‌‌‌‌‍‬﻿‌contains‌‌‌‌‍‬﻿‌‌‌‌‌‍‬﻿﻿‌‌‌‌‌‬‌‌‌‌‌‌‍‍‍﻿‌‌‌‌‍‬﻿﻿ ‌‌‌‌‍﻿‌‬‌‌‌‌‍‬﻿‌zero-width‌‌‌‌‍‬‍‌ chars" | dirtytext --zero -v

will produce the following output:

```text
Contains zero-width characters: True
JSON:    
[{"idx": 0, "char": "\ufeff", "cval": "FEFF", "infos": null}, 
{"idx": 10, "char": "\u200c", "cval": "200C", "infos": null}, 
{"idx": 11, "char": "\u200c", "cval": "200C", "infos": null}, ...]
```

### Looks for CONFUSABLES glyphs: ###

    $> echo "hello" | dirtytext --confusables greek -v

will produce the following output:

```text
Contains confusables characters: True
JSON:
[{"idx": 2, "char": "l", "cval": "006C", "infos": [{"target": "0399", "description": "GREEK CAPITAL LETTER IOTA"}]}, 
{"idx": 3, "char": "l", "cval": "006C", "infos": [{"target": "0399", "description": "GREEK CAPITAL LETTER IOTA"}]}, 
{"idx": 4, "char": "o", "cval": "006F", "infos": [{"target": "03BF", "description": "GREEK SMALL LETTER OMICRON"}, 
{"target": "03C3", "description": "GREEK SMALL LETTER SIGMA"}]}]
```

### Looks and filter anomalies in LATIN text: ###
```text
example.txt:

It ⅽan be argueⅾ that the ⅽomputer ⅰs humanⅰty’s attempt to repⅼⅰⅽate the human brain.
This ⅰs perhaps an unattainable goal. 
However, unattainable goals often lead to outstanding accomplishment.
```
    $> dirtytext --file example.txt --check --filter --save out.txt

```text
out.txt:

It can be argued that the computer is humanity’s attempt to replicate the human brain.
This is perhaps an unattainable goal. 
However, unattainable goals often lead to outstanding accomplishment.
```

# UnicodeDB #
The unicode data that composes dirtytext database are extracted from unicode consortium, 
in particular there are two database files into dirtytext/data directory:

- categories.json: built from data extracted from [here](https://unicode.org/Public/UNIDATA/Scripts.txt)
- confusables.json: built from data extracted from [here](https://unicode.org/Public/security/latest/confusables.txt)

If dirtytext/data doesn't exist, DT downloads and build database before performing the required operations, 
after which you can force the database update by adding the --update option

# License #
Released under GPL-3.0