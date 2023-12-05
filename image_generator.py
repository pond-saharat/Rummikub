# This file is for generating a card picture in *.png in ./src/*.png
import matplotlib.pyplot as plt
import os
import sys

from config import *

joker_number = 2
card_number = 13

class ImageGenerator:
    def __init__(self,number_of_colour_cards,number_of_joker_cards):
        self.number_of_colour_cards = number_of_colour_cards
        self.number_of_joker_cards = number_of_joker_cards
    
    def run(self,regenerate):
        if regenerate == True:
            try:
                os.system("rm ./src/*.png")
                os.system("rm ./src/cards/*.png")
                self.generate_colour_card_png()
                self.generate_joker_card_png()
                self.generate_back_card_png()
                print("The images were generated successfully.")
            except:
                raise RuntimeError("Image generation failed.")

    def generate_colour_card_png(self):
        for number in range(1,self.number_of_colour_cards + 1):
            for colour in COLOURS:
                fig = plt.figure()
                fig.patch.set_facecolor(colour)  # background color
                if colour == "Yellow":
                    plt.text(1.5,2.0,s=f"{number}",c="black",fontsize=120,horizontalalignment='center',verticalalignment='center')
                else:
                    plt.text(1.5,2.0,s=f"{number}",c="white",fontsize=120,horizontalalignment='center',verticalalignment='center')
                plt.xlim([0,3]) 
                plt.ylim([0,4]) 
                plt.axis('off')
                plt.gcf().set_size_inches(3,4)
                plt.savefig(f"./src/cards/{colour.lower()}{number}.png", dpi=300)
                plt.close()

    def generate_joker_card_png(self):
        fig = plt.figure()
        fig.patch.set_facecolor('white')  # the background color of Joker is black
        plt.text(1.5,2.0,s=f"J",c="black",fontsize=120,horizontalalignment='center',verticalalignment='center')
        plt.xlim([0,3]) 
        plt.ylim([0,4]) 
        plt.axis('off')
        plt.gcf().set_size_inches(3,4)
        plt.savefig(f"./src/cards/joker.png", dpi=300)
        plt.close()
    
    def generate_back_card_png(self):
        fig = plt.figure()
        fig.patch.set_facecolor('white')  # the background color of Joker is black
        plt.text(1.5,2.0,s=f"B",c="black",fontsize=120,horizontalalignment='center',verticalalignment='center')
        plt.xlim([0,3]) 
        plt.ylim([0,4]) 
        plt.axis('off')
        plt.gcf().set_size_inches(3,4)
        plt.savefig(f"./src/cards/back.png", dpi=300)
        plt.close()

image_generator = ImageGenerator(card_number, joker_number)
image_generator.run(REGENERATE_IMAGE)
# image_generator.run(True)

