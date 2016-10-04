import bottle
from bottle import run, route, template, request, error

import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)


db = client.serverdb
si = db.serverinfo

plinks = client.plinks

maps = client.maps





@route('/')
def index():
    return template('index', name='phil')
	
	
@route('/login')
def login():
    return template('login', name='phil')
	
	

@route('/maps')
def login():
	data = client.maps.fixedmaps.find()
	return template('maps', dict(name = data))
	
@route('/boottest')
def index():
    return template('start')

@route('/list_databases')
def list_databases():
    data = client.database_names()
    return template('list_databases', dict(name = data))

@route('/list_databases/<datab>')
def list_databases_collect(datab):
    data = client[datab]
    te = data.collection_names()
    return template('list_collections', dict(name = te), n2 = datab)


@route('/list_databases/<datab>/<collect>')
def list_databases_collect(datab,collect):
    data = client[datab]
    te = data[collect]
    t4 = te.find()
    return template('list_data', dict(name = t4), n2 = datab, n3 = collect)





@route('/links')
def links():
    data = plinks.links.find()
    return template('links', dict(x = data))
	
def insert_maps():
    data = maps.fixedmaps.find()
    return template('insert_maps', dict(x = data))

@route('/bootstrap')
def bootstrap():
    data = plinks.links.find()
    return template('bootstrap', dict(x = data))

@route('/links/add', method='POST')
def links_add():
    name = bottle.request.forms.get("name")
    url = bottle.request.forms.get("url")
    desc = bottle.request.forms.get("desc")
    tags = bottle.request.forms.get("tags")
    newData = {'name':name,'url':url, 'desc':desc,'tags':tags}
    plinks.links.insert(newData)
    bottle.redirect('/list_databases/plinks/links')
	
def maps_add():
	company = bottle.request.forms.get("company")
	phone = bottle.request.forms.get("phone")
	address = bottle.request.forms.get("address")
	latitude = bottle.request.forms.get("latitude")
	longitude = bottle.request.forms.get("longitude")
	newData = {'company':company,'phone':phone, 'address':address,'latitude':latitude,'longitude':longitude}
	maps.fixedmaps.insert(newData)
	bottle.redirect('/maps')

@route('/register')
def register():
    return '<h1>on register</h1>'

@route('/user/<name>')
def user(name):
    return '<h1>You are ' + name + '</h1>'

@route('/posted', method='POST')
def posted():
    return '<h1>Posted</h1>'


@route('/jsondata')
def jsondata():
    return {"name" : "jsondata", "myList" : [1,2,3,4,5]}

@route('/querytest')
def querytest():
    param1 = request.query.param1
    param2 = request.query.param2
    return 'Param1 is ' + param1 + ' Param 2 is' +param2

@error(404)
def error404(error):
    return '<h2>404 Page does not exist</h2>'

@route('addData')
def addData():
    myList = si.find()
    return bottle.template('index', dict(myNames = mynames_list))

@route('/enterdata', method='POST')
def enterdata():
    name = bottle.request.forms.get("name")
    maxplayers = bottle.request.forms.get("maxplayers")
    currentplayers  = bottle.request.forms.get("currentplayers")
    ipaddress = bottle.request.forms.get("ipaddress")
    maps = bottle.request.forms.get("map")
    gametype = bottle.request.forms.get("gametype")
    serverdata.insert(name,maxplayers,currentplayers,ipaddress,maps,gametype)



run(host='0.0.0.0', port=80, debug=True, reloader=True)