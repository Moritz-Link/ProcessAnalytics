from django.shortcuts import render
from django.template import loader
import json
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import GeeksForm

from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_exempt
from .models import Graph, CaseData
from django.db.models import Count
#import torch_geometric
#from torch_geometric.nn import GCNConv
#import dill as pickle
import csv, io
import numpy as np
#import torch
#import torch.nn.functional as F
#from django.db.models import F
#from torch_geometric.data import Data
# Create your views here.
import os
#from .gnn_models.model_gnn import Test
#import torch
current_path = os.path.dirname(__file__) 
path = os.getcwd()
print(f'current_path: {current_path}')
print(f'path: {path}')



def mainPage_view(request):

    #template = loader.get_template('main.html')
    template = loader.get_template('mainPage.html')
    return HttpResponse(template.render())


def homePage_view(request):
    template = loader.get_template('homePage.html')
    return HttpResponse(template.render())


def dashboardPage_view(request):
    template = loader.get_template('dashboardPage.html')
    return HttpResponse(template.render())

@csrf_exempt
def graphPage_view(request):
    template = loader.get_template('graphPage.html')
    #data = Graph.objects.all()
    #data = Graph.objects.count()
    #data = Graph.objects.raw( "SELECT * FROM graphAPP1_graph")

    d = Graph.objects.values('case_id').annotate(total=Count('case_id'))
    context = { "process_data" :d   }
    return HttpResponse(template.render(context))

@csrf_exempt
def upload_data_view(request):
    g_d=Graph.objects.all() 
    g_d.delete()
    c_d=CaseData.objects.all() 
    c_d.delete()
    csv_file_activities = request.FILES["file"]
    csv_file_cases = request.FILES["file_case"]
    print(f'csv_file_activities {csv_file_activities}')
    print(f'csv_file_cases {csv_file_cases}')

    data_set_activities = csv_file_activities.read().decode('UTF-8')
    io_string_activities = io.StringIO(data_set_activities)
    for column in csv.reader(io_string_activities, delimiter=',', quotechar="|"):
        _, created = Graph.objects.update_or_create(
            case_id=column[0],
            activity=column[1],
            timestamp = column[2],
            )

    data_set_cases = csv_file_cases.read().decode('UTF-8')
    io_string_cases = io.StringIO(data_set_cases)
    for column in csv.reader(io_string_cases, delimiter=',', quotechar="|"):
         _, created = CaseData.objects.update_or_create(
             case_id=column[0],
             start_time=column[1],
             end_time = column[2],
             duration = column[3],
             repairIn5d = column[4],
             deviceType = column[5],
             servicePoint = column[6],
             deviceCat = column[7],
             warranty = column[8],
             )

    print("Here")
    data =  Graph.objects.values('case_id').annotate(total=Count('case_id'))
    print(data)
    template = loader.get_template('graphPage.html')
    context = {"form":GeeksForm(), "process_data" :data   }
    return HttpResponse(template.render(context))

@csrf_exempt
def load_graph_view(request):
    print("========")
    case_id = json.load(request)['c_id']
    print(f'case_id: {case_id}')
    case_data =  Graph.objects.filter(case_id=case_id).values()
    nodes = []
    edges = []
    id = 1
    x = 0
    y = 100

    for c_step in case_data:
        nodes.append({"id": id, "x":   x, "y": y, "activity" : c_step["activity"]})
        if id < len(case_data):
            edges.append({"from": id, "to": id+1})

        id += 1
        x += 100
        #y += 50

    final_graph = {"nodes":nodes,  "edges":edges}
    # data = { "nodes": [{"id": "Event_1", "x":   0, "y": 100},{"id": "Event_2",   "x":  50, "y": 150},],
    #         "edges": [{"from": "Event_1", "to": "Event_2"},]}
    #print(f'data: {data}')
    #return HttpResponse("Success!")
    return JsonResponse(data=final_graph)

@csrf_exempt
def load_graph_tables_view(request):
    case_id = json.load(request)['c_id']
    case_data =  Graph.objects.filter(case_id=case_id).values()
    activities_l = []
    activities_data = []
    for step in case_data:
        activities_l.append(step["activity"])
        activities_data.append([step["timestamp"]])#["Time1", "Test2"]
    

    gen_case_data =  CaseData.objects.filter(case_id=case_id).values().first()
    #print( CaseData.objects.values())
    #print(gen_case_data)
    general_columns = list(gen_case_data.keys())
    general_values = list(gen_case_data.values())
    #print(general_columns)
    #print(general_values)
    return_data = {"activities":activities_l, "activities_data": activities_data , "general_columns": general_columns, "general_values":general_values}
    return JsonResponse(data=return_data)
    


@csrf_exempt
def update_data_from_process_tables_view(request):


    data = json.load(request)['data']
    print("===")
    #print(data)
    #print()
    print(data["general_data"])
    print()
    print(data["activities"])
    print()
    # print(data["activities"])
    general_data = data["general_data"]
    db_case_id = general_data[1][0]
    case_id = general_data[1][1]
    print(db_case_id)
    print(case_id)
    #Graph, CaseData

    
    case_obj = CaseData.objects.get(id=db_case_id)
    for colid, general_data_col in enumerate(general_data[0]):
        if colid >1:
            print(f'general_data_col: {general_data_col}  general_data[1][colid]: {general_data[1][colid]}')
            setattr(case_obj, general_data_col, general_data[1][colid])
    case_obj.save()
    


    return JsonResponse(data={"test": ["test1"]})


# def build_prediction_graph(data):
#     print("===")
#     #print(data)
#     #print()
#     print(data["general_data"])
#     print()
#     print(data["activities"])
#     print()
#     general_data = data["general_data"]
#     sp_i = 7
#     dt_i = 6
#     target_column_id = 5
#     activity_index_dict_for_caseID = {'Creation': 0,'NoteHotline': 1, 'Letter': 2,'DeviceReceived': 3,'StockEntry': 4,'InDelivery': 5,'Completed': 6,'NoteWorkshop': 7}
#     activities_encoded = ac_encoder.transform(list(np.array(data["activities"]).reshape(-1,1))).toarray()
#     print(f'activities_encoded {activities_encoded}')

#     sp_encoded = sp_encoder.transform([[general_data[1][sp_i]]]).toarray()
#     print(f'sp_encoded {sp_encoded}')

#     dt_encoded = dt_encoder.transform([[general_data[1][dt_i]]]).toarray()
#     print(f'dt_encoded {dt_encoded}')

#     actions_as_int = np.array([activity_index_dict_for_caseID[action] for action in data["activities"]])
#     actions_edges = actions_as_int[1:]
#     actions_as_int = actions_as_int[:-1]

#     edge_index =  torch.from_numpy(np.vstack((actions_as_int, actions_edges)))
#     process_features = torch.from_numpy(np.hstack((sp_encoded , dt_encoded))).float() 
#     x =  torch.from_numpy(activities_encoded)

#     print(f'edge_index.shape {edge_index.shape}')
#     print(f'process_features.shape {process_features.shape}')
#     print(f'x.shape {x.shape}')



#     graph = Data()
#     graph.x = x.float()
#     graph.general_f = process_features
#     graph.edge_index = edge_index

#     print(f'graph: {graph}')




#     prediciton = gnn(graph)
#     print(f'prediciton: {prediciton}')




#     graph = None
#     return graph
@csrf_exempt
def preditct_data_from_process_tables_view(request):
    data = json.load(request)['data']
    #graph = build_prediction_graph(data)
    

    # edge_index
    # #graph.edge_index = edge_index
    # actions_as_int = np.array([activity_index_dict_for_caseID[action] for action in prefix_length_array[:,1]])
        

    # actions_edges = actions_as_int[1:]
    # actions_as_int = actions_as_int[:-1]
        
    # return np.vstack((actions_as_int, actions_edges))

    # event_columns = ["ACTIVITY"]
    # general_columns = ["SERVICEPOINT","DEVICETYPE"]
    # cat_columns = ["SERVICEPOINT", "DEVICETYPE", "ACTIVITY"]

    # process_features = self.get_general_feature(process_df)

    # return_array = None
    # n_f = 0
    # #print(list(process_df.columns))
    # for pd_col in list(process_df.columns):
    #     f_values = np.array([process_df[pd_col].to_numpy().reshape(-1,1)[0]])
    #     if pd_col in self.cat_columns:
    #         f_values = self.encoder_dict[pd_col].transform(f_values).toarray()
    #     if n_f > 0:
    #         return_array = np.hstack((return_array , f_values))
    #     else: return_array = f_values
    #     n_f += 1
    #y = torch.from_numpy(case_id_df[self.target_columns].to_numpy().astype(int))[0]
    # gnn 
    # sp_encoder 
    # dt_encoder 
    # ac_encoder 

    return JsonResponse(data={"graph_prediction": ["0.83"]})