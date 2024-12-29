import pgzrun
import math
import random

# Game Settings
WIDTH = 1200
HEIGHT = 800
TITLE = "Platformer Game"

# Menu Options
menu_options = ["Start Game", "Exit"]
selected_option = 0

# Character and Enemy Classes
class Character:
    def __init__(self, image, pos, animations):
        self.actor = Actor(image, pos)
        self.actor.scale = 0.5
        self.animations = animations
        self.current_animation = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.x_speed = 0
        self.y_speed = 0
        self.is_jumping = False
        self.on_ground = True
        self.gravity = 1

    def draw(self):
        self.actor.draw()

    def update_animation(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= len(self.animations):
            self.animation_timer = 0
        self.actor.image = self.animations[int(self.animation_timer)]

    def update_movement(self):
        self.actor.x += self.x_speed
        if self.actor.left < 0:
            self.actor.left = 0
        elif self.actor.right > WIDTH:
            self.actor.right = WIDTH

        if not self.on_ground:
            self.y_speed += self.gravity
        self.actor.y += self.y_speed

        if self.actor.bottom > HEIGHT:
            self.actor.bottom = HEIGHT
            self.y_speed = 0
            self.on_ground = True
            self.is_jumping = False


class Enemy(Character):
    def __init__(self, image, pos, animations, patrol_area):
        super().__init__(image, pos, animations)
        self.actor.scale = 0.4  # Düşman boyutunu küçültme
        self.patrol_area = patrol_area
        self.direction = 1

    def update(self):
        self.update_animation()
        self.actor.x += self.direction
        if self.actor.x < self.patrol_area[0] or self.actor.x > self.patrol_area[1]:
            self.direction *= -1


# Main Menu
def draw_menu():
    screen.draw.text(TITLE, center=(WIDTH / 2, HEIGHT / 4), fontsize=60)
    for index, option in enumerate(menu_options):
        color = "red" if index == selected_option else "white"
        screen.draw.text(option, center=(WIDTH / 2, HEIGHT / 2 + index * 50), fontsize=40, color=color)



# Game Loop
def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        player.draw()
        for enemy in enemies:
            enemy.draw()


def update():
    global game_state
    if game_state == "playing":
        player.update_animation()
        player.update_movement()
        for enemy in enemies:
            enemy.update()


def on_key_down(key):
    global game_state, selected_option
    if game_state == "menu":
        if key == keys.RETURN:
            if selected_option == 0:
                game_state = "playing"
            elif selected_option == 1:
                exit()
        elif key == keys.UP:
            selected_option = (selected_option - 1) % len(menu_options)
        elif key == keys.DOWN:
            selected_option = (selected_option + 1) % len(menu_options)
    elif game_state == "playing":
        if key == keys.ESCAPE:
            game_state = "menu"
        if key == keys.LEFT:
          player.x_speed = -5
        if key == keys.RIGHT:
          player.x_speed = 5
        if key == keys.SPACE and player.on_ground:
          player.y_speed = -15
          player.is_jumping = True
          player.on_ground = False

def on_key_up(key):
    if game_state == "playing":
      if key == keys.LEFT or key == keys.RIGHT:
        player.x_speed = 0
        

# Game Initialization
def start_game():
    global player, enemies, game_state
    game_state = "menu"
    player = Character("player_idle", (WIDTH // 2, HEIGHT // 2), ["player_idle", "player_run1", "player_run2"])
    enemies = [
        Enemy("enemy_idle", (200, HEIGHT // 2), ["enemy_idle", "enemy_run1", "enemy_run2"], (150, 250)),
        Enemy("enemy_idle", (1000, HEIGHT // 2), ["enemy_idle", "enemy_run1", "enemy_run2"], (950, 1050)),
    ]

start_game()
pgzrun.go()