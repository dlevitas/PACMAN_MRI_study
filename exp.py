from __future__ import division
import os
import pygame
import pandas as pd
from config import *


def quit_check():
    """Quit game when escape key is pressed."""
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()


class Instructions(object):
    """Display instructions during different parts of game."""
    
    def __init__(self, period, buffer_time, pre_run_elapsed_time, run_elapsed_time, trial_end_reason, run_length, end_buffer_time, runID):
        self.text = "Please wait for the scan to begin"
        self.font_color = WHITE
        self.select_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 30)
        self.period = period
        self.buffer_time = buffer_time
        self.pre_run_elapsed_time = pre_run_elapsed_time
        self.run_elapsed_time = run_elapsed_time
        self.trial_end_reason = trial_end_reason
        self.run_length = run_length
        self.end_buffer_time = end_buffer_time
        self.runID = runID
        if int(self.runID) == 0:
            self.buffer_time = 2 # in sec

    def process_events(self):
        if self.period != "pre":
            quit_check()

        if self.period == "start":
            self.cum_run_time = pygame.time.get_ticks() - self.pre_run_elapsed_time
        elif self.period == "ITI":
            self.cum_run_time = pygame.time.get_ticks() - self.run_elapsed_time
        else:
            self.cum_run_time = pygame.time.get_ticks() - self.run_elapsed_time

        self.countdown = (self.buffer_time*1000 - self.cum_run_time)/10

        if self.period == "pre":
            if int(self.runID) == 0:
                self.text = "Please wait for the practice to begin"
                begin_key = pygame.K_RETURN
            else:
                self.text = "Please wait for the experiment to begin"
                begin_key = pygame.K_BACKQUOTE
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    elif event.key == begin_key:
                        return False

        elif self.period == "start":
            if int(self.runID) == 0:
                self.text = "Please wait. The practice will begin shortly"
            else:
                self.text = "Please wait. Run #{} will begin shortly".format(self.runID)
            if self.cum_run_time >= self.buffer_time*1000:
                return False

        elif self.period == "ITI":
            if self.trial_end_reason in ["caught", "no_health"]:
                self.text = "You lost. Please wait several seconds for the next trial to begin"
            else:
                self.text = "You won. Please wait several seconds for the next trial to begin"

            # exit game if ITI buffer period dips into end run buffer period
            if pygame.time.get_ticks() >= self.run_elapsed_time + self.end_buffer_time*1000:
                return False
            if pygame.time.get_ticks() >= self.run_elapsed_time + self.buffer_time*1000:
                return False

        elif self.period == "end":
            self.text = "This run will end in several seconds"
            if self.cum_run_time >= self.end_buffer_time*1000:
                return False

        return True


    def display_frame(self, screen):
        screen.fill(BLACK)

        label = self.font.render(self.text, True, self.select_color)

        width = label.get_width()
        height = label.get_height()

        posX = (SCREEN_WIDTH/2) - (width/2)
        posY = (SCREEN_HEIGHT/2) - (label.get_height()/2)

        if self.period != "pre":
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH/2.5, SCREEN_HEIGHT/1.8, self.countdown/2, 15))
            screen.blit(label, (posX, posY))
        else:
            posX_new = (SCREEN_WIDTH/2.5) - (width/2)
            label2 = self.font.render("* To move UP, hold down the left hand middle finger button", True, self.select_color)
            label3 = self.font.render("* To move DOWN, hold down the left hand index finger button", True, self.select_color)
            label4 = self.font.render("* To move LEFT, hold down the right hand index finger button", True, self.select_color)
            label5 = self.font.render("* To move RIGHT, hold down the right hand middle finger button", True, self.select_color)

            screen.blits(blit_sequence=((label, (posX, posY-80)), 
                                        (label2, (posX_new, posY+20)),
                                        (label3, (posX_new, posY+40)), 
                                        (label4, (posX_new, posY+60)),
                                        (label5, (posX_new, posY+80))))
        pygame.display.flip()


def participant_info():
    """Allows experimenter to enter participant ID and run ID and checks to 
    ensure that they are proper (e.g. no non-alphanumeric characters allowed)."""
    
    print("Enter subject ID:")
    s = input()

    print("Enter run ID:")
    r = input()

    print("------------------")

    subID = s
    runID = r

    if not subID.isnumeric():
        raise ValueError("The subID is not a number. Please restart.")
    if not runID.isnumeric():
        raise ValueError("The runID is not a number. Please restart.")
        
    
    if os.path.isdir("{}/data/sub-{}".format(os.getcwd(), subID)):
        files = sorted([x for x in os.listdir("{}/data/sub-{}".format(os.getcwd(), subID)) if "run-0" not in x])
        if not len(files):
            if int(runID) not in [0,1]:
                raise ValueError("You have specified an incorrect run ID. The correct run ID is 1")
        else:
            recent_runID = int(files[-1].split("run-")[1].split("_trial")[0])
            if int(runID) - recent_runID != 1:
                raise ValueError("You have specified an incorrect run ID. The correct run ID is {}".format(recent_runID + 1))
    else:
        if int(runID) != 1:
            raise ValueError("You have specified an incorrect run ID. The correct run ID is 1")

    return subID, runID


def save_data(data_dir, subID, runID, trial, trial_info_list):
    """Saves data to TSV file. A file is generated for each trial of each run
    of each subject."""
    
    if not os.path.isfile("{}/sub-{}/run-{}_trial-{}.tsv".format(data_dir, subID, runID, trial)):
        df = pd.DataFrame(trial_info_list)
        df.to_csv("{}/sub-{}/run-{}_trial-{}.tsv".format(data_dir, subID, runID, trial),
                  sep="\t", index=False, columns=list(list(trial_info_list[0].keys())))


