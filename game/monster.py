import pygame
import random
import animation


# creer une classe qui va gérer la notion de monstre sur notre jeu
class Monster(animation.AnimateSprite):

    def __init__(self, game, name, size=(50, 50), loot_amount=10): 
        super().__init__(name, size=size)   # Appeler le constructeur d'AnimateSprite
        self.start_animations()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 0
        self.loot_amount = loot_amount  # Montant du loot
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 400  # Garder une position constante


    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1, 2)

    def set_loot_amount(self, amount):
        self.loot_amount = amount

    def damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            # Retirer le monstre
            self.game.all_monsters.remove(self)
            self.game.add_score(self.loot_amount)

            # Ne pas spawner de nouveaux monstres si l'événement météorite est actif ou si la barre est pleine
            if not self.game.is_comet_event_active and not self.game.comet_event.is_full_loaded():
                self.game.spawn_monster(self.game.get_random_monster())







    def update_animation(self):
        self.animate(loop=True)

    def update_health_bar(self, surface):

        # dessiner notre barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 10, self.rect.y - 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 10, self.rect.y - 20, self.health, 5])




    def forward(self):
        # Le déplacement se fait uniquement s'il n'y a pas de collision avec le joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity  # Déplacer vers la gauche

            # Si le monstre sort de l'écran, le supprimer
            if self.rect.right < 0:
                print(f"Le monstre {self.__class__.__name__} est sorti de l'écran et est supprimé.")
                self.game.all_monsters.remove(self)
        else:
            # Si collision avec le joueur, infliger des dégâts
            self.game.player.damage(self.attack)





# definir une classe pour l'Alanqa
class Alanqa(Monster):

    def __init__(self, game):
        super().__init__(game, "alanqa", (130, 130))
        self.set_speed(3)
        self.set_loot_amount(20)
        self.rect.y = 450  # Ajustement pour descendre Alanqa

# definir une classe pour le Baryonyx
class Baryonyx(Monster):

    def __init__(self, game):
        super().__init__(game, "baryonyx", (300, 300), 130)
        self.health = 120
        self.max_health = 120
        self.attack = 0.3
        self.set_speed(0.2)
        self.set_loot_amount(50)

# definir une classe pour Carnotaurus
class Carnotaurus(Monster):

    def __init__(self, game):
        super().__init__(game, "carnotaurus", (300, 300), 130)
        self.health = 100
        self.max_health = 100
        self.attack = 0.2
        self.set_speed(0.2)
        self.set_loot_amount(80)
        
# definir une classe pour Oviraptor
class Oviraptor(Monster):

    def __init__(self, game):
        super().__init__(game, "oviraptor", (400, 300), 130)
        self.health = 150
        self.max_health = 150
        self.attack = 0.3
        self.set_speed(0.2)
        self.set_loot_amount(150)
        
# definir une classe pour de Styracosaurus
class Styracosaurus(Monster):
    def __init__(self, game):
        super().__init__(game, "styracosaurus", (300, 300), 130)
        self.health = 200
        self.max_health = 200
        self.attack = 0.1
        self.set_speed(0.1)  # Rendre le déplacement plus lent
        self.set_loot_amount(200)




