import os, re, random, requests

with open("UA.txt", "r") as f:
    lines = f.readlines()
    UA = lines[0].strip()

base_url = "https://gateway.live-a-hero.jp"

HEADER_GET = {
    'X-Unity-Version': '2022.3.62f2',
    'User-Agent': UA,
    'Accept-Encoding': 'deflate, gzip',
}

#获取最新版本的HousamoAPI更新User-Agent
res0 = requests.get(base_url + '/api/status/version', headers=HEADER_GET)
UA = 'LiveAHeroAPI/' + res0.json().get("client") + ' Android OS 12 / API-32 (V417IR/1747) Redmi 2201116SC'
with open("UA.txt", "w") as f:
    f.write(f"{UA}\n")
    f.write(f"{random.random()}\n")    #防止官方长期不更新API仓库不活跃

#登录
def login_by_authkey(userKey):
    with requests.Session() as s:
        s.headers.update(HEADER_GET)
        s.headers.update({
            "user-identifier": userKey,
        })
        
        login = s.get(f"{base_url}/api/user/login")
        login.raise_for_status()
        print("login:", login.json())
    
        sync_items = s.get(f"{base_url}/api/user/sync/items")
        sync_items.raise_for_status()
        print("sync items:", sync_items.json())
    
        login_popup = s.get(f"{base_url}/api/user/login/popup/get")
        login_popup.raise_for_status()
        print("login popup:", login_popup.json())

if __name__ == '__main__':
    userKeys = eval(os.environ['userKeys'])
    #os.system("echo %s | openssl enc -e -aes-256-cbc -a -pbkdf2 -iter 5 -k 'abc'" %(userKeys['AUTH_KEY_PIPI2']))    #userKey丢了可以加密输出来找回
    pattern = re.compile(r'USERKEY_.*')                #匹配secrets中的userKey
    for item in userKeys.keys():
        if pattern.match(item):
            userKey = userKeys[item]
            login_by_authkey(userKey) 
