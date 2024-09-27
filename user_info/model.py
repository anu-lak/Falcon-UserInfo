class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    @classmethod
    def from_dict(cls, data):
        return cls(data.get('name'),data.get('email'),data.get('age'))

    def to_dict(self):
        return {'name': self.name, 'email': self.email, 'age': self.age}