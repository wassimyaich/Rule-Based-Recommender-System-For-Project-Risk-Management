from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from time import sleep
from rdflib import query
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import random
import numpy as np
import rdflib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#--------- Init ---------#
g = rdflib.Graph()
g.parse("C:/Users/maily/OneDrive/Bureau/final_ontology.owl")
base_uri = "http://www.example.org/"
#--------- Init ---------#

#--------- classes ---------#
class user_choice:
    def __init__(self, name, type, annotation):
        self.name = name
        self.type = type
        self.annotation = annotation
#--------- classes ---------#

#--------- Functions ---------#
def removeURI_arr(resultArr):
    final_result_array = []
    for res in resultArr:
        if("/" in res):
            for i in range(len(res)-1,0,-1):
                if res[i] =="/":
                    final_result_array.append(res[i+1:])
                    break
        else:
            final_result_array.append(res)

    return final_result_array

def removeURI_str(resultStr):
    final_result_string = ""
    if "/" in resultStr:
        for i in range(len(resultStr)-1,0,-1):
        
            if resultStr[i] =="/":
                final_result_string = final_result_string + resultStr[i+1:]
                break
        
    else :
        resultStr
    return final_result_string

def termToString(string):
    return removeURI_str(string[0])

def termsToStrArr(terms):
    strArr = []
    for term in terms:
        strArr.append(term[0])
    return removeURI_arr(strArr)

def removePostfix(name):
    postfixes = ['_p1','_p2','_p3','_p4','_p5','_p6']
    for p in postfixes:
        name = name.replace(p,"")
    return name

def getProcesses():
    raw_processes = g.query("SELECT ?process WHERE {?process a owl:Class .FILTER NOT EXISTS { ?process rdfs:subClassOf ?sup .FILTER(?sup != owl:Thing) }}")
    processes_arr = []
    for process in raw_processes:
        processes_arr.append(removeURI_str(process[0]))

    return processes_arr

def getIOT(processes_arr):  
    inputs_arr = []
    outputs_arr = []
    tt_arr = []

    for i in range(len(processes_arr)):
        process_name = processes_arr[i]
        input_index = "input_p"+str(i+1)
        output_index = "output_p"+str(i+1)
        tt_index = "tools_and_techniques_p"+str(i+1)

        current_inputs_arr = g.query("SELECT ?thing WHERE {?thing rdf:type <http://www.example.org/"+process_name+"/"+input_index+">.}")
        current_outputs_arr = g.query("SELECT ?thing WHERE {?thing rdf:type <http://www.example.org/"+process_name+"/"+output_index+">.}")
        current_tt_arr = g.query("SELECT ?thing WHERE {?thing rdf:type <http://www.example.org/"+process_name+"/"+tt_index+">.}")

        inputs_arr.append(termsToStrArr(current_inputs_arr))
        outputs_arr.append(termsToStrArr(current_outputs_arr))
        tt_arr.append(termsToStrArr(current_tt_arr))
    
    return inputs_arr, outputs_arr, tt_arr

def getURIs(term, processes_arr,inputs_arr,outputs_arr, tt_arr):
    uri = []
    arr = processes_arr
    for i in range(len(arr)):
        if term.lower().strip().replace(" ","_") in arr[i].lower():
            uri.append(base_uri+arr[i].lower())

    arr = inputs_arr
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if term.lower().strip().replace(" ","_") in arr[i][j].lower():
                uri.append(base_uri + processes_arr[i]+"/"+arr[i][j])
                

    arr = outputs_arr         
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if term.lower().strip().replace(" ","_") in arr[i][j].lower():
                uri.append(base_uri + processes_arr[i]+"/"+arr[i][j])
                

    arr = tt_arr         
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if term.lower().strip().replace(" ","_") in arr[i][j].lower():
                uri.append(base_uri + processes_arr[i]+"/"+arr[i][j])
                    
    return uri

def getAnnotation(uri):
    qres = g.query("SELECT ?annotation WHERE {<"+uri+"> rdfs:isDefinedBy ?annotation.}")
    for row in qres:
        return row.annotation
    return 'No description available'

def getType(term, processes, inputs_arr, outputs_arr, tt_arr):
    for process in processes:
        if term.lower() == process.lower():
            return 'Process'
    
    for i in range(len(inputs_arr)):
        for j in range(len(inputs_arr[i])):
            if term.lower() == inputs_arr[i][j].lower():
                return 'Input of '+processes[i]
    
    for i in range(len(outputs_arr)):
        for j in range(len(outputs_arr[i])):
            if term.lower() == outputs_arr[i][j].lower():
                return 'output of '+processes[i]

    for i in range(len(tt_arr)):
        for j in range(len(tt_arr[i])):
            if term.lower() == tt_arr[i][j].lower():
                return 'tool and technique of '+processes[i]

    return 'PROBLEM WITH GLOBAL VARIABLES'

def getProcessDetails(process, processes_arr, inputs_arr, outputs_arr, tt_arr):
    for i in range(len(processes_arr)):
        #print(processes_arr[i].lower().replace("_", " "))
        if processes_arr[i].lower().replace("_", " ") == process:
            return inputs_arr[i], outputs_arr[i], tt_arr[i], getAnnotation(base_uri+processes_arr[i])
    return "PROBLEM WITH GLOBAL VARIABLES"

def createWorld(processes_arr, inputs_arr, outputs_arr, tt_arr):
    world = []
    for i in range(len(processes_arr)):
        world.append(processes_arr[i])
        
    for i in range(len(inputs_arr)):
        for j in range(len(inputs_arr[i])):
            world.append(inputs_arr[i][j])

    for i in range(len(outputs_arr)):
        for j in range(len(outputs_arr[i])):
            world.append(outputs_arr[i][j])

    for i in range(len(tt_arr)):
        for j in range(len(tt_arr[i])):
            world.append(tt_arr[i][j])
    
    return world

def cosine_two_vectors(vec1, vec2):
    vec1 = vec1.reshape(1,-1)
    vec2 = vec2.reshape(1,-1)
    return cosine_similarity(vec1, vec2)[0][0]

def calculateCosine(str1, str2):
    vectorizer = CountVectorizer().fit_transform(list([str1.lower().replace("_"," "), str2.lower().replace("_"," ")]))
    vectors = vectorizer.toarray()
    cosine = cosine_two_vectors(vectors[0], vectors[1])
    return cosine

def getCosineArray(search_string, world):
    cosine_array = []
    for string in world:
        cosine_array.append(calculateCosine(search_string, string))
    return cosine_array

def getBestMatch(cosine_array, world):
    #print('best match : ' + str(world[np.argmax(cosine_array)]))
    return removePostfix(world[np.argmax(cosine_array)])
#--------- Functions ---------#

#--------- Variables ---------#
processes_arr = ['identify_risk', 'monitor_and_control_risks', 
                'perform_qualitative_risk_analysis', 'perform_quantitative_risk_analysis', 
                'Plan_Risk_Management', 'Plan_Risk_Responses']
inputs_arr , outputs_arr , tt_arr = getIOT(processes_arr)
world = createWorld(processes_arr, inputs_arr, outputs_arr, tt_arr)
#--------- Variables ---------#

#--------- Controllers ---------#
def send_request_view(request):
    search_string = request.GET.get('search_string')
    choice = request.GET.get('choice')
    choices = []
    if search_string is not None:
        print('1')
        uris = getURIs(search_string, processes_arr, inputs_arr, outputs_arr, tt_arr)
        cosine_arr = getCosineArray(search_string, world)
        best_match = getBestMatch(cosine_arr, world)

        for uri in uris:
            print(uri)
            annotation = getAnnotation(uri)
            type = getType(removeURI_str(uri), processes_arr, inputs_arr, outputs_arr,tt_arr)
            name =removePostfix(removeURI_str(uri)).replace("_"," ")
            c = user_choice(name, type, annotation)
            choices.append(c)

        if len(choices) == 0:
            print('11')
            suggestion_string = 'Did you mean: '
        else:
            print('12')
            suggestion_string = 'Best match: '
        context = { 
            'choices' : choices,
            'process' : "Process",
            'other' : "other",
            'search_string' : search_string,
            'best_match':best_match.replace("_"," "),
            'suggestion_string': suggestion_string,
        }
        html_string = render_to_string('ResultatRecherche.html', context=context)
        return HttpResponse(html_string)
            
            


    if choice is not None:
        print('2')
            #collect_informations
            #redirect_to_view_uri      
        context = { 
            
            }
        html_string = render_to_string('get_response.html', context=context)
        return HttpResponse()
    print('3')
    context = {  }
    html_string = render_to_string('send_request.html', context=context)
    return render(request, 'send_request.html')


def processView(request):
    process = request.GET.get('process') 
    process_inputs,process_outputs, process_tt, process_annotation = getProcessDetails(process, processes_arr, inputs_arr, outputs_arr, tt_arr)
    for i in range(len(process_inputs)):
        process_inputs[i] = removePostfix(process_inputs[i])
    for i in range(len(process_outputs)):
        process_outputs[i] = removePostfix(process_outputs[i])
    for i in range(len(process_tt)):
        process_tt[i] = removePostfix(process_tt[i])
    context = {
        'process' : process, 
       'inputs' : process_inputs,
       'outputs' : process_outputs,
       'tt' : process_tt,
       'annotation' : process_annotation
    }
    html_string = render_to_string('ProcessDetails.html', context = context)
    return HttpResponse(html_string)

def home_view(request):
    return HttpResponse()

#--------- Controllers ---------#























































































# def send_request_view(request):
#     term = request.GET.get('term')
#     if term is not None:
#         query = getQuery(term)
#         result = g.query(query)
#         first_result_indivs = []
#         for row in result:
#             first_result_indivs.append(row.thing)
#         final_result_indivs = removeURI_arr(first_result_indivs)
#         #-----------------------------------------------------------#
#         query = getQuery2(term)
#         result = g.query(query)
#         first_result_annotations = []
#         for row in result:
#             first_result_annotations.append(row.thing)
#         final_result_annotations = removeURI_arr(first_result_annotations)
#         print(final_result_annotations)        
#         context = { 
#             'indivs':final_result_indivs,
#             'annotations':final_result_annotations
#             }
#         html_string = render_to_string('get_response.html', context=context)
#         return HttpResponse(html_string)

#     context = {  }
#     html_string = render_to_string('send_request.html', context=context)
#     return render(request, 'send_request.html')