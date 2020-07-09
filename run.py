# -*- coding: utf-8 -*-

import sys
from colorama import Fore
from bot import NikeBot
from os import system
from time import sleep
from sys import platform

def show_logo():
    logo = """\n\n
                 .........                   .........                     
               @@@@@@@@@@@@                @@@@@@@@@@@@                   
               @@@@@@@@@@@@                @@@@@@@@@@@@                   
               @@@@@@@@@@@@                @@@@@@@@@@@@                   
               @@@@@@@@@@@@                @@@@@@@@@@@@                   
                                                                          
                                                                          
                                                          %          
               (@                                    @@@@&                
              @@                          ,@@@@@@@@&                      
            @@@@               .@@@@@@@@@@@@@&                            
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                  
           @@@@@@@@@@@@@@@@@@@@@@&                                        
           @@@@@@@@@@@@@@@@@                                              
            @@@@@@@@@%  \n
       ███▄    █  ██▓ ██ ▄█▀▓█████     ▄▄▄▄    ▒█████  ▄▄▄█████▓
       ██ ▀█   █ ▓██▒ ██▄█▒ ▓█   ▀    ▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
      ▓██  ▀█ ██▒▒██▒▓███▄░ ▒███      ▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
      ▓██▒  ▐▌██▒░██░▓██ █▄ ▒▓█  ▄    ▒██░█▀  ▒██   ██░░ ▓██▓ ░ 
      ▒██░   ▓██░░██░▒██▒ █▄░▒████▒   ░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ 
      ░ ▒░   ▒ ▒ ░▓  ▒ ▒▒ ▓▒░░ ▒░ ░   ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   
      ░ ░░   ░ ▒░ ▒ ░░ ░▒ ▒░ ░ ░  ░   ▒░▒   ░   ░ ▒ ▒░     ░    
         ░   ░ ░  ▒ ░░ ░░ ░    ░       ░    ░ ░ ░ ░ ▒    ░      
               ░  ░  ░  ░      ░  ░    ░          ░ ░           
                                            ░       
                                               
    [*] Script made by: guiguat and iuri-pdista\n
    """
    print(Fore.RED + logo)

if platform == "win32":
    system("cls")
else:
    system("clear")

show_logo()
browser = input("[*] Escolha um browser (chrome/edge): ");
size = input("[*] Escolha os tamanhos preferidos (<size1>, <size2>):");
size = str(size).strip().split(",")
bot = NikeBot(browser)
wait = input("[*] Faça login e selecione o produto que deseja comprar (ENTER para continuar):")
bot.set_size(size[0], size[1])
bot.click_buy()
bot.checkout()
bot.go_to_payment()
bot.finish_purchase()

final_msg = ">>>OUR JOB HERE IS DONE, PLEASE CONFIRM YOUR DATA, FINISH THE PURCHASE MANUALLY AND \n ENJOY YOUR SNKRS :)"
print(Fore.BLUE + final_msg + Fore.RESET)

