
class Differ:
    def __init__(self, title, content):
        self.title = title
        self.content = content

class TextComparator:
    
    def __init__(self, standard_text='', version_text=''):
        self.version_text = version_text
        self.standard_text = standard_text


    def text_differences(self):
        standard_words = {word for word in self.standard_text.split()}
        version_words = {word for word in self.version_text.split()}
        diff_words = set.symmetric_difference(version_words, standard_words)
        return ' '.join(diff_words)

    def text_coincidences(self):
        standard_words = {word for word in self.standard_text.split()}
        version_words = {word for word in self.version_text.split()}
        diff_words = set.intersection(version_words, standard_words)
        return ' '.join(diff_words)