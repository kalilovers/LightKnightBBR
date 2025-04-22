#!/bin/bash
# Official Installation Script for LightKnightBBR (Public Version)
# Version: 1.3.1 (Installer Optimized)
# License: MIT

set -euo pipefail
trap 'echo "Error: Script failed at line $LINENO"; exit 1' ERR

REPO_OWNER="kalilovers"
REPO_NAME="LightKnightBBR"
INSTALL_DIR="/opt/lightbbr"
SCRIPT_NAME="lbbr"
MIN_DEBIAN=10
MIN_UBUNTU=18.04

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ---------------------- Core Functions ----------------------
die() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

check_os() {
    echo -e "${YELLOW}Checking OS compatibility...${NC}"
    
    if ! [[ -f /etc/os-release ]]; then
        die "Unsupported operating system"
    fi

    source /etc/os-release
    case $ID in
        debian)
            if (( $(echo "$VERSION_ID < $MIN_DEBIAN" | bc -l) )); then
                die "Debian $VERSION_ID is not supported (Minimum: Debian $MIN_DEBIAN)"
            fi
            ;;
        ubuntu)
            if (( $(echo "$VERSION_ID < $MIN_UBUNTU" | bc -l) )); then
                die "Ubuntu $VERSION_ID is not supported (Minimum: Ubuntu $MIN_UBUNTU)"
            fi
            ;;
        *)
            die "Only Debian/Ubuntu distributions are supported"
            ;;
    esac
}

check_privileges() {
    if [[ $EUID -ne 0 ]]; then
        if ! sudo -n true 2>/dev/null; then
            echo -e "${YELLOW}This operation requires root privileges.${NC}"
            sudo -v || die "Failed to get sudo privileges"
        fi
    fi
}

test_connection() {
    local url="$1"
    local ipv4_url="${url}"
    local ipv6_url="${url}"

    # Test IPv4 connection
    if curl --connect-timeout 5 -4 -s -o /dev/null -w "%{http_code}" "$ipv4_url" >/dev/null; then
        echo "IPv4"
        return
    fi

    # Test IPv6 connection
    if curl --connect-timeout 5 -6 -s -o /dev/null -w "%{http_code}" "$ipv6_url" >/dev/null; then
        echo "IPv6"
        return
    fi

    die "Failed to connect using both IPv4 and IPv6"
}

install_dependencies() {
    export DEBIAN_FRONTEND=noninteractive
    export APT_LISTCHANGES_FRONTEND=none

    local PKGS=(
        curl wget sudo ed
        iproute2 iptables
        python3 python3-pip python3-venv
        jq
    )

    echo -e "${GREEN}Updating package lists...${NC}"
    sudo apt-get update -qq 2>/dev/null || {
        echo -e "${YELLOW}Warning: Some package lists failed to update, continuing anyway...${NC}" >&2
    }

    echo -e "${GREEN}Installing required packages...${NC}"
    sudo apt-get install -y --no-install-recommends -qq \
        -o Dpkg::Options::="--force-confold" \
        -o Dpkg::Options::="--force-unsafe-io" \
        "${PKGS[@]}" 2>/dev/null || {
        echo -e "${YELLOW}Warning: Some packages may have failed to install${NC}" >&2
    }

    echo -e "${GREEN}Installing Python packages...${NC}"
    # Test connection and determine protocol
    local protocol
    protocol=$(test_connection "https://files.pythonhosted.org")

    if [[ "$protocol" == "IPv4" ]]; then
        python3 -m pip install --user --disable-pip-version-check --no-warn-script-location \
            -q requests packaging || {
            echo -e "${RED}Python package installation failed!${NC}" >&2
            exit 1
        }
    elif [[ "$protocol" == "IPv6" ]]; then
        python3 -m pip install --user --disable-pip-version-check --no-warn-script-location \
            -q requests packaging -i https://mirrors.aliyun.com/pypi/simple/ || {
            echo -e "${RED}Python package installation failed!${NC}" >&2
            exit 1
        }
    fi

    echo -e "${GREEN}Verifying core components...${NC}"
    local critical_commands=("python3" "curl" "git" "jq")
    local missing=()
    
    for cmd in "${critical_commands[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            missing+=("$cmd")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        die "Missing critical components: ${missing[*]}"
    fi

    echo -e "\n${GREEN}All critical dependencies verified!${NC}"
}

fetch_latest_release() {
    echo -e "${YELLOW}Fetching latest release info...${NC}" >&2
    local api_url="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest"

    # Test connection and determine protocol
    local protocol
    protocol=$(test_connection "$api_url")

    # Use the appropriate protocol for curl
    if [[ "$protocol" == "IPv4" ]]; then
        local release_info
        release_info=$(curl -4 -fsSL "$api_url" 2>/dev/null) || die "Failed to connect to GitHub"
    elif [[ "$protocol" == "IPv6" ]]; then
        local release_info
        release_info=$(curl -6 -fsSL "$api_url" 2>/dev/null) || die "Failed to connect to GitHub"
    fi

    if ! jq -e '.assets' <<< "$release_info" >/dev/null; then
        die "Invalid GitHub API response"
    fi

    local asset_url
    asset_url=$(jq -r '.assets[] | select(.name == "bbr.py").browser_download_url' <<< "$release_info" | tr -d '\r\n')
    
    [[ -z "$asset_url" || "$asset_url" == "null" ]] && die "Asset 'bbr.py' not found"
    
    echo "$asset_url"
}

setup_application() {
    echo -e "${YELLOW}Setting up LightKnightBBR...${NC}"
    
    sudo mkdir -p "$INSTALL_DIR" || die "❌ Directory creation failed"
    sudo chmod 755 "$INSTALL_DIR"

    echo -e "${YELLOW}Downloading latest release...${NC}"
    local download_url
    download_url=$(fetch_latest_release)
    
    [[ "$download_url" =~ ^https://github.com/.*/releases/download/.*/bbr.py$ ]] || die "❌ Invalid URL pattern"

    # Test connection and determine protocol
    local protocol
    protocol=$(test_connection "$download_url")

    local temp_file
    temp_file=$(mktemp -p "$INSTALL_DIR" bbr.py.XXXXXXXXXX)

    if [[ "$protocol" == "IPv4" ]]; then
        if ! sudo curl -4 -fsSL --retry 3 --retry-delay 2 --max-time 60 -o "$temp_file" "$download_url"; then
            sudo rm -f "$temp_file"
            die "❌ Download failed! Check network connection"
        fi
    elif [[ "$protocol" == "IPv6" ]]; then
        if ! sudo curl -6 -fsSL --retry 3 --retry-delay 2 --max-time 60 -o "$temp_file" "$download_url"; then
            sudo rm -f "$temp_file"
            die "❌ Download failed! Check network connection"
        fi
    fi

    local backup_file
    if [[ -f "${INSTALL_DIR}/bbr.py" ]]; then
        backup_file="${INSTALL_DIR}/bbr.py.bak.$(date +%s)"
        sudo mv -f "${INSTALL_DIR}/bbr.py" "$backup_file" || die "❌ Backup failed"
        echo -e "${GREEN}✔ Backup created: $(basename "$backup_file")${NC}"
    fi

    if sudo mv -f "$temp_file" "${INSTALL_DIR}/bbr.py"; then
        sudo rm -f "$temp_file"
    else
        [[ -n "$backup_file" ]] && sudo mv -f "$backup_file" "${INSTALL_DIR}/bbr.py"
        sudo rm -f "$temp_file"
        die "❌ Atomic replacement failed"
    fi

    sudo chmod 755 "${INSTALL_DIR}/bbr.py"
    sudo ln -sfT "${INSTALL_DIR}/bbr.py" "/usr/local/bin/${SCRIPT_NAME}" || die "❌ Symlink creation failed"

    sudo rm -f "${INSTALL_DIR}"/bbr.py.bak.* 2>/dev/null

    echo -e "\n${GREEN}✅ Successfully installed latest version!${NC}"
}

main() {
    check_os
    check_privileges
    install_dependencies
    setup_application

    echo -e "\n${GREEN}Github : https://github.com/${REPO_OWNER}/${REPO_NAME}${NC}"
    echo -e "\nRun With : ${YELLOW}${SCRIPT_NAME}${NC}\n"
}

main
