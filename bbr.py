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
%%$$$%%$S#::::!!:::!$*$@#SB#%!!#SSSS##S@:!::!:**&S##SSSSSSSSSSSSSSSSSS
%%%%%%@#S@:::!!!!!$S%.:%##%..*##@&####S%:!:!!!**SSSSSSSSSSSS##S#SSSSSS
%%%%%%$SS%!!!!!!!!!**.*S&!.*&S@$$$@###&!!!!!:!!$SSSSBSSSS&S@%&##SSSSSS
%$$$$&#S#*!!!!!!!!:!!:@$!%&SS@$$$@@##S@:!!!!!*!@S#&&@@$*%@##SSSSSSSSSS
%@SSSSSS@!!!!!!!!!!!!$@@#SS#@$&##SSSSS$!!!!!!*:@S@:::.:*#SSSSSSSSSSSSS
#SSS##S&%!!!!!!!!!!@&#####&@$&SSSSSSSS%!!!!:*%:$&!::.%#SSSSSSSSSSSSSSS
SSS##S#$%!!!!!!!*$&######@$$@#SS#S##S&*!!!!:%*!%!:::%#BSSSSSSSSSSSSSSS
SSSSSS$%*!!!!!%@#######&$$@$&SSSS###S&*!!!!!%*!!%::@BSSSSSSSSSSSSSSSSS
SSSSS#$%*!!!%&########@$$$$@SSS#####S@*!!!!!**!!%!&SSSSSSSSSSSSSSSSSSS
    """
    print(ascii_art)

def show_main_menu():
    show_image()
    print("\nSpecial thanks to the Queen")
    print("\n")
    print("\nLightKnight Simple Script For Simple and Stable BBR")
    print("1_BBR Fq")
    print("2_BBR Fq_Codel(Suggested)")
    print("3_Restore")
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
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
