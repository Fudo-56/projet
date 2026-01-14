from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random

class Jeu007:
    def __init__(self):
        self.reset()
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

        if self.tour == 1:
            choix_robot = "R"
        elif self.ammo_robot == 0:
            choix_robot = random.choice(["R", "P"])
        else:
            choix_robot = random.choice(["R", "T", "P"])

        if choix_joueur == "R":
            self.ammo_joueur += 1
        if choix_robot == "R":
            self.ammo_robot += 1

        joueur_tire = choix_joueur == "T" and self.ammo_joueur > 0
        robot_tire = choix_robot == "T" and self.ammo_robot > 0

        ammo_j_before = self.ammo_joueur
        ammo_r_before = self.ammo_robot

        if joueur_tire and choix_robot == "R":
            self.reset()
            return {
                "resultat": "Victoire",
                "ammo_joueur": ammo_j_before,
                "ammo_robot": ammo_r_before,
                "choix_robot": choix_robot
            }

        if robot_tire and choix_joueur == "R":
            self.reset()
            return {
                "resultat": "Défaite",
                "ammo_joueur": ammo_j_before,
                "ammo_robot": ammo_r_before,
                "choix_robot": choix_robot
            }

        if joueur_tire:
            self.ammo_joueur -= 1
        if robot_tire:
            self.ammo_robot -= 1

        self.tour += 1

        return {
            "resultat": f"Tour {self.tour}",
            "ammo_joueur": self.ammo_joueur,
            "ammo_robot": self.ammo_robot,
            "choix_robot": choix_robot
        }


jeu = Jeu007()

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(length))
        choix = data.get("choix")

        resultat = jeu.jouer(choix)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(resultat).encode())


server = HTTPServer(("0.0.0.0", 6000), Handler)
print("🧠 Traitement listening on port 6000")
server.serve_forever()

