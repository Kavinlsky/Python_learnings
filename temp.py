import easyocr

reader=easyocr.Reader(['en'])

path=r"C:\Users\Kavin Yugesh\Downloads\text.png"
result=reader.readtext(path)

for detection in result:
    print(detection[1])