import csv
import phonemizer_test as phonemizer
import re
all_t = {}

with open(f"Transcription_accent_all.csv", "r") as f:
    file = list(csv.reader(f))[1:]

    for row in file:
        all_t.update({row[0]:[row[1], row[2], row[3]]})
        
        
c = 0
c1 = 0
c2 = 0
for k, v in all_t.items():
    
    predicted = phonemizer.Transcriptor(k).transcribe("broad")
    predicted1 = phonemizer.Transcriptor(k).transcribe("narrow")
    predicted2 = phonemizer.Transcriptor(k).transcribe("ipa")

    if predicted != v[0]:
        print(predicted, v[0])
        c+=1
    if predicted1 != v[1]:
        print(predicted1, v[1])
        c1+=1
    if predicted2 != v[2]:
        print(predicted2, v[2])
        c2+=1
    else:
        pass

print(round(c/len(all_t.keys())*100, 2))
print(round(c1/len(all_t.keys())*100, 2))
print(round(c2/len(all_t.keys())*100, 2))
"""

dict_broad = {"д͡з": "q",
                "д͡ж": "s",
                "[̃°·]": "",
                r"(.{1})´:": r"\1´\1´",
                r"(.{1})':": r"\1\1'",
                r"(.{1}):": r"\1\1",
                "'і": "і",
                "ў": "в",
                "ĭ": "j",
                r"\([еиіу]\)": "",
                "q": "д͡з",
                "s": "д͡ж"}

dict_ipa = {"д͡з": "q",
            "д͡ж": "s",
            "[̃°·]": "",
            r"(.{1})´:": r"\1´\1´",
            r"(.{1})':": r"\1'\1'",
            r"(.{1}):": r"\1\1",
            r"\([еиіу]\)": "",
            "ĭ": "j",
            "q": "ʣ",
            "s": "ʤ",
            "ч": "ʧ",
            "ц": "ʦ",
            "л´": "lʲ",
            "л": "ɫ",
            "в(?=[оу])": "w",
            "в": "v",
            "р": "r",
            "б": "b",
            "г": "ɦ",
            "ґ": "g",
            "д": "d",
            "ж": "ʒ",
            "з": "z",
            "к": "k",
            "м": "m",
            "н": "n",
            "п": "p",
            "с": "s",
            "т": "t",
            "ф": "f",
            "х": "x",
            "ш": "ʃ",
            "а": "ɑ",
            "е": "ɛ",
            "и": "ɪ",
            "і": "i",
            "о": "o",
            "у": "u",
            "ў": "w",
            "['´]": "ʲ",
            r"([ɑɛɪiou])́": r"'\1"}

all_t1 = {}
with open(f"Transcription_accent.csv", "r") as f:
    file = list(csv.reader(f))[1:]

    for row in file:
        all_t1.update({row[0]:row[1]})

with open(f"Transcription_accent_all.csv", "w", newline="") as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',')
    file_writer.writerow(["Word", "Broad transcription", "Narrow transcription", "IPA transcription", "Comment"])
    for g_word, word in all_t1.items():

        broad = word
        for pattern1, subst1 in dict_broad.items():
            broad = re.sub(pattern1, subst1, broad)
    
        ipa = word
        for pattern, subst in dict_ipa.items():
            ipa = re.sub(pattern, subst, ipa)

        file_writer.writerow([g_word, broad, word, ipa, ""])"""
