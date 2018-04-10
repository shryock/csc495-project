class Struct():
    def __init__(self, **dic):
        self.__dict__.update(dic)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return '{' + ', '.join(['{}:{}'.format(key, self[key]) for key in sorted(self.__dict__.keys()) if key[0] != '_']) + '}'
