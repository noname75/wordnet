from flask import render_template, Blueprint, request, jsonify
from blog import app
from blog.views.permission_config import admin
from blog.models.db_config import *
from datetime import datetime
import networkx as nx
import re
import time
import math


graphManagement_page = Blueprint('graphManagement', __name__, template_folder='templates')


@app.route('/graphManagement', methods=['GET', 'POST'])
@admin.require(http_exception=403)
def graphManagement():
    graphList = Graph().getGraphList()
    for graph in graphList:
        graph.newPostsCount = Post().getCountOfPosts_byStartTime(graph.creationTime)
        graph.newResponsesCount = ResponseInPack().getAcceptedResponseCount_byStartTime(graph.creationTime)

    return render_template('graphManagement.html', graphList=graphList)


@app.route("/changeGraphActivationStatus", methods=['POST'])
@admin.require(http_exception=403)
def changeGraphActivationStatus():
    graphId = int(request.json['graphId'])
    Graph(id=graphId).getGraph().changeActivationStatus()

    return ''


@app.route("/deleteGraph", methods=['POST'])
@admin.require(http_exception=403)
def deleteGraph():
    graphId = int(request.json['graphId'])
    EdgeInGraph().removeEdges_byGraphId(graphId)
    NodeInGraph().removeNodes_byGraphId(graphId)
    Graph().removeGraph(graphId)

    return ''


@app.route('/getDataCount', methods=['POST'])
@admin.require(http_exception=403)
def getDataCount():
    if request.json['startTime']:
        startTime = datetime.strptime(request.json['startTime'] + ' 00:01:01', "%m/%d/%Y %H:%M:%S")
        finishTime = datetime.strptime(request.json['finishTime'] + ' 23:59:59', "%m/%d/%Y %H:%M:%S")
    else:
        startTime = None
        finishTime = None

    if not startTime:
        postCount = Post().getCountOfPosts()
        responseCount = ResponseInPack().getAcceptedResponseCount()
    else:
        postCount = Post().getCountOfPosts_byStartTimeAndFinishTime(startTime, finishTime)
        responseCount = ResponseInPack().getAcceptedResponseCount_byStartTimeAndFinishTime(startTime, finishTime)

    return jsonify({'postCount': postCount, 'responseCount': responseCount})


@app.route('/makeGraph', methods=['POST'])
@admin.require(http_exception=403)
def makeGraph():
    if request.json['startTime']:
        startTime = datetime.strptime(request.json['startTime'] + ' 00:01:01', "%m/%d/%Y %H:%M:%S")
        finishTime = datetime.strptime(request.json['finishTime'] + ' 23:59:59', "%m/%d/%Y %H:%M:%S")
    else:
        startTime = None
        finishTime = None

    graph = Graph(
        startTime=startTime,
        finishTime=finishTime,
        source=request.json['source'],
        isDirected=request.json['isDirected'],
        minUserOnNode=int(request.json['minUserOnNode']),
        minUserOnEdge=int(request.json['minUserOnEdge']),
        minEdgeWeight=float(request.json['minEdgeWeight']),
        name=request.json['name'],
        moreInfo=request.json['moreInfo'],
        creationTime=time.strftime('%Y-%m-%d %H:%M:%S'),
        isActive=False)

    if graph.source == 'tags':
        posts = getTagsData(graph)
        g = constructTagGraph(posts, graph)
    elif graph.source == 'responses':
        responses = getResponsesData(graph)
        g = constructResponsesGraph(responses, graph)

    if request.json['saveGraph']:
        graph = graph.addGraph()
        saveGraphNodeAndEdges(g, graph)
    return jsonify({'nodeCount': g.number_of_nodes(), 'edgeCount': g.number_of_edges()})


@app.route('/updateGraph', methods=['POST'])
@admin.require(http_exception=403)
def updateGraph():
    graphId = request.json['graphId']
    graph = Graph(id=graphId).getGraph()
    graph.updateCreationTime(time.strftime('%Y-%m-%d %H:%M:%S'))

    EdgeInGraph().removeEdges_byGraphId(graphId)
    NodeInGraph().removeNodes_byGraphId(graphId)

    if graph.source == 'tags':
        posts = getTagsData(graph)
        g = constructTagGraph(posts, graph)
    elif graph.source == 'responses':
        responses = getResponsesData(graph)
        g = constructResponsesGraph(responses, graph)

    saveGraphNodeAndEdges(g, graph)
    return ''



def getResponsesData(graph):
    if not graph.startTime:
        responses = ResponseInPack().getAcceptedResponses()
    else:
        responses = ResponseInPack().getAcceptedResponses_byStartTimeAndFinishTime(graph.startTime, graph.finishTime)
    return responses


def constructResponsesGraph(responses, graph):
    # Construct Graph
    if graph.isDirected:
        g = nx.DiGraph()
    else:
        g = nx.Graph()
    for response in responses:
        source = response.phrase1_id
        target = response.phrase2_id
        number = response.number
        uid = Pack(pack_id=response.pack_id).getPack().user_id
        if not g.has_node(source):
            g.add_node(source, distUserList=[])
        if not g.has_node(target):
            g.add_node(target, distUserList=[])
        if not g.node[source]['distUserList'].__contains__(uid):
            g.node[source]['distUserList'].append(uid)
        if not g.node[target]['distUserList'].__contains__(uid):
            g.node[target]['distUserList'].append(uid)
        if not g.has_edge(source, target):
            g.add_edge(source, target, distUserList=[], weight=0)
        else:
            if g.edge[source][target]['distUserList'].__contains__(uid):
                continue
        g.edge[source][target]['distUserList'].append(uid)
        g.edge[source][target]['weight'] = g.edge[source][target]['weight'] + 1 / (math.log(number + 1) + 1)

    info = {}
    info['#nodes'] = g.number_of_nodes()
    info['#edges'] = g.number_of_edges()
    printInfo(info)


    # Pruning Nodes
    for node in g.nodes():
        if g.node[node]['distUserList'].__len__() < graph.minUserOnNode:
            g.remove_node(node)

    #Normalization
    if graph.isDirected:
        for source, target in g.edges():
            source_distUseList_len = g.node[source]['distUserList'].__len__()
            source_target_weight = g.edge[source][target]['weight']
            g.edge[source][target]['weight'] = source_target_weight / source_distUseList_len
    else:
        for source, target in g.edges():
            source_distUseList_len = g.node[source]['distUserList'].__len__()
            target_distUseList_len = g.node[target]['distUserList'].__len__()
            edge_distUserList_len = g.edge[source][target]['distUserList'].__len__()
            g.edge[source][target]['weight'] = g.edge[source][target]['weight'] / (
                source_distUseList_len + target_distUseList_len - edge_distUserList_len)


    #Pruning Edges
    for s, t in g.edges():
        if g.edge[s][t]['distUserList'].__len__() < graph.minUserOnEdge or g.edge[s][t]['weight'] < graph.minEdgeWeight:
            g.remove_edge(s, t)

    return g


def getTagsData(graph):
    if not graph.startTime:
        posts = Post().getPosts()
    else:
        posts = Post().getPosts_byStartTimeAndFinishTime(graph.startTime, graph.finishTime)
    return posts


def constructTagGraph(posts, graph):
    # Read tagGroups
    tag_pattern = re.compile("(#\\w+)")
    tagCount = 0
    tagGroups = []

    i = 0
    for post in posts:
        uid = post.uid
        tagList = tag_pattern.findall(post.caption)
        if tagList.__len__() == 0:
            continue
        tagGroup = set()
        for tagContent in tagList:
            # prepare tag
            tag = tagContent[1:]
            if any(c.isupper() for c in tag):
                tag = tag.lower()
            tag = tag.replace('ـ', '')
            tag = tag.replace('ة', 'ت')
            tag = tag.replace('ك', 'ک')
            tag = tag.replace('ي', 'ی')
            tag = tag.replace('ﻻ', 'لا')
            #end prepare
            tagGroup.add(tag)
        tagGroups.append((tuple(tagGroup), uid,))
        tagCount = tagCount + tagGroup.__len__()
        i = i + 1
        if i % 1000 == 0:
            print(i, ' / ', posts.__len__())

    info = {}
    info["#Posts"] = posts.__len__()
    if tagCount != 0:
        info['Average#Tags'] = tagCount / tagGroups.__len__()
    info['#TagGroups'] = tagGroups.__len__()
    printInfo(info)

    #Construct Graph
    g = nx.Graph()

    # Add Nodes
    for tagGroup, uid in tagGroups:
        for source in tagGroup:
            if not g.has_node(source):
                g.add_node(source, distUserList=[])
            if not g.node[source]['distUserList'].__contains__(uid):
                g.node[source]['distUserList'].append(uid)


    #Pruning Nodes
    for node in g.nodes():
        if g.node[node]['distUserList'].__len__() < graph.minUserOnNode:
            g.remove_node(node)



    # Add Edges
    for tagGroup, uid in tagGroups:
        for i, source in enumerate(tagGroup[:-1]):
            for distance, target in enumerate(tagGroup[i + 1:]):
                if g.has_node(source) and g.has_node(target):
                    if not g.has_edge(source, target):
                        g.add_edge(source, target, weight=0, occur=0, distUserList=[])
                    else:
                        if g.edge[source][target]['distUserList'].__contains__(uid):
                            continue
                    g.edge[source][target]['weight'] = g.edge[source][target]['weight'] + 1 / (
                        math.log(distance + 1) + 1)
                    g.edge[source][target]['distUserList'].append(uid)

    # Pruning Edges according to minUserOnEdge
    for s, t in g.edges():
        if g.edge[s][t]['distUserList'].__len__() < graph.minUserOnEdge:
            g.remove_edge(s, t)

    #Normalization
    if graph.isDirected:
        di = nx.DiGraph()
        for node in g.nodes():
            di.add_node(node, distUserList=g.node[node]['distUserList'])
        for source, target in g.edges():
            source_distUseList_len = g.node[source]['distUserList'].__len__()
            target_distUseList_len = g.node[target]['distUserList'].__len__()
            source_target_weight = g.edge[source][target]['weight']
            di.add_edge(source, target, weight=source_target_weight / source_distUseList_len,
                        distUserList=g.edge[source][target]['distUserList'])
            di.add_edge(target, source, weight=source_target_weight / target_distUseList_len,
                        distUserList=g.edge[source][target]['distUserList'])
        g = di
    else:
        for source, target in g.edges():
            source_distUseList_len = g.node[source]['distUserList'].__len__()
            target_distUseList_len = g.node[target]['distUserList'].__len__()
            edge_distUserList_len = g.edge[source][target]['distUserList'].__len__()
            g.edge[source][target]['weight'] = g.edge[source][target]['weight'] / (
            source_distUseList_len + target_distUseList_len - edge_distUserList_len)


    # Pruning Edges according to minEdgeWeight
    for s, t in g.edges():
        if g.edge[s][t]['weight'] < graph.minEdgeWeight:
            g.remove_edge(s, t)

    info = {}
    info['#nodes'] = g.number_of_nodes()
    info['#edges'] = g.number_of_edges()
    printInfo(info)

    return g


def printInfo(info):
    print("_______________________INFO______________________\n")
    for i in info.keys():
        print("%30s: %d" % (i, info[i]))
    print("_________________________________________________\n")


def saveGraphNodeAndEdges(g, graph):

    for node in g.nodes():
        weight = g.node[node]['distUserList'].__len__()
        if graph.source == 'tags':
            phrase_id = Phrase(content=node).addIfNotExists().id
        else:
            phrase_id = node
        NodeInGraph(weight=weight, phrase_id=phrase_id, graph_id=graph.id).addNodeInGraph()

    for source, target in g.edges():
        weight = g.edge[source][target]['weight']
        if graph.source == 'tags':
            phrase1_id = Phrase(content=source).getPhrase_byContent().id
            phrase2_id = Phrase(content=target).getPhrase_byContent().id
        else:
            phrase1_id = source
            phrase2_id = target
        EdgeInGraph(weight=weight, phrase1_id=phrase1_id, phrase2_id=phrase2_id, graph_id=graph.id).addEdgeInGraph()
