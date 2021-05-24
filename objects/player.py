import objects.colors as colors


class Player():
    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.score = 0

    def get_fill(self):
        return colors.REDBLOCK if self.color == colors.RED \
            else colors.BLUEBLOCK

    def get_score(self):
        return self.score

    def give_point(self):
        self.score += 1

    def get_color(self):
        return self.color
