from flask import Flask
import matlab.engine as engine

# initialize flask application
app = Flask(__name__)

# server configuration
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['RESULT_FOLDER'] = 'result'

# allowed extensions for files uploaded from client
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# check that the name of file is allowed
def is_allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


# load matlab environment
print('loading MTALAB environment')
en = engine.start_matlab()
print('loading end')
