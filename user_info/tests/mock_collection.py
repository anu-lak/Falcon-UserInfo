# mock_collection.py
class MockCollection:
    def __init__(self):
        self.data = []

    def find_one(self, query, projection=None):
        for item in self.data:
            if item['email'] == query['email']:
                return item
        return None

    def insert_one(self, document):
        self.data.append(document)
