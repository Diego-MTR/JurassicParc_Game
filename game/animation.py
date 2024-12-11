import pygame

# definir une classe qui va s'occuper des animations
class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name, size=(200, 200), animation_speed=10):  # Animation par défaut plus lente
        super().__init__()
        self.size = size
        self.image = pygame.image.load(f'Assets/{sprite_name}.png')
        self.image = pygame.transform.scale(self.image, size)
        self.current_image = 0
        self.images = animations.get(sprite_name, [])
        self.animation = False
        self.animation_speed = animation_speed  # Contrôle de la fluidité de l'animation
        self.animation_counter = 0


    def start_animations(self):
        self.animation = True

    def animate(self, loop=False):
        if self.animation:
            # Vérifier si la liste d'images est vide
            if not self.images:
                self.animation = False
                return

            # Passer à l'image suivante
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.current_image += 1
                self.animation_counter = 0
                # Remettre à zéro si on atteint la fin
                if self.current_image >= len(self.images):
                    self.current_image = 0
                    if not loop:
                        self.animation = False

                # Mettre à jour l'image
                self.image = self.images[self.current_image]
                self.image = pygame.transform.scale(self.image, self.size)


# Dictionnaire contenant le nombre d'images pour chaque dinosaure
dinosaur_images_count = {
    'alanqa': 4,
    'baryonyx': 12,
    'carnotaurus': 11,
    'oviraptor': 9,
    'styracosaurus': 12
}

def load_animation_images(sprite_name, image_count):
    images = []
    path = f"Assets/Png/{sprite_name}/{sprite_name}"
    for num in range(1, image_count + 1):
        image_path = f"{path}{num}.png"
        try:
            images.append(pygame.image.load(image_path))
        except pygame.error:
            print(f"Erreur : Impossible de charger {image_path}")
    return images



# Charger les animations pour tous les dinosaures
animations = {
    name: load_animation_images(name, count)
    for name, count in dinosaur_images_count.items()
}
