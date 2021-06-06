import requests

class API:

    """
        Just a cute little wrapper around oslobysykkel.no gbsf endpoint:
        
            'https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json'
        
        You can read more about the gbsf specification here:
        
            'https://github.com/NABSA/gbfs/blob/master/gbfs.md'
        
        ----------------------------------------------------------
        
        Example usage:

            >>> from oslo_bysykkel import API

            >>> api = API(client_identifier='Tadej Pogačar')

            >>> api.available_feeds

            ['system_information', 'station_information', 'station_status']

            >>> api.get_available_docks()

            {'2306': 17,
             '2305': 15,
             '2304': 15,
             ... }

             >>> api.get_available_bikes()

            {'2306': 1,
             '2305': 0,
             '2304': 3,
             ... }     

             >>> api.get_summary()

             [{'name': 'Økern Portal',
              'station_id': '2306',
              'lat': 59.93097164065915,
              'lon': 10.801829756346933,
              'available_bikes': 1,
              'available_locks': 17},
             {'name': 'Hesselbergs Gate',
              'station_id': '2305',
              'lat': 59.92774803110845,
              'lon': 10.761265771390583,
              'available_bikes': 0,
              'available_locks': 14},
             {'name': 'Hedmarksgata',
              'station_id': '2304',
              'lat': 59.91178403655783,
              'lon': 10.783884345957915,
              'available_bikes': 3,
              'available_locks': 15},
              ... ]
        
    """
    
    def __init__(self, client_identifier=''):
        
        """
            client_identifier: string/value that describes the client app (you or your organization)
        """
        
        self.client_identifier = client_identifier
        self._headers = {'Client-Identifier': client_identifier}
        self._url = 'https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json'
        
        resp = requests.get(self._url, headers=self._headers)
        
        try:
            feed_list = resp.json()['data']['nb']['feeds']
        except KeyError as key_error:
            # SINCE OsloBysykkelAPI does not provide versioned endpoints we are stuck with this
            # Somebody should try to convince them to provide versioned endpoints even though
            # they are optional in the gbfs specification ...
            raise KeyError(f'Seems like OsloBysykkelAPI has changed: KeyError: {key_error}')
        
        # no need to check anything here ... since 'name' and 'url' fields are
        # strictly required by gbfs specification
        self._feeds = { feed['name']: feed['url'] for feed in feed_list }
        self.available_feeds = list(self._feeds.keys())
      
    def get_feed(self, feed_name):
        if feed_name not in self._feeds:
            raise KeyError(f'feed "{feed_name}" is not available')
        return requests.get(self._feeds[feed_name], headers=self._headers).json()
    
    def get_station_information(self):
        return self.get_feed('station_information')['data']['stations']

    def get_station_status(self):
        return self.get_feed('station_status')['data']['stations']
    
    def get_stations_capacity(self):
        return {
            station['station_id']: station['capacity']
            for station in self.get_station_information()
        }
    
    def get_available_docks(self):
        return {
            station['station_id']: station['num_docks_available']
            for station in self.get_station_status()
        }
    
    def get_available_bikes(self):
        return {
            station['station_id']: station['num_bikes_available']
            for station in self.get_station_status()
        }
    
    def get_summary(self):
        
        """
            Get a list of station summary. Including lock and bike availability.
        """
        
        available_bikes = self.get_available_bikes()
        available_locks = self.get_available_docks()
        station_info = self.get_station_information()
        
        summary = [
            {
                'name': station['name'],
                'station_id': station['station_id'],
                'lat': station['lat'],
                'lon': station['lon'],
                'available_bikes': available_bikes[station['station_id']],
                'available_locks': available_locks[station['station_id']]
                
            } for station in station_info
        ]
        
        return summary
    
    def get_summary_dict(self):
        
        """
            Get a dict of station summary. Including lock and bike availability.
        """
        
        summary_list = self.get_summary()
        
        summary_dict = {
            station['station_id'] : station
            for station in summary_list
        }
        
        return summary_dict