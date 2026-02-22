#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014 - 2019, Philip Müller <philm@manjaro.org>
#   Copyright 2016, Artoo <artoo@manjaro.org>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import libcalamares
import subprocess

from shutil import copy2, copytree
from os.path import join, exists
from os import rename, makedirs
from libcalamares.utils import target_env_call, target_env_process_output


class ConfigController:
    def __init__(self):
        self.__root = libcalamares.globalstorage.value("rootMountPoint")
        self.__keyrings = libcalamares.job.configuration.get('keyrings', [])

    @property
    def root(self):
        return self.__root

    @property
    def keyrings(self):
        return self.__keyrings

    def init_keyring(self):
        target_env_call(["pacman-key", "--init"])

    def populate_keyring(self):
        target_env_call(["pacman-key", "--populate"])

    def terminate(self, proc):
        target_env_call(['killall', '-9', proc])

    def copy_file(self, file):
        if exists("/" + file):
            copy2("/" + file, join(self.root, file))

    def copy_folder(self, source, target):
        if exists("/" + source):
            copytree("/" + source, join(self.root, target), symlinks=True, dirs_exist_ok=True)

    def umount(self, mp):
        subprocess.call(["umount", "-l", join(self.root, mp)])

    def mount(self, mp):
        subprocess.call(["mount", "-B", "/" + mp, join(self.root, mp)])

    def rmdir(self, dir):
        subprocess.call(["rm", "-Rf", join(self.root, dir)])

    def mkdir(self, dir):
        subprocess.call(["mkdir", "-p", join(self.root, dir)])

    def find_xdg_directory(self, user, type):
        output = []
        target_env_process_output(["su", "-lT", user, "xdg-user-dir", type], output)
        return output[0].strip()

    def mark_orphans_as_explicit(self) -> None:

        """
        Mark all packages that pacman considers 'orphaned' as explicit.

        This is necessary because in the live ISO (airootfs),
        all packages are normally marked as dependencies (--asdeps),
        which causes 'pacman -Qdtq' to list even the entire graphical environment after installation.

        """

        libcalamares.utils.debug("Marking orphaned packages as explicit in the installed system...")
        libcalamares.utils.target_env_call([
            "sh", "-c",
            "orphans=$(pacman -Qdtq); "
            "if [ -n \"$orphans\" ]; then pacman -D --asexplicit $orphans; fi"
        ])
        libcalamares.utils.debug("Package marking completed.")

    # ---------------------------------------------------------
    # MICROCODE FIX COMPLETO — COMPATIBLE CON MKINITCPIO
    # ---------------------------------------------------------
    def handle_ucode(self):
        vendor = subprocess.getoutput(
            "hwinfo --cpu | awk -F'\"' '/Vendor:/ {print $2; exit}'"
        ).strip()

        libcalamares.utils.debug(f"Detected CPU vendor: {vendor}")

        if vendor == "AuthenticAMD":
            libcalamares.utils.debug("Removing intel-ucode for AMD CPU.")
            target_env_call(["pacman", "-R", "--noconfirm", "intel-ucode"])

        elif vendor == "GenuineIntel":
            libcalamares.utils.debug("Removing amd-ucode for Intel CPU.")
            target_env_call(["pacman", "-R", "--noconfirm", "amd-ucode"])

        else:
            libcalamares.utils.debug("Unknown CPU vendor, skipping microcode removal.")

        # Siempre regenerar initramfs con mkinitcpio
        libcalamares.utils.debug("Regenerating initramfs with mkinitcpio -P ...")
        target_env_call(["mkinitcpio", "-P"])
        libcalamares.utils.debug("mkinitcpio completed.")

    # ---------------------------------------------------------

    def run(self) -> None:
        self.init_keyring()
        self.populate_keyring()

        # --- Microcode FIX ---
        self.handle_ucode()

        # Kill gpg-agent
        self.terminate('gpg-agent')

        # Mark orphan packages
        self.mark_orphans_as_explicit()

        return None


def run():
    config = ConfigController()
    return config.run()
