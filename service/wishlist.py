class Wishlist:
    def __init__(self, name, customer):
        self.name = name
        self.customer = customer

    def get_name(self):
        return self.name

    def update_name(self, name):
        self.name = name

    def get_customer(self):
        return self.customer

    def update_customer(self, customer):
        self.customer = customer
