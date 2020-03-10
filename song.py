class Song:
    def __init__(self, artist="", title="", lyrics="", url=""):
        self.artist = artist
        self.title = title
        self.lyrics = lyrics
        self.filename = url.replace('/', '.')
        self.url = url

    def __repr__(self):
        return f'{self.artist}-{self.title}:\n{self.lyrics}'

    def __eq__(self, other):
        if isinstance(other, Song):
            return hash(self) == hash(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


if __name__ == '__main__':
    s1 = Song('my', 'chemical', 'romance', 'http://hello.me')
    s2 = Song('my', 'chemical', 'romance', 'http://hello.me')
    assert s1 == s2

    s1 = Song('your', 'chemicali', 'rumance', 'http://hello.me')
    s2 = Song('my', 'chemicale', 'romance', 'https://bye.you')
    assert s1 != s2
