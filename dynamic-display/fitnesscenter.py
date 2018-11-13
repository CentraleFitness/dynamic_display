import sys

class fitnesscenter(object):
    def __init__(self):
        self._name = ""
        self._city = ""

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def city(self):
        return self._city
    @city.setter
    def city(self, value):
        self._city = value




