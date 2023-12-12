import re
import random
import string
import enchant
from zxcvbn import generate_password
import math
import hashlib
from hibp import HaveIBeenPwned

capitals_length=0
smalls_length=0
special_chars_length=0
numbers_length=0

def check_length(password):
    if len(password)<12 or len(password)>25:
        print("Password length should be between 12 and 25")
        exit()
    

def capital_check(password):
    upper_count=sum(1 for i in list(password) if i.isupper())
    if upper_count<1:
        print("The password must contain atleast one capital case letter")
        exit()
    else:
        capitals_length=upper_count

def small_check(password):
    lower_count=sum(1 for i in list(password) if i.islower())
    if lower_count<1:
        print("The password must contain atleast one lowercase letter")
        exit()
    else:
        smalls_length=lower_count

def special_chararcter_check(password):
    special_pattern=re.compile('^A-Za-z0-9')
    special_chars=special_pattern.findall(password)
    special_chars_count=len(special_chars)
    if special_chars_count<1:
        print("The password must contain atleast one special character")
        exit()
    else:
        special_chars_length=special_chars_count

def numbers_check(password):
    number_pattern=re.compile('[0-9]')
    numbers=number_pattern.findall(password)
    number_count=len(numbers)
    if number_count<1:
        print("The password must contain atleast one nummerial character")
        exit()
    else:
        numbers_length=number_count

def check_username(user_name):
    if len(user_name)<5:
        print("username must contain atleast 5 charcters")
        exit()

def check_similarity(user_name,password):
    for i in range(len(password)-3):
        for j in range(len(password)-3):
            if user_name[i:i+4]==password[j:j+4]:
                print("There should be no username in password")
                exit()


def check_password(user_name,password):
    check_similarity(user_name,password)
    check_length(password)
    numbers_check(password)
    special_chararcter_check(password)
    small_check(password)
    capital_check(password)

def Entropy_calculation(password):
    capitals_Entropy=math.log2(capitals_length*26)
    smalls_Entropy=math.log2(smalls_length*26)
    special_chars_Entropy=math.log2(special_chars_length*32)
    numbers_Entropy=math.log2(numbers_length*10)
    MAX_ENTROPY=195.25
    Total_Entropy=capitals_Entropy+smalls_Entropy+special_chars_Entropy+numbers_Entropy
    Entropy_percentage=(Total_Entropy/MAX_ENTROPY)*100
    return Entropy_percentage

def Dictionary_vulnerability(password):
    dictionary_vulnerability_meter=0
    dictionary = enchant.Dict("en_US")
    for word in re.split(r"[^a-zA-Z0-9]+", password):
      if len(word) >= 3 and dictionary.check(word):
        dictionary_vulnerability_meter += 1
    patterns = [
    r"(?:[a-z]{3,})",
    r"(?:[A-Z]{3,})",
    r"(?:[0-9]{3,})",
    r"(?:[^a-zA-Z0-9]{3,})",
    r"(?:[qwertyuiop]+)",
    r"(?:asdfghjkl;]+)",
    r"(?:zxcvbnm,.<>/?)+",
    ]
    for pattern in patterns:
      if re.search(pattern, password):
        dictionary_vulnerability_meter+= 0.5
    dictionary_vulnerability_percentage = ( dictionary_vulnerability_meter* 100) / (len(password) + len(patterns))
    return dictionary_vulnerability_percentage

def check_strength(password):
    return 0.5*(100-Dictionary_vulnerability(password)+Entropy_calculation(password))

def leaked_db_check(password):
    pwned = HaveIBeenPwned()
    password_hash = hashlib.sha256(password.encode()).hexadigest()
    is_pwned = pwned.check_password(password_hash)
    return is_pwned

def strengthen_password(password):
    remaining_length=25-len(password)
    special_characters = string.punctuation
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    random_characters = ''.join(random.choice(special_characters) for _ in range(15))
    random_lowercases = ''.join(random.choice(lowercase_letters) for _ in range(15))
    random_uppercases = ''.join(random.choice(uppercase_letters) for _ in range(15))
    password_reccomendations=[]    
    strongest_password_shuffeled=''.join(random.sample(list(password+random_characters[0:remaining_length])))
    password_reccomendations.append(strongest_password_shuffeled)
    password_reccomendations.append(f"Strength %: {check_strength(strongest_password_shuffeled)}")

    strongest_password_non_shuffeled=password+random_characters[0:remaining_length]
    password_reccomendations.append(strongest_password_non_shuffeled)
    password_reccomendations.append(f"Strength %: {check_strength(strongest_password_non_shuffeled)}\n")
    
    medium_strength_password_shuffeled=''.join(random.sample(list(password+random_lowercases[0:remaining_length/4]+random_uppercases[0:remaining_length/4]+random_characters[0:remaining_length/2])))
    password_reccomendations.append(medium_strength_password_shuffeled)
    password_reccomendations.append(f"Strength %: {check_strength(medium_strength_password_shuffeled)}\n")
    
    medium_strength_password_non_shuffeled=password+random_lowercases[0:remaining_length/4]+random_uppercases[0:remaining_length/4]+random_characters[0:remaining_length/2]
    password_reccomendations.append(medium_strength_password_non_shuffeled)
    password_reccomendations.append(f"Strength %: {check_strength(medium_strength_password_non_shuffeled)}\n")

    machine_generated_passowrd=generate_password(length=25)
    password_reccomendations.append("Machine generated Password\n")
    password_reccomendations.append(machine_generated_passowrd)
    password_reccomendations.append(f"Strength %: {check_strength(machine_generated_passowrd)}\n")
    
    return password_reccomendations
    


    
def generate_usable_strong_password():
    fav_movie=input("Please name your favourite movie: ")
    fav_celebrity=input("Plese name your favourite celebrity: ")
    fav_number=input("Please enter your favourite number: (4 digits or above)")
    length=int(input("please enter length of password you want(12 or above): "))
    random_positions=random.sample(range(5,length+1),3)
    new_password=fav_movie[0:4]+fav_celebrity[0:4]+str(fav_number)[0:4]
    special_characters = string.punctuation
    for i in random_positions:
        new_password[i]=random.choice(special_characters)
    usable_password=[new_password,f"Strength: {check_strength(new_password)}"]
    return usable_password

    
def generate_report(username,password):
    report=[f"Username: {user_name}\n",f"password: {password}\n",f"Entrophy strength: {Entropy_calculation(password)}\n",f"Strength against Dictionary attack: {100-Dictionary_vulnerability(password)}\n",f"Overall_password_strength: {check_strength(password)}\n",f"Leaked: {leaked_db_check(password)}\n"]
    return report

user_name=input("Please enter your username: ")
check_username(user_name)
password=input("Please enter your password: ")
check_password(user_name,password)
print("Your password is safe to use:")
#print("Password Strength report: \n")
#for i in generate_report(user_name,password):
#    print(i)

