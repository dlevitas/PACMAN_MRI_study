from __future__ import division
import os
import glob
import pygame
import random
import pandas as pd
from config import *
from game import Game
from layout import enviroment_setup
from exp import Instructions, participant_info, save_data, generate_ITI_distribution

try:
    from natsort import natsorted
except:
    os.system('pip install natsort --user')
    from natsort import natsorted

# Begin
ITI_distribution = generate_ITI_distribution(ITI_list, ITI_distribution_type)

def main(threat_chase_level, ITI_distribution):
    """Runs the PACPAL game. All classes and functions are referenced here.
    
    Parameters
    ----------
    threat_chase_level : int
        Threat chase level threshold (0-100) of the ghosts. The value
        corresponds to the % likelihood that the ghosts will seek to chase
        you at each intersection, during the threat salience period.
        
    ITI_distribution: list
        An inter-trial interval (ITI) distribution (exponential or normal)
        list, where after each trial a value from the list is randomly selected.
    """
    
    # get subject and run IDs
    subID, runID = participant_info()

    # set path(s) for saved data
    if not os.path.isdir("{}".format(data_dir)):
        os.mkdir("{}".format(data_dir))
    if not os.path.isdir("{}/sub-{}".format(data_dir, subID)):
        os.mkdir("{}/sub-{}".format(data_dir, subID))
    if len([x for x in os.listdir("{}/sub-{}".format(data_dir, subID)) if "run-{}".format(runID) in x]):
        raise ValueError("There is already data saved for run {}. Please select the next run number.".format(runID))

    # initialize all imported pygame modules
    pygame.init()

    # set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # set the current window caption
    pygame.display.set_caption("PACPAL")
    
    # clock
    clock = pygame.time.Clock()
    
    """Adjust difficulty levels depending on run.
    These level increases occur at set runs regardless of player performance.
    Meant to keep player(s) engaged throughout the experiment.
    """
    if runID == "0": # practice
        threat_chase_level = threat_chase_level-10
        ghosts_threat_speed_options = [player_max_speed-1, player_max_speed-1, player_max_speed-1, player_max_speed-1,
                                       player_max_speed,
                                       player_max_speed+1]
    elif runID in ["1","2"]: # runs 1-2
        ghosts_threat_speed_options = [player_max_speed-1, 
                                        player_max_speed, player_max_speed, 
                                        player_max_speed+1, player_max_speed+1]
    elif runID in ["3","4"]: # runs 3-4
        threat_chase_level = threat_chase_level+5
        ghosts_threat_speed_options = [player_max_speed-1, 
                                       player_max_speed, player_max_speed, 
                                       player_max_speed+1, player_max_speed+1, player_max_speed+1]
    elif runID in ["5","6"]: # runs 5-6
        threat_chase_level = threat_chase_level+10
        ghosts_threat_speed_options = [player_max_speed-1, 
                                       player_max_speed, player_max_speed, 
                                       player_max_speed+1, player_max_speed+1, player_max_speed+1, player_max_speed+1]
    
    # set timers and index values for experiment
    cum_run_time = 0
    logging_timer = 0
    sal_period_timer_index = 1
    logging_timer_index = 1
    ITI_index = 0
    cum_ITI_buffer_time = 0

    # variables to loop over through experiment
    run_over = False
    pre_exp = True
    start_buffer = True
    end_buffer = True

    # salience period variables
    sal_period_info = {"safe": safe_chase_level, "threat": threat_chase_level}
    sal_period, ghost_chase_level = random.choice(list(sal_period_info.items()))

    # trial variables information
    trial = 1
    trial_info_list = []
    ITI_buffer_time = random.choice(ITI_distribution)
    rand_num = random.randrange(100) # used to set seed that randomizes grid and player/ghosts locations
    
    # determine trial number and cumulative experiment bonus amount
    try:
        recent_log_file = natsorted([x for x in glob.glob("{}/data/sub-{}/*.tsv".format(os.getcwd(), subID)) 
                                 if "run-0" not in x])[-1]
        trial = int(recent_log_file.split("trial-")[1].split(".tsv")[0]) + 1
        cum_bonus = pd.read_csv(recent_log_file, sep="\t")["cumulative_bonus"].iloc[-1]
    except:
        trial = 1
        cum_bonus = 0.00
        
    # create game and instructions objects
    grid, player_start_pos, ghosts_start_pos, dots_info, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way = enviroment_setup(rand_num)
    all_points_info = horizontal + vertical + intersection_2way + intersection_3way + intersection_4way
    game = Game(player_max_speed, grid, player_start_pos, ghosts_start_pos, 
                dots_info, grid_id, horizontal, vertical, intersection_2way, 
                intersection_3way, intersection_4way, all_points_info, cum_bonus, 
                sal_period, loss_penalty, health_decay, ghosts_threat_speed_options,
                health_bump, bonus_increase)
    instructions = Instructions("pre", 0, 0, 0, "N/A", run_length, 
                                end_run_buffer_time, runID, loss_penalty)

    # display waiting screen until scanner sends trigger signaling the beginning of the scan
    while pre_exp:
        pre_exp = instructions.process_events()
        instructions.display_frame(screen)

    # determine how much time elapsed from pygame initiation to right before start of run (i.e. now)
    pre_run_elapsed_time = pygame.time.get_ticks()

    # -------- Experiment run loop -----------
    while not run_over:
        clock.tick(30) # limit to 30 frames/sec

        cum_run_time = pygame.time.get_ticks() - pre_run_elapsed_time

        while start_buffer:
            instructions.__init__("start", start_run_buffer_time, 
                                  pre_run_elapsed_time, 0, game.trial_end_reason, 
                                  run_length, end_run_buffer_time, runID, 
                                  loss_penalty)
            start_buffer = instructions.process_events()
            instructions.display_frame(screen)

        # process events (keystrokes, mouse clicks, etc) and check if run ends
        if response_device == "keyboard":
            run_over = game.keyboard_process_events()
        elif response_device == "mri":
            run_over = game.mri_process_events()
        elif response_device == "test":
            run_over = game.test_process_events()
        else:
            raise ValueError("Unknown response device specified. Please use 'keyboard', 'mri', or 'test'.")
        # game logic is here, including checking for when the trial ends
        trial_over = game.run_logic(rand_num, sal_period, ghost_chase_level)
        # draw the current frame
        game.display_frame(screen)
        
        if not trial_over:
            if not len(trial_info_list): # let first row of log be the trial onset information
                info = game.log_information()
                info["salience_period"] = sal_period
                info["ghosts_chase_level"] = ghost_chase_level
                info["cumulative_run_time"] = (pygame.time.get_ticks() - pre_run_elapsed_time)/1000
                info["ITI_length"] = ITI_buffer_time
                trial_info_list.append(info)
            
            logging_timer = pygame.time.get_ticks() - pre_run_elapsed_time - start_run_buffer_time*1000 - cum_ITI_buffer_time*1000
            sal_period_timer = pygame.time.get_ticks() - pre_run_elapsed_time - start_run_buffer_time*1000 - cum_ITI_buffer_time*1000              

            # log game information every log interval, but not in-between trials
            if logging_timer/logging_timer_index >= log_interval*1000:
                logging_timer_index += 1
    
                info = game.log_information()
                
                info["cumulative_run_time"] = cum_run_time/1000
                info["ITI_length"] = ITI_buffer_time
                trial_info_list.append(info)

            # update salience period
            if sal_period_timer/sal_period_timer_index >= sal_period_len*1000:
                sal_period, ghost_chase_level = [x for x in sal_period_info.items() if x[0] != sal_period][0]
                sal_period_timer_index += 1

        else: # trial ends, enter inter trial interval (ITI) buffer period
            if len(trial_info_list): # add log information from trial offset, even if not at log interval
                info = game.log_information()
                info["cumulative_run_time"] = cum_run_time/1000
                info["ITI_length"] = ITI_buffer_time
                trial_info_list.append(info)
            
            # Save/update log information and update some variables
            save_data(data_dir, subID, runID, trial, trial_info_list)
            trial_info_list = []
            trial += 1
            ITI_index += 1
            rand_num = random.randrange(100)
            ITI_buffer = True
            run_elapsed_time = pygame.time.get_ticks()
            instructions.__init__("ITI", ITI_buffer_time, pre_run_elapsed_time, 
                                  run_elapsed_time, game.trial_end_reason, 
                                  run_length, end_run_buffer_time, runID, 
                                  loss_penalty)

            while ITI_buffer:
                ITI_buffer = instructions.process_events()
                instructions.display_frame(screen)
            
            cum_ITI_buffer_time += ITI_buffer_time
            ITI_buffer_time = random.choice(ITI_distribution)

        # stop gameplay several seconds before the end of the run
        if cum_run_time >= run_length*60*1000 - end_run_buffer_time*1000:
            if len(trial_info_list): # add log information at trial offset, even if not at log interval
                info = game.log_information()
                info["cumulative_run_time"] = cum_run_time/1000
                info["ITI_length"] = ITI_buffer_time
                info["trial_end_reason"] = "run_end"
                trial_info_list.append(info)
                
            run_elapsed_time = pygame.time.get_ticks()
            instructions.__init__("end", end_run_buffer_time, 
                                  pre_run_elapsed_time, run_elapsed_time, 
                                  game.trial_end_reason, run_length, 
                                  end_run_buffer_time, runID, loss_penalty)

            while end_buffer:
                end_buffer = instructions.process_events()
                instructions.display_frame(screen)
            run_over = True

    # save data if it wasn't already. Occurs if game quit before the current trial was over
    if len(trial_info_list):
        save_data(data_dir, subID, runID, trial, trial_info_list)

    # quit the game, due to the run ending, or from pressing the Esc key
    pygame.quit()

# Run the experiment
if __name__ == '__main__':
    main(threat_chase_level, ITI_distribution)
