import json, csv

folders = ["低脂","生酮","低醣","沙拉","高蛋白","健身","高纖"]

ID_list = {}
for i in folders:
    with open(f'{i}/{i}.txt', 'r', encoding='utf-8') as f:
        for line in f:              # 使用迴圈方式一條一條抓
            data = json.loads(line)
            ID_list[data['food_ID']] = i


fd = open('./ok-nutris-ver2.csv', 'r', encoding='utf-8-sig')
csvRdr = csv.DictReader(fd, delimiter=',', quotechar='"')

# need argument "newline=''" to remove extra newline
with open('./ok-nutris-ver3.csv', 'w', newline='', encoding='utf-8-sig') as wfd:
    header = csvRdr.fieldnames.copy()
    header.insert(4, 'group')

    xf3 = csv.DictWriter(wfd, header, delimiter=',', quotechar='"')
    xf3.writeheader()

    for row in csvRdr:
        row['group'] = ID_list[row['food_ID']]
        xf3.writerow(row)

fd.close()