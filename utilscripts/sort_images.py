import shutil

pwf = open('finland.txt', 'r')

for text in pwf:
    if len(text) > 15:
        image = text.replace('.txt', '.png').strip()
        shutil.copyfile(image, './target/' + image)

