Direct Code Execution steps:

1. Install all dependencies from 'requirements.txt' file
   - pip install -r requirements.txt

#Right now the model is trained for 450 samples. If you want to train on more sample data, please execute the below two steps

2. Execute 'ExtractTextRuleEngine.py' to get intput for the ML model for any number of training samples
   - The number of training samples can be adjusted in the main function

3. Exceute modelTrain() in 'CustomParser.py' to train the model

4. Execute model


Docker Image Extraction steps:

1. cd /folderpath (folder in which 'Dockerfile' is present)

2. docker image build -t <docker_image_name> .

#to check if image is built or not
3. docker images

4. docker run -p 80:80 <docker_image_name>