import matplotlib.pyplot as plt
import os
import sys

joker_number = 2
card_number = 13
colours =["red","blue","yellow","green"]

os.system("rm ./src/*.png")
for number in range(1,card_number+1):
    for colour in colours:
        fig = plt.figure()
        plt.text(1.5,2.0,s=f"{number}",c=f"{colour}",fontsize=60,horizontalalignment='center',verticalalignment='center')
        plt.xlim([0,3]) 
        plt.ylim([0,4]) 
        plt.axis('off')
        plt.gcf().set_size_inches(3,4)
        plt.savefig(f"./src/{colour[0].upper()}{number}.png", dpi=300)
        plt.close()

for number in range(1,joker_number+1):
    fig = plt.figure()
    plt.text(1.5,2.0,s=f"Joker",c="black",fontsize=60,horizontalalignment='center',verticalalignment='center')
    plt.xlim([0,3]) 
    plt.ylim([0,4]) 
    plt.axis('off')
    plt.gcf().set_size_inches(3,4)
    plt.savefig(f"./src/Joker{number}.png", dpi=300)
    plt.close()