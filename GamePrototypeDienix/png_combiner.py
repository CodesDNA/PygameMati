import pygame
import os

def make_spritesheet(folder_path, output_file):
    pygame.init()
    pygame.display.set_mode((1, 1))  # FIX: allow convert_alpha()

    # Get list of image files
    files = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith((".png", ".jpg"))
    ])

    if not files:
        raise Exception("No image files found in folder.")

    # Load first image to get width & height
    first_image = pygame.image.load(os.path.join(folder_path, files[0])).convert_alpha()
    frame_width, frame_height = first_image.get_size()

    # Create spritesheet surface
    sheet_width = frame_width * len(files)
    sheet_height = frame_height

    spritesheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)

    # Paste all frames next to each other
    x_offset = 0
    for filename in files:
        img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
        spritesheet.blit(img, (x_offset, 0))
        x_offset += frame_width

    # Save sheet
    pygame.image.save(spritesheet, output_file)
    print(f"Spritesheet saved as {output_file}")


# Example use
if __name__ == "__main__":
    make_spritesheet(
        r"GamePrototypeDienix\sprites\Reaper_Man_1\PNG\PNG Sequences\Running",
        r"GamePrototypeDienix\spritesheets\running.png"
    )
