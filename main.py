import os
from flask import request, make_response, send_file, abort
from werkzeug.utils import secure_filename

from server import app
from server import is_allowed_file
from server import en


# upload image
@app.route('/upload', methods=['POST'])
def upload():
    # get the uploaded image: original_image (same with the name uploaded from client)
    original_image = request.files['original_image']

    # get the uploaded image name
    original_image_name = secure_filename(original_image.filename)

    # check that the filename is allowed
    # then, save to the folder for uploaded images
    if is_allowed_file(original_image.filename):
        original_image.save(os.path.join(app.config['UPLOAD_FOLDER'], original_image_name))
    else:
        abort(500)

    try:
        # process the image
        processed_image_name = process_image(original_image_name)

        # make response for sending the processed image to client
        response = make_response(send_file(
            os.path.join(app.config['RESULT_FOLDER'], processed_image_name)))

        # set headers for response
        response.headers["Content-Disposition"] = "attachment; filename=" + processed_image_name + ";"

        # success
        return response
    except:
        # internal server error
        abort(500)


# interface to test if the server is ok
@app.route('/test')
def test():
    return make_response('Server OK')


# process image
def process_image(original_image_name):
    # define the processed image name
    processed_image_name = 'processed_' + original_image_name
    # change working directory
    # run deblur algorithm
    en.cd('../Vision_Code')
    en.run(os.path.join('../DeblurServer', app.config['UPLOAD_FOLDER'], original_image_name),
           os.path.join('../DeblurServer', app.config['RESULT_FOLDER'], processed_image_name),
           nargout=0)
    # return the processed image name
    return processed_image_name


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
