import random

class Jeu007:
    def __init__(self):
        self.ammo_joueur = 0
        self.ammo_robot = 0
        self.tour = 1

        self.map_choix = {
            "Attaque": "T",
            "Bouclier": "P",
            "Recharge": "R"
        }

    def reset(self):
        self.ammo_joueur = 0
        self.ammo_robot = 0
        self.tour = 1

    def jouer(self, choix_gui):
        if choix_gui not in self.map_choix:
            return {"resultat": "Choix invalide"}

        choix_joueur = self.map_choix[choix_gui]

        # Choix du robot
        if self.tour == 1:
            choix_robot = "R"
        elif self.ammo_robot == 0:
            choix_robot = random.choice(["R", "P"])
        else:
            choix_robot = random.choice(["R", "T", "P"])

        # Recharge
        if choix_joueur == "R":
            self.ammo_joueur += 1
        if choix_robot == "R":
            self.ammo_robot += 1


        # Déterminer qui tire pendant ce tour
        joueur_tire = choix_joueur == "T" and self.ammo_joueur > 0
        robot_tire = choix_robot == "T" and self.ammo_robot > 0

        ammo_j_before = self.ammo_joueur
        ammo_r_before = self.ammo_robot

        # Si je tire et le robot recharge alors je gagne
        if joueur_tire and choix_robot == "R":
            
            resultat = {"resultat": "Victoire", "ammo_joueur": ammo_j_before, "ammo_robot": ammo_r_before, "choix_robot": choix_robot}
            self.reset()
            return resultat

        # Si le robot tire pendant que le joueur recharge alors je perd
        if robot_tire and choix_joueur == "R":
            resultat = {"resultat": "Défaite", "ammo_joueur": ammo_j_before, "ammo_robot": ammo_r_before, "choix_robot": choix_robot}
            self.reset()
            return resultat

        # Si il n'y a pas de fin de partie alors on applique la consommation des tirs
        if joueur_tire:
            self.ammo_joueur -= 1
        if robot_tire:
            self.ammo_robot -= 1

        self.tour += 1

        # Print pour suivre les échanges
        print(f"Tour {self.tour-1}: joueur={choix_joueur} (tire={joueur_tire}), robot={choix_robot} (tire={robot_tire}), ammo_j={self.ammo_joueur}, ammo_r={self.ammo_robot}", flush=True)

        return {
            "resultat": f"Tour {self.tour}",
            "ammo_joueur": self.ammo_joueur,
            "ammo_robot": self.ammo_robot,
            "choix_robot": choix_robot
        }
