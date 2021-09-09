# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 10:06:21 2020
"""
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from typing import List

import sys
import os

from ExtractTextRuleEngine import extractText
#from src.dl_based_parser_predict import GetResumeExtract
#
#from dl_based_parser_predict import GetResumeExtract

app = FastAPI()

@app.get("/")
def main():
    content = """
    <!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Group 10 - Resume chatbot project </title>
  <meta name="description" content="Group 10 - Resume chatbot project">
  <meta name="author" content="Dinesh Goyal">

  <style>
    * {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-font-smoothing: antialiased;
  -moz-font-smoothing: antialiased;
  -o-font-smoothing: antialiased;
  font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

body {
  font-family: "Roboto", Helvetica, Arial, sans-serif;
  font-weight: 100;
  font-size: 12px;
  line-height: 30px;
  color: #777;
  background: #ddf2dc;
}

.container {
  max-width: 400px;
  width: 100%;
  margin: 0 auto;
  position: relative;
}

#contact input[type="text"],
#contact input[type="email"],
#contact input[type="tel"],
#contact input[type="url"],
#contact textarea,
#contact button[type="submit"] {
  font: 400 12px/16px "Roboto", Helvetica, Arial, sans-serif;
}

#contact {
  background: #F9F9F9;
  padding: 25px;
  margin: 150px 0;
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
}

#contact h3 {
  display: block;
  font-size: 30px;
  font-weight: 300;
  margin-bottom: 10px;
}

#contact h4 {
  margin: 5px 0 15px;
  display: block;
  font-size: 13px;
  font-weight: 400;
}

fieldset {
  border: medium none !important;
  margin: 0 0 10px;
  min-width: 100%;
  padding: 0;
  width: 100%;
}

#contact input[type="text"],
#contact input[type="email"],
#contact input[type="tel"],
#contact input[type="url"],
#contact textarea {
  width: 100%;
  border: 1px solid #ccc;
  background: #FFF;
  margin: 0 0 5px;
  padding: 10px;
}

#contact input[type="text"]:hover,
#contact input[type="email"]:hover,
#contact input[type="tel"]:hover,
#contact input[type="url"]:hover,
#contact textarea:hover {
  -webkit-transition: border-color 0.3s ease-in-out;
  -moz-transition: border-color 0.3s ease-in-out;
  transition: border-color 0.3s ease-in-out;
  border: 1px solid #aaa;
}

#contact textarea {
  height: 100px;
  max-width: 100%;
  resize: none;
}

#contact button[type="submit"] {
  cursor: pointer;
  width: 100%;
  border: none;
  background: #4CAF50;
  color: #FFF;
  margin: 0 0 5px;
  padding: 10px;
  font-size: 15px;
}

#contact button[type="submit"]:hover {
  background: #43A047;
  -webkit-transition: background 0.3s ease-in-out;
  -moz-transition: background 0.3s ease-in-out;
  transition: background-color 0.3s ease-in-out;
}

#contact button[type="submit"]:active {
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
}

.copyright {
  text-align: center;
}

#contact input:focus,
#contact textarea:focus {
  outline: 0;
  border: 1px solid #aaa;
}

::-webkit-input-placeholder {
  color: #888;
}

:-moz-placeholder {
  color: #888;
}

::-moz-placeholder {
  color: #888;
}

:-ms-input-placeholder {
  color: #888;
}
    </style>

</head>

<body>
  <div class="container">  
    <form id="contact" action="/uploadResumes/" enctype="multipart/form-data"  method="post">
    <h3>Resume Parser</h3>
    <h4>Upload Resume for prediction - The supported files are word(.docx), PDF</h4>
    <fieldset>
      <input name="files" type="file" multiple>
    </fieldset>
    
    <fieldset>
      <button name="submit" type="submit" id="contact-submit" data-submit="...Sending">Submit</button>
    </fieldset>
      </form>
</div>
</body>
</html>
    
    
    """

    return HTMLResponse(content=content)

def PredictResume(filename):
#    current_dir = os.path.dirname("__file__")
#    current_dir = current_dir if current_dir is not '' else '.'
#    sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))
    
    from keras_en_parser_and_analyzer.library.dl_based_parser import ResumeParser
    from keras_en_parser_and_analyzer.library.utility.io_utils import read_pdf_and_docx
    current_dir = os.getcwd()
    data_dir_path = current_dir + '/app/src/data' # directory to scan for any pdf and docx files
    
    #file_path = data_dir_path 
    p = list()
    def parse_resume(file_path, file_content):
        print('parsing file: ', file_path)

        parser = ResumeParser()
        parser.load_model('./demo/models')
        parser.parse(file_content)
        #print(parser.raw)  # print out the raw contents extracted from pdf or docx files

        if parser.unknown is False:
            p.append(parser.summary())
            

        #print('++++++++++++++++++++++++++++++++++++++++++')

    collected = read_pdf_and_docx(data_dir_path, command_logging=True, callback=lambda index, file_path, file_content: {
        parse_resume(file_path, file_content)
    })
    #print('+++++++',collected)
    #print('count: ', len(collected))
    return p

def ShowDetails(filename):
    # root = Root()
    # root.mainloop()
    
    current_dir = os.getcwd()
    # current_dir = current_dir if current_dir is not '' else '.'
    data_dir_path = current_dir + '/src/data' # directory to scan for any pdf, docx, jpeg, png files
    output_dir_path = current_dir + '/src/training_data' # directory to keep output txt files

    # extract text with the help of rule engine
    #text = extractText(filename)
    
    #predict on basis of model and show 
    predictedText = PredictResume(filename)
    #print(predictedText)
    #s = "\n".join(predictedText) 
    pText = list()
    for l in predictedText:
        pText.append(l.split("\n"))
        
    return{
            "status":1,
            "http_code":200,
            "Filename":filename,
#            "data":text,
            "Predicted":pText
            }
    #GetResumeExtract()
    # file1 = open((output_dir_path + '/ResumeOutput.txt'),"r")
    #file1 = open((output_dir_path + '/output.json'),"r")
    #Outputtext = file1.read()
    # print(Outputtext)
    #file1.close()
    #return(Outputtext)
#
#
@app.post("/uploadResumes/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        
        target_path = './app/src/data'
        file_name = target_path + "/" + file.filename
        image_bytes = file.file.read()
        image_len = len(image_bytes)
    
        with open(file_name, "wb") as f:
            f.write(image_bytes)
            # return {"filenames": [file.filename for file in files]}
        return (ShowDetails(file.filename))
#
#@app.post("/uploadfile/")
#async def create_upload_file(file: UploadFile = File(...)):
#    return {"filename": file.filename}