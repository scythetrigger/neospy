# Standard Libraries
import base64
import requests
from bs4 import BeautifulSoup

# Third-Party Libraries
import amplParser.amplParser as amplParser

# Information
__author__ = 'Nicholas Parham'
__copyright__ = ''
__credits__ = ['Nicholas Parham']
__license__ = 'Apache Software License'
__version__ = '0.0.1'
__maintainer__ = 'Nicholas Parham'
__email__ = 'nick-99@att.net'
__status__ = 'Dev'

# NEOS AMPL API (https://neos-server.org/neos/xml-rpc.html)

def neosRequest(method, parameters = []):
    # makes XML requests to the NEOS server
    params = ''
    if parameters != []:
        for param in parameters:
            try:
                int(param)
                params += '<param><value><int>{param}</int></value></param>'.format(param = param)
            except:
                params += '<param><value><string>{param}</string></value></param>'.format(param = param)
    
    url = 'https://neos-server.org:3333'
    headers = {'Content-Type': 'application/xml'}
    body = '<?xml version="1.0"?><methodCall><methodName>{method}</methodName><params>{params}</params></methodCall>'.format(method = method, params = params)
    response = requests.post(url, data = body, headers = headers)
    content = response.text
    
    soup = BeautifulSoup(content, 'xml')
    if method == 'submitJob':
        results = [x.text for x in soup.find_all('int')] + [x.text for x in soup.find_all('string')]
    elif method == 'getFinalResults' or method == 'getOutputFile':
        results = [base64.b64decode(x.text).decode('utf-8') for x in soup.find_all('base64')]
    else:
        results = [x.text for x in soup.find_all('string')]
    return results



def neosHelp():
    # implements NEOS help function
    # returns NEOS help message
    results = neosRequest(method = 'help')
    print(results[0])



def neosWelcome():
    # implements NEOS welcome function
    # returns NEOS welcome message
    results = neosRequest(method = 'welcome')
    print(results[0])
    
    

def neosVersion():
    # implements NEOS version function
    # returns NEOS version number
    results = neosRequest(method = 'version')
    print(results[0])



def neosPing():
    # implements NEOS ping function
    # returns NEOS status
    results = neosRequest(method = 'ping')
    print(results[0])
    
    

def neosPrintQueue():
    # implements NEOS printQueue function
    # returns NEOS list of current jobs
    results = neosRequest(method = 'printQueue')
    print(results[0])
    
    

def neosListAllSolvers():
    # implements NEOS listAllSolvers function
    # returns NEOS list of solvers by category hooked to AMPL
    solvers = {}
    
    results = neosRequest(method = 'listAllSolvers')  
    for result in results:
        category, solver, language = result.split(':')
        
        if language not in solvers.keys():
            solvers[language] = {}
            
        if category in solvers[language].keys():
            solvers[language][category].append(solver)
        else:
            solvers[language][category] = [solver]
    
    solvers = solvers['AMPL']
    
    print('AMPL Solvers:')
    print()
    print('Category    Solver')
    print('------------------------')
    
    for category in solvers.keys():
        for solver in solvers[category]:
            line = str(category).ljust(12) + str(solver).ljust(12)
            print(line)
    
    

def neosListAllCategories():
    # implements NEOS listCategories function
    # returns NEOS list of categories supported by AMPL
    results = neosRequest(method = 'listCategories')
    
    print('AMPL Categories:')
    print()
    print('Category'.ljust(60) + 'Abbreviation'.ljust(10))
    print('-' * 72)
    
    for result in results:
        initials = [x[0] for x in result.split(' ')]
        if initials == ['k']:
            initials = ['kestrel']
        print(result.ljust(60) + ''.join(initials).lower())



def neosListSolversInCategory(category):
    # implements NEOS listSolversInCategory
    # returns NEOS list of solvers hooked to AMPL in category
    solvers = {}
    
    results = neosRequest(method = 'listAllSolvers')  
    for result in results:
        cat, solver, language = result.split(':')
        
        if language not in solvers.keys():
            solvers[language] = {}
            
        if cat in solvers[language].keys():
            solvers[language][cat].append(solver)
        else:
            solvers[language][cat] = [solver]
    
    solvers = solvers['AMPL']
    
    print('AMPL Solvers:')
    print()
    print('Category    Solver')
    print('------------------------')
    
    for solver in solvers[category]:
        line = str(category).ljust(12) + str(solver).ljust(12)
        print(line)



def neosSubmitJob(modFile, datFile, runFile, solver, category, email, comments = '', report = True):
    # implements NEOS submitJob function
    # returns NEOS job number and password
    modFile = modFile
    datFile = datFile
    runFile = runFile
    if report:
        runFile = amplParser.addReport(runFile)
    
    
    results = neosRequest(method = 'getSolverTemplate', parameters = [category, solver, 'AMPL'])[0]
    xmlTemplate = BeautifulSoup(results, 'xml')
    xmlTemplate.find('model').string.replace_with('<![CDATA[{modFile}]]>'.format(modFile = modFile))
    xmlTemplate.find('data').string.replace_with('<![CDATA[{datFile}]]>'.format(datFile = datFile))
    xmlTemplate.find('commands').string.replace_with('<![CDATA[{runFile}]]>'.format(runFile = runFile))
    xmlTemplate.find('comments').string.replace_with('<![CDATA[{comments}]]>'.format(comments = comments))
    emailTag = xmlTemplate.new_tag('email')
    emailTag.string = '<![CDATA[{email}]]>'.format(email = email)
    xmlTemplate.document.append(emailTag)
    xmlJob = str(xmlTemplate.document).replace('>', '&gt;').replace('<', '&lt;')
    
    results = neosRequest(method = 'submitJob', parameters = [xmlJob])
    print('Job Number:', results[0])
    print('Password:', results[1])
    
    return results[0], results[1]



def neosGetJobStatus(jobNumber, password):
    # implements NEOS getJobStatus function
    # returns NEOS job status
    results = neosRequest(method = 'getJobStatus', parameters = [jobNumber, password])
    print('Job Status:', results[0])
    
    return results[0]



def neosGetCompletionCode(jobNumber, password):
    # implements NEOS getCompletionCode function
    # returns NEOS completion code
    results = neosRequest(method = 'getCompletionCode', parameters = [jobNumber, password])
    print('Completion Code:', results[0])
    
    return results[0]



def neosGetJobInfo(jobNumber, password):
    # implements NEOS getJobInfo function
    # returns NEOS job info
    results = neosRequest(method = 'getJobInfo', parameters = [jobNumber, password])
    print('Job Info:', results[0])
    
    return results[0]
    
    

def neosKillJob(jobNumber, password, message = ''):
    # implements NEOS killJob function
    results = neosRequest(method = 'killJob', parameters = [jobNumber, password, message])
    print(results[0])
    
    return results[0]
    

    
def neosGetFinalResults(jobNumber, password):
    # implements NEOS getFinalResults function
    # returns NEOS job final results
    results = neosRequest(method = 'getFinalResults', parameters = [jobNumber, password])
    print(results[0])
    
    return results[0]
    
    

def neosEmailJobResults(jobNumber, password):
    # implements NEOS emailJobResults function
    results = neosRequest(method = 'emailJobResults', parameters = [jobNumber, password])
    print(results[0])
    
    return results[0]
    
    
    
def neosGetOutputFile(jobNumber, password, filename):
    # implements NEOS getOutputFile function
    # returns NEOS output file content
    results = neosRequest(method = 'getOutputFile', parameters = [jobNumber, password, filename])
    print(results[0])
    
    return results[0]



if __name__ == '__main__':
    neosWelcome()
    pass