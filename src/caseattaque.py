from case import Case


class CaseAttaque(Case):
    """Enfant de la classe Case"""

    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.presence_bateau = False
