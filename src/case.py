class Case:
    """Représente une case classique"""

    def __init__(self, x, y, z):
        """Initie une case
        Parameters:
            x (int): abscisse de la case (0 <= x < 15)
            y (int): ordonnée de la case (0 <= y < 15)
            z (int): profondeur de la case (0 <= z < 3)
        """

        self.index = 0
        self.x = x
        self.y = y
        self.z = z
        self.impact = False
