from flask import Flask, render_template, redirect, url_for
import os

app = Flask(__name__)

image_folder = './static/images'
images = os.listdir(image_folder)
images.sort() #sort the elements 
result = []
i = 0
while i < len(images):
    result.append([images[i],images[i+1]])
    i += 2
num_images = len(result)
current_index = 0

@app.route('/')
def index():
    global current_index
    if num_images >= 1:
        image1 = result[current_index][0]
        image2 = result[current_index][1]
    else:
        image1 = image2 = None
    return render_template('index.html', image1=f'./static/images/{image1}', image2=f'./static/images/{image2}')


@app.route('/next', methods=['POST'])
def next_image():
    global current_index
    current_index = (current_index + 1) % num_images
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
