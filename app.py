from flask import Flask, render_template, request
import cv2
import os
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(_name_)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def aging_effect(image_path):
    img = cv2.imread(image_path)

    # تغميق الصورة
    dark_img = cv2.convertScaleAbs(img, alpha=0.7, beta=-30)

    # إضافة ضبابية
    blurred_img = cv2.GaussianBlur(dark_img, (7, 7), 0)

    # طبقة تجاعيد (ضوضاء بيضاء خفيفة)
    noise = np.random.normal(0, 10, img.shape).astype(np.uint8)
    aged = cv2.addWeighted(blurred_img, 0.95, noise, 0.05, 0)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'aged_' + os.path.basename(image_path))
    cv2.imwrite(output_path, aged)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    processed_image = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            processed_image = aging_effect(path)
    return render_template('index.html', processed_image=processed_image)

if _name_ == '_main_':
    app.run(debug=True)
