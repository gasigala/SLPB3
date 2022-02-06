# Angel F. Garcia Contreras, UTEP, July 2020
# Speech and Language Processing
# Assignment B1: Introduction to Prediction
import sys

def is_arabic(word):
    word= word.lower()
    if "an" in word or "zz" in word:
        return True
    if "jj" in word or "hal" in word:
        return True
    if "had" in word or "ss" in word:
        return True
    return False

def is_chinese(word):
    word = word.lower()
    if "ao" in word or "ng" in word:
        return True
    if "iu" in word or "in" in word:
        return True
    return False

def is_czech(word):
    word = word.lower()
    if len(word) < 2:
        return False
    if word[-2:] == "ak" or word[-2:] == "ek":
        return True
    if word[-2:] == "ko" or word[-2:] == "ik":
        return True
    if word[-2:] == "ko" or word[-2:] == "ik":
        return True
    return False

def is_dutch(word):
    word = word.lower()
    if "aa" in word or "ee" in word or "oo" in word:
        return True
    return False

def is_english(word):
    word = word.lower()
    if len(word) < 2:
        return False
    if word[-3:] == "ell" or word[-3:] == "all":
        return True
    if word[-2:] == "ey" or word[-2:] == "tt":
        return True
    if word[-2:] == "er" or word[-2:] == "on":
        return True
    return False
    
def is_french(word):
    word = word.lower()
    if len(word)< 2:
        return False
    if word[:2] == "la" or word[:2] == "le" or word[:2] == "du":
        return True
    return False

def is_german(word):
    word = word.lower()
    if "ave" in word or "er" in word or "eh" in word:
        return True
    return False

def is_irish(word):
    word = word.lower()
    if word[0] == "o":
        return True
    return False

def is_italian(word):
    word = word.lower()
    if len(word) < 3:
        return False
    if word[-3:] == "lli" or word[-2:] == "ri":
        return True
    if word[-2:] == "hi" or word[-2:] == "ti":
        return True
    if word[-2:] == "fi" or word[-2:] == "di":
        return True
    return False

def is_japanese(word):
    word = word.lower()
    if "ka" in word or "ya" in word or "ku" in word:
        return True
    return False

def is_korean(word):
    return len(word) <= 3

def is_russian(word):
    word = word.lower()
    return word[-1] == "v" or word[-2:] == "in"

    
def is_spanish(word):
    """Naive Spanish Surname Identification"""
    word = word.lower()
    keys = "Ã¡Ã©Ã­Ã³ÃºÃ¼Ã±"
    for letter in word:
        if letter in keys:
            return True
    return False



def check_nationality(word):
    """Naive Nationality Identification

    Returns "Unknown" for nationalities that are detected as 
    other than Spanish, Italian or Japanese
    """
    if is_arabic(word):
       return "Arabic"
    if is_chinese(word):
        return "Chinese"
    if is_czech(word):
        return "Czech"
    if is_dutch(word):
        return "Dutch"
    if is_english(word):
        return "English"
    if is_french(word):
        return "French"
    if is_german(word):
        return "German"
    if is_irish(word):
        return "Irish"
    if is_italian(word):
        return "Italian"
    if is_japanese(word):
        return "Japanese"
    if is_korean(word):
        return "Korean"
    if is_russian(word):
        return "Russian"
    if is_spanish(word):
        return "Spanish"
    return "Unknown"

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) != 3:
        print("Usage: python b1.py " +
              "<input file> <output file>" )
        sys.exit()

    with open(sys.argv[1], mode="r", encoding="utf-8") as input_file, \
          open(sys.argv[2], mode="w", encoding="utf-8") as output_file:
        for surname in input_file:
            surname = surname.strip()
            output_file.write(surname)
            output_file.write(",")
            output_file.write(check_nationality(surname))
            output_file.write("\n")