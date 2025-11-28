packer {
    required_plugins {
        qemu = {
            version = "~> 1"
            source  = "github.com/hashicorp/qemu"
        }
        virtualbox = {
            version = "~> 1"
            source  = "github.com/hashicorp/virtualbox"
        }
        vagrant = {
            version = "~> 1"
            source = "github.com/hashicorp/vagrant"
        }
    }
}

source "qemu" "practice-vm" {
    iso_url = "https://releases.ubuntu.com/noble/ubuntu-24.04.3-live-server-amd64.iso"
    iso_checksum            = "file:https://releases.ubuntu.com/noble/SHA256SUMS"
    disk_size = "10000M"
    memory = "4096"
    cores = 4
    threads = 4
    output_directory = "build"
    format = "qcow2"
    vm_name = "practice-vm"
    net_device        = "virtio-net"
    disk_interface    = "virtio"
    headless = true
    vnc_bind_address = "0.0.0.0"
    vnc_use_password = true
    accelerator       = "kvm"
    boot_wait         = "10s"
    http_directory = "cloud-init"
    boot_steps = [
        ["<wait>e", "Wait for GRUB menu, and enter command edit mode."],
        ["<wait><down><down><down><end><left><left><left><left> autoinstall ip=dhcp cloud-config-url=http://{{.HTTPIP}}:{{.HTTPPort}}/autoinstall.yaml<wait><f10><wait>", "Enter the command to bootstrap the autoinstall.yaml"]
    ]
    communicator = "ssh"
    ssh_pty = true
    ssh_username = "ubuntu"
    ssh_password = "ubuntu"
    ssh_timeout = "10h"
    shutdown_command  = "echo 'ubuntu' | sudo -S shutdown -P now"
    shutdown_timeout = "10h"
}

source "virtualbox-iso" "practice-vm" {
    vm_name = "practice-vm"
    guest_os_type = "Ubuntu_64"
    hard_drive_discard = true
    format = "ova"
    iso_url = "https://releases.ubuntu.com/noble/ubuntu-24.04.3-live-server-amd64.iso"
    iso_checksum            = "file:https://releases.ubuntu.com/noble/SHA256SUMS"
    output_directory = "build"
    headless = true
    memory = 4096
    cpus = 4
    vboxmanage = [
        ["modifyvm", "{{.Name}}", "--vram", "128"]
    ]
    vrdp_bind_address = "0.0.0.0"
    communicator = "ssh"
    ssh_pty = true
    ssh_username = "ubuntu"
    ssh_password = "ubuntu"
    ssh_timeout = "10h"
    shutdown_command  = "echo 'ubuntu' | sudo -S shutdown -P now"
    shutdown_timeout = "10h"
    http_directory = "cloud-init"
    boot_command = [
        "<wait>e",
        "<wait><down><down><down><end><left><left><left><left> autoinstall ip=dhcp cloud-config-url=http://{{.HTTPIP}}:{{.HTTPPort}}/autoinstall.yaml<wait><f10><wait>"
    ]
}

build {
    sources = ["sources.qemu.practice-vm", "sources.virtualbox-iso.practice-vm"]

    # Setup for development
    provisioner "shell" {
        inline = [
            # Fix the boot lagging issue (we already have NetworkManager)
            "echo 'ubuntu' | sudo -S systemctl disable systemd-networkd",
            # "echo 'ubuntu' | sudo -S systemctl disable NetworkManager-wait-online.service",

        ]
    }

    # Clean packages and logs
    provisioner "shell" {
        inline = [
            "echo 'ubuntu' | sudo -S apt-get autoremove -y",
            "echo 'ubuntu' | sudo -S apt-get clean",
            "echo 'ubuntu' | sudo -S rm -rf /var/log/*",
            "echo 'ubuntu' | sudo -S rm -rf /var/cache/apt/*",
            "echo 'ubuntu' | sudo -S journalctl --vacuum-size=1M",
            "echo 'ubuntu' | sudo -S rm -f /swapfile || true",
            "echo 'ubuntu' | sudo -S fstrim /"
        ]
    }

    # Zero free space (big compression win)
    provisioner "shell" {
        inline = [
            "echo 'ubuntu' | sudo -S dd if=/dev/zero of=/EMPTY bs=1M || true",
            "echo 'ubuntu' | sudo -S rm -f /EMPTY"
        ]
    }

    post-processor "vagrant" {
        keep_input_artifact = true
        output = "build/{{.BuildName}}-{{.Provider}}.box"
        compression_level = 9
    }
}
