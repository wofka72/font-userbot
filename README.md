# font-userbot

The project uses userbot Telegram abilities ([video in Russian](https://www.youtube.com/watch?v=fpKODiSHL24)).

The project was inspired by [funny pictures generator](https://stardisk.xyz/funpics/) (more in [article](https://tjournal.ru/internet/88873-veselye-kartinki-generator-teksta-s-bukvami-chelovechkami-iz-populyarnogo-detskogo-zhurnala)) 

Tested on Ubuntu 18.04 and 20.04.

Assumed you have Python3 installed on your system.

## Launch:
1. Register Telegram app https://my.telegram.org/auth?to=apps.
2. Download repo.
3. Install dependencies (there are extra dependencies now) `pip install -r requirements`.
4. Run program `python font-userbot.py`. Login to your Telegram account (my program doesn't safe any information; I will check if main dependency `pyrogram` saves something, but almost sure it's not).

## Telegram usage:
 - Type `.simple <TEXT>`, where `<TEXT>` is from `абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789 .,!?:;()[]{}-_+=<>*/&^%$#@~|\'"`.
 - `.fun <TEXT>` or `.fun-tp <TEXT>`, where `<TEXT>` is from `абвгдеёжзийклмнопрстуфхцчшщъыьэюя abcdefghijklmnoprqstuvwxyz 1234567890 .,!?:;()-`.
 - `.custom <FONT> <TEXT>`, where `<FONT>` is now controlled by global `FONT_MAPPING` variable (Sprite Graffiti Shadow, Slimamif Medium and XBAND Rough Cyrillic AA are in `fonts` folder), `<TEXT>` is string consisting of any symbols supported by your font font.

You could add your own letters for a. or b. Add any permitted fonts for c.

## Examples
 - Will be added soon.
