import pygame
import os

# Verifier si les fichiers d'images existent avant de charger

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Fichier manquant : {file_path}")
        return False
    return True

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name, size=(200, 200), animation_speed=10):
        super().__init__()
        self.size = size
        self.sprite_name = sprite_name
        self.image = None
        self.current_image = 0
        self.images = animations.get(sprite_name, [])
        self.animation = False
        self.animation_speed = animation_speed
        self.animation_counter = 0
        self.flipped = False  # Ajout de l'attribut flipped

        # Charger la première image si possible
        first_image_path = f'Assets/Png/{sprite_name}/{sprite_name}1.png'
        if check_file_exists(first_image_path):
            self.image = pygame.image.load(first_image_path)
            self.image = pygame.transform.scale(self.image, size)
        else:
            print(f"Erreur : Première image non chargée pour {sprite_name}")

    def start_animations(self):
        self.animation = True

    def flip_images(self):
        """Retourner toutes les images de l'animation."""
        self.images = [pygame.transform.flip(img, True, False) for img in self.images]
        self.flipped = not self.flipped

    def animate(self, loop=True):
        if self.animation:
            if not self.images:
                self.animation = False
                return

            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.current_image += 1
                self.animation_counter = 0

                if self.current_image >= len(self.images):
                    self.current_image = 0 if loop else len(self.images) - 1

                # Redimensionner l'image uniquement pour l'affichage
                current_image = self.images[self.current_image]
                self.image = pygame.transform.scale(current_image, self.size)
                print(f"Frame de l'animation de {self.sprite_name} : {self.current_image}")  # Debug

# Charger et vérifier les fichiers d'animation

def load_animation_images(sprite_name, image_count):
    images = []
    path = f"Assets/Png/{sprite_name}/{sprite_name}"
    for num in range(1, image_count + 1):
        image_path = f"{path}{num}.png"
        if check_file_exists(image_path):
            try:
                images.append(pygame.image.load(image_path))
                print(f"Image chargée : {image_path}")
            except pygame.error:
                print(f"Erreur : Impossible de charger {image_path}")
        else:
            print(f"Fichier d'image manquant : {image_path}")
    return images

# Dictionnaire contenant le nombre d'images pour chaque dinosaure
dinosaur_images_count = {
    'alanqa': 4,
    'baryonyx': 12,
    'carnotaurus': 11,
    'oviraptor': 9,
    'styracosaurus': 12
}

# Charger les animations pour tous les dinosaures
animations = {
    name: load_animation_images(name, count)
    for name, count in dinosaur_images_count.items()
}

# Charger les images d'animation du joueur
def load_player_animation_images():
    images = []
    for num in range(1, 8):  # Charger les 7 images
        image_path = f"Assets/Png/player/player{num}.png"
        if check_file_exists(image_path):
            try:
                images.append(pygame.image.load(image_path))
                print(f"Image chargée pour le joueur : {image_path}")
            except pygame.error:
                print(f"Erreur : Impossible de charger {image_path}")
    return images

# Ajouter cette animation uniquement pour le joueur
animations['player'] = load_player_animation_images()

# Fin du script de débogage
