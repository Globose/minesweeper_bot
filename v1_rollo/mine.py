"""Mine.py"""
import mine_game as game

def main():
    """Main"""
    image = game.screenshot()
    tiles = game.find_tiles(image)
    games = game.create_games(tiles)
    for g in games:
        g.solve_game()

if __name__ == '__main__':
    main()
