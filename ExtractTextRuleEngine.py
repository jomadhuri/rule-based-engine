#!/usr/bin/env python
# coding: utf-8

#imports for pymupdf
#!pip install pymupdf

import sys,fitz
import re
import random
from collections import OrderedDict 
from copy import deepcopy

#imports for excel writer/reader
import os
import os.path
import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook

#!pip3 install camelot-py[cv]
#!conda install -c conda-forge camelot-py
import camelot
import pandas as pd

wb = load_workbook(filename='Template.xlsx')
sheet = wb.active

#patterns and sub patterns for rule based parsing
patterns = {'Education': ['EDUCATIONAL QUALIFICATION', 'Educational Qualifcations', 'Educational Background', 'ACADEMIC QUALIFICATION', 'E ducational Qualification :',
                         'EDUCATION QUALIFICATION', 'EDUCATIONAL ATTAINMENT', 'TECHINICAL EDUCATION','EDUCATIONAL CREDENTIALS','ACADEMIC PROFILE', 'Education Qualification: ',
                         'ACADEMIC CREDENTIALS:','ACADEMIC QUALIFICATION:', 'EDUCATIONAL QUALIFICATIONS', 'ACADEMIC SEMINAR UNDERTAKEN', ' ACADEMIC PROJECT UNDERTAKEN ', 'ACADEMIC DETAILS',
                         'ACADEMIC INTERESTS','TECHNICAL/ EDUCATIONAL QUALIFICATION','Educational Qualification:','Academics', 'Academic Trainings:', 'Technical Qualification: ',
                         'Educational Qualifications:','EDUCATIONAL QUALIFICATIONS:','Academic Qualification','Education qualification:','Educational Qualification', 'Summary:',          
                         'SCHOLASTICS','Education Detail:','Academic','ACADEMICS','EDUCATION:', 'EDUCATION QUALIFICATION :-', 'ACADEMIC QUALIFICATION:-', 'DEGREE DETAIL:',
                         'ACADEMIC DETAILS: ', 'EDUCATION ', 'Specialization:', 'QUALIFICATION:- ', 'Education', 'Summary of Qualifications: ', 'QUALIFICATIONS '],
            
            'Knowledge': ['TECHNICAL QUALIFICATION', 'Software Skill:', 'Technical Skill:', 'Functional Skill Areas and Key Strengths', 'Computer literacy:',
                      'TECHNICAL PROFICIENCY', 'TECHNICAL SKILLS', 'Computer literacy:', 'Professional Skill:', 'COMPUTER SKILLS', 'Computer Skills : -',
                      'JOB ROLE AND KEY SKILLS', 'Personal Skills','SOFTWARE SKILLS:','STRENGTHS:','EXPERTISE:','CORE STRENGTH:','KNOWLEDGE PURVIEW:', 'Skills & Abilities',
                      'SKILLS:','COMPUTER PROFICIENCY','LANGUAGES KNOWN','KEY SKILLS','Academic Projects & Technical skills','COMPUTER SKILLS:', 'CAREER SYNOPSIS',
                      'Language known','Skills Sets:','Technical Skills:','Software proficiency','Core Strength:','Technical and personal skills', 
                      'Strength','Computer Proficiency','PROFESSIONAL SKILLS:','STRENGTH:','Computer knowledge :','  Skills : ','Technical Skills',
                      'COMPUTER KNOWLEDGE','KEY STRENGTH','STRENGHTS','Strengths:','AREAS OF INTEREST','SKILLS:', 'Skills in IT', 'Conceptual Knowledge',
                      'KEY SKILLS AND ATTRIBUTES','AREA OF INTEREST','Area of Expertise', 'COMPUTER KNOWLEDGE', 'Key Result Area : -', 'Computer Skill :',
                      'Seminars/ Project/ Workshops attended: '],
            
            'Others': ['Personal Details', 'PERSONAL PROFILE', 'Personal:','PASSPORT DETAILS :','PERSONAL DETAILS :','PERSONAL INFORMATION', 'Personal Data:', 
                                 'Address for Correspondence: –','PERSONAL DETAILS','PERSONAL DETAILS:','Permanent Address', 'Place of Issue:', 'PERSONAL DATA',
                                 'LANGUAGES KNOWN','PERSONAL DETAILS','PERSONALITIES TRAITS', 'Passport No.:', 'Expiry Date :', 'PERSONAL PARTICULARS:', 'Personal Detail',
                                 'Language known','Personal Details:','Personal Qualities:','PERSONAL PROFILE','Personal Information:', 'Current Address:', 'Permanent Address:',
                                 'ADDRESS FOR     COMMUNICATION:','FIELD OF INTERESTS :','PERSONAL PROFILE :','Personal Profile','Personal Assets','PERSONALITY TRAITS',
                                 'Personal Information', 'PERSONAL INFORMATION:', 'PERSONAL DOSSIER', 'PERSONAL PROFILE :-', 'Present Address:', 'PERSONAL DETAILS:-',                  
                                 'Current Address:', 'Permanent Address:', 'Mobile Number: '],
            
            'Experience': ['Professional Experience','Work Experience','Employment History','Work Experience:', 'Job Responsibilities:','Project work:', 'FINAL YEAR PROJECT',
                           'Major Projects:','MAJOR PROJECT WORK:','EXPERIENCE :','EXPERIENCE DETAILS ','JOB ROLE AND KEY SKILLS', 'TRAINING AND PROJECTS UNDERTAKEN',
                           'PROJECTS UNDERTAKEN:','PROJECTS/TRAINING','WORK EXPERIENCE','Summary of Experience:','Professional Experience:','Key Activities:', 'Employment History:',
                           'Previous Assignments:','Project and Training Undertaken:','Current working:','PROJECT UNDERTAKEN:','Job experience :', 'Work Experience:-', 
                           'PROJECTS','Major project','Minor project','WORK DONE','Career Highlight','Summer Internship:', 'INTERNSHIP& WORK EXPERIENCE', 'INTERNSHIP & WORK EXPERIENCE',
                           'FINAL YEAR PROJECT:','Academic Projects & Technical skills','TRAINING AND PROJECTS UNDERTAKEN', 'EXPERIENCE', 'Experience ',
                           'Professional Exposure', 'WORKING EXPERIENCE :-', 'Previous Company Profile:', 'Experience Of Work: ', 'Professional Summary', 'Internship '],
            
            'Licenses And Certifications': ['TRAINING CERTIFICATION', 'EXPERIENCE CERTIFICATION','Additional Qualifications: ','CERTIFICATION','PROFESSIONAL QUALIFICATION',                  
                               'CERTIFICATION','CERTIFICATIONS','TRAINING CERTIFICATION', 'Professional Trainings', 'TRAINING:', 'Industrial Summer Training', 'Activities:',
                               'INDUSTRIAL VISITS AND TRAINING:','PROJECTS/TRAINING','Project and Training Undertaken:','Industrial Training :','TRAINING UNDERTAKEN :',
                               'Vocational Trainings','Industrial Visits','INDUSTRIAL VISITS:','TRAINING & VISITS:','Industrial Training','Training', 'TRANNING & VISITS:', 
                               'Trainings: ', 'TRAINING AND PROJECT', 'Industrial Summer Training', 'Industrial Training', 'TRAINING '],
            
            
            'Recommendation': ['Driving licenseReferees'],

            'achievements': ['PAPER PRESENTATION:','AWARD ACHIEVEMENT','ACHIEVEMENTS:',' ACHEIVEMENTS ','Achiements:','Achievements','ACHIEVMENTS:','ACHIEVEMENTS', 'AWARD ACHIEVEMENT :'],

            'extra': ['Extra Curricular Activity:', 'EXTRA CURRICULAR ACTIVITIES:', 'Extra-curricular Activities', 'EXTRA ACTIVIES :', 'ACADEMIC / EXTRA CURRICULAR ACHIEVEMENTS',
                      'CO-CURRICULAR:', 'Extra & Co-Curricular Activities:','Extra Curricular activities:-','CO/EXTRA-CURRICULAR ACHIEVEMENTS',
                      'CO-CURRICULAR ACTIVITIES & EXPERIENCE:','Extra Curricular Activities','EXTRA CO-CURRICULAR  ACTIVITIES', 'EXTRA CO-CURRICULAR ACTIVITIES',
                      'EXTRA CURRILUCAR ACTIVITIES', 'EXTRA CURRICULAR ACTIVITIES:-','EXTRA-CURRICULAR ACTIVITIES'],    
               
            'Headline': ['CAREER OBJECTIVE :-','CAREER OBJECTIVE','OBJECTIVE:','AIM:','Objectives:','Objective','Career Objective:','Career Objective', 
                         'CAREER OBJECTIVE:', 'Objective:', 'OBJECTIVE', 'CAREER OBJECTIVE:-', 'Purpose'],
            
            'declaration': ['DECLARATION:','Declaration :','Declaration', 'DECLARATION', 'DECLAIRATION:', 'Declaration:', 'DECLARATION:-'],
            
            'misc': ['STRENTH:', 'Strength:   ', 'PERSONALITY TRAITS', 'HOBBIES', 'KEY STRENGTH', 'Social Responsibility:', 'Strength:', 'Principles:', 'STRENGHTS', 'ABOUT ME', 'HOBBIES & INTREASTS',
                     'HOBBIES AND INTEREST:', 'Interests and Hobbies', 'Strengths', 'Hobbies/ Interest', 'Hobbies: -', 'Strength: -', 'Languages Known: -', 'STRENGTHS ']}

sub_patterns = OrderedDict()
sub_patterns = {'Experience': ['Date :', 'Role: ', 'Position :', 'Employer :', 'Duties :', 'From –', 'EMPLOYER -', 'Project:',  'Roles & Responsibilities:', 'Summer Internship:', 'Job Description ',
                               'Designation -', 'Head Quarter –', 'Employment History:', 'Major Projects:', 'Running Project-', 'Role:', 'Project Title:', 'Description:', 'Software used:',
                               'Responsibilities:', 'Company Name :', 'Working Period :', 'Designation :', 'Experience :', 'Working', 'Worked', 'Job Responsibilities:', 'Name of Company: -',
                               'Designation:', 'Other experience :', '1)', '2)', '3)', 'Roles and responsibilities:', 'Current Salary: -', 'Expected Salary: -', 'since', 'from', 'Apprentice'],
                
                'User Information': ['Date of Birth :', 'Address :', 'Language Known :', 'Marital Status : ', 'Languages Known : ', 'NAME ', 'BIRTH DATE ', 'MARITAL STATUS ', 'GENDER ', 
                                     'LANGUAGE KNOWN ', 'NATIONALITY ' ,'COMPUTER SKILL ', 'Nationality : ', 'Sex : ', ' Current Address: ', ' Permanent Address: ', ' Passport No.: ', ' Expiry Date : ',
                                     'Place of Issue:', 'Place of Birth : ', 'Interests : '],
                
                'Education': ['Date :', 'Institution :', 'Course :', 'Grade :', 'Bachelor', 'XIIth', 'Xth', 'Professional:-', 'Academic:-', 'Graduation :', 'Intermediate :', 'Matriculation :', ' Matriculation ',
                              'Topic: ', 'DIPLOMA:', 'B.TECH', 'Diploma', 'DIPLOMA PROJECT: ', 'Year of Passing –', ' Secondary ', 'BS', 'MS', 'MBA', 'B.A', 'M.A', 'BSc', 'Institution','Institute',
                              'School/ College Name','University / Institutes','INSTITUTION/ UNIVERSITY','UNIVERSITY','BOARD/UNIVERSITY', 'Institustion', 'YEAR','Year of Passing','Passing Year',
                              'Course','SPECIALIZATION','Qualification','Examination Passed' ,'Degree/Examination','Degree/Certificates','DEGREE/COURSE','CLASS', 'PassingYear','YEAR  OF PASSING'],

                'Licenses And Certifications': ['Date :', 'Institution :','Course :', 'Grade :', 'Training:-', 'Project-', 'Title : ', 'Duration : ', 'Organization : ']}

course = ['Course','SPECIALIZATION','Qualification','Examination Passed' ,'Degree/Examination','Degree/Certificates','DEGREE/COURSE','CLASS']
institute = ['Institution','Institute','Institustion','School/ College Name','University / Institutes','INSTITUTION/ UNIVERSITY','UNIVERSITY','BOARD/UNIVERSITY'] 
year = ['YEAR','Year of Passing','Passing Year','PassingYear','YEAR  OF PASSING']
address_subpatterns = ["Address","contact no.", "e-mail","Date of Birth"]

template = {'Experience': {'Date': ['Date :', 'From –', 'Working Period :', 'since', 'from'], 'Company Name': ['Working', 'Worked', 'Employer :', 'EMPLOYER -', 'Name of Company: -', 'Company Name :', 'Apprentice'], 
                           'Location': ['Head Quarter –'], 'Title': ['Position :', 'Role: ', 'Designation -', 'Designation:', 'Designation :'], 'Description': ['Duties :', 'Project:',
                           'Roles & Responsibilities:', 'Summer Internship:', 'Responsibilities:', 'Project Title:', 'Job Responsibilities:', 'Project Description:', 'Project: ', 'Job Description ']},
            'Education': {'School': ['Institution :'], 'FieldOfStudy': ['Course :', 'Bachelor', 'XIIth', 'Xth', 'Professional:-', 'Academic:-', 'Graduation :', 'Intermediate :', 'Matriculation :',
                          'Topic: ', 'DIPLOMA:', 'B.TECH', 'Diploma', 'DIPLOMA PROJECT: '], 'Date': ['Date :', 'Year of Passing –']},
            'Licenses And Certifications': {'Name': ['Course :', 'Training:-', 'Project-', 'Title : '], 'Issuer': ['Institution :', 'Organization : '], 'Issuedate': ['Date :', 'Duration : ']}}

#extract raw text from PDF
def extract_raw_text(filename):
    fname = 'Resume/cv/pdf/'+filename
    doc = fitz.open(fname)
    text = ""
    for page in doc:
        text = text + str(page.getText())
        
        tx = " ".join(text.split("\n"))
        #print(tx)
        
    tables = camelot.read_pdf(fname)
    if tables:
        if tables[0].parsing_report['accuracy'] == 0:
            return re.sub(r'[\uf0de√\uf07d\uf0d8\u25cf\uf0a7\x80\ufffd\uf02a\u02da]|\s+', ' ', tx)
        elif tables[0].parsing_report['accuracy'] > 50:
            return re.sub(r'[\uf0de√\uf07d\uf0d8\u25cf\uf0a7\x80\ufffd\uf02a\u02da]|\s+', ' ', tx), tables
    
    else:
        return re.sub(r'[\uf0de√\uf07d\uf0d8\u25cf\uf0a7\x80\ufffd\uf02a\u02da\u02da]|\s+', ' ', tx)
		
def extract_email(tx1):
    email = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", tx1)
    return email
	
def extract_mobile(tx1):
    mobile = re.findall(r'[\+\(]?[0-9]{12}', tx1)

    if len(mobile)==0:
        #format +91 9953578789
        #91-731-2489229
        #09713215260
        #+91 94800 02037
        #+20100 1877 466
        mobile = re.findall(r'\d{2}-\d{3}-\d{7}|\+\d{2}\s\d{10}|0\d{10}|\+\d{2}\s\d{5}\s\d{5}|\+\d{5}\s\d{4}\s\d{3}|\+\d{2}-\d{10}|\d{10}', tx1)    

    return mobile
	
def extract_name(text):
    all_data = re.split('\r|\n',text)
    #print(all_data)
    #first_line = all_data[0].lower().strip()
    name =''
    for w in all_data:
        #print('>>>>',w.lower().strip())
        if(w.lower().strip() == 'curriculum vitae' or w.lower().strip() == 'curriculum viate' or w.lower().strip() =='curriculum- vitae' or w.lower().strip() =='curriculam vitae'):
            continue
        elif w.lower().strip() == 'resume' or w.lower().strip() == 'resu' or w.lower().strip() =='resum':
            continue
        elif w.lower().strip() == '':
            continue
        elif w.lower().strip() == 'page 1':
            continue
        elif w.lower().strip() == 'career objective' or w.lower().strip() == 'personal details':
            continue
        elif w.lower().strip() == '3 years':
            continue
        elif w.lower().strip() == 'personal' or w.lower().strip() == 'bio-data' or w.lower().strip() == 'c.v.':
            continue    
        else:
            name = w.lower().strip()
            break
   
    #print("Name: ",name)
    return name
		
#get position, data and dictionary of patterns with their values
def get_position(pat, text, start):
    #get each position of the patterns available in the text
    position = dict() 
    for k, v in pat.items():
        for each in list(set(v)):
            try:
                if text.find(each) != -1:
                    position[each] = text.find(each, start)
            
            except Exception as e:
                return e

    if position:
        #sort by position value of the pattern   
        sorted_position = {k:v for k, v in sorted(position.items(), key=lambda item: item[1])}

    else:
        sorted_position = {}
    
    return sorted_position

def get_details(sorted_position, value, end_pos=None):
    #get the data from the text according to the sorted positions 
    data = list()
    for pos, (k, v) in enumerate(sorted_position.items()):
        try:
            if v != -1:
                next_pos = pos+1
                if next_pos <= len(list(sorted_position.values()))-1:      
                    next_val = list(sorted_position.values())[next_pos]-1
                    data.append(value[v:next_val].strip())
                else:
                    if end_pos != None:
                        data.append(value[v:end_pos].strip())
                    else:
                        data.append(value[v:].strip())

        except Exception as e:
            return e
    
    return data

def dictionary(pat, sorted_position, data):
    #make dict of the pattern key to its data
    excel = dict()
    if data:
        index = 0
        for k, v in sorted_position.items():
            for head, val in pat.items():
                if k in val:
                    if head in excel:
                        if not isinstance(excel[head], list):
                            # If type is not list then make it list
                            excel[head] = [excel[head]]
                        # Append the value in list
                        excel[head].append(data[index])
                    
                    else:
                        # As key is not in dict, so add key-value pair
                        excel[head] = data[index]
                        
            index += 1   
                 
            
    return excel
	
#from patterns and text, get the corresponding sub patterns and text, if present
def subpatterns(exl, sub_patterns):
    output = dict()
    #iterating through the patterns information dictionary
    for key, value in exl.items():
        f = dict()
        output[key] = list()
        #iterating through subpatterns dictionary
        for k, v in sub_patterns.items():
            if key == k:
                count = OrderedDict()  
                #iterating through each value if key of the pattern information dict matches with key of the subpattern dict       
                for va in v:  
                    #checking if the value in the pattern information dict is a list or string
                    if isinstance(value, list):
                        #if pattern informtion dict value is a list, iterating through each element of the value
                        for val in value:
                            #if the subpattern dict value is found in the pattern information string value, take a count
                            if re.findall(va, val):
                                f[va] = list()
                                count[va] = len(re.findall(va, val))
                                #if at least one value of the subpattern dict is found in the pattern information value string, 
                                #find the starting point of each of the subpattern value
                                if max(list(count.values())) >= 1:         
                                    for sub_pat in re.finditer(va, val):
                                        f[va].append(sub_pat.start())
                       
                        #'start' variable provides the start and end position of the sub pattern to be found in the string
                        start = 0
                        #iterating through the subpattern position values
                        for subk, subv in f.items():
                            #iterating through the number of times the subpattern occurs
                            for sub in subv:
                                #iterating through each value of the data list
                                for val in value:
                                    #if the subpattern value is present in the string, form the dictionary 
                                    if re.findall(va, val):
                                        sub_pos = get_position(sub_patterns, val, f[subk][start])
                                        if start < len(f[subk])-1:
                                            sub_details = get_details(sub_pos, val, f[subk][start+1])
                                            output[key].append(sub_details) 
                                        else:
                                            sub_details = get_details(sub_pos, val)
                                            output[key].append(sub_details)
                                        start += 1
                            break
                        break
                        
                    else:
                        if re.findall(va, value):
                            f[va] = list()
                            count[va] = len(re.findall(va, value))
                            if max(list(count.values())) >= 1:         
                                for sub_pat in re.finditer(va, value):
                                    f[va].append(sub_pat.start())
                        
                        start = 0
                        for subk, subv in f.items():
                            for sub in subv:
                                if re.findall(va, value):
                                    sub_pos = get_position(sub_patterns, value, f[subk][start])
                                    if start < len(f[subk])-1:
                                        sub_details = get_details(sub_pos, value, f[subk][start+1])
                                        output[key].append(sub_details)
                                    else:
                                        sub_details = get_details(sub_pos, value)
                                        output[key].append(sub_details)
                                    start += 1
                            break
                        break
                        
    return output
	
def fetch_education(tables):
    df_new = dict()
    df_new['Education'] = list()
    course_row, course_col = 0, 0;
    school_row, school_col = 0, 0
    year_row, year_col = 0, 0
    if tables.n > 0:
        for i in range(tables.n):
            df = tables[i].df
            row, col = df.shape
            if(2 < col < 5):
                for j in range(row):
                    cell = ''
                    for k in range(col):
                        ctxt = df.iloc[j,k]
                        cell = ctxt.replace("\n", " ", ) + ' ' + cell
                    if j > 0:
                        if len(cell) > 6:
                            df_new['Education'].append(cell)
        
    return df_new
	
#creating list with 'NA' that gets updated with each pdf
def merge_patsubpat(exl, output, df=None):
    for key, value in exl.items():
        for subk, subv in output.items():
            if key == subk:
                if subk == 'Education':
                    if df:
                        if 'Education' in df:
                            output[subk] = df['Education']                      
                if output[subk]:
                    pass
                else:
                    output[subk] = value
            if isinstance(output[subk], list):
                if '' in output[subk]:
                    output[subk].remove('')

    #structured output of the pdf text
    return output
	
def parse_text(output, pdf_no, raw_text):
    txt_name = str(pdf_no) + '.txt'
    txt_path = "td_new/" + txt_name
    with open(txt_path, 'w+') as fw:
        for subk in output:
            #if subk == 'Experience' or subk == 'Education' or subk == 'Knowledge' or subk == 'Others':
            if isinstance(output[subk], list):
                for head in output[subk]:
                    if isinstance(head, list):
                        if head:
                            for h in head:
                                if len(h) > 6 :
                                    fw.write('header'+'\t'+subk.lower()+'\t'+h+'\n')

                    else:
                        if len(head) > 6:
                            if '. ' in head:
                                hd = head.split('. ')
                                for h in hd:
                                    if len(h) > 6:
                                        fw.write('header'+'\t'+subk.lower()+'\t'+h+'\n')
                            else:
                                fw.write('header'+'\t'+subk.lower()+'\t'+head+'\n')

            else:
                if len(output[subk]) > 6:
                    if '. ' in output[subk]:
                        hd = output[subk].split('. ')
                        for h in hd:
                            if len(h) > 6:
                                fw.write('header'+'\t'+subk.lower()+'\t'+h+'\n')                
                    else:
                        fw.write('header'+'\t'+subk.lower()+'\t'+output[subk]+'\n')
        
        #name = extract_name(raw_text)
        #if name != '':
        #    fw.write('header'+'\t'+"name"+'\t'+name+'\n')
        
        email = extract_email(raw_text)
        for em in email:
            if em != '':
                fw.write('header'+'\t'+'email'+'\t'+em+'\n')

        mobile = extract_mobile(raw_text)
        for mb in mobile:
            if mb != '':
                fw.write('header'+'\t'+'mobile'+'\t'+mb+'\n')

def extractText(pdf_num):
	import os

	for i in range(int(pdf_num)):
		pdf_no = i+1
		pdfname= str(pdf_no)+'.pdf'
		if(str(os.path.exists('Resume/cv/pdf/'+pdfname)) == 'False'):
			print("skipping ",pdfname)
			continue;
		print(pdfname)

		#get the text from pdf
		tx = extract_raw_text(pdfname)

		#if table exists in pdf
		if isinstance(tx, tuple):
			pos = get_position(patterns, tx[0], 0)
			tables = tx[1]
			
		#when no table in pdf
		else:
			pos = get_position(patterns, tx, 0)
			tables = 0

		if tables:
			#get patterns and corresponding text
			data = get_details(pos, tx[0])
			exl = dictionary(patterns, pos, data)
			output = subpatterns(exl, sub_patterns)
			df_new = fetch_education(tables)
			output = merge_patsubpat(exl, output, df_new)
			parse_text(output, pdf_no, tx[0])
			
		else:
			#get patterns and corresponding text
			data = get_details(pos, tx)
			exl = dictionary(patterns, pos, data)
			output = subpatterns(exl, sub_patterns)
			output = merge_patsubpat(exl, output)
			parse_text(output, pdf_no, tx)

def main(pdf_num):
    print(extractText(pdf_num))

if __name__ == '__main__':
    #enter the number of training samples to be generated
    main(pdf_num)






