# Angel F. Garcia Contreras, UTEP, July 2020
# Speech and Language Processing
# Assignment B1: Introduction to Prediction

import sys

def is_spanish(word):
    """Naive Spanish Surname Identification"""
    word = word.lower()
    keys = "Ã¡Ã©Ã­Ã³ÃºÃ¼Ã±"
    for letter in word:
        if letter in keys:
            return True
    return False

def is_italian(word):
    """Naive Italian Surname Identification"""
    return word.count("i") >= 3    

def is_japanese(word):
    """Naive Japanese Surname Identification"""
    if "naka" in word:
        return True
    elif "tsu" in word:
        return True
    elif "kawa" in word:
        return True
    else:
        return False

def check_nationality(word):
    """Naive Nationality Identification

    Returns "Unknown" for nationalities that are detected as 
    other than Spanish, Italian or Japanese
    """
    if is_spanish(word):
        return "Spanish"
    if is_italian(word):
        return "Italian"
    if is_japanese(word):
        return "Japanese"
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
        
    with open(sys.argv[1], mode="r", encoding="utf-8") as input_file, \
          open(sys.argv[2], mode="w", encoding="utf-8") as output_file: