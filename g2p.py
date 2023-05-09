import re
import argparse

dict_phoneme = {r"\n": " ", r"[^ а-яієїґ́'\+]": "", r"\+": "́",
         "щ": "шч", "ь": "´", "'": "2", "дз": "q", "дж": "s", "я": "jа", "ю": "jу", "є": "jе",
         "(?<=[дзлнрстцq])j": "´", "(?<=[бвгжкмпфхчшґs])j": "'", "ї": "jі", "й": "j", "(?<=[дзлнрстцq])і": "´і",
         "2": "", "т´с(?=´а)": "ц´ц", "(?<=н)т(?=с´к|ств)": "", "стс´к": "с´к", "(?<=с)т(?=[чцндс])": "",
         "(?<=з)д(?=ц)": "", "тс": "ц", r"((?<=\bсере)|(?<=\bна)|(?<=\bпі)|(?<=\bпре)|(?<=\bпере)|(?<=\bві))q": "qз",
         r"((?<=\bсере)|(?<=\bна)|(?<=\bпі)|(?<=\bпре)|(?<=\bпере)|(?<=\bві))s": "sж", r"\bз(?=[сцчш])": "с",
         "п(?=[бдзжгґqs])": "б", "т(?=´?[бдзжгґqs])": "д", "с(?=´?[бдзжгґqs])": "з", "ш(?=[бдзжгґqs])": "ж",
         "к(?=[бдзжгґqs])": "ґ", "х(?=[бдзжгґqs])": "г", "ц(?=´?[бдзжгґqs])": "q", "ч(?=[бдзжгґqs])": "s",
         "[дs](?=´?[цзсq])": "q", "[тч](?=´?[цзсq])": "ц", "[дq](?=´?[чжшs])": "s", "[тц](?=´?[чжшs])": "ч",
         "з(?=´?[чжшs])": "ж", "с(?=´?[чжшs])": "ш", "(?<=[жчшs])´": "", "ж(?=[зсцq])": "з", "ш(?=[зсцq])": "с",
         r"(?<![ин])г(?!ти\b)(?=[кт])": "х", "(?<=[дтнзсцлq])(?=[дтнзсцлq]´)": "´", "q": "д͡з", "s": "д͡ж"}
dict_allophone = {"д͡з": "q", "д͡ж": "s", "в(?!['аоеуіив])": "ў", r"(?<=[^аеоуиі ])ў\b": "в", "j(?![аоеуіи])": "ĭ",
         "(?<=[бвгжкмпфхчшґs])і": "'і", "(?<=[мн][аеиоу])|(?<=м'[аеіу])|(?<=н´[аеоуі])": "̃",
         "(?<=[j´])(?=[аеоу])": "·", "(?<=[бвгґжкпфхчшдзлрстцмнqsj'´])(?=·?[оу])": "°",
         "(?<=[иіаеоу])(?=[мн])": "̃", "((?<=[аеоу])|(?<=[аеоу]̃))(?=[дзлрстцнq]´|[jĭ])": "·",
         "(?<=[иіаеоу])́(?=[мн])": "̃́", "((?<=[аеоу]́)|(?<=[аеоу]̃́))(?=[дзлрстцнq]´|[jĭ])": "·",
         r"([дтнлзсцqр]´)\1°": r"\1°:", r"([жчшs])\1'°": r"\1'°:", r"([дтнлзсцqр]´)\1": r"\1:", r"([жчшs])\1'": r"\1':",
         r"([бвгґжкпфхчшдзлрстцмнqs])\1°": r"\1°:", r"([бвгґжкпфхчшдзлрстцмнqs])\1": r"\1:", "q": "д͡з", "s": "д͡ж"}
dict_accent = {"(?<=·)е(?=̃?·)": "n", "е(?!́|̃́)": "h", "и(?!́|̃́)": "u", "h̃": "е̃(и)", "ũ": "и̃(е)", "ñ": "е̃(і)", "h": "е(и)",
         "u": "и(е)", "n": "е(і)", "о(?=[^аеоуиіnhu ]+у̃?́)": "w", "о(?=[^аеоуиіnhu ]+і̃?́)": "w", "w̃": "о̃(у)", "w": "о(у)"}
dict_ipa = {"[̃°·]": "", "н´": "ɲ", "л´": "ʎ", ":": "ː", "д͡з´": "dzʲ", "д͡ж'": "dʒʲ", "д͡з": "d̪z̪", "д͡ж": "dʒ",
            "д´": "dʲ", "с´": "sʲ", "ц´": "tsʲ", "т´": "tʲ", "з´": "zʲ", "р": "ɾ",
            "б": "b", "в": "ʋ", "г": "ɦ", "д": "d̪", "ґ": "ɡ", "ж": "ʒ", "к": "k", "п": "p", "ф": "f", "х": "x", 
            "ч": "tʃ", "ш": "ʃ", "з": "z̪", "л": "l", "с": "s̪", "т": "t̪", "ц": "t̪s̪", "м": "m", "н": "n̪", "j": "j",
            "ĭ": "j", "ў": "u", "а": "ɑ", "е": "ɛ", "и": "ɪ", "і": "i", "о": "ɔ", "у": "u", "['´]": "ʲ"}
dict_ipa2 = {r"ɛ\(ɪ\)": "e", r"ɪ\(ɛ\)": "e", r"ɛ\(i\)": "e", r"ɔ\(u\)": "o", "ɑ(?!́)": "ɐ", "u(?!́)": "ʊ", "́": ""}


class Transcriptor:
    def __init__(self, text):
        self.text = text

    def transcribe(self, tr_type):
        phoneme = self.text.lower()
        for pattern, subst in dict_phoneme.items():
            phoneme = re.sub(pattern, subst, phoneme)
        allophone = phoneme
        for pattern1, subst1 in dict_allophone.items():
            allophone = re.sub(pattern1, subst1, allophone)
        if "́" in allophone:
            for pattern2, subst2 in dict_accent.items():
                allophone = re.sub(pattern2, subst2, allophone)
        else:
            pass
        if tr_type == "phonemic":
            return phoneme
        elif tr_type == "phonetic":
            return allophone
        else:
            return "\n".join([phoneme, allophone])

    def to_ipa(self):
        ipa = self.transcribe("phonetic")
        for pattern, subst in dict_ipa.items():
            ipa = re.sub(pattern, subst, ipa)
        if "́" in ipa:
            for pattern2, subst2 in dict_ipa2.items():
                ipa = re.sub(pattern2, subst2, ipa)
        else:
            pass
        return ipa


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--transcribe", type=str, metavar="", default=None, help="аналіз тексту у параметрі")
    group.add_argument("-c", "--console", action='store_true', help="аналіз тексту, введеного з консолі")
    group.add_argument("-f", "--file", type=str, metavar="", default="", help="аналіз тексту з файлу")
    parser.add_argument("-p", "--type", metavar="", default="", help="тип транскрипції(фонематична - phonemic, фонетична - phonetic, у символах МФА - ipa)")
    args = parser.parse_args()

    input_str = None
    result = None
    if args.console:
        input_str = input("Введіть текст: ")
    elif args.file:
        try:
            with open(args.file, "r") as f:
                input_str = f.read()
        except FileNotFoundError:
            print("Файл не знайдено")
    elif args.transcribe is not None:
        input_str = args.transcribe
    else:
        print("Не вказано текст, який потрібно аналізувати")

    if input_str is not None:
        if args.type == "ipa":
            result = Transcriptor(input_str).to_ipa()
        elif args.type:
            result = Transcriptor(input_str).transcribe(args.type)
        else:
            print("Не вказано тип транскрипції")
    else:
        pass

    if result is not None:
        print(result)
        response = input("Записати результат у файл(y/n)?: ")
        if response.lower()[:1] == "y":
            with open("output.txt", "w") as f2:
                f2.write(result)
        else:
            pass
