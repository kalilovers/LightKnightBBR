#!/usr/bin/env python3

# -*- coding: utf-8 -*-


###################### v1.5.3 Changes:
#Some sensitive parameters were commented out

##################### Bugs:
#Some optimizations are needed.



"""
Copyright (c) 2025 Kalilovers (https://github.com/kalilovers)

This file is part of [LightKnightBBR]. It is licensed under the MIT License.
You may not remove or alter the above copyright notice.
Any modifications or redistributions must retain the original author's credit.
For more details, please refer to the LICENSE file in the project root.
"""







import os
import shutil
import platform
import subprocess
import sys
# Atomic file lock for safe writes
try:
    from filelock import FileLock, Timeout
except ImportError:
    FileLock = None
    Timeout = None

# Utility: run command safely
def run_cmd(cmd, check=True, capture_output=False, shell=False):
    """Run a shell command safely, return output or None."""
    try:
        result = subprocess.run(cmd, check=check, capture_output=capture_output, text=True, shell=shell)
        return result.stdout if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}\n{e}")
        return None

# Utility: atomic file write with filelock
def atomic_write(filepath, content, mode="a"):
    """Write to file atomically using filelock if available."""
    lockfile = f"{filepath}.lock"
    if FileLock:
        lock = FileLock(lockfile)
        try:
            with lock:
                with open(filepath, mode) as f:
                    f.write(content)
        except Timeout:
            print(f"Could not acquire lock for {filepath}")
    else:
        with open(filepath, mode) as f:
            f.write(content)




VERSION = "1.5.3"
REPO_OWNER = "kalilovers"
REPO_NAME = "LightKnightBBR"
INSTALL_PATH = "/opt/lightbbr/bbr.py"
RELEASE_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"





#--------------------Colors--------------------

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"





def clear_screen():
    try:
        subprocess.run(["clear"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️ Failed to clear screen")







def show_image():
    ascii_art = f"""
{GREEN}%%%%%%%%%%%%%%%%$%%$%$$$$%%%%%%%%%%%%%
%%%%%%%%%%%%%$!!****:!*!*$%$%%%%%%%%%%
%%%%%%%%%%%$:%**:*%:!*:::!!%%%%%%%%%%%
%%%%%%%%%%*!$*&%$%%@:!!:::!:%$%%%%%%%%
%%%%%%%%%!%$*%****$*$$@:::*::!%%%%%%%%
%%%%%%%%**%%$::*$:$:*:::::%!::*%%%%%%%
%%%%%%%%*:$!%%**%*$:**!*::%*:%:$%%%%%%
%%%%%%%%!*$*%!::::!%$$!!::%%:$*$!%%%%%
%%%%%%%%:%*%$@:::::$@$@:::$%:$%$!%%%%%
%%%%%%%*!*!%::!:::::::*::!*%**$$*%%%%%
%%%%%%**!!!*:::::::::%!!!*$$$%%$$$%%%%
%%%%%%!*!!:$%*:::::*$!!!%$@%%$%%%$%%%%
%%%%%%:!!:%%%%$*%%*%$:::*@@SSSSSSSS%%%
%%%%%::!::$$#B%!SS#S::!*S#SSSSSSSSS%%%
%%%%%!!!!!**&.&@$@#&!!:!SSBSS$@#SSS%%%
%%%%%!!!!!!@#S@&#SS$!!!:S:::#SSSSSS%%%
%%%%%!!!*&###$@&SS#S*!!%!!:#SSSSSSS%%%
%%%%%!%####@$$SS##S*!!*!%&SSSSSSSSS%%%{RESET}
    """
    print(ascii_art)

def show_main_menu():
    clear_screen()
    show_image()
    print(f"Version : {CYAN}v{VERSION}{RESET}")
    print(f"GitHub  : {CYAN}https://github.com/kalilovers{RESET}")
    print(f"{BLUE}═══════════════════════════════════════{RESET}")
    print("")
    print(f"0 | {YELLOW}Status{RESET}")
    print("1 | BBR Base (Recommended)")
    print("2 | Hybla Base")
    print("3 | Cubic Base")
    print("4 | Restore Default Settings")
    print("5 | Speed Test")
    print("6 | Update Script")
    print("7 | Uninstall Script")
    print(f"\nq | {RED}Exit{RESET}")
    print("")







def show_status_menu():
    congestion_control, qdisc_algorithm = get_current_settings()
    clear_screen()
    print(f"\n{GREEN}Current Setting:{RESET}")
    print("")
    print(f"Current Congestion Control : {GREEN}{congestion_control}{RESET}")
    print(f"Current Qdisc Algorithm    : {GREEN}{qdisc_algorithm}{RESET}")
    print("\n0 |  Back")
    print("")







def show_bbr_menu():
    clear_screen()
    print(f"\n{GREEN}BBR Base{RESET}")
    print("")
    print("1 | BBR + Fq")
    print("2 | BBR + Fq_Codel (Recommended)")
    print("3 | BBR + Cake")
    print("0 | Back")
    print("")





def show_fq_menu():
    clear_screen()
    print(f"\n{GREEN}Apply With Fq{RESET}")
    print("")
    print(f"{RED}Warning , Choose carefully :{RESET}")
    print(f"1 | Delete Old File Then Setup+Backup ({GREEN}Recommended for proper optimization{RESET}) ")
    print(f"2 | Setup Without Delete ({YELLOW}If you have special settings in sysctl.conf{RESET})")
    print("0 | Back")
    print("")






def show_fq_codel_menu():
    clear_screen()
    print(f"\n{GREEN}Apply With Fq_Codel{RESET}")
    print("")
    print(f"{RED}Warning , Choose carefully :{RESET}")
    print(f"1 | Delete Old File Then Setup+Backup ({GREEN}Recommended for proper optimization{RESET}) ")
    print(f"2 | Setup Without Delete ({YELLOW}If you have special settings in sysctl.conf{RESET})")
    print("0 | Back")
    print("")





def show_cake_menu():
    clear_screen()
    print(f"\n{GREEN}Apply With Cake{RESET}")
    print("")
    print(f"{RED}Warning , Choose carefully :{RESET}")
    print(f"1 | Delete Old File Then Setup+Backup ({GREEN}Recommended for proper optimization{RESET}) ")
    print(f"2 | Setup Without Delete ({YELLOW}If you have special settings in sysctl.conf{RESET})")
    print("0 | Back")
    print("")






def show_hybla_menu():
    clear_screen()
    print(f"\n{GREEN}Hybla Base{RESET}")
    print("")
    print("1 | Hybla + Fq")
    print("2 | Hybla + Fq_Codel")
    print("3 | Hybla + Cake")
    print("0 | Back")
    print("")





def show_cubic_menu():
    clear_screen()
    print(f"\n{GREEN}Cubic Base{RESET}")
    print("")
    print("1 | Cubic + Fq")
    print("2 | Cubic + Fq_Codel")
    print("3 | Cubic + Cake")
    print("0 | Back")
    print("")





def show_speed_test_menu():
    clear_screen()
    print(f"\n{GREEN}Speed Test{RESET}")
    print("")
    print("1 | Bench Method1")
    print("2 | Bench Method2")
    print("3 | Iperf3 (Between 2 Server)")
    print("4 | Speedtest Ookla")
    print("0 | Back")
    print("")






def show_iperf_menu():
    clear_screen()
    print(f"\n{GREEN}Choose which one you are:{RESET}")
    print("")
    print("1 | Client (iran or...)")
    print("2 | Server (Kharej/Target or...)")
    print("0 | Back")
    print("")






def activate_parameters_persistent():
    print("Activating parameters persistently...")
    try:
        atomic_write("/etc/sysctl.conf", "\n# Enabled parameters\n", "a")
        atomic_write("/etc/sysctl.conf", "#net.ipv4.tcp_ecn = 1\n", "a")
        atomic_write("/etc/sysctl.conf", "#net.ipv4.tcp_keepalive_time = 2700\n", "a")
        atomic_write("/etc/sysctl.conf", "#net.ipv4.tcp_keepalive_intvl = 900\n", "a")
        atomic_write("/etc/sysctl.conf", "#net.ipv4.tcp_keepalive_probes = 2\n", "a")
        atomic_write("/etc/sysctl.conf", "net.ipv4.tcp_sack = 1\n", "a")
        run_cmd(['sysctl', '-p'])
        print("parameters activated and will remain active after reboot.")
        return True
    except Exception as e:
        print(f"parameters activation error: {e}")
        return False

def get_main_interface():
    """Find the main interface based on 'UP' status and highest MTU."""
    try:
        interfaces = os.listdir("/sys/class/net/")
        main_interface = None
        highest_mtu = -1
        virtual_interfaces = ['tun', 'docker', 'veth', 'lo', 'br', 'gre', 'sit', 'vxlan', 'tap', 'gretap', 'ipip']

        for interface in interfaces:
            if any(interface.startswith(v) for v in virtual_interfaces):
                continue

            result = run_cmd(['ip', 'addr', 'show', interface], capture_output=True)
            if result and "UP" in result:
                try:
                    with open(f"/sys/class/net/{interface}/mtu", "r") as mtu_file:
                        mtu = int(mtu_file.read().strip())
                        if mtu > highest_mtu:
                            highest_mtu = mtu
                            main_interface = interface
                except Exception as e:
                    print(f"Error reading MTU for {interface}: {e}")

        if main_interface:
            print(f"Main interface detected: {main_interface} with MTU {highest_mtu}")
            return main_interface
        else:
            print("No main interface found.")
            return None

    except Exception as e:
        print(f"Error detecting main interface: {e}")
        return None

def get_current_settings():
    main_interface = get_main_interface()
    if not main_interface:
        return "Unknown", "Unknown"

    try:
        qdisc_result = run_cmd(f"tc qdisc show dev {main_interface}", capture_output=True, shell=True)
        if not qdisc_result:
            print(f"Error retrieving qdisc for {main_interface}")
            return "Unknown", "Unknown"
    except Exception:
        print(f"Error retrieving qdisc for {main_interface}")
        return "Unknown", "Unknown"

    qdisc_lines = qdisc_result.splitlines()
    root_qdisc = None
    for line in qdisc_lines:
        if "root" in line:
            root_qdisc = line.split()[1]
            break

    try:
        congestion_control = subprocess.check_output("sysctl net.ipv4.tcp_congestion_control", shell=True).decode().split('=')[1].strip()
    except subprocess.CalledProcessError:
        print("Error retrieving TCP congestion control")
        congestion_control = "Unknown"

    return congestion_control, root_qdisc if root_qdisc else "Unknown"

def setup_qdisc(algorithm):
    """Apply the Qdisc to the main interface."""
    print("Setting the queuing algorithm on the main network interface...")
    interface = get_main_interface()
    
    if not interface:
        print("No main network interface found. Exiting script.")
        return False

    try:
        run_cmd(['tc', 'qdisc', 'replace', 'dev', interface, 'root', algorithm])
        print(f"The {algorithm} queuing algorithm was set on the {interface} interface.")
        return True
    except Exception as e:
        print(f"Error in setting the queuing algorithm on {interface}: {e}. Exiting script.")
        return False


def make_qdisc_persistent(algorithm):
    """Create a systemd service to persist the Qdisc settings after reboot."""
    print("Creating systemd service to preserve qdisc settings after reboot on the main interface...")

    interface = get_main_interface()
    
    if not interface:
        print("No main network interface found. Exiting script.")
        return False

    exec_command = f"/sbin/tc qdisc replace dev {interface} root {algorithm}"

    service_content = f"""[Unit]
Description=Set qdisc {algorithm} on the main network interface
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c '{exec_command}'
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
"""
    service_path = "/etc/systemd/system/qdisc-setup.service"
    try:
        atomic_write(service_path, service_content, "w")
        run_cmd(['systemctl', 'daemon-reload'])
        run_cmd(['systemctl', 'enable', 'qdisc-setup.service'])
        run_cmd(['systemctl', 'start', 'qdisc-setup.service'])
        print("The systemd service was successfully created and activated for the main interface.")
        return True
    except Exception as e:
        print(f"Error creating systemd service: {e}. Exiting script.")
        return False

def prompt_restart():
    while True:
        try:
            choice = input(f"\n{GREEN}The mission was successfully completed. Do you want to restart? (Required) Yes or No: {RESET}").strip().lower()

            if choice in ['n', 'no']:
                break
            elif choice in ['y', 'yes']:
                os.system("reboot")
                break
            else:
                print("Invalid input. Please enter Yes or No.")
        except UnicodeDecodeError:
            print("Invalid input. Please use only English characters.")
############################################## For BBR Base
def check_kernel_and_os():
    print("Checking the compatibility of operating system and kernel...")
    try:
        with open("/etc/os-release", "r") as f:
            lines = f.readlines()
        distro = ""
        for line in lines:
            if line.startswith("ID="):
                distro = line.strip().split("=")[1].strip('"').lower()
                break
    except FileNotFoundError:
        distro = ""

    if distro not in ['ubuntu', 'debian']:
        print("The operating system is not supported. Only Ubuntu and Debian are supported.")
        return False

    kernel_version = platform.release()
    version_numbers = kernel_version.split(".")
    try:
        kernel_major = int(version_numbers[0])
        kernel_minor = int(version_numbers[1])
    except (IndexError, ValueError):
        print(f"Kernel version {kernel_version} could not be detected.")
        return False

    if kernel_major > 4 or (kernel_major == 4 and kernel_minor >= 9):
        print(f"The kernel version is compatible with BBR.")
        return True
    else:
        print(f"Kernel version {kernel_version} is not supported. Requires version 4.9 or higher.")
        return False

def check_kernel_and_os_cake():
    print("Checking the compatibility of operating system and kernel for Cake...")
    try:
        with open("/etc/os-release", "r") as f:
            lines = f.readlines()
        distro = ""
        for line in lines:
            if line.startswith("ID="):
                distro = line.strip().split("=")[1].strip('"').lower()
                break
    except FileNotFoundError:
        distro = ""

    if distro not in ['ubuntu', 'debian']:
        print("The operating system is not supported. Only Ubuntu and Debian are supported.")
        return False

    kernel_version = platform.release()
    version_numbers = kernel_version.split(".")
    try:
        kernel_major = int(version_numbers[0])
        kernel_minor = int(version_numbers[1])
    except (IndexError, ValueError):
        print(f"Kernel version {kernel_version} could not be detected.")
        return False

    if kernel_major > 4 or (kernel_major == 4 and kernel_minor >= 19):
        print(f"The kernel version is compatible with Cake and BBR.")
        return True
    else:
        print(f"Kernel version {kernel_version} is not supported. Requires version 4.19 or higher.")
        return False

def configure_bbr(algorithm):
    print("Setting up BBR...")

    if activate_parameters_persistent():
        print("parameters has been activated with BBR.")

    try:
        atomic_write("/etc/sysctl.conf", f"\n# {algorithm} Light Knight\n", "a")
        atomic_write("/etc/sysctl.conf", f"net.core.default_qdisc = {algorithm}\n", "a")
        atomic_write("/etc/sysctl.conf", "net.ipv4.tcp_congestion_control = bbr\n", "a")
        run_cmd(['sysctl', '-p'])
        print("BBR settings applied.")
    except Exception as e:
        print(f"Error in setting BBR: {e}")
        return False

    if not setup_qdisc(algorithm):
        return False

    if not make_qdisc_persistent(algorithm):
        return False

    return True





def delete_old_file_then_setup(algorithm):
    print("Deleting old files and setting new (+Backup)...")
    backup_path = "/etc/sysctl.confback-lightbbr"
    original_path = "/etc/sysctl.conf"

    try:
        if os.path.exists(backup_path):
            print(f"\n⚠️ WARNING: Backup '{backup_path}' already exists.")
            print("⚠️ It is recommended to restore previous settings before proceeding.")
            while True:
                confirm = input("\nDo you want to DELETE this backup and proceed? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    os.remove(backup_path)
                    print("✅ Old backup deleted.")
                    break
                elif confirm in ['n', 'no']:
                    print("❌ Operation canceled. No changes were made.")
                    input("\nPress Enter to return to the main menu...")
                    return False
                else:
                    print("❌ Invalid input. Please enter 'y' or 'n'.")

        if os.path.exists(original_path):
            shutil.copy(original_path, backup_path)
            os.remove(original_path)
            print(f"✅ Original sysctl.conf backed up to '{backup_path}' and deleted.")
        else:
            print("⚠️ Original sysctl.conf not found. Operation aborted.")
            input("\nPress Enter to return to the main menu...")
            return False

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        input("\nPress Enter to return to the main menu...")
        return False

    if configure_bbr(algorithm):
        prompt_restart()
        print("✅ BBR settings applied successfully.")
    else:
        print("❌ Failed to configure BBR settings.")


    input("\nPress Enter to return to the main menu...")
    return True






def setup_without_delete(algorithm):
    print("Setting up without deleting old files...")
    backup_path = "/etc/sysctl.confback-lightbbr"
    original_path = "/etc/sysctl.conf"

    try:
        if os.path.exists(backup_path):
            print(f"\n⚠️ WARNING: Backup '{backup_path}' already exists.")
            print("⚠️ It is recommended to restore previous settings before proceeding.")
            while True:
                confirm = input("\nDo you want to REPLACE this backup? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    os.remove(backup_path)
                    print("✅ Old backup deleted to create new one.")
                    break
                elif confirm in ['n', 'no']:
                    print("❌ Operation canceled. No changes were made.")
                    input("\nPress Enter to return to the main menu...")
                    return False
                else:
                    print("❌ Invalid input. Please enter 'y' or 'n'.")

        if not os.path.exists(backup_path):
            if os.path.exists(original_path):
                shutil.copy(original_path, backup_path)
                print(f"✅ sysctl.conf backed up to '{backup_path}'.")
            else:
                print("⚠️ Original sysctl.conf not found. Operation aborted.")
                input("\nPress Enter to return to the main menu...")
                return False

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        input("\nPress Enter to return to the main menu...")
        return False

    if configure_bbr(algorithm):
        prompt_restart()
        print("✅ BBR settings applied successfully.")
    else:
        print("❌ Failed to configure BBR settings.")

    input("\nPress Enter to return to the main menu...")
    return True




###################### End of BBr based




############################################## For Hybla Base

def configure_bbr_hybla(algorithm):
    print("Setting up hybla...")

    if activate_parameters_persistent():
        print("parameters has been activated with hybla.")

    try:
        atomic_write("/etc/sysctl.conf", f"\n# {algorithm} Light Knight\n", "a")
        atomic_write("/etc/sysctl.conf", f"net.core.default_qdisc = {algorithm}\n", "a")
        atomic_write("/etc/sysctl.conf", "net.ipv4.tcp_congestion_control = hybla\n", "a")
        run_cmd(['sysctl', '-p'])
        print("hybla settings applied.")
    except Exception as e:
        print(f"Error in setting hybla: {e}")
        return False

    if not setup_qdisc(algorithm):
        return False

    if not make_qdisc_persistent(algorithm):
        return False

    return True




def delete_old_file_then_setup_hybla(algorithm):
    print("Deleting old files and setting new (+Backup)...")
    backup_path = "/etc/sysctl.confback-lightbbr"
    original_path = "/etc/sysctl.conf"

    try:
        if os.path.exists(backup_path):
            print(f"\n⚠️ WARNING: Backup '{backup_path}' already exists.")
            print("⚠️ It is recommended to restore previous settings before proceeding.")
            while True:
                confirm = input("\nDo you want to DELETE this backup and proceed? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    os.remove(backup_path)
                    print("✅ Old backup deleted.")
                    break
                elif confirm in ['n', 'no']:
                    print("❌ Operation canceled. No changes were made.")
                    input("\nPress Enter to return to the main menu...")
                    return False
                else:
                    print("❌ Invalid input. Please enter 'y' or 'n'.")

        if os.path.exists(original_path):
            shutil.copy(original_path, backup_path)
            os.remove(original_path)
            print(f"✅ Original sysctl.conf backed up to '{backup_path}' and deleted.")
        else:
            print("⚠️ Original sysctl.conf not found. Operation aborted.")
            input("\nPress Enter to return to the main menu...")
            return False

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        input("\nPress Enter to return to the main menu...")
        return False

    if configure_bbr_hybla(algorithm):
        prompt_restart()
        print("✅ Hybla settings applied successfully.")
    else:
        print("❌ Failed to configure Hybla settings.")

    input("\nPress Enter to return to the main menu...")
    return True







def setup_without_delete_hybla(algorithm):
    print("Setting up without deleting old files...")
    backup_path = "/etc/sysctl.confback-lightbbr"
    original_path = "/etc/sysctl.conf"

    try:
        if os.path.exists(backup_path):
            print(f"\n⚠️ WARNING: Backup '{backup_path}' already exists.")
            print("⚠️ It is recommended to restore previous settings before proceeding.")
            while True:
                confirm = input("\nDo you want to REPLACE this backup? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    os.remove(backup_path)
                    print("✅ Old backup deleted to create new one.")
                    break
                elif confirm in ['n', 'no']:
                    print("❌ Operation canceled. No changes were made.")
                    input("\nPress Enter to return to the main menu...")
                    return False
                else:
                    print("❌ Invalid input. Please enter 'y' or 'n'.")

        if not os.path.exists(backup_path):
            if os.path.exists(original_path):
                shutil.copy(original_path, backup_path)
                print(f"✅ sysctl.conf backed up to '{backup_path}'.")
            else:
                print("⚠️ Original sysctl.conf not found. Operation aborted.")
                input("\nPress Enter to return to the main menu...")
                return False

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        input("\nPress Enter to return to the main menu...")
        return False

    if configure_bbr_hybla(algorithm):
        prompt_restart()
        print("✅ Hybla settings applied successfully.")
    else:
        print("❌ Failed to configure Hybla settings.")

    input("\nPress Enter to return to the main menu...")
    return True




###################### End of Hybla based

############################################# For Cubic Base
def configure_bbr_cubic(algorithm):
    print("Setting up Cubic...")

    if activate_parameters_persistent():
        print("parameters has been activated with Cubic.")

    try:
        atomic_write("/etc/sysctl.conf", f"\n# {algorithm} Light Knight\n", "a")
        atomic_write("/etc/sysctl.conf", f"net.core.default_qdisc = {algorithm}\n", "a")
        atomic_write("/etc/sysctl.conf", "net.ipv4.tcp_congestion_control = cubic\n", "a")
        run_cmd(['sysctl', '-p'])
        print("Cubic settings applied.")
    except Exception as e:
        print(f"Error in setting Cubic: {e}")
        return False

    if not setup_qdisc(algorithm):
        return False

    if not make_qdisc_persistent(algorithm):
        return False

    return True





def delete_old_file_then_setup_cubic(algorithm):
    print("Deleting old files and setting new (+Backup)...")
    backup_path = "/etc/sysctl.confback-lightbbr"
    original_path = "/etc/sysctl.conf"

    try:
        if os.path.exists(backup_path):
            print(f"\n⚠️ WARNING: Backup '{backup_path}' already exists.")
            print("⚠️ It is recommended to restore previous settings before proceeding.")
            while True:
                confirm = input("\nDo you want to DELETE this backup and proceed? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    os.remove(backup_path)
                    print("✅ Old backup deleted.")
                    break
                elif confirm in ['n', 'no']:
                    print("❌ Operation canceled. No changes were made.")
                    input("\nPress Enter to return to the main menu...")
                    return False
                else:
                    print("❌ Invalid input. Please enter 'y' or 'n'.")

        if os.path.exists(original_path):
            shutil.copy(original_path, backup_path)
            os.remove(original_path)
            print(f"✅ Original sysctl.conf backed up to '{backup_path}' and deleted.")
        else:
            print("⚠️ Original sysctl.conf not found. Operation aborted.")
            input("\nPress Enter to return to the main menu...")
            return False

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        input("\nPress Enter to return to the main menu...")
        return False

    if configure_bbr_cubic(algorithm):
        prompt_restart()
        print("✅ Cubic settings applied successfully.")
    else:
        print("❌ Failed to configure Cubic settings.")

    input("\nPress Enter to return to the main menu...")
    return True








def setup_without_delete_cubic(algorithm):
    print("Setting up without deleting old files...")
    backup_path = "/etc/sysctl.confback-lightbbr"
    original_path = "/etc/sysctl.conf"

    try:
        if os.path.exists(backup_path):
            print(f"\n⚠️ WARNING: Backup '{backup_path}' already exists.")
            print("⚠️ It is recommended to restore previous settings before proceeding.")
            while True:
                confirm = input("\nDo you want to REPLACE this backup? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    os.remove(backup_path)
                    print("✅ Old backup deleted to create new one.")
                    break
                elif confirm in ['n', 'no']:
                    print("❌ Operation canceled. No changes were made.")
                    input("\nPress Enter to return to the main menu...")
                    return False
                else:
                    print("❌ Invalid input. Please enter 'y' or 'n'.")

        if not os.path.exists(backup_path):
            if os.path.exists(original_path):
                shutil.copy(original_path, backup_path)
                print(f"✅ sysctl.conf backed up to '{backup_path}'.")
            else:
                print("⚠️ Original sysctl.conf not found. Operation aborted.")
                input("\nPress Enter to return to the main menu...")
                return False

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        input("\nPress Enter to return to the main menu...")
        return False

    if configure_bbr_cubic(algorithm):
        prompt_restart()
        print("✅ Cubic settings applied successfully.")
    else:
        print("❌ Failed to configure Cubic settings.")

    input("\nPress Enter to return to the main menu...")
    return True




###################### End of Cubic based


def restore():
    print("Restoring default settings...")
    backup_path = "/etc/sysctl.confback-lightbbr"
    original_path = "/etc/sysctl.conf"

    try:
        if not os.path.exists(backup_path):
            print(f"❌ Error: No backup found at '{backup_path}'. Restoration canceled.")
            input("Press Enter to exit...")
            return False


        if os.path.exists(original_path):
            os.remove(original_path)
        shutil.copy(backup_path, original_path)
        os.remove(backup_path)
        print(f"✅ Backup restored to sysctl.conf and removed.")


        service_path = "/etc/systemd/system/qdisc-setup.service"
        if os.path.exists(service_path):
            run_cmd(['systemctl', 'disable', 'qdisc-setup.service'])
            os.remove(service_path)
            run_cmd(['systemctl', 'daemon-reload'])
            print("✅ Systemd service removed.")
        if os.path.exists("/etc/systemd/system/multi-user.target.wants/qdisc-setup.service"):
            os.remove("/etc/systemd/system/multi-user.target.wants/qdisc-setup.service")
            print("✅ Removed multi-user service link.")


        interface = get_main_interface()
        if interface:
            try:
                run_cmd(['tc', 'qdisc', 'delete', 'dev', interface, 'root'])
                print(f"✅ Default qdisc restored on {interface}.")
            except Exception:
                print(f"⚠️ Failed to reset qdisc on {interface}. Applying 'fq'...")
                run_cmd(['tc', 'qdisc', 'replace', 'dev', interface, 'root', 'fq'])
                print(f"✅ 'fq' set on {interface}.")
        else:
            print("⚠️ No main interface found!")

        try:
            run_cmd(['sysctl', '-p'])
            print("✅ sysctl settings applied.")
        except Exception as e:
            print(f"❌ sysctl error: {e}")
            input("Press Enter to exit...")
            return False

    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        input("Press Enter to exit...")
        return False

    prompt_restart()
    input("\nPress Enter to return to the main menu...")
    return True







def run_bench_method1():
    print("Running Bench Method1...")
    run_cmd("wget -qO- bench.sh | bash", shell=True)

def run_bench_method2():
    print("Running Bench Method2...")
    run_cmd("curl -Lso- bench.sh | bash", shell=True)

def run_iperf_client():
    print("Starting Iperf3 as client...")
    run_cmd(["apt", "update"])
    run_cmd(["apt", "install", "iperf3", "-y"])
    run_cmd(["ufw", "allow", "5201"])
    server_ip = input("What is the IP address of your target server? Enter Your Target IP: ")
    run_cmd(f"iperf3 -c {server_ip} -i 1 -t 10 -P 20", shell=True)
    input("The download speed test was done. To test the upload speed, press Enter...")
    run_cmd(f"iperf3 -c {server_ip} -R -i 1 -t 10 -P 20", shell=True)
    input("The upload speed test was done. To Back to the menu, press Enter...")

def run_iperf_server():
    print("Starting Iperf3 as server...")
    run_cmd(["apt", "update"])
    run_cmd(["apt", "install", "iperf3", "-y"])
    run_cmd(["ufw", "allow", "5201"])
    run_cmd(["iperf3", "-s"])
    input("You are active as a server, please do not log out. If it is finished, to Back to the menu, press Enter...")

def run_speedtest_ookla():
    print("Downloading and running Ookla Speedtest (linux-x86_64) ...")
    run_cmd(["wget", "https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz"])
    run_cmd(["tar", "zxvf", "ookla-speedtest-1.2.0-linux-x86_64.tgz"])

    server_num = input(f"{GREEN}Enter your{RESET} {YELLOW}ookla-server number{RESET}.{GREEN} Or press Enter to let Speedtest automatically select the closest server: {RESET}")
    print(f"{CYAN}Speed ​​test starting, please wait...{RESET}")
    if not server_num:
        run_cmd(["./speedtest"])
    else:
        run_cmd(["./speedtest", "-s", server_num])

    try:
        os.remove("ookla-speedtest-1.2.0-linux-x86_64.tgz")
        if os.path.exists("ookla-speedtest-1.2.0-linux-x86_64"):
            shutil.rmtree("ookla-speedtest-1.2.0-linux-x86_64")
        if os.path.exists("./speedtest"):
            os.remove("./speedtest")
        for filename in os.listdir("."):
            if "ookla" in filename or filename.startswith("speedtest"):
                if os.path.isfile(filename):
                    os.remove(filename)
                elif os.path.isdir(filename):
                    shutil.rmtree(filename)
    except Exception as e:
        print(f"Error cleaning up files: {e}")
    input(f"{GREEN}SpeedTest Done and files removed, to Back to the menu, press Enter{RESET}")








# -------------------- Uninstall Script --------------------

def uninstall_script():

    try:

        paths = [
            "/opt/lightbbr",
            "/usr/local/bin/lbbr",
            "/etc/lightbbr",
            "/var/log/lightbbr.log"
        ]
        
        print("\n" + "="*40)
        print("⚠️CAUTION: SCRIPT UNINSTALL⚠️".center(40))
        print("="*40)
        

        existing = [p for p in paths if os.path.exists(p)]
        if not existing:
            print("ℹ️ No installation found!")
            return True
            
        for p in existing:
            print(f"• {p}")
        

        confirm = input("\nDelete ALL? (y/N): ").strip().lower()
        if confirm != 'y':
            print("🚫 Cancelled!")
            return False
        

        for path in existing:
            try:
                if os.path.islink(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                print(f"✓ {path}")
            except Exception as e:
                print(f"✗ {path} - {str(e)}")
                sys.exit(1)
        

        print("Re Install :")
        print("\nbash <(curl -fsSL https://raw.githubusercontent.com/kalilovers/LightKnightBBR/main/install.sh)")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)






 
# -------------------- UpdateScript --------------------
 
 
class UpdateScript:


    @staticmethod
    def get_latest_release_info():

        import requests
        try:
            response = requests.get(RELEASE_API_URL, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Network Error: {str(e)}")
            return None



    @staticmethod
    def backup_file():

        if not os.path.exists(INSTALL_PATH):
            print(f"Error: Main script not found at {INSTALL_PATH}")
            return False
        try:
            backup_path = f"{INSTALL_PATH}.bak"
            os.replace(INSTALL_PATH, backup_path)
            print(f"Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"Backup failed: {str(e)}")
            return None




    @staticmethod
    def download_asset(asset_url):

        import requests
        try:
            response = requests.get(asset_url, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Download failed: {str(e)}")
            return None



    @staticmethod
    def update_script():

        release_info = UpdateScript.get_latest_release_info()
        if not release_info:
            return False

        latest_version = release_info.get("tag_name", "").lstrip("v")
        if VERSION == latest_version:
            print("✓ Already up-to-date")
            return True


        asset = next((a for a in release_info.get("assets", []) 
                    if a.get("name") == "bbr.py"), None)
        if not asset:
            print("✗ Asset not found")
            return False

        temp_path = None
        backup_path = None
        try:

            backup_path = UpdateScript.backup_file()
            if not backup_path:
                return False


            new_script = UpdateScript.download_asset(asset["browser_download_url"])
            if not new_script:
                raise RuntimeError("Download failed")


            temp_path = f"{INSTALL_PATH}.tmp"
            with open(temp_path, "wb") as f:
                f.write(new_script)


            os.replace(temp_path, INSTALL_PATH)
            os.chmod(INSTALL_PATH, 0o755)
            print("✓ Update successful")


            os.remove(backup_path)
            return True

        except Exception as e:
            print(f"✗ Critical error: {str(e)}. Restoring backup...")

            if backup_path and os.path.exists(backup_path):
                os.replace(backup_path, INSTALL_PATH)
                print("✓ Previous version restored")
            return False

        finally:

            for path in [temp_path, backup_path]:
                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass



    @staticmethod
    def handle_script_update():
        print(f"{'―'*30}")
        print("       Update Script")
        print(f"{'―'*30}")


        choice = input("Check for updates? [Y/n] ").strip().lower()
        
        if choice not in {'', 'y'}:
            print("Update cancelled")
            return

        try:
            success = UpdateScript.update_script()
            if success:
                print(f"\nUpdate applied successfully! Run the script again using: {CYAN}lbbr{RESET}")
                sys.exit(0)
            else:
                print("\nUpdate check completed")
        except Exception as e:
            print(f"\nFatal error: {str(e)}")
        

        input("Press Enter to return to the main menu...")
 












def main():
    if os.geteuid() != 0:
        print("⚠️ This script requires root access. Please run with 'sudo' .")
        sys.exit(1)

    try:
        while True:
            show_main_menu()
            choice = input(f"{CYAN}Please enter your choice: {RESET}")

            if choice == '0':
                while True:
                    show_status_menu()
                    status_choice = input("Please enter your choice (0 to go back): ")
                    if status_choice == '0':
                        break
                    else:
                        print("Invalid choice, please try again.")
            elif choice == '1':
                while True:
                    show_bbr_menu()
                    bbr_choice = input("Please enter your choice: ")
                    if bbr_choice == '1':
                        while True:
                            show_fq_menu()
                            fq_choice = input("Please enter your choice: ")
                            if fq_choice == '1':
                                if check_kernel_and_os():
                                    delete_old_file_then_setup("fq")
                            elif fq_choice == '2':
                                if check_kernel_and_os():
                                    setup_without_delete("fq")
                            elif fq_choice == '0':
                                break
                            else:
                                print("Invalid choice, please try again.")
                    elif bbr_choice == '2':
                        while True:
                            show_fq_codel_menu()
                            fq_codel_choice = input("Please enter your choice: ")
                            if fq_codel_choice == '1':
                                if check_kernel_and_os():
                                    delete_old_file_then_setup("fq_codel")
                            elif fq_codel_choice == '2':
                                if check_kernel_and_os():
                                    setup_without_delete("fq_codel")
                            elif fq_codel_choice == '0':
                                break
                            else:
                                print("Invalid choice, please try again.")
                    elif bbr_choice == '3':
                        while True:
                            show_cake_menu()
                            cake_choice = input("Please enter your choice: ")
                            if cake_choice == '1':
                                if check_kernel_and_os_cake():
                                    delete_old_file_then_setup("cake")
                            elif cake_choice == '2':
                                if check_kernel_and_os_cake():
                                    setup_without_delete("cake")
                            elif cake_choice == '0':
                                break
                            else:
                                print("Invalid choice, please try again.")
                    elif bbr_choice == '0':
                        break
                    else:
                        print("Invalid choice, please try again.")
            elif choice == '2':
                while True:
                    show_hybla_menu()
                    hybla_choice = input("Please enter your choice: ")
                    if hybla_choice == '1':
                        while True:
                            show_fq_menu()
                            fq_choice = input("Please enter your choice: ")
                            if fq_choice == '1':
                                if check_kernel_and_os():
                                    delete_old_file_then_setup_hybla("fq")
                            elif fq_choice == '2':
                                if check_kernel_and_os():
                                    setup_without_delete_hybla("fq")
                            elif fq_choice == '0':
                                break
                            else:
                                print("Invalid choice, please try again.")
                    elif hybla_choice == '2':
                        while True:
                            show_fq_codel_menu()
                            fq_codel_choice = input("Please enter your choice: ")
                            if fq_codel_choice == '1':
                                if check_kernel_and_os():
                                    delete_old_file_then_setup_hybla("fq_codel")
                            elif fq_codel_choice == '2':
                                if check_kernel_and_os():
                                    setup_without_delete_hybla("fq_codel")
                            elif fq_codel_choice == '0':
                                break
                            else:
                                print("Invalid choice, please try again.")
                    elif hybla_choice == '3':
                        while True:
                            show_cake_menu()
                            cake_choice = input("Please enter your choice: ")
                            if cake_choice == '1':
                                if check_kernel_and_os_cake():
                                    delete_old_file_then_setup_hybla("cake")
                            elif cake_choice == '2':
                                if check_kernel_and_os_cake():
                                    setup_without_delete_hybla("cake")
                            elif cake_choice == '0':
                                break
                            else:
                                print("Invalid choice, please try again.")
                    elif hybla_choice == '0':
                        break
                    else:
                        print("Invalid choice, please try again.")
            elif choice == '3':
                while True:
                    show_cubic_menu()
                    cubic_choice = input("Please enter your choice: ")
                    if cubic_choice == '1':
                        while True:
                            show_fq_menu()
                            fq_choice = input("Please enter your choice: ")
                            if fq_choice == '1':
                                if check_kernel_and_os():
                                    delete_old_file_then_setup_cubic("fq")
                            elif fq_choice == '2':
                                if check_kernel_and_os():
                                    setup_without_delete_cubic("fq")
                            elif fq_choice == '0':
                                break
                            else:
                                print("Invalid choice, please try again.")
                    elif cubic_choice == '2':
                        while True:
                            show_fq_codel_menu()
                            fq_codel_choice = input("Please enter your choice: ")
                            if fq_codel_choice == '1':
                                if check_kernel_and_os():
                                    delete_old_file_then_setup_cubic("fq_codel")
                            elif fq_codel_choice == '2':
                                if check_kernel_and_os():
                                    setup_without_delete_cubic("fq_codel")
                            elif fq_codel_choice == '0':
                                break
                            else:
                                print("Invalid choice, please try again.")
                    elif cubic_choice == '3':
                        while True:
                            show_cake_menu()
                            cake_choice = input("Please enter your choice: ")
                            if cake_choice == '1':
                                if check_kernel_and_os_cake():
                                    delete_old_file_then_setup_cubic("cake")
                            elif cake_choice == '2':
                                if check_kernel_and_os_cake():
                                    setup_without_delete_cubic("cake")
                            elif cake_choice == '0':
                                break
                            else:
                                print("Invalid choice, please try again.")
                    elif cubic_choice == '0':
                        break
                    else:
                        print("Invalid choice, please try again.")
            elif choice == '4':
                restore()
            elif choice == '5':
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


            elif choice == '6':
                UpdateScript.handle_script_update()



            elif choice == '7':
                success = uninstall_script()
                
                if success:
                    print("\n✅ Uninstall completed successfully!")
                    sys.exit(0)
                else:
                    print("\n⚠️ Uninstall completed with warnings!")




            elif choice == 'q':
                print("Goodbye!")
                break


            else:
                input(f"{RED}Invalid choice, please try again.{RESET}")
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()
if __name__ == "__main__":
    if "--uninstall" in sys.argv:
        if os.geteuid() != 0:
            print("Please run with sudo!")
            sys.exit(1)
        uninstall_script()
        sys.exit(0)
    else:
        main()
