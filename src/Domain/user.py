class UserDomain:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email        
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,            
        }
