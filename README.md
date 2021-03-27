# font-userbot

The project uses userbot Telegram abilities ([video in Russian](https://www.youtube.com/watch?v=fpKODiSHL24)).

The project was inspired by [funny pictures generator](https://stardisk.xyz/funpics/) (more in [article](https://tjournal.ru/internet/88873-veselye-kartinki-generator-teksta-s-bukvami-chelovechkami-iz-populyarnogo-detskogo-zhurnala)) 

Tested on Ubuntu 20.04.

Assumed you have Python3 installed on your system.

## Launch:
1. Register Telegram app https://my.telegram.org/auth?to=apps.
2. Download repo.
3. Install dependencies (there are extra dependencies now) `pip install -r requirements`.
4. Run program `python font.py`. Login to your Telegram account (my program doesn't safe any information; I will check if main dependency `pyrogram` saves something, but almost sure it's not).

## Telegram usage:
 - Type `.font-simple <TEXT>`, where `<TEXT>` consists of cyrillic letters.
 - `.font-fun <TEXT>` or `.font-fun-tp <TEXT>` (`<TEXT>` is from `абвгдеёжзийклмнопрстуфхцчшщъыьэюя abcdefghijklmnoprqstuvwxyz 1234567890 .,!?:;()-`).
 - `.font-custom <FONT> <TEXT>`, where `<FONT>` is from `[sgraffiti, rough, slimamif]` `<TEXT>` is from any symbols (Python module `wand` with underlying `ImageMagick` will render it, but your font should support lettersin order to render correctly).

You could add your own letters for a. or b. Add any permitted fonts for c.

## Examples
 - Will be added soon.
