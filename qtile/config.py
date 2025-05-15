from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Window navigation
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),

    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Resize windows
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),

    # Layouts and spawning
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "Tab", lazy.next_layout()),

    # Window management
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),

    # Reload and quit
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),

    # Custom launcher
    Key([mod], "r", lazy.spawn("bash /home/enzo/rofi/files/launchers/type-4/launcher.sh")),
]

groups = [Group(str(i), label="●") for i in range(1, 7)]

for group in groups:
    keys.extend([
        Key([mod], group.name, lazy.group[group.name].toscreen()),
        Key([mod, "shift"], group.name, lazy.window.togroup(group.name, switch_group=True)),
    ])

layouts = [
    layout.Columns(
        border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_width=0,
        border_focus="#7b5cb5",
        border_normal="#7b5cb5",
        margin=6,
        ratio=0.5,
    ),
    layout.Max(),
]

widget_defaults = dict(font="Fira Code Nerd Font", fontsize=13, padding=4)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method="text",
                    rounded=True,
                    inactive="#666666",
                    active="#fca197",
                    this_current_screen_border="#d16b60",
                    urgent_border="#FF00FF",
                    fontsize=26,
                    margin_x=1,
                    padding=1,
                    disable_drag=True,
                ),

                widget.Spacer(length=10),
                widget.Prompt(),
                widget.Spacer(length=bar.STRETCH),
                widget.Systray(padding=5),
                
                widget.TextBox("", fontsize=26, padding=-1, foreground="#d9a179", background="#1f2129"),
                widget.CheckUpdates(distro="Arch", update_interval=1800, no_update_string="", display_format=" {updates}", foreground="#b3c4fc", background="#d9a179", colour_have_updates="#000000", colour_no_updates="#000000", font="Fira Code Nerd Font", padding=8, mouse_callbacks={'Button1': lazy.spawn("alacritty -e sudo pacman -Syu")}),

                widget.TextBox("", fontsize=28, padding=-1, foreground="#6d54bf", background="#d9a179"),
                widget.Clock(format=" %d/%m/%Y", foreground="#000000", background="#6d54bf"),
                widget.Clock(format="- %H:%M", foreground="#000000", background="#6d54bf"),
               
                widget.TextBox("", fontsize=28, padding=-0, foreground="#ffffff", background="#6d54bf"),
                widget.TextBox(text=" ", fontsize=20, background="#ffffff", foreground="#586af5", padding=-1),

            ],
            28,
            margin=[4, 5, 3, 5],
            background="#1f2129",
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
    border_focus="#655ec4",
    border_normal="#7b5cb5",
    border_width=1,
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "LG3D"

# Autostart apps
autostart = [
    "picom &",
    "nitrogen --restore &",
]

for app in autostart:
    os.system(app)
