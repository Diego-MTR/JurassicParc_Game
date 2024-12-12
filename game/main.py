import pygame
import math
from game import Game
pygame.init()

# definir une clock
clock = pygame.time.Clock()
FPS = 60



# generer la fenetre de notre jeu
pygame.display.set_caption("Jurassic Park")
screen = pygame.display.set_mode((1080, 720))

# importer de charger l'arrière plan de notre jeu
background = pygame.image.load('Assets/bg.jpg')
# Redimensionne l'image à la taille de l'écran
background = pygame.transform.scale(background, screen.get_size())  

# importer charger notre bannière
banner = pygame.image.load('Assets/banner.png')
banner = pygame.transform.scale(banner, (525, 350))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)
banner_rect.y = math.ceil(screen.get_height() / 8)

# import charger notre bouton pour lancer la partie
play_button = pygame.image.load('Assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)




# charger notre jeu
game = Game()

running = True

# boucle tant que cette condition est vrai
# boucle tant que cette condition est vraie
while running:

    # appliquer l'arrière-plan de notre jeu
    screen.blit(background, (0, 0))

    # vérifier si le jeu est en cours
    if game.is_playing:
        # déclencher les instructions de la partie
        game.update(screen)

    # vérifier si le jeu n'a pas commencé (écran d'accueil)
    elif not game.is_playing:
        # Ajouter mon écran de bienvenue
        screen.blit(banner, banner_rect)
        screen.blit(play_button, play_button_rect)

    # mettre à jour l'écran
    pygame.display.flip()

    # gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu")

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            # Détecter si la flèche du haut est pressée pour sauter
            if event.key == pygame.K_UP and game.is_playing:
                game.player.jump()

            # Espace pour tirer un projectile
            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.launch_projectile()
                else:
                    game.start()
                    game.sound_manager.play('click')

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # vérification pour savoir si la souris est en collision avec le bouton jouer
            if play_button_rect.collidepoint(event.pos) and not game.is_playing:
                game.start()
                game.sound_manager.play('click')

            # vérification pour le bouton retry
            elif retry_button_rect.collidepoint(event.pos) and game.player.health <= 0:
                game.player.health = game.player.max_health  # Réinitialiser la santé
                game.start()  # Redémarrer le jeu
                game.sound_manager.play('click')

    # fixer le nombre de fps sur ma clock
    clock.tick(FPS)

