import pygame, random
import os



def load_filed_sprites(FILE, frames_count, SCALE):
    #Looking inside the file and takes every .png sprite and cuts it the frames and returns a list with 
    #You must name the animations in the folder with """"_down,left,up,right
    #animation lists: [0]=down, [1]=left, [2]=right, [3]=up
    frames_list = []
    try:
        for file in sorted(os.listdir(FILE)):
            if file.endswith(".png"):
                img = pygame.image.load(os.path.join(FILE, file)).convert_alpha()

                img = pygame.transform.scale(
                    img,
                    (img.get_width() * SCALE, img.get_height() * SCALE)
                )

                frame_w = img.get_width() // frames_count   # 4 frames horizontally
                frame_h = img.get_height()

                temp_list = []
                for i in range(4):
                    frame = img.subsurface(pygame.Rect(i * frame_w, 0, frame_w, frame_h))
                    temp_list.append(frame)
            frames_list.append(temp_list)
    except FileNotFoundError:
        print(f"Cannot load image: {FILE}")
        raise SystemExit
        
    return frames_list


def load_sprite(filename, frames_count, scale_amount):
    #Looking inside the file and takes every .png sprite and cuts it the frames and returns a list with 
    #You must name the animations in the folder with """"_down,left,up,right
    #animation lists: [0]=down, [1]=left, [2]=right, [3]=up
    frames_list = []
    try:
        for file in sorted(os.listdir(filename)):
            if file.endswith(".png"):
                img = pygame.image.load(os.path.join(filename, file)).convert_alpha()

                img = pygame.transform.scale(
                    img,
                    (img.get_width() * scale_amount, img.get_height() * scale_amount)
                )

                frame_w = img.get_width() // frames_count   # 4 frames horizontally
                frame_h = img.get_height()

                for i in range(4):
                    frame = img.subsurface(pygame.Rect(i * frame_w, 0, frame_w, frame_h))
                    frames_list.append(frame)
    except FileNotFoundError:
        print(f"Cannot load image: {filename}")
        raise SystemExit
        
    return frames_list


def load_tiles(folder, tile_size):
    tiles = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img_path = os.path.join(folder, filename)
            image = pygame.image.load(img_path).convert_alpha()
            image = pygame.transform.scale(image, (tile_size, tile_size))
            tiles.append(image)
    return tiles

def load_random_image(folder, tile_size):
    # Πάρε όλα τα .png από τον φάκελο
    files = [f for f in os.listdir(folder) if f.endswith(".png")]

    # Διάλεξε τυχαία μία
    chosen = random.choice(files)

    # Φόρτωσε την εικόνα
    img = pygame.image.load(os.path.join(folder, chosen)).convert_alpha()
    img = pygame.transform.scale(img, (tile_size, tile_size))
    return img



