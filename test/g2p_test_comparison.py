import csv
from ipa_uk import pronunciation as ipa
import re
import epitran


dict_ipa_uk = {"в°": "w",
            "[̃°·]": "",
            ":": "ː",
            "д͡з": "d͡z",
            "д͡ж": "d͡ʒ",
            "ч": "t͡ʃ",
            "ц": "t͡s",
            "л´": "lʲ",
            "л": "ɫ",
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
            "ĭ": "i̯",
            "ў": "u̯",
            "а": "a",
            "е": "ɛ",
            "и": "ɪ",
            "і": "i",
            "о": "ɔ",
            "у": "u",
            "['´]": "ʲ",
            r"ɛ\(ɪ\)": "e",
             r"ɪ\(ɛ\)": "e",
             r"ɛ\(i\)": "e",
             r"ɔ\(u\)": "o",
             "a(?!́)": "ɐ",
             "u(?!́)": "ʊ",
             "ʊ̯": "u̯",
             "́": ""}

dict_ipa_epi = {"д͡з": "q",
            "д͡ж": "s",
            "в°": "v",
            "[̃°·]": "",
            r"(.{1})´:": r"\1´\1´",
            r"(.{1})':": r"\1\1'",
            r"(.{1}):": r"\1\1",
            "q": "dz",
            "s": "dʐ",
            "ч": "ʈ͡ʂ",
            "ц": "t͡s",
            "л": "l",
            "р": "r",
            "б": "b",
            "в": "v",
            "г": "ɦ",
            "д": "d",
            "ґ": "ɡ",
            "ж": "ʐ",
            "к": "k",
            "п": "p",
            "ф": "f",
            "х": "x",
            "ш": "ʂ",
            "з": "z",
            "с": "s",
            "т": "t",
            "м": "m",
            "н": "n",
            "ĭ": "j",
            "ў": "v",
            "а": "ɑ",
            "е": "ɛ",
            "и": "ɪ",
            "і": "i",
            "о": "ɔ",
            "у": "u",
            "['´]": "ʲ",
            r"ɛ\(ɪ\)": "ɛ",
             r"ɪ\(ɛ\)": "ɪ",
             r"ɛ\(i\)": "ɛ",
             r"ɔ\(u\)": "ɔ",
             "ʊ̯": "u̯",
             "́": ""}

dict_ipa_cyber = {"[jĭ]": "й",
            "д͡з": "z",
            "д͡ж": "j",
            "[̃°·]": "",
            "ў": "в",
            r"(.{1})´:": r"\1´\1´",
            r"(.{1})':": r"\1'\1'",
            r"(.{1}):": r"\1\1",
            "['´]": "'",
            r"\([еиіу]\)": "",
             "́": ""}


"""def split_to_phonemes(input_text):
    input_text = re.split(" ", input_text)
    split_list = [list(filter(None, re.split(r"(d͡[zʒ]ʲ?ː?|t͡[sʃ]ʲ?ː?|i̯|u̯|[a-zʍʣʋʤɡʧʊɔɐʦɫɦʒʃɑɛɪ]ʲ?ː?)", t)))
                    for t in input_text]
    return split_list"""

def to_ipa(ipa, dict_ipa):
    for pattern, subst in dict_ipa.items():
        ipa = re.sub(pattern, subst, ipa)
    return ipa


epi = epitran.Epitran('ukr-Cyrl').transliterate

def open_csv_file():
    correct = {}
    with open(f"Transcription_accent2.csv", "r") as f:
        file = list(csv.reader(f))[1:]
        for row in list(file):
            correct.update({row[0]:[row[1], row[2], row[3], row[4]]})
    return correct

def evalute_cyber():
    correct1 = open_csv_file()
    c1 = 0
    for k, v in correct1.items():
        if v[1] != "":
            actual = to_ipa(v[1], dict_ipa_cyber)
        else:
            actual = to_ipa(v[0], dict_ipa_cyber)
        predicted1 = v[2]
        predicted2 = v[3]
        if predicted1 != actual and predicted2 != actual:
            #print(predicted1, predicted2, actual)
            c1+=1
    return round(c1/len(correct1.keys())*100, 2)


def evalute_system(phonemize, dict_symbols):
    correct = open_csv_file()
    c1 = 0
    for k, v in correct.items():
        if phonemize == epi:
            k = re.sub("́", "", k)
        predicted = re.sub("ˈ", "", phonemize(k))
        actual1 = to_ipa(v[0], dict_symbols)
        actual2 = to_ipa(v[1], dict_symbols)
        if predicted != actual1 and predicted != actual2:
            #print(predicted, actual1)
            c1+=1
    return round(c1/len(correct.keys())*100, 2)


print(evalute_system(ipa, dict_ipa_uk))
print(evalute_system(epi, dict_ipa_epi))
print(evalute_cyber())

