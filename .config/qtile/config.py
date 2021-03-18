import os
import socket
import subprocess
from libqtile import qtile, bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401

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
    Key([mod], "XF86AudioLowerVolume",
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

group_names = [("WWW", { "layout": "monadtall" }),
               ("DEV", { "layout": "monadtall" }),
               ("SYS", { "layout": "monadtall" }),
               ("DOC", { "layout": "monadtall" }),
               ("CHAT", { "layout": "monadtall" }),
               ("GFX", { "layout": "floating" }),
               ("ETC", { "layout": "monadtall" })]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.extend([
        Key([mod], str(i), lazy.group[name].toscreen(),
            desc="Switch to Group {}".format(name)),
        Key([mod, "shift"], str(i), lazy.window.togroup(name),
            desc="Move focused window to group {}".format(name))
    ])

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
        layout.MonadTall(**layout_theme),
        layout.Max(**layout_theme),
        layout.Tile(shift_windows=True, **layout_theme),
        layout.Stack(num_stacks=2),
        layout.TreeTab(
            font = "Ubuntu Mono",
            fontsize = 14,
            sections = ["FIRST", "SECOND"],
            section_fontsize = 12,
            bg_color = "2e3440",
            active_bg = "5e81ac",
            active_fg = "eceff4",
            inactive_bg = "4c566a",
            inactive_fg = "d8dee9",
            padding_y = 5,
            section_top = 16,
            panel_width = 320
            ),
        layout.Floating(**layout_theme)
]

colors = [["#2E3440", "#2E3440"], # panel background
          ["#4c566a", "#4c566a"], # background for current screen tab
          ["#eceff4", "#eceff4"], # font color for group names
          ["#88c0d0", "#88c0d0"], # border line color for current tab
          ["5e81ac", "#5e81ac"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#434c5e", "#434c5e"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"]] # window name

prompt = "{0}@{1}".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font='Ubuntu Mono',
    fontsize=12,
    padding=2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.Spacer(
            length = 6,
            background = colors[0]
            ),
        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground = colors[2],
            background = colors[0],
            padding = 0,
            scale = 0.7
            ),
        widget.Spacer(
            length = 6,
            background = colors[0]
            ),
        widget.GroupBox(
            font = "Ubuntu Bold",
            fontsize = 9,
            margin_y = 3,
            margin_x = 0,
            padding_y = 5,
            padding_x = 3,
            borderwidth = 3,
            active = colors[2],
            inactive = colors[2],
            rounded = False,
            highlight_color = colors[1],
            highlight_method = "line",
            this_current_screen_border = colors[3],
            this_screen_border = colors[4],
            other_current_screen_border = colors[6],
            other_screen_border = colors[4],
            foreground = colors[2],
            background = colors[0]
            ),
        widget.Prompt(
            prompt = prompt,
            font = "Ubuntu Mono",
            padding = 10,
            foreground = colors[3],
            background = colors[1]
            ),
        widget.Spacer(
            background = colors[0],
            length = bar.STRETCH
        ),
        widget.Systray(
            background = colors[0],
            padding = 5
            ),
        widget.TextBox(
            text = "",
            background = colors[0],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = "",
            background = colors[5],
            foreground = colors[2],
            ),
        widget.Wlan(
            foreground = colors[2],
            background = colors[5],
            format = "{essid} ({percent:0.0%})",
            padding = 5
            ),
        widget.TextBox(
            text = '',
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
            ),
        widget.Net(
            interface = "wlan0",
            format = "{down} ↓↑{up}",
            foreground = colors[2],
            background = colors[4],
            padding = 5
            ),
        widget.TextBox(
            text = "",
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
            ),
        widget.Volume(
            background = colors[5],
            foreground = colors[2],
            emoji = True,
            device = "pulse"
            ),
        widget.Volume(
            background = colors[5],
            foreground = colors[2],
            device = "pulse",
            padding = 5
            ),
        widget.TextBox(
            text = "",
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = "",
            padding = 2,
            foreground = colors[2],
            background = colors[4],
            fontsize = 11
            ),
        widget.Backlight(
            background = colors[4],
            foreground = colors[2],
            backlight_name = "amdgpu_bl0",
            padding = 5
            ),
        widget.TextBox(
            text = "",
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = "🖬",
            foreground = colors[2],
            background = colors[5],
            padding = 0,
            fontsize = 14
            ),
        widget.Memory(
            foreground = colors[2],
            background = colors[5],
            measure_mem = "G",
            measure_swap = "G",
            format = "{MemPercent: .0f}%",
            mouse_callbacks = { "Button1": lambda: qtile.cmd_spawn(terminal + " -e htop")},
            padding = 5
            ),
        widget.TextBox(
            text = "",
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = "",
            foreground = colors[2],
            background = colors[4],
            padding = 5
            ),
        widget.CPU(
            foreground = colors[2],
            background = colors[4],
            padding = 5,
            format = "{load_percent}%"
            ),
        widget.TextBox(
            text = "",
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = "🌡",
            padding = 2,
            foreground = colors[2],
            background = colors[5],
            fontsize = 11
            ),
        widget.ThermalSensor(
            foreground = colors[2],
            background = colors[5],
            threshold = 90,
            padding = 5
            ),
        widget.TextBox(
            text = "",
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
            ),
        widget.Battery(
            background = colors[4],
            foreground = colors[2],
            charge_char = "",
            discharge_char = "",
            emtpy_char = "",
            format = "{char} {percent:3.0%} ({hour:d}:{min:02d})",
            padding = 5
            ),
        widget.TextBox(
            text = "",
            background = colors[4],
            foreground = colors[5],
            padding = 0,
            fontsize = 37
            ),
        widget.TextBox(
            text = "⟳",
            padding = 2,
            foreground = colors[2],
            background = colors[5],
            fontsize = 14
            ),
        widget.CheckUpdates(
            update_interval = 1800,
            distro = "Arch_checkupdates",
            display_format = "{updates} Updates",
            no_update_string = "0 Updates",
            foreground = colors[2],
            mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn(terminal+" -e sudo pacman -Syu")},
            background = colors[5],
            padding = 5
            ),
        widget.TextBox(
            text = "",
            background = colors[5],
            foreground = colors[4],
            padding = 0,
            fontsize = 37
            ),
        widget.Clock(
            foreground = colors[2],
            background = colors[4],
            format = "%a, %b %d | %I:%M %p",
            padding = 5
            )
        ]
    return widgets_list

def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_list(), opacity=1.0, size=20))
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

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
