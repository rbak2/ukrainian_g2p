import re
import argparse
from main import *


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--transcribe", type=str, metavar="", default=None, help="аналіз тексту у параметрі")
    group.add_argument("-c", "--console", action='store_true', help="аналіз тексту, введеного з консолі")
    group.add_argument("-f", "--file", type=str, metavar="", default="", help="аналіз тексту з файлу")
    parser.add_argument("-t", "--type", metavar="", default="", help="тип транскрипції (фонематична - broad, фонетична - narrow, у символах МФА - ipa, "
                                                                     "перевести в орфографічний текст - p2g)")
    parser.add_argument("-s", "--splitlist", action='store_true', help="поділ на фонеми/алофони")
    parser.add_argument("-r", "--removepunct", action='store_true', help="токенізація та обробка абревіатур")
    parser.add_argument("-w", "--addstress", action='store_true', help="додати наголоси")
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
    
    if input_str is not None and args.addstress:
        input_str = add_stress(input_str)

    if input_str is not None and args.removepunct:
        input_str = remove_punctuation(input_str)

    if input_str is not None:
        if args.type == "p2g":
            result = Transcriptor(input_str).p2g()
        elif args.type:
            result = Transcriptor(input_str).transcribe(args.type)
        else:
            print("Не вказано тип транскрипції")

    if args.splitlist and result is not None:
        print(split_to_phonemes(result))
    elif result is not None:
        print(result)
        response = input("Записати результат у файл(y/n)?: ")
        if response.lower()[:1] == "y":
            with open("output.txt", "w") as f2:
                f2.write(result)
