import pickle


class Example:
    def __init__(self):
        self.a_string='HELLO'
        self.a_number = 22
        self.a_list = ['string1, string2']
        self.a_dict = {"name": 'Nick'}
        self.a_tuple = (46, 89, 11)

    def hi(self, name):
        print(f'Hello {name}')


obj = Example()
print("original", obj.a_string, obj.a_number, obj.a_list, obj.a_dict, obj.a_tuple)
with open('data.dump', 'wb') as file:
    pickle.dump(obj, file)

obj.a_list[0] = True
obj.a_dict['name'] = 999
print("modified", obj.a_string, obj.a_number, obj.a_list, obj.a_dict, obj.a_tuple)

with open('data.dump', 'rb') as file:
    data = pickle.load(file)
    data = Example()
    print('restored', data)