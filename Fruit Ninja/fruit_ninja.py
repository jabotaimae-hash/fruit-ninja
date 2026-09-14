import pygame
import pygame.camera
import random
import math
import statistics
import os

try:
    import mediapipe as mp
    import numpy as np
except ImportError:
    mp = None
    np = None

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Fruit Ninja")

clock = pygame.time.Clock()

# -----------------------------
# Colors
# -----------------------------
WHITE = (255, 255, 255)
RED = (220, 50, 50)
YELLOW = (240, 220, 50)
ORANGE = (255, 140, 30)
PURPLE = (170, 70, 220)

# -----------------------------
# Fonts
# -----------------------------
font = pygame.font.SysFont("Arial", 32, bold=True)
big_font = pygame.font.SysFont("Arial", 60, bold=True)

# -----------------------------
# Fruit class
# -----------------------------
class Fruit:

    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT + 50

        self.radius = 35
        self.fruit_type = random.choice([
            "pineapple",
            "tomato",
            "melon",
            "cucumber",
            "pumpkin"
        ])

        self.color = {
            "pineapple": (218, 170, 45),
            "tomato": (220, 55, 45),
            "melon": (95, 185, 85),
            "cucumber": (70, 155, 75),
            "pumpkin": (235, 125, 35)
        }[self.fruit_type]

        # Random horizontal speed
        self.vx = random.uniform(-3, 3)

        # Upward speed
        self.vy = random.uniform(-14, -10)

        # Gravity
        self.gravity = 0.35

        self.alive = True

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += self.gravity

    def draw(self):

        fruit_x = int(self.x)
        fruit_y = int(self.y)

        pygame.draw.ellipse(
            screen,
            (25, 35, 35),
            (fruit_x - 30, fruit_y + 25, 60, 12)
        )

        if self.fruit_type == "pineapple":

            pygame.draw.polygon(
                screen,
                self.color,
                [
                    (fruit_x - 23, fruit_y - 20),
                    (fruit_x + 23, fruit_y - 20),
                    (fruit_x + 17, fruit_y + 27),
                    (fruit_x - 17, fruit_y + 27)
                ]
            )

            for leaf_offset in [-18, -9, 0, 9, 18]:
                pygame.draw.line(
                    screen,
                    (45, 130, 55),
                    (fruit_x, fruit_y - 18),
                    (fruit_x + leaf_offset, fruit_y - 42),
                    5
                )

            for row in range(3):
                pygame.draw.line(
                    screen,
                    (155, 105, 25),
                    (fruit_x - 17, fruit_y - 8 + row * 11),
                    (fruit_x + 17, fruit_y - 8 + row * 11),
                    2
                )

            for diamond_y in range(-8, 25, 12):
                for diamond_x in range(-14, 15, 14):
                    pygame.draw.circle(
                        screen,
                        (245, 205, 75),
                        (fruit_x + diamond_x, fruit_y + diamond_y),
                        2
                    )

            pygame.draw.circle(screen, (255, 225, 125),
                               (fruit_x - 10, fruit_y - 10), 5)

        elif self.fruit_type == "tomato":

            pygame.draw.circle(screen, self.color, (fruit_x, fruit_y), 31)
            pygame.draw.polygon(
                screen,
                (45, 135, 55),
                [
                    (fruit_x, fruit_y - 8),
                    (fruit_x - 15, fruit_y - 20),
                    (fruit_x - 4, fruit_y - 4),
                    (fruit_x + 2, fruit_y - 22),
                    (fruit_x + 9, fruit_y - 4),
                    (fruit_x + 22, fruit_y - 14),
                    (fruit_x + 10, fruit_y + 2)
                ]
            )
            pygame.draw.arc(
                screen,
                (245, 105, 85),
                (fruit_x - 23, fruit_y - 23, 43, 43),
                math.pi * 0.9,
                math.pi * 1.8,
                4
            )
            pygame.draw.circle(screen, (125, 75, 35),
                               (fruit_x, fruit_y - 10), 4)

        elif self.fruit_type == "melon":

            pygame.draw.ellipse(
                screen,
                self.color,
                (fruit_x - 37, fruit_y - 27, 74, 54)
            )

            for stripe_x in [-20, -10, 0, 10, 20]:
                pygame.draw.line(
                    screen,
                    (45, 125, 65),
                    (fruit_x + stripe_x, fruit_y - 23),
                    (fruit_x + stripe_x, fruit_y + 23),
                    2
                )

            pygame.draw.arc(
                screen,
                (175, 225, 135),
                (fruit_x - 30, fruit_y - 22, 42, 40),
                math.pi * 0.7,
                math.pi * 1.5,
                5
            )
            pygame.draw.line(
                screen,
                (75, 120, 55),
                (fruit_x, fruit_y - 25),
                (fruit_x + 2, fruit_y - 34),
                4
            )

        elif self.fruit_type == "cucumber":

            pygame.draw.ellipse(
                screen,
                self.color,
                (fruit_x - 18, fruit_y - 38, 36, 76)
            )
            pygame.draw.line(
                screen,
                (35, 105, 50),
                (fruit_x - 7, fruit_y - 27),
                (fruit_x - 7, fruit_y + 27),
                3
            )
            for spot_x, spot_y in [(-9, -15), (7, -4), (-6, 10), (8, 18)]:
                pygame.draw.circle(
                    screen,
                    (120, 195, 95),
                    (fruit_x + spot_x, fruit_y + spot_y),
                    2
                )
            pygame.draw.line(
                screen,
                (35, 105, 50),
                (fruit_x + 7, fruit_y - 27),
                (fruit_x + 7, fruit_y + 27),
                3
            )

        else:

            pygame.draw.ellipse(
                screen,
                self.color,
                (fruit_x - 35, fruit_y - 30, 70, 60)
            )

            for groove_x in [-18, -9, 0, 9, 18]:
                pygame.draw.arc(
                    screen,
                    (175, 75, 25),
                    (fruit_x - 35 + groove_x, fruit_y - 29,
                     70 - abs(groove_x), 58),
                    math.pi / 2,
                    math.pi * 1.5,
                    2
                )

            pygame.draw.rect(
                screen,
                (75, 95, 35),
                (fruit_x - 5, fruit_y - 35, 10, 9)
            )

            pygame.draw.arc(
                screen,
                (255, 175, 75),
                (fruit_x - 28, fruit_y - 23, 48, 43),
                math.pi * 0.8,
                math.pi * 1.6,
                5
            )

        pygame.draw.circle(
            screen,
            (255, 225, 180),
            (fruit_x - 10, fruit_y - 12),
            5
        )


class SliceEffect:

    def __init__(self, x, y, color):

        self.x = x
        self.y = y
        self.color = color
        self.age = 0
        self.duration = 24
        self.particles = []

        for _ in range(8):

            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)

            self.particles.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "size": random.randint(3, 7)
            })

    def update(self):

        self.age += 1

        for particle in self.particles:

            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.18

        return self.age < self.duration

    def draw(self):

        progress = self.age / self.duration
        half_size = max(8, int(28 - progress * 15))
        separation = int(progress * 65)
        left_x = int(self.x - separation)
        right_x = int(self.x + separation)
        y = int(self.y + progress * 25)

        pygame.draw.circle(screen, self.color, (left_x, y), half_size)
        pygame.draw.circle(screen, self.color, (right_x, y), half_size)

        pygame.draw.line(
            screen,
            WHITE,
            (left_x, y - half_size),
            (right_x, y + half_size),
            4
        )

        ring_radius = int(15 + progress * 45)
        ring_color = (255, max(80, int(240 - progress * 150)), 80)
        pygame.draw.circle(
            screen,
            ring_color,
            (int(self.x), int(self.y)),
            ring_radius,
            3
        )

        for particle in self.particles:

            particle_size = max(1, int(particle["size"] * (1 - progress)))

            pygame.draw.circle(
                screen,
                WHITE,
                (int(particle["x"]), int(particle["y"])),
                particle_size
            )


# -----------------------------
# Game variables
# -----------------------------
fruits = []

slice_effects = []

score = 0
player_scores = [0, 0]
player_count = 1
current_player = 0
score_history = []
round_time = 60.0

spawn_timer = 0

mouse_position = None
mouse_blade_segments = []
mouse_trail = []
mouse_motion = False

camera_capture = None
camera_surface = None
camera_error = ""
camera_frame_counter = 0
hand_landmarker = None
hand_timestamp = 0
hand_positions = [None, None]
previous_hand_positions = [None, None]
hand_blade_segments = []
hand_trails = [[], []]

HAND_MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "hand_landmarker.task"
)


# -----------------------------
# Check if blade hits fruit
# -----------------------------
def check_collision(fruit, mouse_x, mouse_y):

    distance_x = fruit.x - mouse_x
    distance_y = fruit.y - mouse_y
    hit_radius = fruit.radius + 15

    return distance_x ** 2 + distance_y ** 2 < hit_radius ** 2


def check_blade_collision(fruit, start_point, end_point):

    start_x, start_y = start_point
    end_x, end_y = end_point
    segment_x = end_x - start_x
    segment_y = end_y - start_y
    segment_length_squared = segment_x ** 2 + segment_y ** 2

    if segment_length_squared == 0:
        return check_collision(fruit, end_x, end_y)

    position = (
        ((fruit.x - start_x) * segment_x + (fruit.y - start_y) * segment_y)
        / segment_length_squared
    )
    position = max(0, min(1, position))
    closest_x = start_x + position * segment_x
    closest_y = start_y + position * segment_y

    return check_collision(fruit, closest_x, closest_y)


def reset_mouse_sensor():

    global mouse_position
    global mouse_blade_segments
    global mouse_trail
    global mouse_motion

    mouse_position = None
    mouse_blade_segments = []
    mouse_trail = []
    mouse_motion = False


def reset_hand_sensor():

    global hand_positions
    global previous_hand_positions
    global hand_blade_segments
    global hand_trails

    hand_positions = [None, None]
    previous_hand_positions = [None, None]
    hand_blade_segments = []
    hand_trails = [[], []]


def update_mouse_sensor():

    global mouse_position
    global mouse_blade_segments
    global mouse_trail
    global mouse_motion

    is_pressed = pygame.mouse.get_pressed()[0]
    if game_state != "playing" or not is_pressed:
        if mouse_position is not None:
            reset_mouse_sensor()
        return

    current_position = pygame.mouse.get_pos()
    if mouse_position is None:
        mouse_position = current_position
        mouse_trail = [current_position]
        mouse_blade_segments = []
        mouse_motion = False
        return

    if current_position == mouse_position:
        return

    mouse_blade_segments.append((mouse_position, current_position))
    mouse_blade_segments = mouse_blade_segments[-20:]
    mouse_trail.append(current_position)
    mouse_trail = mouse_trail[-20:]
    mouse_position = current_position
    mouse_motion = True


def start_camera():

    global camera_capture
    global camera_error
    global hand_landmarker
    global hand_timestamp

    try:
        pygame.camera.init()
        devices = pygame.camera.list_cameras()
        if not devices:
            camera_error = "No camera found"
            return

        camera_capture = pygame.camera.Camera(devices[0], (640, 480), "RGB")
        camera_capture.start()
        hand_landmarker = None
        hand_timestamp = 0
        camera_error = ""

        if mp is None or np is None:
            camera_error = "Hand tracking unavailable: install requirements.txt"
        elif not os.path.exists(HAND_MODEL_PATH):
            camera_error = "Hand tracking unavailable: hand_landmarker.task missing"
        else:
            base_options = mp.tasks.BaseOptions(
                model_asset_path=HAND_MODEL_PATH
            )
            hand_options = mp.tasks.vision.HandLandmarkerOptions(
                base_options=base_options,
                running_mode=mp.tasks.vision.RunningMode.VIDEO,
                num_hands=2,
                min_hand_detection_confidence=0.6,
                min_hand_presence_confidence=0.6,
                min_tracking_confidence=0.6
            )
            hand_landmarker = mp.tasks.vision.HandLandmarker.create_from_options(
                hand_options
            )
    except Exception as error:
        camera_capture = None
        camera_error = f"Camera unavailable: {error}"
        pygame.camera.quit()


def stop_camera():

    global camera_capture
    global camera_surface
    global camera_frame_counter
    global hand_landmarker

    if camera_capture is not None:
        camera_capture.stop()
    if hand_landmarker is not None:
        hand_landmarker.close()
    pygame.camera.quit()
    camera_capture = None
    camera_surface = None
    camera_frame_counter = 0
    hand_landmarker = None
    reset_hand_sensor()


def update_camera():

    global camera_surface
    global camera_error
    global camera_frame_counter
    global hand_timestamp
    global hand_positions
    global previous_hand_positions
    global hand_blade_segments
    global hand_trails

    camera_frame_counter += 1
    if camera_frame_counter % 3 != 0:
        return

    try:
        if camera_capture is None or not camera_capture.query_image():
            return
        camera_frame = pygame.transform.flip(
            camera_capture.get_image(),
            True,
            False
        )
        camera_surface = pygame.transform.scale(camera_frame, (WIDTH, HEIGHT))

        if hand_landmarker is not None:
            # MediaPipe reads packed RGB rows; transpose alone leaves strided pixels.
            frame_array = np.ascontiguousarray(
                np.transpose(pygame.surfarray.array3d(camera_frame), (1, 0, 2))
            )
            hand_timestamp += 33
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=frame_array
            )
            result = hand_landmarker.detect_for_video(
                mp_image,
                hand_timestamp
            )
            detected_hands = [None, None]
            if result.hand_landmarks:
                for hand_index, landmarks in enumerate(result.hand_landmarks):
                    slot = hand_index
                    if hand_index < len(result.handedness):
                        label = result.handedness[hand_index][0].category_name.lower()
                        if label == "left":
                            slot = 0
                        elif label == "right":
                            slot = 1
                    if slot < 2:
                        detected_hands[slot] = landmarks[8]

            hand_blade_segments = []
            for hand_index, fingertip in enumerate(detected_hands):
                if fingertip is None:
                    previous_hand_positions[hand_index] = None
                    hand_positions[hand_index] = None
                    hand_trails[hand_index] = []
                    continue

                current_hand_position = (
                    max(0, min(WIDTH, int(fingertip.x * WIDTH))),
                    max(0, min(HEIGHT, int(fingertip.y * HEIGHT)))
                )
                if previous_hand_positions[hand_index] is not None:
                    hand_blade_segments.append((
                        previous_hand_positions[hand_index],
                        current_hand_position
                    ))
                previous_hand_positions[hand_index] = current_hand_position
                hand_positions[hand_index] = current_hand_position
                hand_trails[hand_index].append(current_hand_position)
                hand_trails[hand_index] = hand_trails[hand_index][-20:]
            hand_blade_segments = hand_blade_segments[-40:]
    except Exception as error:
        camera_error = f"Camera error: {error}"
        stop_camera()


def reset_game():

    global fruits
    global slice_effects
    global score
    global player_scores
    global current_player
    global spawn_timer
    global round_time
    global camera_error

    reset_mouse_sensor()
    stop_camera()
    camera_error = ""
    fruits = []

    slice_effects = []

    score = 0
    player_scores = [0, 0]
    current_player = 0

    spawn_timer = 0
    round_time = 30.0 if player_count == 2 else 60.0



def finish_game():

    global game_state

    if game_state == "playing":
        reset_mouse_sensor()
        stop_camera()
        if player_count == 2:
            score_history.extend(player_scores)
        else:
            score_history.append(score)
        game_state = "finished"


def finish_player_turn():

    global current_player
    global round_time
    global fruits
    global slice_effects

    if current_player == 0:
        current_player = 1
        round_time = 30.0
        fruits = []
        slice_effects = []
        reset_mouse_sensor()
    else:
        finish_game()


def draw_menu(title, options):

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))

    title_text = big_font.render(title, True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 155))
    screen.blit(title_text, title_rect)

    buttons = []
    mouse_position = pygame.mouse.get_pos()
    button_height = 45 if len(options) > 4 else 55
    button_gap = button_height + 15

    for index, (label, action) in enumerate(options):
        button_rect = pygame.Rect(
            WIDTH // 2 - 150,
            245 + index * button_gap,
            300,
            button_height
        )
        is_hovered = button_rect.collidepoint(mouse_position)
        button_color = ORANGE if is_hovered else PURPLE

        pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
        button_text = font.render(label, True, WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
        buttons.append((button_rect, action))

    return buttons


def draw_background(time_ms):

    top_color = (7, 22, 45)
    bottom_color = (18, 92, 92)

    for y in range(HEIGHT):

        blend = y / HEIGHT

        color = (
            int(top_color[0] + (bottom_color[0] - top_color[0]) * blend),
            int(top_color[1] + (bottom_color[1] - top_color[1]) * blend),
            int(top_color[2] + (bottom_color[2] - top_color[2]) * blend)
        )

        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    glow = int(12 + math.sin(time_ms * 0.002) * 5)
    pygame.draw.circle(screen, (20, 115 + glow, 125 + glow), (WIDTH - 120, 120), 105)

    for grid_y in range(250, HEIGHT, 35):
        pygame.draw.line(screen, (22, 118, 116), (0, grid_y), (WIDTH, grid_y), 1)
    for grid_x in range(0, WIDTH, 50):
        pygame.draw.line(screen, (18, 103, 108), (grid_x, 220), (grid_x, HEIGHT), 1)

    pygame.draw.line(screen, (255, 165, 65), (0, HEIGHT - 7), (WIDTH, HEIGHT - 7), 5)


# -----------------------------
# Main game loop
# -----------------------------
running = True
game_state = "mode_select"

while running:

    # -------------------------
    # Events
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "mode_select" and event.key in (pygame.K_1, pygame.K_RETURN):
                player_count = 1
                reset_game()
                game_state = "playing"

            elif game_state == "mode_select" and event.key == pygame.K_2:
                player_count = 2
                reset_game()
                game_state = "playing"

            elif game_state == "playing" and event.key in (pygame.K_ESCAPE, pygame.K_p):
                reset_mouse_sensor()
                reset_hand_sensor()
                game_state = "paused"

            elif game_state == "paused" and event.key in (pygame.K_ESCAPE, pygame.K_p):
                game_state = "playing"

            elif game_state == "paused" and event.key == pygame.K_r:
                reset_game()
                game_state = "playing"

            elif game_state == "playing" and event.key == pygame.K_f:
                finish_game()

            elif game_state in ("mode_select", "paused", "finished") and event.key == pygame.K_q:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            button_x = WIDTH // 2 - 150
            button_y = 245

            if game_state == "mode_select":
                button_x = WIDTH // 2 - 150
                if pygame.Rect(button_x, 245, 300, 55).collidepoint(event.pos):
                    player_count = 1
                    reset_game()
                    game_state = "playing"
                elif pygame.Rect(button_x, 315, 300, 55).collidepoint(event.pos):
                    player_count = 2
                    reset_game()
                    game_state = "playing"
                elif pygame.Rect(button_x, 385, 300, 55).collidepoint(event.pos):
                    running = False

            elif game_state == "paused":
                if pygame.Rect(button_x, button_y, 300, 55).collidepoint(event.pos):
                    game_state = "playing"
                elif pygame.Rect(button_x, button_y + 80, 300, 55).collidepoint(event.pos):
                    reset_game()
                    game_state = "playing"
                elif pygame.Rect(button_x, button_y + 160, 300, 55).collidepoint(event.pos):
                    running = False

            elif game_state == "finished":
                if pygame.Rect(button_x, button_y, 300, 55).collidepoint(event.pos):
                    reset_game()
                    game_state = "playing"
                elif pygame.Rect(button_x, button_y + 80, 300, 55).collidepoint(event.pos):
                    running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "playing":
                if pygame.Rect(760, 15, 100, 40).collidepoint(event.pos):
                    game_state = "paused"
                elif pygame.Rect(870, 15, 110, 40).collidepoint(event.pos):
                    finish_game()

    if game_state == "playing" and camera_capture is None and not camera_error:
        start_camera()

    if game_state in ("playing", "paused") and camera_capture is not None:
        update_camera()

    update_mouse_sensor()

    slicing = mouse_motion or bool(hand_blade_segments)
    blade_segments = mouse_blade_segments + hand_blade_segments

    if game_state == "playing":
        if mouse_position is None:
            mouse_trail.clear()

    # -------------------------
    # Background
    # -------------------------
    if camera_surface is not None and game_state in ("playing", "paused"):
        screen.blit(camera_surface, (0, 0))
        camera_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        camera_overlay.fill((0, 20, 35, 55))
        screen.blit(camera_overlay, (0, 0))
    else:
        draw_background(pygame.time.get_ticks())

    if game_state == "playing":

        round_time -= clock.get_time() / 1000

        if round_time <= 0:
            round_time = 0
            if player_count == 2:
                finish_player_turn()
            else:
                finish_game()

        spawn_timer += 1

        if spawn_timer > 24 and len(fruits) < 12:
            wave_size = random.choices(
                [1, 2, 3],
                weights=[3, 5, 2],
                k=1
            )[0]
            wave_size = min(wave_size, 12 - len(fruits))
            fruits.extend(Fruit() for _ in range(wave_size))
            spawn_timer = 0

    # -------------------------
    # Update fruits
    # -------------------------
    if game_state == "playing":
        for fruit in fruits:

            fruit.update()

            if slicing and any(
                check_blade_collision(fruit, blade_start, blade_end)
                for blade_start, blade_end in blade_segments
            ):

                    fruit.alive = False

                    if len(slice_effects) < 40:
                        slice_effects.append(
                            SliceEffect(fruit.x, fruit.y, fruit.color)
                        )

                    if player_count == 2:
                        player_scores[current_player] += 10
                    else:
                        score += 10

            if fruit.y > HEIGHT + 100:

                fruit.alive = False

        mouse_blade_segments = []
        mouse_motion = False
        hand_blade_segments = []

    # Remove dead fruits
    fruits = [
        fruit for fruit in fruits
        if fruit.alive
    ]

    slice_effects = [
        effect for effect in slice_effects
        if effect.update()
    ]

    # -------------------------
    # Draw fruits
    # -------------------------
    for fruit in fruits:
        fruit.draw()

    for effect in slice_effects:
        effect.draw()

    # -------------------------
    if game_state == "playing" and len(mouse_trail) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, mouse_trail, 12)
        pygame.draw.lines(screen, (255, 220, 100), False, mouse_trail, 3)
        mouse_tip = mouse_trail[-1]
        pygame.draw.circle(screen, (255, 220, 100), mouse_tip, 14)
        pygame.draw.circle(screen, WHITE, mouse_tip, 5)

    if game_state == "playing":
        hand_colors = [(80, 255, 180), (255, 150, 80)]
        for hand_index, hand_trail in enumerate(hand_trails):
            if len(hand_trail) > 1:
                pygame.draw.lines(
                    screen,
                    hand_colors[hand_index],
                    False,
                    hand_trail,
                    7
                )
                pygame.draw.lines(screen, WHITE, False, hand_trail, 2)

            hand_position = hand_positions[hand_index]
            if hand_position is not None:
                pygame.draw.circle(
                    screen,
                    hand_colors[hand_index],
                    hand_position,
                    16,
                    3
                )
                pygame.draw.circle(screen, WHITE, hand_position, 5)

    if game_state == "playing":
        if player_count == 2:
            score_text = font.render(
                f"P1: {player_scores[0]}   P2: {player_scores[1]}",
                True,
                WHITE
            )
            turn_text = font.render(
                f"Player {current_player + 1}'s turn",
                True,
                YELLOW
            )
            screen.blit(turn_text, (20, 58))
        else:
            score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        timer_text = font.render(f"Time: {math.ceil(round_time)}", True, YELLOW)
        screen.blit(timer_text, (20, 94 if player_count == 2 else 58))

        input_text = "MOUSE: DRAG TO SLICE"
        if camera_error:
            input_text = f"{input_text} | {camera_error}"
        elif camera_capture is not None:
            input_text = f"{input_text} | CAMERA ACTIVE"
        tracked_hand_count = sum(
            hand_position is not None for hand_position in hand_positions
        )
        if hand_landmarker is not None:
            input_text = f"{input_text} | HANDS TRACKED: {tracked_hand_count}/2"
        input_status = font.render(input_text, True, WHITE)
        screen.blit(input_status, (20, 130 if player_count == 2 else 94))

        pygame.draw.rect(screen, PURPLE, (760, 15, 100, 40), border_radius=6)
        pygame.draw.rect(screen, RED, (870, 15, 110, 40), border_radius=6)
        pause_text = font.render("PAUSE", True, WHITE)
        finish_text = font.render("FINISH", True, WHITE)
        screen.blit(pause_text, pause_text.get_rect(center=(810, 35)))
        screen.blit(finish_text, finish_text.get_rect(center=(925, 35)))

    elif game_state == "mode_select":
        draw_menu(
            "CHOOSE PLAYERS",
            [("1 PLAYER", "single"), ("2 PLAYERS", "multi"), ("QUIT", "quit")]
        )

    elif game_state == "paused":
        draw_menu(
            "GAME PAUSED",
            [("RESUME", "resume"), ("RESTART", "restart"), ("QUIT", "quit")]
        )

    elif game_state == "finished":
        draw_menu("ROUND FINISHED", [("PLAY AGAIN", "start"), ("QUIT", "quit")])

        if player_count == 2:
            if player_scores[0] > player_scores[1]:
                winner_text = "PLAYER 1 WINS!"
            elif player_scores[1] > player_scores[0]:
                winner_text = "PLAYER 2 WINS!"
            else:
                winner_text = "DRAW GAME!"

            winner = big_font.render(winner_text, True, YELLOW)
            screen.blit(winner, winner.get_rect(center=(WIDTH // 2, 475)))

        if score_history:
            highest_score = max(score_history)
            lowest_score = min(score_history)
            middle_score = statistics.median(score_history)
            stats = [
                f"Highest score: {highest_score}",
                f"Lowest score: {lowest_score}",
                f"Middle score: {middle_score:g}"
            ]

            for index, stat in enumerate(stats):
                stat_text = font.render(stat, True, WHITE)
                stat_rect = stat_text.get_rect(center=(WIDTH // 2, 490 + index * 32))
                screen.blit(stat_text, stat_rect)

    # -------------------------
    # Update screen
    # -------------------------
    pygame.display.flip()

    clock.tick(60)


stop_camera()
pygame.quit()
