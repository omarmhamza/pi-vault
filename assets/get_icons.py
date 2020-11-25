import requests
import lxml.html as lh
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["vault"]
mycol = mydb["icons"]

url = 'https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/'
# Create a handle, page, to handle the contents of the website
page = requests.get(url)
# Store the contents of the website under doc
doc = lh.fromstring(page.content)
# Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')
w = 0
# Check the length of the first 12 rows
names = []
for T in tr_elements[2:]:
    x = []
    for key, r in enumerate(T.iterchildren()):
        if key == 1 or key == 4 or key == 5 or key == 3:
                if key !=1 and key !=3 and key!=4:
                    content = r.text_content().replace("\n", '').split()
                else:
                    content = r.text_content().replace("\n", '').strip()
                if key==3 and "fas" in content:
                    x = []
                    continue
                else:
                    if key == 1:
                        names.append(content)
                    x.append(content)
    try:
        insert = mycol.insert_one(
            {
                "name":str(x[0]),
                "unicode":str(x[2]),
                "tags":x[3]
            })
    except:
        pass
    if x:
        print(w,x)
        w+=1
