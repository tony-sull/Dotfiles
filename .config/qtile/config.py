import os
import socket
import subprocess
from libqtile import qtile, bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401
from custom.pomodoro import Pomodoro as CustomPomodoro
from custom.windowname import WindowName as CustomWindowName

mod = "mod4"                  # Sets mod key to SUPER/WINDOWS
terminal = "alacritty"         # My terminal of choice
dmscripts = "/home/tony/.dmscripts/"   # Root directory for dmenu scripts

keys = [
    ### The essentials
    Key([mod], "Return",
        lazy.spawn(terminal),
        desc="Launches My Terminal"
        ),
    Key([mod, "shift"], "Return",
        lazy.spawn("dmenu_run -p 'Run: '"),
        desc="Run Launcher"
        ),
    Key([mod], "Tab",
        lazy.next_layout(),
        desc="Toggle thorugh layouts"
        ),
    Key([mod, "shift"], "c",
        lazy.window.kill(),
        desc="Kill active window"
        ),
    Key([mod, "shift"], "r",
        lazy.restart(),
        desc="Restart Qtile"
        ),
    Key([mod, "shift"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"
        ),
    Key(["control", "shift"], "e",
        lazy.spawn("emacsclient -c -a emacs"),
        desc="Doom Emacs"
        ),
    ### Switch focus of monitors
    Key([mod], "period",
        lazy.next_screen(),
        desc="Move focus to next monitor"
        ),
    Key([mod], "comma",
        lazy.prev_screen(),
        desc="Move focus to previous monitor"
        ),
    ### Treetab controls
    Key([mod, "control"], "k",
        lazy.layout.section_up(),
        desc="Move up a section in treetab"
        ),
    Key([mod, "control"], "j",
        lazy.layout.section_down(),
        desc="Move down a section in treetab"
        ),
    ### Window controls
    Key([mod], "k",
        lazy.layout.down(),
        desc="Move focus down in current stack pane"
        ),
    Key([mod], "j",
        lazy.layout.up(),
        desc="Move focus up in current stack pane"
        ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_down(),
        desc="Move windows down in current stack"
        ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_up(),
        desc="Move windows up in current stack"
        ),
    Key([mod], "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc="Shrink window (MonadTall), decrease number in master pane (Tile)"
        ),
    Key([mod], "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc="Expand window (MonadTall), increase number in master pane (Tile)"
        ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc="normalize window size ratios"
        ),
    Key([mod], "m",
        lazy.layout.maximize(),
        desc="toggle window between minimum and maximum sizes"
        ),
    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc="toggle floating"
        ),
    Key([mod, "shift"], "m",
        lazy.window.toggle_fullscreen(),
        desc="toggle fullscreen"
        ),
    ### Stack controls
    Key([mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc="Switch which side main pane occupies (XmonadTall)"
        ),
    Key([mod], "space",
        lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"
        ),
    Key([mod, "control"], "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"
        ),
    ### Emacs programs launched using hte key chord CTRL+e followed by 'key'
    KeyChord(["control"], "e", [
        Key([], "e",
            lazy.spawn("emacsclient -c -a 'emacs'"),
            desc="Launch Emacs"
            ),
        Key([], "d",
            lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'"),
            desc="Launch dired inside Emacs"
            )
    ]),
    ### Dmenu scripts launched using the key chord SUPER+p followed by 'key'
    KeyChord([mod], "p", [
        Key([], "i",
            lazy.spawn(dmscripts+"dmscrot"),
            desc="Take screenshots via dmenu"
            ),
        Key([], "k",
            lazy.spawn(dmscripts+"dmkill"),
            desc="Kill processes via dmenu"
            ),
        Key([], "l",
            lazy.spawn(dmscripts+"dmlogout"),
            desc="A logout menu"
            ),
        Key([], "m",
            lazy.spawn(dmscripts+"dman"),
            desc="Search manpages in dmenu"
            ),
        Key([], "s",
            lazy.spawn(dmscripts+"dmsearch"),
            desc="Search various search engines via dmenu"
            ),
        Key([], "v",
            lazy.spawn(dmscripts+"dmnord"),
            desc="Manage NordVPN connections"
            )
    ]),
    ### Thinkpad function keys
    Key([], "XF86AudioMute",
        lazy.spawn("amixer -D pulse set Master toggle")
        ),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("amixer -D pulse set Master 5%-")
        ),
    Key([mod], "XF86AudioLowerVolume",
        lazy.spawn("amixer -D pulse set Master 1%-")
        ),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -D pulse set Master 5%+")
        ),
    Key([mod], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -D pulse set Master 1%+")
        ),
    Key([], "XF86AudioMicMute",
        lazy.spawn("amixer -D pulse set Capture toggle")
        ),
    Key([], "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl -d 'amdgpu_bl0' set 5%+")
        ),
    Key([mod], "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl -d 'amdgpu_bl0' set 1%+")
        ),
    Key([], "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl -d 'amdgpu_bl0' set 5%-")
        ),
    Key([mod], "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl -d 'amdgpu_bl0' set 1%-")
        )
]

### Helper functions
def update():
    qtile.cmd_spawn(terminal + "-e yay")

def open_powermenu():
    qtile.cmd_spawn(dmscripts + "dmlogout")

def nordvpn():
    return (
        subprocess.check_output(["./.config/qtile/get-nordvpn.sh"])
        .decode("utf-8")
        .strip()
    )

def bluetooth():
    return (
        subprocess.check_output(["./.config/qtile/system-bluetooth-bluetoothctl.sh"])
        .decode("utf-8")
        .strip()
    )

def toggle_bluetooth():
    qtile.cmd_spawn("./.config/qtile/system-bluetooth-bluetoothctl.sh --toggle")


def open_bt_menu():
    qtile.cmd_spawn("blueman-manager")

def open_wifi_menu():
    qtile.cmd_spawn("networkmanager_dmenu")

def open_vpn_menu():
    qtile.cmd_spawn(dmscripts+"dmnord")

# Define colors

colors = [
    ["#2e3440", "#2e3440"],  # 0  background
    ["#d8dee9", "#d8dee9"],  # 1  foreground
    ["#3b4252", "#3b4252"],  # 2  background lighter
    ["#bf616a", "#bf616a"],  # 3  red
    ["#a3be8c", "#a3be8c"],  # 4  green
    ["#ebcb8b", "#ebcb8b"],  # 5  yellow
    ["#81a1c1", "#81a1c1"],  # 6  blue
    ["#b48ead", "#b48ead"],  # 7  magenta
    ["#88c0d0", "#88c0d0"],  # 8  cyan
    ["#e5e9f0", "#e5e9f0"],  # 9  white
    ["#4c566a", "#4c566a"],  # 10 grey
    ["#d08770", "#d08770"],  # 11 orange
    ["#8fbcbb", "#8fbcbb"],  # 12 super cyan
    ["#5e81ac", "#5e81ac"],  # 13 super blue
    ["#242831", "#242831"],  # 14 super dark background
]

### Define groups and screens

workspaces = [
    { "name": "", "key": "1", "matches": [Match(wm_class="firefox")] },
    { "name": "", "key": "2", "matches": [Match(wm_class="thunderbird")] },
    { "name": "", "key": "3", "matches": [Match(wm_class="libreoffice"), Match(wm_class="org.pwmt.zathura")] },
    { "name": "", "key": "4", "matches": [Match(wm_class="emacs"), Match(wm_class="code-oss")] },
    { "name": "", "key": "5", "matches": [Match(wm_class="Alacritty")] },
    { "name": "", "key": "6", "matches": [Match(wm_class="signal-desktop"), Match(wm_class="discord")] },
    { "name": "", "key": "7", "matches": [Match(title="GNU Image Manipulation Program"), Match(wm_class="figma-linux")] },
    { "name": "", "key": "8", "matches": [Match(wm_class="com.bitwarden.desktop")] }
]

groups = []

for workspace in workspaces:
    ws_matches = workspace["matches"] if "matches" in workspace else None
    ws_layout = workspace["layout"] if "layout" in workspace else "monadtall"
    groups.append(Group(workspace["name"], matches=ws_matches, layout=ws_layout))
    keys.append(
        Key(
            [mod],
            workspace["key"],
            lazy.group[workspace["name"]].toscreen(),
            desc="Focus this desktop",
        )
    )
    keys.append(
        Key(
            [mod, "shift"],
            workspace["key"],
            lazy.window.togroup(workspace["name"]),
            desc="Move focused window to another group",
        )
    )

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors[6][0].replace("#", ""),
    "border_normal": colors[0][0].replace("#", ""),
    "font": "FiraCode Nerd Font",
    "grow_amount": 2
}

layouts = [
        layout.MonadTall(**layout_theme),
        layout.Max(**layout_theme),
        layout.Tile(shift_windows=True, **layout_theme),
        layout.Stack(num_stacks=2),
        layout.TreeTab(
            **layout_theme,
            fontsize = 16,
            sections = ["FIRST", "SECOND"],
            section_fontsize = 18,
            section_fg = colors[1],
            bg_color = "2e3440",
            active_bg = colors[14],
            active_fg = colors[1],
            inactive_bg = colors[0],
            inactive_fg = colors[1],
            ),
        layout.Floating(**layout_theme)
]

prompt = "{0}@{1}".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font='FiraCode Nerd Font',
    fontsize=18,
    padding=3,
    background=colors[0]
)
extension_defaults = widget_defaults.copy()

def separator(padding, size_percent = 50):
    return widget.Sep(
        linewidth = 0,
        foreground = colors[2],
        background = colors[0],
        padding = padding,
        size_percent = size_percent
    )

def group_head():
    return widget.TextBox(
            text = "",
            foreground = colors[14],
            background = colors[0],
            fontsize = 28,
            padding = 0
    )

def group_tail():
    return widget.TextBox(
        text = "",
        foreground = colors[14],
        background = colors[0],
        fontsize = 28,
        padding = 0
    )

group_box_settings = {
    "padding": 5,
    "borderwidth": 4,
    "active": colors[6],
    "inactive": colors[10],
    "disable_drag": True,
    "rounded": True,
    "highlight_color": colors[2],
    "block_highlight_text_color": colors[1],
    "highlight_method": "block",
    "this_current_screen_border": colors[14],
    "this_screen_border": colors[7],
    "other_current_screen_border": colors[14],
    "other_screen_border": colors[14],
    "foreground": colors[1],
    "background": colors[14],
    "urgent_border": colors[3],
    "fontsize": 24,
    "font": "Font Awesome 5 Brands",
}

def init_widgets_list():
    widgets_list = [
        separator(20, 40),
        group_head(),
#        widget.GroupBox(**group_box_settings),
        widget.GroupBox(
            visible_groups = [""],
            **group_box_settings
        ),
        widget.GroupBox(
            visible_groups = ["", "", "", "", ""],
            **group_box_settings
        ),
        widget.GroupBox(
            visible_groups = ["", ""],
            **group_box_settings
        ),
        group_tail(),
        separator(10),
        group_head(),
        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground = colors[2],
            background = colors[14],
            padding = -2,
            scale = 0.55
        ),
        group_tail(),
        separator(10),
        widget.CheckUpdates(
            background = colors[0],
            foreground = colors[3],
            fontsize = 16,
            update_interval = 1800,
            distro = "Arch_checkupdates",
            display_format = "⟳ {updates} Updates",
            mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn(terminal+" -e sudo pacman -Syu")},
            padding = 5
        ),
        widget.Spacer(),
        group_head(),
        CustomPomodoro(
            background=colors[14],
            fontsize=26,
            color_active=colors[3],
            color_break=colors[6],
            color_inactive=colors[10],
            timer_visible=False,
            prefix_active="",
            prefix_break="",
            prefix_inactive="",
            prefix_long_break="",
            prefix_paused=""
        ),
        group_tail(),
        separator(10),
        group_head(),
        widget.TextBox(
            text = " ",
            foreground = colors[8],
            background = colors[14],
            font = "Font Awesome 5 Free Solid",
            fontsize = 20
        ),
        widget.Volume(
            background = colors[14],
            foreground = colors[8],
            fontsize = 16,
            device = "pulse",
            padding = 5
            ),
        group_tail(),
        separator(10),
        group_head(),
        widget.GenPollText(
            func = bluetooth,
            background = colors[14],
            foreground = colors[6],
            fontsize = 16,
            update_interval = 3,
            mouse_callbacks = {
                "Button1": toggle_bluetooth,
                "Button3": open_bt_menu
            }
        ),
        group_tail(),
        separator(10),
        group_head(),
        widget.Wlan(
            foreground = colors[7],
            background = colors[14],
            fontsize = 16,
            format = "  {essid}",
            padding = 5,
            mouse_callbacks = { "Button1": open_wifi_menu }
        ),
        group_tail(),
        separator(10),
        group_head(),
        widget.GenPollText(
            func = nordvpn,
            background = colors[14],
            foreground = colors[11],
            fontsize = 16,
            update_interval = 3,
            mouse_callbacks = {
                "Button1": open_vpn_menu
            }
        ),
        group_tail(),
        separator(10),
        group_head(),
        widget.Clock(
            fontsize = 16,
            format = "  %a, %b %d",
            background = colors[14],
            foreground = colors[5]
        ),
        group_tail(),
        separator(10),
        group_head(),
        widget.Clock(
            fontsize = 16,
            format = "  %I:%M %p",
            background = colors[14],
            foreground = colors[4]
        ),
        group_tail(),
        separator(10),
        group_head(),
        widget.Battery(
            background = colors[14],
            foreground = colors[8],
            fontsize = 16,
            low_foreground = colors[3],
            low_percentage = 0.15,
            charge_char = "",
            discharge_char = "",
            emtpy_char = "",
            format = "{char}  {percent:3.0%} ({hour:d}:{min:02d})",
            padding = 5
        ),
        group_tail(),
        separator(20),
        widget.TextBox(
            text = "⏻",
            foreground = colors[13],
            background = colors[0],
            font = "Font Awesome 5 Free Solid",
            fontsize = 30,
            mouse_callbacks = { "Button1": open_powermenu }
        ),
        separator(20)
        ]
    return widgets_list

def init_screens():
    return [
        Screen(
            wallpaper = "~/Git/Personal/Dotfiles/backgrounds/dnord4k_dark.png",
            wallpaper_mode = "fill",
            top = bar.Bar(
                widgets = init_widgets_list(),
                size = 34,
            ),
        )
    ]

if __name__ in ["config", "__main__"]:
    screens = init_screens()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])

# Go to group when app opens on matched gropu
@hook.subscribe.client_new
def modify_window(client):
    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[
                group.name
            ]  # there can be multiple instances of a group
            targetgroup.cmd_toscreen(toggle=False)
            break

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"
