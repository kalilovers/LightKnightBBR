import os
import shutil

def show_image():
    ascii_art = """
$$$$$$$$$$$%%%$$$$$$$$%%%%%%%%%$$$%%%%$$%%$$$$$%$$%%%%%%%%%%%%%%%%%%%$
$$$$$$$$$%%%%$$$$$$$$%%%%%%%%%%**!!****%%%***%%$$%%$$%%%%%%%%%%%%%%%%%
$$$$$$$$%%%%$$$$$$$$%%%%%$$*!!!**!*****!::!***!!*$$$%$$$%%%%%%%%%%%%%%
$$$$$$$%%%%%$$$$$$$%%%%$%*:!%$*:!%**!:!*%!::::!::!*%$$%%%%%%%%%%%%%%%%
$$$$$$%%%%$$$$$$$$%%%$$*:!%$*!*!:!*%%*::!%*::::::!!!!%%%%%%%%%%%%%%%%%
$$$$$%%%%$$$$%%$$%%%$$!:%%!:*%%!::!!*%%:::%*:::::::**:*%%%%$%%%%%%%%%%
%%$$%%%%$$$$$$$$%%%%*:!$$$*%&$%$$*%$%%@@::!@!:::::::!%::%$$$%%%%%%%%%%
%%%%%%$$$$$$$$$%%%$!.*#@$@&&%*%$@@&@%%&#&@$$$:::::::!!*::*$%%%%%%%%%%%
%%%%%$$$$$$$$$%%%$!:%&$$*%%:*%*!*!*$$**!$@$*@!:::::!*!:!::!%%%%%%%%%%%
%%%%%$$$$$$$$%%%$!:%$%%!!$!:::*:%:::%::!**!%*%:::::!%$:::::!%%%%%%%%%%
%%%%%%$$$$$$%%%$*:**%%%:$%:::**:$:::$::**%:::%::::::%$!::!::*$%%%%%%%%
%%%%%%%$$$$%%%%%:*!!$%!*%*:!!%*!$!:!$!:**%!::%!:::::%%!::!*::%@%%%%%%%
%%%%%%%%$%%%%%$!**:%$%!%%%%*****%***$!:****!!%*:::::%%*::*%::*$$%%%%%$
$$$$$$$$%%%%%$%%$:!%%%%***!:::::::*%%%%%%**!!%*:::::%%*::*$::!$%%%%%$$
$$$$$$$%%%%%%$%&!:*$$**!%!!:::::::::!*%*$%$*!$!:::::%$%::%$:*:$$!$%$$$
$$$$$$%%%%%%%@$%::*%$%%$$$%::::::::*%$$@@@&$!$::::::$%%::%$:*:$$:%$$$$
$$$$$%%%%%%%%$%!::%!*%%%$@@*:::::::!:*$$@@$%@*::::::$*%::$$:%!$$!!$$$$
$$$$%%%%%%%%$*%!!!%!!*!!!!:::::::::::!***::!@::::::!%%%!!$%!%*%@*!$$$$
$$$%%%%%%%%%$**!!%*!!!%::::!!::::::::::::::**:::::!***%**@*%$%$$**$$$$
$%%%%%%%$$$$%**!*!!!!!%!::::::::::::::::::!%:::::!*%!$*%%@*$$%@%*$$$$%
%%%%%%$$$$$$****!!!!!!*%::::::::::::::::::%*!!!%!**$$$*$%$%%*$@$$$$$%%
%%%%%%$$%%%$!*%!!!!!:**$%!::::::!!::::***%%*%*****$$@$$$%%%%%$$$$$$%%%
%%%%$$%%%%%%!**!!!!::*$%%%*!::::::::::*%$$!!!!!!%%$$@$%%%%$%%%%%%%$$%%
%%%$$$%%%%$!!!!!!!!:!$%%%%%%*!:::::!!*%%$*!!!:!!*%&&&%%%$#S&@$$&$&S#@&
%%$$$$$$@%%::!!!!!::%@%%%%%%$$*%%%%%**%@$::::::!*$@@@@S#SSSSSSSSSSSSSS
%$$$$$$%#S*:::::::::&#####&&S@%@S#$@&#SS*:::::!*%$@$&SSSSSSSSSSSSSSSSS
%%$$$%%$S#::::!!:::!$*$@#SB#%!!#SSSS##S@:!::!:**SS##SSSSSSSSSSSSSSSSSS
%%%%%%@#S@:::!!!!!$S%.:%##%..*##@&####S%:!:!!!**SSSSBSSSS&S@%&##SSSSSS
%%%%%%$SS%!!!!!!!!!**.*S&!.*&S@$$$@###&!!!!!:!!$SSSSBSSSS@$$@##SSSSSSS
%$$$$&#S#*!!!!!!!!:!!:@$!%&SS@$$$@@##S@:!!!!!*!@S#&&@@$*%@##SSSSSSSSSS
%@SSSSSS@!!!!!!!!!!!!$@@#SS#@$&##SSSSS$!!!!!!*:@S@:::.:*#SSSSSSSSSSSSS
#SSS##S&%!!!!!!!!!!@&#####&@$&SSSSSSSS%!!!!:*%:$&!::.%#SSSSSSSSSSSSSSS
SSS##S#$%!!!!!!!*$&######@$$@$&SSSS###S&*!!!!:%*!%!::%#BSSSSSSSSSSSSSS
SSSSSS$%*!!!!!%@#######&$$@$&SSSS###S&*!!!!:%*!!%::@BSSSSSSSSSSSSSSSSS
SSSSS#$%*!!!%&########@$$$$@SSS#####S@*!!!!!**!!%!&SSSSSSSSSSSSSSSSSSS
    """
    print(ascii_art)

def show_main_menu():
    show_image()
    print("\nSpecial thanks to the Queen")
    print("\nView the project on GitHub: https://github.com/kalilovers")
    print("\nLightKnight Simple Script For Simple and Stable BBR")
    print("1_BBR Fq")
    print("2_BBR Fq_Codel(Recommend - Especially For IPSec And Local TUNS)")
    print("3_Restore")
    print("4_Speed Test")
    print("0_Exit")

def show_fq_menu():
    print("\nFq")
    print("1_Delete Old File Then Setup(+Backup)")
    print("2_Setup Without Delete")
    print("0_Back")

def show_fq_codel_menu():
    print("\nFq_Codel")
    print("1_Delete Old File Then Setup(+Backup)")
    print("2_Setup Without Delete")
    print("0_Back")

def show_speed_test_menu():
    print("\nSpeed Test")
    print("1_Bench Method1")
    print("2_Bench Method2")
    print("3_Iperf3 (Between 2 Server)")
    print("4_Speedtest Ookla")
    print("0_Back")

def show_iperf_menu():
    print("\nChoose which one you are:")
    print("1_Client (iran or...)")
    print("2_Server (Kharej/Traget or...)")
    print("0_Back")

def prompt_restart():
    while True:
        choice = input("The mission was successfully completed. Do you want to restart? (Required) Yes or No: ").lower()
        if choice in ['n', 'no']:
            break
        elif choice in ['y', 'yes']:
            os.system("reboot")
            break

def delete_old_file_then_setup(algorithm):
    os.chdir("/")
    backup_path = "/etc/sysctl.confback"
    original_path = "/etc/sysctl.conf"

    if os.path.exists(original_path):
        shutil.copy(original_path, backup_path)
        os.remove(original_path)

    with open(original_path, "w") as file:
        file.write(f"#{algorithm} Light Knight\n")
        file.write(f"net.core.default_qdisc = {algorithm}\n")
        file.write("net.ipv4.tcp_congestion_control = bbr\n")
    
    os.system("sysctl -p")
    prompt_restart()

def setup_without_delete(algorithm):
    os.chdir("/")
    with open("/etc/sysctl.conf", "w") as file:
        file.write(f"#{algorithm} Light Knight\n")
        file.write(f"net.core.default_qdisc = {algorithm}\n")
        file.write("net.ipv4.tcp_congestion_control = bbr\n")
    
    os.system("sysctl -p")
    prompt_restart()

def restore():
    os.chdir("/")
    backup_path = "/etc/sysctl.confback"
    original_path = "/etc/sysctl.conf"

    if os.path.exists(original_path):
        os.remove(original_path)

    if os.path.exists(backup_path):
        os.rename(backup_path, original_path)
    
    prompt_restart()

def run_bench_method1():
    os.system("wget -qO- bench.sh | bash")

def run_bench_method2():
    os.system("curl -Lso- bench.sh | bash")

def run_iperf_client():
    os.system("apt update")
    os.system("apt install iperf3")
    server_ip = input("What is the IP address of your target server?Enter Your Target IP: ")
    os.system(f"iperf3 -c {server_ip} -i 1 -t 10 -P 20")
    input("The download speed test was done. To test the upload speed, enter or press a button... ")
    os.system(f"iperf3 -c {server_ip} -R -i 1 -t 10 -P 20")
    input("The upload speed test was done. To Back to the menu, enter or press a button... ")

def run_iperf_server():
    os.system("apt update")
    os.system("apt install iperf3")
    os.system("ufw allow 5201")
    os.system("iperf3 -s")
    input("You are active as a server, please do not log out. If it is finished, to Back to the menu, enter or press a button... ")

def run_speedtest_ookla():
    os.system("wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz")
    os.system("tar zxvf ookla-speedtest-1.2.0-linux-x86_64.tgz")
    server_num = input("Enter your ookla-server number. Or by pressing a button, the Amsterdam server can be used by default: ")
    if not server_num:
        server_num = "54746"
    os.system(f"./speedtest -s {server_num}")
    input("Test Done, please do not log out. If it is finished, to Back to the menu, enter or press a button... ")

def main():
    while True:
        show_main_menu()
        choice = input("Please enter your choice: ")
        
        if choice == '1':
            while True:
                show_fq_menu()
                fq_choice = input("Please enter your choice: ")
                if fq_choice == '1':
                    delete_old_file_then_setup("fq")
                elif fq_choice == '2':
                    setup_without_delete("fq")
                elif fq_choice == '0':
                    break
                else:
                    print("Invalid choice, please try again.")
        elif choice == '2':
            while True:
                show_fq_codel_menu()
                fq_codel_choice = input("Please enter your choice: ")
                if fq_codel_choice == '1':
                    delete_old_file_then_setup("fq_codel")
                elif fq_codel_choice == '2':
                    setup_without_delete("fq_codel")
                elif fq_codel_choice == '0':
                    break
                else:
                    print("Invalid choice, please try again.")
        elif choice == '3':
            restore()
        elif choice == '4':
            while True:
                show_speed_test_menu()
                speed_test_choice = input("Please enter your choice: ")
                if speed_test_choice == '1':
                    run_bench_method1()
                elif speed_test_choice == '2':
                    run_bench_method2()
                elif speed_test_choice == '3':
                    while True:
                        show_iperf_menu()
                        iperf_choice = input("Please enter your choice: ")
                        if iperf_choice == '1':
                            run_iperf_client()
                        elif iperf_choice == '2':
                            run_iperf_server()
                        elif iperf_choice == '0':
                            break
                        else:
                            print("Invalid choice, please try again.")
                elif speed_test_choice == '4':
                    run_speedtest_ookla()
                elif speed_test_choice == '0':
                    break
                else:
                    print("Invalid choice, please try again.")
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
