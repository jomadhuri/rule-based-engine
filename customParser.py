import numpy as np
import os
import nltk
nltk.download('punkt')

#If you are using colab, please run the below commented steps
'''
from google.colab import drive
drive.mount('/content/drive')

import sys
sys.path.insert(0,'/content/drive/My Drive/Colab Notebooks/Final_code')

import os
os.environ['PYTHONPATH'] += ":/content/drive/My Drive/Colab Notebooks/Final_code/demo/data"
'''
#to train the model on the training samples
def modelTrain():
    random_state = 42
    np.random.seed(random_state)

    #current_dir = os.path.dirname("_file_")
    #current_dir = current_dir if current_dir is not '' else '.'
    output_dir_path =  '/content/drive/My Drive/Colab Notebooks/Final_code/demo/models'
    training_data_dir_path = '/content/drive/My Drive/Colab Notebooks/Final_code/demo/data/training_data'
    
    #add keras_en_parser_and_analyzer module to the system path
    #sys.path.append('/content/drive/My Drive/capstone/model/')
    #print(sys.path.append(os.path.join(os.path.dirname("_file_"), '..')))
    from keras_en_parser_and_analyzer.library.dl_based_parser import ResumeParser

    classifier = ResumeParser()
    batch_size = 32
    epochs = 100
    #print(training_data_dir_path,">>>>>>>>>>")
    history = classifier.fit(training_data_dir_path=training_data_dir_path,
                             model_dir_path=output_dir_path,
                             batch_size=batch_size, epochs=epochs,
                             test_size=0.3,
                             random_state=random_state)

#to predict 
def modelPredict():
    #current_dir = os.path.dirname("_file_")
    #current_dir = current_dir if current_dir is not '' else '.'
    #sys.path.append(os.path.join(os.path.dirname("_file_"), '..'))
    
    from keras_en_parser_and_analyzer.library.dl_based_parser import ResumeParser
    from keras_en_parser_and_analyzer.library.utility.io_utils import read_pdf_and_docx
    
    data_dir_path =  '/content/drive/My Drive/Colab Notebooks/Final_code/demo/data/resume_samples' # directory to scan for any pdf and docx files

    def parse_resume(file_path, file_content):
        print('parsing file: ', file_path)

        parser = ResumeParser()
        parser.load_model('/content/drive/My Drive/Colab Notebooks/Final_code/demo/models')
        parser.parse(file_content)
        #print(parser.raw)  # print out the raw contents extracted from pdf or docx files

        if parser.unknown is False:
            print(parser.summary())

        print('++++++++++++++++++++++++++++++++++++++++++')

    collected = read_pdf_and_docx(data_dir_path, command_logging=True, callback=lambda index, file_path, file_content: {
        parse_resume(file_path, file_content)
    })

    print('count: ', len(collected))

							 
							 
#modelTrain()
#modelPredict()



