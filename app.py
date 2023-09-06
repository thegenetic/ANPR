import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
from flask import Flask, render_template, request
import test

app = Flask(__name__)
reader = easyocr.Reader(['en'])

@app.route('/', methods=['GET'])
def hello_word():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    imagefile= request.files['file']
    image_path = "./images/" + imagefile.filename
    imagefile.save(image_path)

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200)

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour,10, True)
        if len(approx) == 4:
            location = approx
            break

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    cropped_image =cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

    result = reader.readtext(cropped_image)

    text = result[0][-2]

    query = test.main(text)
    # cv2.imwrite('1.png', cropped_image)
    return render_template('index.html', text = query)


if __name__ == '__main__':
    app.run(debug=True)
