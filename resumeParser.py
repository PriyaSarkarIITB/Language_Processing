#!/usr/bin/env python

import nltk, os, subprocess, code, glob, re, traceback, sys, inspect
from time import clock, sleep
from pprint import pprint
import json
import zipfile
# import ner
from convertPDFToText import convertPDFToText
from convertDocxToText import convertDocxToText
from convertRtfToText import convertRtfToText

from clint.textui import progress, puts, colored, columns, indent

import MySQLdb as mdb 

def printSourceLines(function):
    '''Can be used during debugging for printing a function's code'''
    try:
        print "".join(inspect.getsourcelines(function)[0])
    except:
        print "Invalid function/Failed to retrieve source code"

def printList(inputList):
    for el in inputList:
        print el, "\n"

class exportToCSV:
    def __init__(self, fileName='resultsCSV.txt', resetFile=False):
        headers = ['FILE NAME',
               'NAME',
               'EMAIL1', 'EMAIL2', 'EMAIL3', 'EMAIL4',
               'PHONE1', 'PHONE2', 'PHONE3', 'PHONE4',
               'DOB',
               'EXPERIENCE',
               'DEGREES','INSTITUTES','YEARS'
               'PASSPORT',
               'TIME'
               ]
        if not os.path.isfile(fileName) or resetFile:
            # Will create/reset the file as per the evaluation of above condition
            fOut = open(fileName, 'w')
            fOut.close()
        fIn = open(fileName)
        inString = fIn.read()
        fIn.close()
        if len(inString) <= 0:
            fOut = open(fileName, 'w')
            fOut.write(','.join(headers)+'\n')
            fOut.close()

    def write(self, infoDict):
        fOut = open('resultsCSV.txt', 'a+')
        # Individual elements are dictionaries
        writeString = ''
        try:
            writeString += str(infoDict['fileName']) + ','
            writeString += str(infoDict['name']) + ','
            writeString += str(','.join(infoDict['email'][:4])) + ','
            if len(infoDict['email']) < 4:
                writeString += ','*(4-len(infoDict['email']))
            writeString += str(','.join(infoDict['phone'][:4])) + ','
            if len(infoDict['phone']) < 4:
                writeString += ','*(4-len(infoDict['phone']))
            writeString += str(','.join(infoDict['degree'][:4])) + ',' # For the remaining elements
            writeString += str(','.join(infoDict['%sinstitute'%'c\.?a']))
            writeString +=str(','.join(infoDict['%syear'%'c\.?a']))
            writeString += str(','.join(infoDict['%sinstitute'%'b\.?com']))
            writeString +=str(','.join(infoDict['%syear'%'b\.?com']))
            writeString += str(','.join(infoDict['%sinstitute'%'icwa']))
            writeString +=str(','.join(infoDict['%syear'%'icwa']))
            writeString += str(','.join(infoDict['%sinstitute'%'m\.?com']))
            writeString +=str(','.join(infoDict['%syear'%'m\.?com']))
            writeString += str(','.join(infoDict['%sinstitute'%'mba']))
            writeString +=str(','.join(infoDict['%syear'%'mba'])) 
            fOut.write(writeString)
        except:
            fOut.write('FAILED_TO_WRITE\n')
        fOut.close()

# def insertToDBforeducations(infoList,D1,D2):
#     for info in infolist:
#             print info['degree']
            
#             for deg in info['degree']:
#                 #code.interact(local=locals())
#                 print deg
#                 if D2==deg:
#                     query = "insert into educations1 (candidate_id,degree_id,institute_id) values"
#                     for institute in info['%sinstitute'%D1]:
#                         query+="(%d, '%v','%t','%u')," %(info['candidate_id'],D2,info['%sinstitute'%D1])
#                         # Reconnect con now because *with* released it
#                         con = mdb.connect(host, user, password, database)
#                         with con:
#                             cur = con.cursor()
#                             cur.execute(query)
#                     query = "insert into educations1 (candidate_id,degree_id,passing_year) values"
#                     for institute in info['%sinstitute'%D1]:
#                         query+="(%d, '%v','%t','%u')," %(info['candidate_id'],D2,info['%sinstitute'%D1])
#                         # Reconnect con now because *with* released it
#                         con = mdb.connect(host, user, password, database)
#                         with con:
#                             cur = con.cursor()
#                             cur.execute(query)


def insertToDB(infoList):
    # Lists and dictionaries are passed *by reference* - this function will change them
    # Max 1000 records can be inserted at a time
    infoList = [el for el in infoList if not el['fileReadFailed']]
    # Credentials and connection information
    host = 'localhost'
    user = 'root'
    password = 'test123'
    database = 'quezx'
    # For writing to resumes2s table, this map is needed. The info dictionary has an 'extension' key that stores the required value
    extensionMap = {
    'doc':1,
    'docx':2,
    'pdf':3,
    'rtf':4,
    }
    try:
        # name,experience -> candidates table
        con = mdb.connect(host, user, password, database)
        #  *with* automatically releases resources; no need to call con.close()
        with con:
            cur = con.cursor()
            for info in infoList:
                cur.execute("insert into candidates (name,total_exp) values ('%s',%s)" %(info['name'],info['experience']))
                insertid = "select last_insert_id()"
                cur.execute(insertid)
                lastID = cur.fetchone()
                # Above returns a tuple like (80000L,)
                info['candidate_id'] = lastID[0]
        
        # phone number -> phone_numbers table, linked with foreign key to candidates table
        query = "insert into phone_numbers (candidate_id, number) values "
        for info in infoList:
            for number in info['phone'][:4]:
                # Take just the first 4 numbers
                query += "(%d,'%s'), " %(info['candidate_id'], number)
        # Syntax error otherwise, remove the last whitespace and comma
        query = query[:-2]
        # Reconnect con now because *with* released it
        con = mdb.connect(host, user, password, database)
        with con:
            cur = con.cursor()
            cur.execute(query)
            #code.interact(local=locals())
        
        # email -> emails table
        query = "insert into emails (candidate_id, email) values "
        for info in infoList:
            for email in info['email'][:4]:
                # Take just the first 4 emails
                query += "(%d, '%s'), " %(info['candidate_id'], email)
        # Syntax error otherwise, remove the last whitespace and comma
        query = query[:-2]
        # Reconnect con now because *with* released it
        con = mdb.connect(host, user, password, database)
        with con:
            cur = con.cursor()
            cur.execute(query)
            #code.interact(local=locals())


        #fetching degree ids from degree table
        query="select id,degree from degrees"
        con = mdb.connect(host, user, password, database)
        with con:
                cur = con.cursor()
                cur.execute(query)
                rows=cur.fetchall()
        
        for row in rows:
            if row.degree.lower() in 'ca':
                info['degree_id']=row.id
            if row.degree.lower() in 'b.com':
                info['degree_id']=row.id
            if row.degree.lower() in 'icwa':
                info['degree_id']=row.id
            if row.degree.lower() in 'm.com':
                info['degree_id']=row.id
            if row.degree.lower() in 'mba':
                info['degree_id']=row.id
        
        #degree,year-->educations 
        for info in infoList:
            for deg in info['degree']:
                if r'ca' in deg:

                    query="insert into educations (candidate_id,degree_id,passing_year) values(%d, %s,%s)" %(info['candidate_id'],info['degree_id'],info['%syear'%'c\.?a'])
                    # Reconnect con now because *with* released it
                    con = mdb.connect(host, user, password, database)
                    with con:
                        cur = con.cursor()
                        try:    
                            cur.execute(query)

                        except mdb.Error as e:
                            try:
                                print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
                            except IndexError:
                                print "MySQL Error %s"%str(e)
                if r'b.com' in deg:
                    #code.interact(local=locals())
                    try:
                        query="insert into educations (candidate_id,degree_id,passing_year) values(%d, %s,%s)" %(info['candidate_id'],info['degree_id'],info['%syear'%'b\.?com'])                                # Reconnect con now because *with* released it
                        con = mdb.connect(host, user, password, database)
                        with con:
                            cur = con.cursor()
                            cur.execute(query)
                    except mdb.Error as e:
                        try:
                            print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
                        except IndexError:
                            print "MySQL Error %s"%str(e)
                if r'icwa' in deg:
                    try:
                        query="insert into educations (candidate_id,degree_id,passing_year) values(%d, %s,%s)" %(info['candidate_id'],info['degree_id'],info['%syear'%'icwa'])
                        # Reconnect con now because *with* released it
                        con = mdb.connect(host, user, password, database)
                        with con:
                            cur = con.cursor()
                            cur.execute(query)
                    except mdb.Error as e:
                        try:
                            print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
                        except IndexError:
                            print "MySQL Error %s"%str(e)
                if r'm.com' in deg:
                    try:
                        query="insert into educations (candidate_id,degree_id,passing_year) values(%d, %s,%s)" %(info['candidate_id'],info['degree_id'],info['%syear'%'m\.?com'])
                        # Reconnect con now because *with* released it
                        con = mdb.connect(host, user, password, database)
                        with con:
                            cur = con.cursor()
                            cur.execute(query)
                    except mdb.Error as e:
                        try:
                            print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
                        except IndexError:
                            print "MySQL Error %s"%str(e)
                if r'mba'in deg:
                    try:
                        query="insert into educations (candidate_id,degree_id,passing_year) values(%d, %s,%s)" %(info['candidate_id'],info['degree_id'],info['%syear'%'mba'])
                        # Reconnect con now because *with* released it
                        con = mdb.connect(host, user, password, database)
                        with con:
                            cur = con.cursor()
                            cur.execute(query)
                    except mdb.Error as e:
                        try:
                            print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
                        except IndexError:
                            print "MySQL Error %s"%str(e)
            
        # for info in infoList:
        #     for deg in info['degree']:
        #         if r'ca' in deg:
        #             query="insert into educations1 (candidate_id,degree_id,institute_id,passing_year) values(%d, '%s','%s','%s')" %(info['candidate_id'],'ca',info['%sinstitute'%'c\.?a'],info['%syear'%'c\.?a'])
        #             # Reconnect con now because *with* released it
        #             con = mdb.connect(host, user, password, database)
        #             with con:
        #                 cur = con.cursor()
        #                 try:    
        #                     cur.execute(query)

        #                 except mdb.Error as e:
        #                     try:
        #                         print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
        #                     except IndexError:
        #                         print "MySQL Error %s"%str(e)
        #         if r'b.com' in deg:
        #             #code.interact(local=locals())
        #             try:
        #                 query ="insert into educations1 (candidate_id,degree_id,institute_id,passing_year) values(%d, '%s','%s','%s')" %(info['candidate_id'], 'b.com',info['%sinstitute'%'b\.?com'],info['%syear'%'b\.?com'])
        #                 # Reconnect con now because *with* released it
        #                 con = mdb.connect(host, user, password, database)
        #                 with con:
        #                     cur = con.cursor()
        #                     cur.execute(query)
        #             except mdb.Error as e:
        #                 try:
        #                     print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
        #                 except IndexError:
        #                     print "MySQL Error %s"%str(e)
        #         if r'icwa' in deg:
        #             try:
        #                 query ="insert into educations1 (candidate_id,degree_id,institute_id,passing_year) values(%d, '%s','%s','%s')" %(info['candidate_id'], 'icwa',info['%sinstitute'%'icwa'],info['%syear'%'icwa'])
        #                 # Reconnect con now because *with* released it
        #                 con = mdb.connect(host, user, password, database)
        #                 with con:
        #                     cur = con.cursor()
        #                     cur.execute(query)
        #             except mdb.Error as e:
        #                 try:
        #                     print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
        #                 except IndexError:
        #                     print "MySQL Error %s"%str(e)
        #         if r'm.com' in deg:
        #             try:
        #                 query ="insert into educations1 (candidate_id,degree_id,institute_id,passing_year) values(%d, '%s','%s','%s')" %(info['candidate_id'], 'm.com',info['%sinstitute'%'m\.?com'],info['%syear'%'m\.?com'])
        #                 # Reconnect con now because *with* released it
        #                 con = mdb.connect(host, user, password, database)
        #                 with con:
        #                     cur = con.cursor()
        #                     cur.execute(query)
        #             except mdb.Error as e:
        #                 try:
        #                     print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
        #                 except IndexError:
        #                     print "MySQL Error %s"%str(e)
        #         if r'mba'in deg:
        #             try:
        #                 query ="insert into educations1 (candidate_id,degree_id,institute_id,passing_year) values(%d, '%s','%s','%s')" %(info['candidate_id'], 'mba',info['%sinstitute'%'mba'],info['%syear'%'mba'])
        #                 # Reconnect con now because *with* released it
        #                 con = mdb.connect(host, user, password, database)
        #                 with con:
        #                     cur = con.cursor()
        #                     cur.execute(query)
        #             except mdb.Error as e:
        #                 try:
        #                     print"MySQL Error [%d]: %s"%(e.args[0],e.args[1])
        #                 except IndexError:
        #                     print "MySQL Error %s"%str(e)
        
        
       

    except Exception as e:
        with indent(4):
            puts(str(e))
    
def searchDB(tableName):
    returnVal = False
    # Credentials and connection information
    host = 'localhost'
    user = 'root'
    password = 'test123'
    database = 'quezx'
    try:
        con = mdb.connect(host, user, password, database)
        with con:
            cur = con.cursor()
            cur.execute('select * from %s;' %tableName)
            val = cur.fetchone()
            if val:
                returnVal = val
                print val
    except Exception as e:
        with indent(4):
            puts(str(e))
    finally:
        con.close()
        return returnVal

def converttoZIP(file1):
    myzip=zipfile.ZipFile('filesread.zip', 'a')
    myzip.write(file1)
    myzip.close()

def convertToHTML(infoDict, outdir='resumesHTML'):
    '''
    Takes a set or list of fileNames.
    Default takes resumes in the directory resumes/, and puts converted files in resumesHTML/
    It then reads in the converted files, and deletes the folder containing the converted files
    Note: Takes ~ 1 second per file
    '''
    try:
        # Uses LibreOffice's command line utility to convert the file to HTML
        command = 'soffice --headless --convert-to html --outdir "resumesHTML" "%s"' %(infoDict['fileName'])
        status = os.popen(command).read()
        # The second argument creates the converted file's name
        converted = open('%s/%s' %(outdir, ".".join(infoDict['fileName'].split('/')[-1].split('.')[:-1])+".html"))
        html = converted.read()
        # Following try-except block is for removing characters that cause a format error
        try: 
            infoDict['resumeHTML'] = html.decode('ascii', 'ignore')
        except:
            infoDict['resumeHTML'] = html.encode('ascii', 'ignore')
            try:
                infoDict['resumeHTML'] = html
            except:
                infoDict['resumeHTML'] = ''
        converted.close()
        os.system('rm -rf %s' %(outdir))
    except Exception as e:
        print str(e)
        infoDict['resumeHTML'] = ""
        pass
    
class Parse():
    # List (of dictionaries) that will store all of the values
    # For processing purposes
    information=[]
    inputString = ''
    tokens = []
    lines = []
    sentences = []

    def __init__(self, verbose=False):
        #csv = exportToCSV()
        puts(colored.yellow('Starting Programme'))
        t = [0,0] # For benchmarking
        fields = ["name", "address", "email", "phone", "mobile", "telephone", "residence status","experience","degree","cainstitute","cayear","caline","b.cominstitute","b.comyear","b.comline","icwainstitue","icwayear","icwaline","m.cominstitute","m.comyear","m.comline","mbainstitute","mbayear","mbaline"]

        t[0] = clock()
        
        # Glob module matches certain patterns
        doc_files = glob.glob("resumes/*.doc")
        docx_files = glob.glob("resumes/*.docx")
        pdf_files = glob.glob("resumes/*.pdf")
        rtf_files = glob.glob("resumes/*.rtf")
        text_files = glob.glob("resumes/*.txt")

        files = set(doc_files + docx_files + pdf_files + rtf_files + text_files)
        # For testing; remove next line later
        files = list(files)[:5]
        with indent(4): puts(colored.blue("%d files identified" %len(files)))
        t[1] = clock()
        with indent(8): puts(colored.white("took %f seconds" %(t[1]-t[0])))
        
        col = 30
        # puts(columns([colored.magenta('File Name'), col], [colored.magenta('Read Failed'), col], [colored.magenta('Name'), col], [colored.magenta('email'), col], [colored.magenta('Phone'), col]))
        for f in files:
            # info is a dictionary that stores all the data obtained from parsing
            info = {}
            
            t[0] = clock()
            self.inputString, info['extension'] = self.readFile(f)
            t[1] = clock()
            readTime = round(t[1]-t[0],6)
            
            info['fileName'] = f
            if len(self.inputString) == 0:
                info['fileReadFailed'] = True
            else:
                info['fileReadFailed'] = False
                converttoZIP(f)
            t[0] = clock()
            self.tokenize(self.inputString)
            t[1] = clock()
            stringProcessTime = round(t[1]-t[0], 6)
            t[0] = clock()
            self.getEmail(self.inputString, info)
            t[1] = clock()
            emailTime = round(t[1]-t[0], 6)
            t[0] = clock()
            self.getPhone(self.inputString, info)
            t[1] = clock()
            phoneTime = round(t[1]-t[0], 6)
            t[0] = clock()
            self.getName(self.inputString, info)
            t[1] = clock()
            nameTime = round(t[1]-t[0], 6)
            self.Qualification(self.inputString,info)
            self.getExperience(self.inputString,info,debug=False)
            # t[0] = clock()
            # convertToHTML(info)
            # t[1] = clock()
            #csv.write(info)
            self.information.append(info)
            print "\n", pprint(info), "\n"
            
            # Debug
            # code.interact(local=dict(globals(), **locals()))
        
        #insertToDB(self.information) #used for inserting the final obtained values into the database
        # code.interact(local = locals())
       
        failedCount = 0
        for el in self.information:
            if el["fileReadFailed"]:
                failedCount += 1
        print "\n%d/%d files processed. Look into or delete damaged files.\n" %(len(files)-failedCount, len(files))
        response = raw_input("Write final result to file? (y/n): ")
        if response == 'y':
            out_file = raw_input("Input file name: ")
            if ".txt" not in out_file: out_file = str(out_file) + ".txt"
            while True:
                try:
                    out = open(str(out_file), "w")
                    t[0] = clock()
                    json_string = json.dumps(self.information)
                    out.write(json_string)
                    t[1] = clock()
                    print "\n...... dumping info to file (%s) in %f seconds" %(out_file,(t[1]-t[0]))
                    out.close()
                    break
                except:
                    response = raw_input("Write failed; retry? (y/n): ")
                    if response == 'y':
                        continue
                    else:
                        break
        

    def readFile(self, fileName):
        '''
        Read a file given its name as a string.
        Modules required: os
        UNIX packages required: antiword, ps2ascii
        '''
        extension = fileName.split(".")[-1]
        if extension == "txt":
            f = open(fileName, 'r')
            string = f.read()
            f.close() 
            return string, extension
        elif extension == "doc":
            # Run a shell command and store the output as a string
            # Antiword is used for extracting data out of Word docs. Does not work with docx, pdf etc.
            return subprocess.Popen(['antiword', fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0], extension
        elif extension == "docx":
            try:
                return convertDocxToText(fileName), extension
            except:
                return ''
        elif extension == "rtf":
            try:
                return convertRtfToText(fileName), extension
            except:
                return ''
        elif extension == "pdf":
            # ps2ascii converst pdf to ascii text
            # May have a potential formatting loss for unicode characters
            # return os.system(("ps2ascii %s") (fileName))
            try:
                return convertPDFToText(fileName), extension
            except:
                return ''
        else:
            print 'Unsupported format'
            return '', ''

    def preprocess(self, document):
        '''
        Information Extraction: Preprocess a document with the necessary POS tagging.
        Returns three lists, one with tokens, one with POS tagged lines, one with POS tagged sentences.
        Modules required: nltk
        '''
        try:
            # Try to get rid of special characters
            try:
                document = document.decode('ascii', 'ignore')
            except:
                document = document.encode('ascii', 'ignore')
            # Newlines are one element of structure in the data
            # Helps limit the context and breaks up the data as is intended in resumes - i.e., into points
            lines = [el.strip() for el in document.split("\n") if len(el) > 0]  # Splitting on the basis of newlines 
            lines = [nltk.word_tokenize(el) for el in lines]    # Tokenize the individual lines
            lines = [nltk.pos_tag(el) for el in lines]  # Tag them
            # Below approach is slightly different because it splits sentences not just on the basis of newlines, but also full stops 
            # - (barring abbreviations etc.)
            # But it fails miserably at predicting names, so currently using it only for tokenization of the whole document
            sentences = nltk.sent_tokenize(document)    # Split/Tokenize into sentences (List of strings)
            sentences = [nltk.word_tokenize(sent) for sent in sentences]    # Split/Tokenize sentences into words (List of lists of strings)
            tokens = sentences
            sentences = [nltk.pos_tag(sent) for sent in sentences]    # Tag the tokens - list of lists of tuples - each tuple is (<word>, <tag>)
            # Next 4 lines convert tokens from a list of list of strings to a list of strings; basically stitches them together
            dummy = []
            for el in tokens:
                dummy += el
            tokens = dummy
            # tokens - words extracted from the doc, lines - split only based on newlines (may have more than one sentence)
            # sentences - split on the basis of rules of grammar
            return tokens, lines, sentences
        except Exception as e:
            print e 

    def tokenize(self, inputString):
        try:
            self.tokens, self.lines, self.sentences = self.preprocess(inputString)
            return self.tokens, self.lines, self.sentences
        except Exception as e:
            print e

    def getEmail(self, inputString, infoDict, debug=False): 
        '''
        Given an input string, returns possible matches for emails. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''
        # Note: The dictionary passed is passed by reference, so it will be changed by the function
        # t = [0,0] # For benchmarking
        # t[0] = clock()
        email = None
        try:
            pattern = re.compile(r'\S*@\S*')
            matches = pattern.findall(inputString) # Gets all email addresses as a list
            email = matches
        except Exception as e:
            print e
        # t[1] = clock()
        infoDict['email'] = email
        # print "...... email in %f seconds" %(t[1]-t[0])
        if debug:
            print "\n", pprint(infoDict), "\n"
            code.interact(local=locals())
        return email

    def getPhone(self, inputString, infoDict, debug=False):
        '''
        Given an input string, returns possible matches for phone numbers. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''
        t = [0,0]
        t[0] = clock()
        number = None
        try:
            pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
                # Understanding the above regex
                # +91 or (91) -> [+(]? \d+ -?
                # Metacharacters have to be escaped with \ outside of character classes; inside only hyphen has to be escaped
                # hyphen has to be escaped inside the character class if you're not incidication a range
                # General number formats are 123 456 7890 or 12345 67890 or 1234567890 or 123-456-7890, hence 3 or more digits
                # Amendment to above - some also have (0000) 00 00 00 kind of format
                # \s* is any whitespace character - careful, use [ \t\r\f\v]* instead since newlines are trouble
            match = pattern.findall(inputString)
            # match = [re.sub(r'\s', '', el) for el in match]
                # Get rid of random whitespaces - helps with getting rid of 6 digits or fewer (e.g. pin codes) strings
            # substitute the characters we don't want just for the purpose of checking
            match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el))>6]
                # Taking care of years, eg. 2001-2004 etc.
            match = [re.sub(r'\D$', '', el).strip() for el in match]
                # $ matches end of string. This takes care of random trailing non-digit characters. \D is non-digit characters
            match = [el for el in match if len(re.sub(r'\D','',el)) <= 15]
                # Remove number strings that are greater than 15 digits
            try:
                for el in list(match):
                    # Create a copy of the list since you're iterating over it
                    if len(el.split('-')) > 3: continue # Year format YYYY-MM-DD
                    for x in el.split("-"):
                        try:
                            # Error catching is necessary because of possibility of stray non-number characters
                            # if int(re.sub(r'\D', '', x.strip())) in range(1900, 2100):
                            if x.strip()[-4:].isdigit():
                                if int(x.strip()[-4:]) in range(1900, 2100):
                                    # Don't combine the two if statements to avoid a type conversion error
                                    match.remove(el)
                        except:
                            pass
            except:
                pass
            number = match
        except:
            pass
        t[1] = clock()
        infoDict['phone'] = number
        # print "...... phone numbers in %f seconds" %(t[1]-t[0])
        if debug:
            print "\n", pprint(infoDict), "\n"
            code.interact(local=locals())
        return number

    def getName(self, inputString, infoDict, debug=False):
        '''
        Given an input string, returns possible matches for names. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''
        t = [0,0]
        # Reads Indian Names from the file, reduce all to lower case for easy comparision [Name lists]
        indianNames = open("allNames.txt", "r").read().lower()
        # Lookup in a set is much faster
        indianNames = set(indianNames.split())
        
        t[0] = clock()
        otherNameHits = []
        nameHits = []
        name = None

        try:
            # tokens, lines, sentences = self.preprocess(inputString)
            tokens, lines, sentences = self.tokens, self.lines, self.sentences
            # Try a regex chunk parser
            # grammar = r'NAME: {<NN.*><NN.*>|<NN.*><NN.*><NN.*>}'
            grammar = r'NAME: {<NN.*><NN.*><NN.*>*}'
            # Noun phrase chunk is made out of two or three tags of type NN. (ie NN, NNP etc.) - typical of a name. {2,3} won't work, hence the syntax
            # Note the correction to the rule. Change has been made later.
            chunkParser = nltk.RegexpParser(grammar)
            all_chunked_tokens = []
            for tagged_tokens in lines:
                # Creates a parse tree
                if len(tagged_tokens) == 0: continue # Prevent it from printing warnings
                chunked_tokens = chunkParser.parse(tagged_tokens)
                all_chunked_tokens.append(chunked_tokens)
                for subtree in chunked_tokens.subtrees():
                    #  or subtree.label() == 'S' include in if condition if required
                    if subtree.label() == 'NAME':
                        for ind, leaf in enumerate(subtree.leaves()):
                            if leaf[0].lower() in indianNames and 'NN' in leaf[1]:
                                # Case insensitive matching, as indianNames have names in lowercase
                                # Take only noun-tagged tokens
                                # Surname is not in the name list, hence if match is achieved add all noun-type tokens
                                # Pick upto 3 noun entities
                                hit = " ".join([el[0] for el in subtree.leaves()[ind:ind+3]])
                                # Check for the presence of commas, colons, digits - usually markers of non-named entities 
                                if re.compile(r'[\d,:]').search(hit): continue
                                nameHits.append(hit)
                                # Need to iterate through rest of the leaves because of possible mis-matches
            # Going for the first name hit
            if len(nameHits) > 0:
                nameHits = [re.sub(r'[^a-zA-Z \-]', '', el).strip() for el in nameHits] 
                name = " ".join([el[0].upper()+el[1:].lower() for el in nameHits[0].split() if len(el)>0])
                otherNameHits = nameHits[1:]

        except Exception as e:
            print traceback.format_exc()
            print e         
        t[1] = clock()
        infoDict['name'] = name
        infoDict['otherNameHits'] = otherNameHits
        # print "...... name in %f seconds" %(t[1]-t[0])
        if debug:
            print "\n", pprint(infoDict), "\n"
            code.interact(local=locals())
        return name, otherNameHits  
    
    def getExperience(self,inputString,infoDict,debug=False):
        experience=[]
        try:
            for sentence in self.lines:#find the index of the sentence where the degree is find and then analyse that sentence
                    sen=" ".join([words[0].lower() for words in sentence]) #string of words in sentence
                    if re.search('experience',sen):
                        sen_tokenised= nltk.word_tokenize(sen)
                        tagged = nltk.pos_tag(sen_tokenised)
                        entities = nltk.chunk.ne_chunk(tagged)
                        for subtree in entities.subtrees():
                            for leaf in subtree.leaves():
                                if leaf[1]=='CD':
                                    experience=leaf[0]
        except Exception as e:
            print traceback.format_exc()
            print e 
        if experience:
            infoDict['experience'] = int(experience)
        else:
            infoDict['experience']=0
        if debug:
            print "\n", pprint(infoDict), "\n"
            code.interact(local=locals())
        return experience


        

    def getQualification(self,inputString,infoDict,D1,D2):
        t = [0,0]
        #key=list(qualification.keys())
        qualification={'institute':'','year':''}
        nameofinstitutes=open('nameofinstitutes.txt','r').read().lower()#open file which contains keywords like institutes,university usually  fond in institute names
        nameofinstitues=set(nameofinstitutes.split())
        instiregex=r'INSTI: {<DT.>?<NNP.*>+<IN.*>?<NNP.*>?}'
        chunkParser = nltk.RegexpParser(instiregex)
        
        
        try:
            t[0] = clock()
            
            index=[]
            line=[]#saves all the lines where it finds the word of that education
            for ind, sentence in enumerate(self.lines):#find the index of the sentence where the degree is find and then analyse that sentence
                sen=" ".join([words[0].lower() for words in sentence]) #string of words
                if re.search(D1,sen) or re.search(D2,sen):
                    index.append(ind)  #list of all indexes where word Ca lies
            if index:#only finds for Ca rank and CA year if it finds the word Ca in the document
                
                for indextocheck in index:#checks all nearby lines where it founds the degree word.ex-'CA'
                    for i in [indextocheck,indextocheck+1]: #checks the line with the keyword and just the next line to it
                        try:
                            wordstr=" ".join(words[0] for words in self.lines[i])#string of that particular line
                            #if re.search(r'\D\d{1,3}\D',wordstr.lower()) and qualification['rank']=='':
                                    #qualification['rank']=re.findall(r'\D\d{1,3}\D',wordstr.lower())
                                    #line.append(wordstr)
                            if re.search(r'\b[21][09][8901][0-9]',wordstr.lower()) and qualification['year']=='':
                                    qualification['year']=re.findall(r'\b[21][09][8901][0-9]',wordstr.lower())
                                    line.append(wordstr)
                            chunked_line = chunkParser.parse(self.lines[i])#regex chunk for searching univ name
                            for subtree in chunked_line.subtrees():
                                    if subtree.label()=='INSTI':
                                        for ind,leaves in enumerate(subtree):
                                            if leaves[0].lower() in nameofinstitutes and leaves[1]=='NNP' and qualification['institute']=='':
                                                qualification['institute']=' '.join([words[0]for words in subtree.leaves()])
                                                line.append(wordstr)
                                
                        except Exception as e:
                            print traceback.format_exc()
            t[1] = clock()
            if D1=='c\.?a':
                infoDict['%sinstitute'%D1] ="I.C.A.I"
            else:
                if qualification['institute']:
                    infoDict['%sinstitute'%D1] = str(qualification['institute'])
                else:
                    infoDict['%sinstitute'%D1] = "NULL"
            if qualification['year']:
                infoDict['%syear'%D1] = int(qualification['year'][0])
            else:
                infoDict['%syear'%D1] =0
            infoDict['%sline'%D1]=set(line)
            #print "...... qualification in %f seconds" %(t[1]-t[0])
            #return infoDict['%sinstitute'%D1],infoDict['%syear'%D1],set(line)
        except Exception as e:
            print traceback.format_exc()
            print e 


    def Qualification(self,inputString,infoDict,debug=False):
        degre=[]
        #Q={'CAinformation':'','ICWAinformation':'','B.Cominformation':'','M.Cominformation':'','MBAinformation':''}
        #degree=[]
        #degree1=open('degree.txt','r').read().lower()#string to read from the txt file which contains all the degrees
        #degree=set(el for el in degree1.split('\n'))#saves all the degrees seperated by new lines,degree name contains both abbreviation and full names check file
        #qualification1={'CAline':'','CAcollege':'','CArank':'','CAyear':''}
        self.getQualification(self.inputString,infoDict,'c\.?a','chartered accountant')
        if infoDict['%sline'%'c\.?a']:
         degre.append('ca')
        self.getQualification(self.inputString,infoDict,'icwa','icwa')
        if infoDict['%sline'%'icwa']:
         degre.append('icwa')
        self.getQualification(self.inputString,infoDict,'b\.?com','bachelor of commerce')
        if infoDict['%sline'%'b\.?com']:
         degre.append('b.com')
        self.getQualification(self.inputString,infoDict,'m\.?com','masters of commerce')
        if infoDict['%sline'%'m\.?com']:
         degre.append('m.com') 
        self.getQualification(self.inputString,infoDict,'mba','mba')
        if infoDict['%sline'%'mba']:
         degre.append('mba')
        if degre:
            infoDict['degree'] = degre
        else:
            infoDict['degree'] = "NONE"
        if debug:
            print "\n", pprint(infoDict), "\n"
            code.interact(local=locals())
        return infoDict['degree']


if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = Parse(verbose)
