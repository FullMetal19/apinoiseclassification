from pydub import AudioSegment
import numpy as np
import os
import shutil


# ***************************************************************************************************************************
#  ALL ABOUT CONVERSION'S CODE
# 
# ***************************************************************************************************************************

def converter( file_name ):

    file_extension = file_name.split('.')[-1].lower()
    ALLOWED_AUDIO_EXTENSIONS = {'wav', 'm4a', 'mp3'}

    if file_extension in ALLOWED_AUDIO_EXTENSIONS :
    
        if file_extension == 'm4a': convert_from_m4a_to_wav( file_name )

        if file_extension == 'mp3': convert_from_mp3_to_wav( file_name )

        if file_extension == 'wav': os.rename( file_name, "converted_file.wav" )
    
        return True
        
    else : return False


def convert_from_m4a_to_wav( audio_file ):

    audio = AudioSegment.from_file(audio_file, format="m4a")
    audio.export( "converted_file.wav" , format="wav")
    try:
        os.remove(audio_file)
        print("File removed successfully!")
    except PermissionError:
        print("You do not have permission to remove this file.")


def convert_from_mp3_to_wav( audio_file ):

    audio = AudioSegment.from_mp3( audio_file )
    audio.export( "converted_file.wav" , format="wav")
    try:
        os.remove(audio_file)
        print("File removed successfully!")
    except PermissionError:
        print("You do not have permission to remove this file.")


# ***************************************************************************************************************************
#  ALL ABOUT FOLDER CHECKER
# 
# ***************************************************************************************************************************

def folder_checker( folder_name ):
    if not os.path.exists( folder_name ):
        os.makedirs( folder_name )


# ***************************************************************************************************************************
#  ALL ABOUT SPLITER'S CODE
# 
# ***************************************************************************************************************************

def save_chunks_file( audi_file ): 

    chunks = split_audio( audi_file , 3000) 
    output_dir = "output_chunks"
    folder_checker( output_dir )

    for i, chunk in enumerate(chunks):
        chunk.export( os.path.join(output_dir, f"chunk{i}.wav"), format="wav")


def split_audio(file_path, chunk_length_ms):
    audio = AudioSegment.from_file(file_path)
    chunk_length_ms = chunk_length_ms  
    chunks = []

    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunks.append(chunk)
    
    return chunks


# ***************************************************************************************************************************
#   ALL ABOUT DECIBLE
# 
# ***************************************************************************************************************************

def calculate_db( audio_file ):

    audio = AudioSegment.from_file( audio_file )
    samples = np.array(audio.get_array_of_samples())
    rms = np.sqrt(np.max(samples**2))
    db = 20 * np.log10(rms)

    return db
