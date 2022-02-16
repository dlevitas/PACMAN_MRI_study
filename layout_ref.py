import pygame
import random
from config import *


def enviroment_setup(rand_num):
    """Determines which grid is used for the trial as well as the player, ghosts,
    and dots locations. Since there are a variety of options to choose from, this
    information is randomized when a new trial is initialized."""
    
    # generate random seed
    random.seed(rand_num)

    grid_options = []

    gridA = {"grid":   ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                        (0, 3, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 3, 0),
                        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0),
                        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0),
                        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0),
                        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0),
                        (0, 4, 1, 1, 4, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 4, 1, 1, 4, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0),
                        (0, 4, 1, 1, 4, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 4, 1, 1, 4, 0),
                        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0),
                        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0),
                        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4, 1, 1, 1, 4, 0, 0, 2, 0),
                        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0),
                        (0, 3, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 3, 0),
                        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
             "id": "A",
             "player_start_pos": [(32, 32), (32, 512), (704, 32), (704, 512)],
             "slime_start_pos": [(256, 192), (480, 192), (256, 352), (480, 352)]
             }

    gridB = {"grid":   ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                        (0, 3, 1, 1, 1, 3, 0, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 3, 0),
                        (0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0),
                        (0, 2, 0, 0, 0, 4, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0),
                        (0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0),
                        (0, 4, 1, 1, 1, 4, 1, 1, 1, 1, 5, 1, 1, 1, 4, 1, 1, 4, 1, 1, 1, 1, 4, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0),
                        (0, 4, 1, 1, 1, 1, 1, 4, 1, 1, 5, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 3, 0),
                        (0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0),
                        (0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0),
                        (0, 4, 1, 1, 1, 1, 1, 3, 0, 0, 4, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 3, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0),
                        (0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0),
                        (0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 3, 0),
                        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
             "id": "B",
             "player_start_pos": [(32, 32), (32, 512), (704, 32), (704, 512)],
             "slime_start_pos": [(320, 160), (320, 320), (576, 416)]
            }


    # combine grid options
    grid_options.append([gridA, gridB])
    grid_options = [x for y in grid_options for x in y] # flatten list of dics

    # randomly select a grid option
    grid_data = random.choice(grid_options)

    # grid
    grid = grid_data["grid"]

    # grid ID
    grid_id = grid_data["id"]

    # randomly select player start position
    player_start_pos = random.choice(grid_data["player_start_pos"])

    # randomly select slimes start positions
    slime1_start_pos = random.choice(grid_data["slime_start_pos"])
    slime2_start_pos = random.choice([x for x in grid_data["slime_start_pos"] if x != slime1_start_pos])
    slimes_start_pos = [slime1_start_pos, slime2_start_pos]

    # get all intersections (2-way, 3-way, 4-way) and horizontal and vertical
    horizontal = []
    vertical = []
    intersection_2way = []
    intersection_3way = []
    intersection_4way = []

    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item == 1:
                pos_type = "horizontal"
                upVal, downVal, leftVal, rightVal = 0, 0, 1, 1
                legal_directions = ["left", "right"]
                horizontal.append(((j*32, i*32), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))

            elif item == 2:
                pos_type = "vertical"
                upVal, downVal, leftVal, rightVal = 2, 2, 0, 0
                legal_directions = ["up", "down"]
                vertical.append(((j*32, i*32), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))

            elif item in [3, 4, 5]:
                legal_directions = []
                upVal = grid[i-1][j]
                downVal = grid[i+1][j]
                leftVal = grid[i][j-1]
                rightVal = grid[i][j+1]

                if upVal != 0:
                    legal_directions.append("up")
                if downVal != 0:
                    legal_directions.append("down")
                if leftVal != 0:
                    legal_directions.append("left")
                if rightVal != 0:
                    legal_directions.append("right")

                if item == 3:
                    pos_type = "2way"
                    intersection_2way.append(((j*32, i*32), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))
                elif item == 4:
                    pos_type = "3way"
                    intersection_3way.append(((j*32, i*32), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))
                elif item == 5:
                    pos_type = "4way"
                    intersection_4way.append(((j*32, i*32), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))

    dots_pos = [x[0] for x in intersection_2way+intersection_3way+intersection_4way if x[0] != player_start_pos]
    dots_pos = random.sample(dots_pos, 15)

    return grid, player_start_pos, slimes_start_pos, dots_pos, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way


def draw_enviroment(screen, grid):
    """Creates the grid."""
    
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item == 1:
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32, i*32], 3) # line drawn left
                pygame.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32, i*32+32], 3) # line drawn right
            elif item == 2:
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32, i*32+32], 3) # line drawn up
                pygame.draw.line(screen, BLUE , [j*32+32, i*32], [j*32+32, i*32+32], 3) # line drawn down
            elif item in [3, 4]:
                upVal = grid[i-1][j]
                downVal = grid[i+1][j]
                leftVal = grid[i][j-1]
                rightVal = grid[i][j+1]

                # 2-way intersection
                if [upVal, downVal, leftVal, rightVal] == [0, 2, 0, 1]: # down<-->right
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32, i*32], 3)
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32, i*32+32], 3)
                elif [upVal, downVal, leftVal, rightVal] == [2, 0, 0, 1]: # up<-->right
                    pygame.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32, i*32+32], 3)
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32, i*32+32], 3)
                elif [upVal, downVal, leftVal, rightVal] == [0, 2, 1, 0]: # down<-->left
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32, i*32], 3)
                    pygame.draw.line(screen,BLUE ,[j*32+32,i*32],[j*32+32,i*32+32],3)
                elif [upVal,downVal,leftVal,rightVal] == [2,0,1,0]: # up<-->left
                    pygame.draw.line(screen,BLUE ,[j*32,i*32+32],[j*32+32,i*32+32],3)
                    pygame.draw.line(screen,BLUE ,[j*32+32,i*32],[j*32+32,i*32+32],3)

                # 3-way intersection
                elif [upVal,downVal,leftVal,rightVal] == [2,2,0,1]: # up<-->down<-->right
                    pygame.draw.line(screen,BLUE ,[j*32,i*32],[j*32,i*32+32],3)
                elif [upVal,downVal,leftVal,rightVal] == [0,2,1,1]: # down<-->left<-->right
                    pygame.draw.line(screen,BLUE ,[j*32,i*32],[j*32+32,i*32],3)
                elif [upVal,downVal,leftVal,rightVal] == [2,2,1,0]: # up<-->down<-->left
                    pygame.draw.line(screen,BLUE ,[j*32+32,i*32],[j*32+32,i*32+32],3)
                elif [upVal,downVal,leftVal,rightVal] == [2,0,1,1]: # up<-->left<-->right
                    pygame.draw.line(screen,BLUE ,[j*32,i*32+32],[j*32+32,i*32+32], 3)
                else:
                    pass