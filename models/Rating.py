class Rating:
    def __init__(self, id_rater, id_rated, rating_text, rating_number, average_stars=None):
        self.id_rater = id_rater
        self.id_rated = id_rated
        self.rating_text = rating_text
        self.rating_number = rating_number
        self._rater = None
        self.average_stars = average_stars

    @classmethod
    def init_rating_with_json(cls, json):
        return cls(json["id_rater"], json["id_rated"], json["rating_text"], json["rating_number"])

    def setRater(self, rater):
        self._rater = rater

    def convert_to_json(self):
        json = {
            "id_rated": self.id_rated,
            "rating_text": self.rating_text,
            "rating_number": self.rating_number,
        }
        if self._rater is not None:
            json['rater'] = self._rater.convert_to_json(False)
        else:
            json['id_rater'] = self.id_rater
        return json
