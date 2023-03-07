import tcod
import imageio
wall_tile = 256
def main():
    # Load the font sheet as an ndarray
    font_sheet = imageio.v3.imread("./DawnLike/Objects/Wall.png")

    # Create a new font from the font sheet
    font = tcod.tileset.load_tilesheet("./DawnLike/Objects/Wall.png",16,16,tcod.tileset.CHARMAP_CP437)
    tcod.console_set_custom_font("./DawnLike/Objects/Wall.png",tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)
    def load_custom_font():
        a=256
        for y in range(5,6):
            for x in range(0,16):
                tcod.console_map_ascii_code_to_font(a,x,y)
                a+=32
        

    # Create a new console
    console = tcod.console.Console(80, 50)

    # Draw a single tile to the console
    tile_x, tile_y = 32, 32 # Coordinates of the top-left corner of the tile
    tile_w, tile_h = 16, 16 # Width and height of the tile in pixels
    tile_char = ord("#") # ASCII character representing the tile
    console.print_(0, 0, chr(tile_char), fg=tcod.white, bg=tcod.black, font=font)

    # Flush the console to the screen
    with tcod.context.new_terminal(console.width, console.height) as context:
        while True:
            console.print_(0, 1, "Hello, world!")
            console.blit(context)
            tcod.console_put_char_ex(console.)
            tcod.console_flush()
            key = tcod.console_check_for_keypress()
            if key.vk == tcod.KEY_ESCAPE:
                break

if __name__ == "__main__":
    main()