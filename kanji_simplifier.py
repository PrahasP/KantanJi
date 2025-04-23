import pykakasi

class KanjiSimplifier:
    @staticmethod
    def generate_furigana(text):
        kks = pykakasi.kakasi()
        result = kks.convert(text)
        furigana = ''.join(item['hira'] for item in result)
        return furigana
