# Imports
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os

# Configuration for mod and terminal
mod = "mod4"  # Set the modifier key (Mod4 is the "Windows" key)
terminal = guess_terminal()  # Guess the default terminal (e.g., urxvt, alacritty)

# Keybindings
keys = [
    # Window navigation
    Key([mod], "h", lazy.layout.left(), desc="Move focus to the left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to the right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move focus to the next window"),

    # Move windows between columns and stack
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Resize windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between layouts
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit layouts"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Switch between layouts"),

    # Window management commands
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),

    # Reload and shutdown
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Launch a custom app (e.g., a launcher script)
    Key([mod], "r", lazy.spawn("bash /home/hp/rofi/files/launchers/type-4/launcher.sh"), desc="Open launcher"),
]

# Define groups (workspaces)
groups = [Group(f"{i}", label=f" ●") for i in "123456789"]

# Bind keys for switching and moving windows between groups
for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Switch to & move focused window to group {i.name}"),
        ]
    )

# Layout configuration
layouts = [
    layout.Columns(
        border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_width=0,
        border_focus="#ff0000",  # Focused window border color
        border_normal="#444444",  # Non-focused window border color
        margin=8,  # Space between windows
        ratio=0.5,  # Equal column size
    ),
    layout.Max(),  # Max layout
]

# Widget defaults
widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# Screen configuration
screens = [
    Screen(
        top=bar.Bar(
            [
                # Left section

                
                widget.GroupBox(
                        highlight_method="text",  
                        rounded=True,  
                        inactive="#666666",  
                        active="#c0cefc",  
                        this_current_screen_border="#9cb3ff", 
                        other_current_screen_border="#1E3A5F",  
                        this_screen_border="#FFD700", 
                        other_screen_border="#1E3A5F", 
                        urgent_border="#FF00FF",  
                        highlight_color=["f7f7f5"],  
                        disable_drag=True,  
                        fontsize=20, 
                        margin_x=1,  
                        padding=1,  
                        use_mouse_wheel=False,
                ),
                widget.Prompt(),  # Command prompt widget
                
                # Center separator
                widget.Spacer(length=bar.STRETCH),
                widget.TextBox("", fontsize=34, padding=-1, foreground="#1b1f2e", background="#202433"),
                widget.WindowName(foreground="#b3c4fc", background="#1b1f2e", padding=-1, font="Fira Code Nerd Font"),
                widget.Systray(foreground="#ffffff", background="#1b1f2e", font=""),  
                widget.TextBox("", fontsize=34, padding=-1, foreground="#1b1f2e", background="#202433"),

                # Central section
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),

                # Right separator
                widget.Spacer(length=bar.STRETCH),

                # Right section
                widget.TextBox("", fontsize=34, padding=1, foreground="#24293b", background="#202433"),
                widget.Clock(format=" %I:%M", foreground="#b3c4fc", background="#24293b", font="Fira Code Nerd Font"),

                widget.TextBox("", fontsize=34, padding=1, foreground="#23293d", background="#24293b"),
                widget.Clock(format=" %d/%m/%Y", foreground="#b3c4fc", background="#23293d", font="Fira Code Nerd Font"),
                
                widget.TextBox("", fontsize=33, padding=1, foreground="#202433", background="#23293d"),
                widget.Image(
                    filename="~/.config/qtile/logo.png", background="#202433",  # Path to the image
                    margin=6,  # Change image size
                ), 
            ],
            40,  # Bar height
            background="#202433",
            margin=[7, 10, -2, 10],  # Margins
            border_width=[0, 0, 0, 0],  # Bar borders
            opacity=10,
        ),
    ),
]

# Mouse configuration (drag and click actions)
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# Floating window layout configuration
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # For gitk
        Match(wm_class="makebranch"),  # For gitk
        Match(wm_class="maketag"),  # For gitk
        Match(wm_class="ssh-askpass"),  # For ssh-askpass
        Match(title="branchdialog"),  # For gitk
        Match(title="pinentry"),  # For GPG key password entry
    ],
    border_focus="#ff0000",  # Border color for focused floating windows
    border_normal="#444444",  # Border color for non-focused floating windows
    border_width=0,  # Border width
)

# Additional configuration
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# Wayland configuration
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24

# Window Manager name
wmname = "LG3D"

# Autostart applications
autostart = [
   "picom &",  # Start picom (compositor for transparency and effects)
   "nitrogen --restore &",  # Restore the wallpaper using nitrogen
]

# Execute autostart applications
for app in autostart:
    os.system(app)
