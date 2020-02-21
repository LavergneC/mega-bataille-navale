from case import Case


class CaseAttaque(Case):
    """Instance d'une case spécialisée pour la carte
       de type attaque héritant de Case"""

    def __init__(self, x, y, z):
        """Initie une case

        Parameters:
            x (int): abscisse de la case (0 <= x < 15)
            y (int): ordonnée de la case (0 <= y < 15)
            z (int): profondeur de la case (0 <= z < 3)

         """

        super().__init__(x, y, z)
        self.presence_bateau = False
