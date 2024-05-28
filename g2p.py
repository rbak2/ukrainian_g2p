import re
import argparse
from uk_stemmer import UkStemmer
import words_spell as ws

dict_narrow = {r"\n": " ",
                r"[^ а-яієїґ́'\+]": "",
                r"\+": "́",
                "щ": "шч",
                "ь": "´",
                "'": "2",
                "дз": "q",
                "дж": "s",
                "я": "jа",
                "ю": "jу",
                "є": "jе",
                "(?<=[дзлнрстцq])j": "´",
                "(?<=[бвгжкмпфхчшґs])j": "'",
                "ї": "jі",
                "й": "j",
                "(?<=[дзлнрстцq])і": "´і",
                "2": "",
                "т´с(?=´а)": "ц´ц",
                "(?<=с)ц(?=´ц)": "",
                "(?<=д)[шч](?=с)": "",
                "ст(?=с´к)": "",
                "(?<=[сшн])т(?=[чцдс])": "",
                "тс(?=´к|тв)": "ц",
                "(?<=с)т(?=н)": "",
                "(?<=з)д(?=ц)": "",
                r"((?<=на|ві|пі)|(?<=[сп]ере))q": "qз",
                r"((?<=\sна|\sві)|(?<=пі|^на|^ві)|(?<=\sпере)|(?<=^пере))s": "sж",
                r"((?<=\sі|^не|^по)|(?<=\sне|\sпо)|(?<=\s|^і)|(?<=^))з(?=[сцчш])": "с",
                "п(?=[бдзжгґqs])": "б",
                "к(?=[бдзжгґqs])": "ґ",
                "х(?=[бдзжгґqs])": "г",
                "т(?=´?[бдзжгґqs])": "д",
                "с(?=´?[бдзжгґqs])": "з",
                "ш(?=[бдзжгґqs])": "ж",
                "ц(?=´?[бдзжгґqs])": "q",
                "ч(?=[бдзжгґqs])": "s",
                "[дs](?=´?[цзсq])": "q",
                "[тч](?=´?[цзсq])": "ц",
                "[дq]´?(?=[чжшs])": "s",
                "[тц]´?(?=[чжшs])": "ч",
                "з´?(?=[чжшs])": "ж",
                "с´?(?=[чжшs])": "ш",
                "ж(?=[зсцq])": "з",
                "ш(?=[зсцq])": "с",
                r"((?<=н´і)|(?<=во|ле|де|кі)|(?<=д´[оі]))г(?=[кт])": "х",
                "(?<=[дтнзсцлq])(?=[дтнзсцлq]´)": "´",
                "в(?!['аоеуіив])": "ў",
                r"(?<=[^́аеоуиі ])ў(?=\s|$)": "в",
                "ф(?=[бдзжгґqs])": "в",
                "j(?![аоеуіи])": "ĭ",
                "(?<=[бвгжкмпфхчшґs])і": "'і",
                "(?<=[мн][аеиоу])|(?<=м'[аеіу])|(?<=н´[аеоуі])": "̃",
                "(?<=[j´'])(?=[аеоу])": "·",
                "(?<=[бвгґжкпфхчшдзлрстцмнqsj'´])(?=·?[оу])": "°",
                "(?<=[иіаеоу])(?=[мн])": "̃",
                "((?<=[аеоу])|(?<=[аеоу]̃))(?=[дзлрстцнq]´|[jĭ]|[бвгжкмпфхчшґs]')": "·",
                "(?<=[иіаеоу])́(?=[мн])": "̃́",
                "((?<=[аеоу]́)|(?<=[аеоу]̃́))(?=[дзлрстцнq]´|[jĭ]|[бвгжкмпфхчшґs]')": "·",
                r"([бвгґжкпфхчшдзлрстцмнqs]´?)\1(['´]?°?)": r"\1\2:",
                "q": "д͡з",
                "s": "д͡ж"}

dict_accent = {"(?<=·)е(?=̃?·)": "n",
                "е(?!́|̃́)": "h",
                "и(?!́|̃́)": "u",
                "о(?=[^аеоуиіnhu ]+[уі]̃?́)": "w",
                r"h(?=̃?(·в'і|м|·j°·у)?(\s|$))": "е",
                r"n(?=̃?(·в'і|·j°·у)(\s|$))": "е",
                r"u(?=̃?(х|ĭ|м|ш|т´)?(\s|$))": "и",
                r"((?<=\s)|(?<=^))h": "е",
                r"((?<=\s)|(?<=^))u": "и",
                "h̃": "е̃(и)",
                "ũ": "и̃(е)",
                "ñ": "е̃(і)",
                "h": "е(и)",
                "u": "и(е)",
                "n": "е(і)",
                "w̃": "о̃(у)",
                "w": "о(у)"}

dict_narrow_simple = {"[°·̃́]": "",
                      "[jĭ]": "й"}

dict_broad = {"д͡з": "q",
                "д͡ж": "s",
                "[°·̃́]": "",
                "'і": "і",
                r"(.{1})´:": r"\1´\1´",
                r"(.{1})':": r"\1\1'",
                r"(.{1}):": r"\1\1",
                "ў": "в",
                "ĭ": "j",
                r"\([еиіу]\)": "",
                "q": "д͡з",
                "s": "д͡ж"}

dict_grapheme = {
            r"\n": " ",
            r"[^ а-яієїґ'´:ўjĭ͡()]": "",
            "д͡з": "q",
            "д͡ж": "s",
            "[°·̃́]": "",
            r"(.{1})´:": r"\1\1´",
            r"(.{1})':": r"\1\1'",
            r"(.{1}):": r"\1\1",
            "(?<=[дтнзсцq])´(?=[дтнзсцqл]´)": "",
            "(?<=л)´(?=л´)": "",
            "ў": "в",
            "(?<=[бвгґжкпфхчшдзлрстцмнqs])(?=j[аеуі])": "1",
            "[jĭ]": "й",
            "['´]і": "і",
            "['´й]а": "я",
            "['´й]у": "ю",
            "['´й]е": "є",
            "йі": "ї",
            "1": "'",
            "´": "ь",
            "шч": "щ",
            "s": "дж",
            "q": "дз",
            r"\([еиіу]\)": "",
            r"((?<=\bна)|(?<=\bякна)|(?<=\bщона)|(?<=\bщоякна))я": "йа",
            r"((?<=\bна)|(?<=\bякна)|(?<=\bщона)|(?<=\bщоякна))ю": "йу",
            r"((?<=\bна)|(?<=\bякна)|(?<=\bщона)|(?<=\bщоякна))є": "йе",
            r"((?<=\bна)|(?<=\bякна)|(?<=\bщона)|(?<=\bщоякна))ї": "йі",
            r"((?<=ле)|(?<=де)|(?<=ні)|(?<=кі)|(?<=во)|(?<=ді)|(?<=дьо))х(?=[кт])": "г",
            r"цця\b": "ться",
            r"(?<=[еиєїюь])сся\b": "шся",
            r"цся\b": "чся",
            r"зся\b": "жся",
            r"сч": "щ",
            r"\bміз(?=[зсц])": "між",
            r"(?<!мі)ж(?=[шж][аоуие])": "з",
            r"шш(?![яюі])": "сш",
            r"чш": "тш",
            r"чч(?!ин|[яюі])": "тч",
            r"цці\b": "чці",
            r"(?<=[уюї])с(?=ц)": "ш",
            r"(?<=[юїр])з(?=[цзс])": "ж",
            r"цц(?!і\b)": "тц",
            r"цс": "тс",
            "д[зж](?=[сцзшжчщ])": "д",
            "д[зж](?=д[зж])": "д",
            "дзь(?=[сцзшжчщ])": "дь",
            r"дся\b": "дься",
            r"нся\b": "нься",
            "ґ(?=[бдзжг])": "к",
            r"((?<=ро)|(?<=бе)|(?<=чере))ж(?=дж|[чшщ])": r"з",
            r"((?<=\bі)|(?<=\bне)|(?<=\bпо)|(?<=\bнапів)|(?<=\b))ж(?=дж|[чшщ])": r"з",
            r"((?<=\bі)|(?<=\bне)|(?<=\bпо)|(?<=\bнапів)|(?<=\b))[шс](?=[цсчшщ])": r"з",
            "(?<=дво|рьо)г(?=[бдзжгкт])": "х",
            "(?<=я)д(?=де)": "т",
            "(?<=ші)[зс](?=[дснц])": "ст"
            }

dict_ipa = {"в°": "w",
            "[̃°·]": "",
            ":": "ː",
            "д͡з": "d͡z",
            "д͡ж": "d͡ʒ",
            "ч": "t͡ʃ",
            "ц": "t͡s",
            "л": "l",
            "р": "r",
            "б": "b",
            "в": "ʋ",
            "г": "ɦ",
            "д": "d",
            "ґ": "ɡ",
            "ж": "ʒ",
            "к": "k",
            "п": "p",
            "ф": "f",
            "х": "x",
            "ш": "ʃ",
            "з": "z",
            "с": "s",
            "т": "t",
            "м": "m",
            "н": "n",
            "j": "j",
            "ĭ": "i̯",
            "ў": "u̯",
            "а": "ɑ",
            "е": "ɛ",
            "и": "ɪ",
            "і": "i",
            "о": "ɔ",
            "у": "u",
            "['´]": "ʲ"}
dict_ipa2 = {r"ɛ\(ɪ\)": "e",
             r"ɪ\(ɛ\)": "e",
             r"ɛ\(i\)": "e",
             r"ɔ\(u\)": "o",
             "ɑ(?!́)": "ɐ",
             "u(?!́)": "ʊ",
             "́": ""}


class Transcriptor:
    def __init__(self, text):
        self.text = text

    def transcribe(self, tr_type):
        patterns = []
        substitution = []
        patterns1 = []
        substitution1 = []
        allophone = self.text.lower()
        for pattern1, subst1 in dict_narrow.items():
            if re.findall(pattern1, allophone):
                patterns.append(pattern1)
                substitution.append(re.findall(pattern1, allophone))
            allophone = re.sub(pattern1, subst1, allophone)
        if "́" in allophone:
            for pattern2, subst2 in dict_accent.items():
                allophone = re.sub(pattern2, subst2, allophone)
        allophone_s = allophone
        for pattern3, subst3 in dict_narrow_simple.items():
            allophone_s = re.sub(pattern3, subst3, allophone_s)
        phoneme = allophone
        for pattern, subst in dict_broad.items():
            if re.findall(pattern, phoneme):
                patterns1.append(pattern)
                substitution1.append(re.findall(pattern, phoneme))
            phoneme = re.sub(pattern, subst, phoneme)
        if tr_type == "broad":
            return phoneme
        elif tr_type == "narrow":
            return allophone
        elif tr_type == "narrow_simple":
            return allophone_s
        else:
            return [allophone, patterns, substitution, phoneme, patterns1, substitution1]

    def to_ipa(self):
        ipa = self.transcribe("narrow")
        for pattern, subst in dict_ipa.items():
            ipa = re.sub(pattern, subst, ipa)
        if "́" in ipa:
            for pattern2, subst2 in dict_ipa2.items():
                ipa = re.sub(pattern2, subst2, ipa)
        return ipa

    def p2g(self):
        grapheme = self.text.lower().split(" ")
        list_res = []
        stemmer = UkStemmer()
        for i in grapheme:
            p2g = i
            for pattern_p2g, subst_p2g in dict_grapheme.items():
                p2g = re.sub(pattern_p2g, subst_p2g, p2g)
            if p2g in ws.arr.keys():
                p2g = p2g.replace(p2g, ws.arr[p2g])
            s = stemmer.stem_word(p2g)
            if s in ws.arr1.keys():
                p2g = p2g.replace(s, ws.arr1[s])
            list_res.append(p2g)
        return " ".join(list_res)


def remove_punctuation(input_punct):
    clean_txt = re.split(r"[,.?!;:–]", input_punct)
    clean_txt = [t for t in clean_txt if t != ""]
    return clean_txt


def split(input_text):
    input_text = re.split(" ", input_text)
    split_list = [list(filter(None, re.split(r"(д͡[жз]['´]?°?:?|·?[аеоуиі]̃?́?(?:\([еиуі]\))?·?|[а-яіґĭўj]['´]?°?:?)", t)))
                  for t in input_text]
    return split_list


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--transcribe", type=str, metavar="", default=None, help="аналіз тексту у параметрі")
    group.add_argument("-c", "--console", action='store_true', help="аналіз тексту, введеного з консолі")
    group.add_argument("-f", "--file", type=str, metavar="", default="", help="аналіз тексту з файлу")
    parser.add_argument("-p", "--type", metavar="", default="", help="тип транскрипції(фонематична - broad, фонетична - narrow, у символах МФА - ipa, "
                                                                     "перевести в орфографічний текст - p2g)")
    parser.add_argument("-s", "--split", action='store_true', help="поділ на фонеми/алофони")
    parser.add_argument("-r", "--removepunct", action='store_true', help="поділ на синтагми")
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
        elif args.type == "p2g":
            result = Transcriptor(input_str).p2g()
        elif args.type and args.removepunct:
            result = []
            input_str = remove_punctuation(input_str)
            for word in input_str:
                result.append(Transcriptor(word).transcribe(args.type))
            result = "\n//".join(result)
        elif args.type:
            result = Transcriptor(input_str).transcribe(args.type)
        else:
            print("Не вказано тип транскрипції")

    if args.split and result is not None and not args.removepunct:
        print(split(result))
    elif result is not None:
        print(result)
        response = input("Записати результат у файл(y/n)?: ")
        if response.lower()[:1] == "y":
            with open("output.txt", "w") as f2:
                f2.write(result)
