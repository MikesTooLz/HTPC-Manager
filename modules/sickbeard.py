import os, cherrypy, htpc
from urllib import quote
from urllib2 import urlopen
from json import loads

class Sickbeard:
    def __init__(self):
        htpc.modules.append({
            'name': 'Sickbeard',
            'id': 'sickbeard',
            'test': '/sickbeard/ping',
            'fields': [
                {'type':'bool', 'label':'Enable', 'name':'sickbeard_enable'},
                {'type':'text', 'label':'Menu name', 'name':'sickbeard_name'},
                {'type':'text', 'label':'IP / Host *', 'name':'sickbeard_host'},
                {'type':'text', 'label':'Port *', 'name':'sickbeard_port'},
                {'type':'text', 'label':'API key', 'name':'sickbeard_apikey'}
        ]})

    @cherrypy.expose()
    def index(self):
        return htpc.lookup.get_template('sickbeard.html').render()

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def ping(self, sickbeard_host, sickbeard_port, sickbeard_apikey, **kwargs):
        try:
            url = 'http://'+sickbeard_host+':'+sickbeard_port+'/api/'+sickbeard_apikey+'/?cmd=';
            response = loads(urlopen(url+'sb.ping', timeout=10).read())
            if response.get('result') == "success":
                return response
        except:
            return

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def GetShowList(self):
        return self.fetch('shows&sort=name')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def GetNextAired(self):
        return self.fetch('future')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def GetPoster(self, tvdbid):
        return self.fetch('show.getposter&tvdbid='+tvdbid)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def GetHistory(self, limit=''):
        return self.fetch('history&limit='+limit)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def GetLogs(self):
        return self.fetch('logs&min_level=info')

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def AddShow(self, tvdbid):
        return self.fetch('show.addnew&tvdbid='+tvdbid)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def GetShow(self, tvdbid):
        return self.fetch('show&tvdbid='+tvdbid)

    @cherrypy.expose()
    def SearchShow(self, query):
        try:
            url = 'http://www.thetvdb.com/api/GetSeries.php?seriesname='+quote(query)
            return loads(urlopen(url, timeout=10).read())
        except:
            return

    def fetch(self, cmd):
        try:
            settings = htpc.settings.Settings()
            host = settings.get('sickbeard_host', '')
            port = str(settings.get('sickbeard_port', ''))
            apikey = settings.get('sickbeard_apikey', '')
            url = 'http://' + host + ':' + str(port) + '/api/' + apikey + '/?cmd='+cmd;
            return loads(urlopen(url, timeout=10).read())
        except:
            return

htpc.root.sickbeard = Sickbeard()