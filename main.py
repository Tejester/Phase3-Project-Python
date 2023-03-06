import copy
import traceback

import tcod

import color

from engine import Engine
import entity_factories
from procgen import generate_dungeon

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 43
    # map_height = 45

    # player_x = int(screen_width / 2)
    # player_y = int(screen_height / 2)

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 2

    # tileset = tcod.tileset.load_tilesheet(
    #     "dejavu16x16_gs_tc.png",32,8,tcod.tileset.CHARMAP_TCOD
    # )

    tileset = tcod.tileset.load_tilesheet(
        "./dejavu16x16_gs_tc.png",32,8,tcod.tileset.CHARMAP_TCOD
    )


    # tileset = tcod.tileset.load_tilesheet(
    #     "./testsheet.png",8,20,tcod.tileset.CHARMAP_CP437
    # )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)


    # game_map = GameMap(map_width,map_height)
    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine
    )

    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    # engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="MY roguelike",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width,screen_height,order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)

            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception: # Handle exceptions in the game.
                traceback.print_exc() # Print the exception to the console.
                # Then print the error to the message log.
                engine.message_log.add_message(traceback.format_exc(),color.error)
            
            # engine.event_handler.handle_events(context)

            # engine.render(console=root_console,context=context)
            # engine.event_handler.handle_events()
            # root_console.put_char(player.x,player.y,ord("☺"),tcod.BKGND_NONE)
            # events = tcod.event.wait()
            # engine.handle_events(events)

if __name__ == "__main__":
    main()