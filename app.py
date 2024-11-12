from model_module import *
from module import *
from flask import Flask, request
from flask_cors import CORS
import glob

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

#***********************************************************************************************
# Route pour récupérer tous les livres
@app.route('/', methods=['GET'])
def get_desc():
    return 'THIS IS OUR API FOR A MASTER\'S THESIS PROJECT ABOUT ACOUSTIC NOISE'


#***********************************************************************************************
#
@app.route('/api/audio-file/upload', methods=['POST'])
def upload_audio():
    # check if file is uploaded well
    if 'file' not in request.files:
        return 'Aucun fichier trouvé', 400

    file = request.files['file']
    if file.filename == '':
        return 'Nom de fichier vide', 400

    # save it into the right folder
    file.save(file.filename) 

    if converter( file.filename ):
        save_chunks_file( "converted_file.wav" )
        files = glob.glob(os.path.join("output_chunks", '*'))
        # return files
        dicts = {}
        # db_dicts = {}
        # res = {}
        data = []
        #i = 0; 

        for file in files:
            file = file.split('\\')[-1].lower()
            file = f'output_chunks/{file}'

            label = get_mym_model( file )
            if label in dicts:  dicts[label] += 1
            else: dicts[label] = 1

            # decibel = calculate_db( file ) 
            # db_dicts[i] = [ label, decibel ]
            # i += 1
        for key, value in dicts.items() : 
            line = { 'class' : key , 'value' : value } 
            data.append(line)
        # res['decibels'] = db_dicts
        # res['occurs'] = dicts
        # os.rmdir("output_chunks")
        os.remove("converted_file.wav")
        return  data
    

   
    
            # decibel = calculate_db( file ) 
            # db_dicts[label] = decibel

            # res['decibels'] = db_dicts
            # res['occurs'] = dicts

        


#***********************************************************************************************
#
if __name__ == '__main__':
    app.run(debug=True)
