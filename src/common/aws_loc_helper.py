

class LocationHelper:
    def get_address(self, long, lat):
        raise NotImplementedError()


class AwsLocationHelper(LocationHelper):
    def __init__(self, client):
        self.client = client
    
    def get_address(self, long, lat):
        return self.client.search_place_index_for_position(IndexName='sony-place-index-here', Language='en', MaxResults=1, Position=[long, lat])

