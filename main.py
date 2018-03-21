import os
from PIL import Image
from flask import request, make_response, send_file
from werkzeug.utils import secure_filename

from server import app
from server import is_allowed_file


# upload image
@app.route('/upload', methods=['POST'])
def upload():

    # get the uploaded image: original_image (same with the name uploaded from client)
    original_image = request.files['original_image']

    # check that the filename is allowed
    # then, save to the folder for uploaded images
    if is_allowed_file(original_image.filename):
        original_image.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                         secure_filename(original_image.filename)))

    # process the image
    processed_image_name = process_image(original_image)

    # make response for sending the processed image to client
    response = make_response(send_file(
        os.path.join(app.config['RESULT_FOLDER'], processed_image_name)))

    # set headers for response
    response.headers["Content-Disposition"] = "attachment; filename=" + processed_image_name + ";"

    return response


@app.route('/')
def test():

    return 'test'


# process image
def process_image(original_image):

    original_im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'],
                                          secure_filename(original_image.filename)))

    processed_im = original_im.rotate(45)

    processed_image_name = 'processed_' + secure_filename(original_image.filename)

    processed_im.save(os.path.join(app.config['RESULT_FOLDER'], processed_image_name))

    return processed_image_name


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
