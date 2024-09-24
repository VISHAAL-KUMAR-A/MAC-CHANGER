import subprocess
import optparse
import re


def change_mac(interface, new_mac):
    print(f"[+]Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguements():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguements) = parser.parse_args()
    if not options.interface:
        print("[-]Please specify the an interface, use --help for more info")
    elif not options.new_mac:
        print("[-]Please specify an MAC address, use --help for more info")
    return options


def current_mac(interface):
    change_result = subprocess.check_output(
        ["ifconfig", get_arguements().interface]).decode('utf-8')
    search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", change_result)
    if search_result:
        return search_result.group(0)
    else:
        return "[-]Could not read MAC address"


cur_mac = current_mac(get_arguements().interface)
print(f"current MAC = {cur_mac}")
change_mac(get_arguements().interface, get_arguements().new_mac)
