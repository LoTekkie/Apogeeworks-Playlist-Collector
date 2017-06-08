__author__ = 'Apogee'

import tkinter
from tkinter import ttk
from tkinter import Tk
from tkinter import filedialog
import constants as c
import tkinter.constants as tkc
from datetime import datetime
from apcollections import Collector
import random
import utils
import os
import sys


if hasattr(sys, 'frozen'):
    DIR_BASE = os.path.abspath(os.path.dirname(sys.executable))
else:
    DIR_BASE = os.path.abspath(os.path.dirname(__file__))

DIR_ASSETS = os.path.join(DIR_BASE, 'assets')
DIR_IMAGES = os.path.join(DIR_ASSETS, 'images')
DIR_CURSORS = os.path.join(DIR_ASSETS, 'cursors')


class StyledFrame(tkinter.Frame):
    def __init__(self, parent, **kwargs):
        tkinter.Frame.__init__(self, parent, **kwargs)

        self.propagate(False)
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.config(
            relief=tkc.RAISED
        )
        self.parent = parent
        self.root = utils.tk_get_root(self)

    def init_ui(self):
        pass


class StyledTopLevel(tkinter.Toplevel):
    def __init__(self, parent, **kwargs):
        tkinter.Toplevel.__init__(self, parent, **kwargs)

        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.is_viewing = False
        self.parent = parent
        self.root = utils.tk_get_root(self)

    def init_ui(self):
        pass


class SizedTextBox(tkinter.Frame):
    def __init__(self, master, width=0, height=0, **kwargs):
        self.width = width
        self.height = height
        tkinter.Frame.__init__(self, master, width=self.width, height=self.height)

        self.widget = tkinter.Text(
            self,
            font=utils.tk_font(size=10),
            highlightbackground=c.COLOR_WHITE,
            highlightcolor=c.COLOR_BLUE,
            highlightthickness=0,
            width=20,
            wrap=tkc.CHAR,
            state=tkc.DISABLED,
            spacing3=5
        )
        sb_y = ttk.Scrollbar(
            orient=tkc.VERTICAL,
            command=self.widget.yview
        )
        sb_y.pack(
            in_=self, side=tkc.RIGHT, fill=tkc.Y
        )
        self.widget['yscroll'] = sb_y.set

        self.widget.pack(
            expand=tkc.YES,
            fill=tkc.BOTH
        )

    def pack(self, *args, **kwargs):
        tkinter.Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)
        return self.widget

    def grid(self, *args, **kwargs):
        tkinter.Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)
        return self.widget


class RootFrame(Tk):
    def __init__(self, parent, **kwargs):
        Tk.__init__(self, **kwargs)

        self.overrideredirect(True)
        self.resizable(False, False)
        self.propagate(False)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.attributes('-topmost', False)

        self.w, self.h = 425, 425

        self.parent = parent

        self.init_ui()

        self.bind(
            "<Map>", self.bind_redirect
        )

        # self.bind_all("<Key>", self.track_keys)
        self.bind_all("<Control-l>", self.track_keys)
        self.bind_all("<Control-e>", self.track_keys)
        self.bind_all("<Control-k>", self.track_keys)
        self.bind_all("<Control-d>", self.track_keys)
        self.bind_all("<Control-m>", self.track_keys)
        self.bind_all("<Control-n>", self.track_keys)
        self.bind_all("<Control-s>", self.track_keys)
        self.bind_all("<Alt-i>", self.track_keys)
        self.bind_all("<Alt-x>", self.track_keys)
        self.bind_all("<Alt-q>", self.track_keys)

        self.key_map = {
            #     76: self.menu_frame.viewLoadGroup, #"<Control-l>"
            #     75: self.menu_frame.askClearGroup, #"<Control-k>"
            #     69: self.menu_frame.viewEditGroup, #"<Control-e>"
            #     68: self.menu_frame.askDeleteGroup, #"<Control-d>"
            #     78: self.menu_frame.viewNewGroup, #"<Control-n>"
            #     77: self.menu_frame.viewDeleteMultipleGroup, #"<Control-m>"
            #     83: self.summoned, #"<Control-s>"
            #     73: self.destroy, #"<Alt-i>"
            #     88: self.destroy, #"<Alt-x>"
            81: self.destroy,  # "<Alt-q>"
        }

        self.tip_map = {
            c.TIP_BROWSE: 'Browse for and select your paths.',
            c.TIP_START: 'Press the "Start" button to begin!',
            c.TIP_RANDOM: [
                'You can disable these tips in "Options" > "Configure"',
                '',
            ],
            c.TIP_LAST: ''
        }

        self.error_map = {
        }

        self.track_events()
        self.on_start()

    def init_ui(self):
        self.title("Apogeeworks Playlist Collector")

        self.configure(
            bg=c.COLOR_WHITE,
            relief=tkc.RAISED,
            width=self.w,
            height=self.h
        )
        center_x, center_y = self.center_frame()
        self.geometry(
            '%dx%d+%d+%d' % (self.w, self.h, center_x, center_y)
        )
        #TODO: show splash
        #self.frame_splash = RootSplashFrame(self)
        self.update_idletasks()

        self.frame_main = RootMainFrame(self)
        self.frame_tool = RootToolFrame(self)
        self.frame_menu = RootMenuFrame(self)
        self.frame_footer = RootFooterFrame(self)
        #self.control_frame = RootViewControlFrame(self)

        self.update()

    def on_hover(self, event):
        pass

    def exit_hover(self, event):
        pass

    def bind_redirect(self, event):
        if self.wm_state() == c.STATE_ICONIC:
            self.bind(
                "<Map>", self.un_minimize
            )

    def un_minimize(self, event):
        self.update_idletasks()
        self.overrideredirect(True)
        self.wm_deiconify()

        self.bind(
            "<Map>", self.bind_redirect
        )

    def minimize(self):
        self.update_idletasks()
        self.overrideredirect(False)
        self.wm_iconify()

    def center_frame(self):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        return screen_w/2-self.w/2, screen_h/2-self.h/2

    def cloak(self, alpha):
        if not self.is_cloaked:
            self.attributes("-alpha", alpha)
            self.is_cloaked = True

    def un_cloak(self):
        self.attributes("-alpha", 1)
        self.is_cloaked = False

    def track_cursor(self):
        if not self.busy:
            cursor_x, cursor_y = self.winfo_pointerxy()

    def track_keys(self, event):
        self.key_map[event.keycode]()

    def track_events(self):
        self.after(50, self.track_events)

    def alert_action_info(self, text, fg="white", bg=c.COLOR_ORANGE, font=utils.tk_font()):
        self.frame_footer.label_action_info.config(fg=fg, bg=bg, font=font, text=text)

    def alert_action_symbol(self, text, fg="white", bg=c.COLOR_BLUE):
        self.frame_footer.label_action_symbol.config(fg=fg, bg=bg, text=text)

    def get_tip(self, tip):
        format_tip = '[Tip]: %s'
        if not tip is c.TIP_RANDOM:
            self.tip_map.update(last=self.tip_map[tip])
            return format_tip % self.tip_map.get('last')

        list_tips = self.tip_map[tip]
        self.tip_map.update(last=random.choice(list_tips))
        return format_tip % self.tip_map.get('last')

    def get_error(self, err):
        pass

    def console(self, msg, prefix=" >> ", end="\n", tag='', tag_start='insert-1c', tag_end='insert lineend+1c'):
        self.frame_main.console(
            msg,
            prefix=prefix,
            end=end,
            tag=tag,
            tag_start=tag_start,
            tag_end=tag_end,
        )

    def on_start(self):
        self.console('process started')
        self.console('not ready', tag=c.TAG_TEXT_RED)
        self.alert_action_symbol('v%s' % utils.get_version())
        self.alert_action_info(self.get_tip(c.TIP_BROWSE), fg=c.COLOR_DARK_KNIGHT)


class RootSplashFrame(StyledTopLevel):
    def __init__(self, parent, **kwargs):
        StyledTopLevel.__init__(self, parent, **kwargs)

        self.init_ui()
        self.show_logo()

    def init_ui(self):
        self.config(
            bg=c.COLOR_DARK_KNIGHT
        )
        center_x, center_y = self.root.center_frame()
        #TODO: fix image size
        self.image_logo = tkinter.PhotoImage(
            file=os.path.join(DIR_IMAGES, "logo_apogeeworks.gif")
        )
        self.canvas_logo = tkinter.Canvas(
            master=self,
            bg=c.COLOR_DARK_KNIGHT,
            border=None,
            width=400, height=161,
            bd=0,
            highlightthickness=0,
            relief='ridge'
        )
        self.canvas_logo.create_image(0, 0, image=self.image_logo, anchor=tkc.NW)

        self.geometry(
            '%dx%d+%d+%d' % (self.root.w, self.root.h, center_x, center_y)
        )
        self.canvas_logo.pack(
            expand=tkc.YES,
        )

    def show_logo(self, duration_seconds=2):
        self.update()
        self.after(2000, self.hide_logo)

    def hide_logo(self):
        self.after_cancel(self.hide_logo)
        self.destroy()


class RootToolFrame(StyledFrame):
    def __init__(self, parent, **kwargs):
        StyledFrame.__init__(self, parent, **kwargs)

        self.init_ui()

        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_motion)
        self.tool_label.bind("<ButtonPress-1>", self.start_move)
        self.tool_label.bind("<ButtonRelease-1>", self.stop_move)
        self.tool_label.bind("<B1-Motion>", self.on_motion)
        self.tool_label.bind("<Enter>", self.on_hover)
        self.tool_label.bind("<Leave>", self.exit_hover)
        self.btn_close.bind("<Enter>", self.on_hover)
        self.btn_close.bind("<Leave>", self.exit_hover)
        self.btn_minimize.bind("<Enter>", self.on_hover)
        self.btn_minimize.bind("<Leave>", self.exit_hover)

    def init_ui(self):
        self.config(
            background=c.COLOR_DARK_KNIGHT,
            relief=tkc.FLAT,
            width=self.parent.winfo_width(),
            height=25
        )
        self.tool_label = tkinter.Label(
            self,
            font=utils.tk_font(),
            background=c.COLOR_DARK_KNIGHT,
            width=38,
        )
        self.btn_minimize = tkinter.Button(
            self,
            text=c.UNICODE_BTN_MINIMIZE,
            font=utils.tk_font(size=20),
            background=c.COLOR_DARK_KNIGHT,
            fg=c.COLOR_WHITE,
            width=2,
            relief=tkc.FLAT,
            command=self.parent.minimize
        )
        self.btn_close = tkinter.Button(
            self,
            text=c.UNICODE_BTN_CLOSE,
            font=utils.tk_font(size=20),
            background=c.COLOR_RED,
            fg=c.COLOR_WHITE,
            width=2,
            relief=tkc.FLAT,
            command=self.parent.destroy
        )
        self.grid(
            column=0, row=0,
            sticky="ew"
        )
        self.btn_close.pack(
            side=tkc.RIGHT,
            padx=(10, 10)
        )
        self.btn_minimize.pack(
            side=tkc.RIGHT,
        )
        self.tool_label.pack(
            side=tkc.RIGHT,
        )

        self.update()

    def on_hover(self, event):
        if not event.widget['state'] == tkc.DISABLED:
            event.widget['cursor'] = c.CURSOR_HAND_2

    def exit_hover(self, event):
        event.widget['cursor'] = c.CURSOR_ARROW

    def start_move(self, event):
        self.parent.lift()
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        event.widget['cursor'] = c.CURSOR_HAND_2
        self.dragging_parent = False
        self.parent.un_cloak()

    def on_motion(self, event):
        self.dragging_parent = True
        #self.parent.cloak(self.parent.frame_drag_alpha_value.get())

        delta_x = event.x - self.x
        delta_y = event.y - self.y

        root_x = self.parent.winfo_x()
        root_y = self.parent.winfo_y()

        new_x = root_x + delta_x
        new_y = root_y + delta_y

        self.parent.geometry('+%s+%s' % (new_x, new_y))


class RootMenuFrame(StyledFrame):
    def __init__(self, parent, **kwargs):
       StyledFrame.__init__(self, parent, **kwargs)

       self.init_ui()

       self.file_menu.bind("<<MenuSelect>>", self.menu_select_callback)

    def init_ui(self):
        self.config(
            background=c.COLOR_GREY,
            relief=tkc.FLAT,
            width=self.parent.winfo_width(), height=22,
        )
        self.menu_file = tkinter.Menubutton(
            self, text="File",
            font=utils.tk_font(),
            background=c.COLOR_GREY
        )
        self.menu_options = tkinter.Menubutton(
            self, text="Options",
            font=utils.tk_font(),
            background=c.COLOR_GREY
        )
        self.menu_label = tkinter.Label(
            self,
            text="Apogeeworks Playlist Collector",
            relief=tkc.FLAT,
            font=utils.tk_font(),
            bg=c.COLOR_BLUE,
            fg=c.COLOR_WHITE,
            height=2, width=27,
        )
        self.grid(
            column=0, row=1,
            sticky="n",
        )
        self.menu_label.pack(
            side=tkc.RIGHT,
        )
        self.menu_file.pack(
            side=tkc.LEFT,
            padx=(0, 0)
        )
        self.menu_options.pack(
            side=tkc.LEFT,
            padx=(5, 0)
        )
        self.file_menu = tkinter.Menu(
            self.menu_file,
            tearoff=0
        )
        self.menu_file['menu'] = self.file_menu

        self.options_menu = tkinter.Menu(
            self.menu_options,
            tearoff=0
        )
        self.menu_options['menu'] = self.options_menu

        self.file_menu.add_command(
            label="{0}{1}{2}".format("Quit", " "*8, "(Alt + Q)"),
            command=self.parent.destroy
        )
        self.options_menu.add_command(
            label="Configure...",
            command=self.view_menu_config()
        )
        self.options_menu.add_separator()
        self.options_menu.add_command(
            label="View Tutorial...",
            command=self.view_menu_tutorial()
        )

        self.update()

    def menu_select_callback(self, event):
        pass

    def view_menu_config(self):
        pass

    def view_menu_tutorial(self):
        pass


class RootMainFrame(StyledFrame):
    def __init__(self, parent, **kwargs):
        StyledFrame.__init__(self, parent, **kwargs)

        self.var_console_text_size = tkinter.IntVar()
        self.var_console_text_size.set(9)

        self.init_ui()

        self.map_tracked_entries = {
            'collection': {
                'widget': self.entry_collection_path,
                'verified': lambda path: os.path.isdir(path),
                'set': False,
                'last': None,
                'browser': self.browser_collection_path
            },
            'playlist': {
                'widget': self.entry_playlist_path,
                'verified': lambda path: self.verify_path_playlist(path),
                'set': False,
                'last': None,
                'browser': self.browser_playlist_path
            }
        }

        self.state_ready_collect = c.STATE_NOT_READY

        self.textbox_console_output.tag_configure(
            c.TAG_TEXT_RED, foreground=c.COLOR_RED
        )
        self.textbox_console_output.tag_configure(
            c.TAG_TEXT_GREEN, foreground=c.COLOR_GREEN
        )
        self.textbox_console_output.tag_configure(
            c.TAG_TEXT_ORANGE, foreground=c.COLOR_ORANGE
        )
        self.textbox_console_output.tag_configure(
            c.TAG_TEXT_BLUE, foreground=c.COLOR_BLUE
        )

        self.track_path_entries()
        self.track_console_output()
        self.track_collection_state()

    def init_ui(self):
        self.config(
            bg=c.COLOR_WHITE,
            width=self.root.winfo_width(),
            height=self.root.winfo_height()
        )
        self.control_panel = StyledFrame(
            self,
            width=self.root.w - 25,
            height=self.root.h - 120,
            relief=tkc.RAISED
        )
        self.group_playlist = tkinter.LabelFrame(
            self.control_panel,
            font=utils.tk_font(size=10, weight=c.FONT_WEIGHT_BOLD),
            text="Media Playlist",
        )
        self.label_playlist_path_entry = tkinter.Label(
            self.group_playlist,
            text="File Path :"
        )
        self.entry_playlist_path = tkinter.Entry(
            self.group_playlist,
            width=40,
        )
        self.group_collection = tkinter.LabelFrame(
            self.control_panel,
            font=utils.tk_font(size=10, weight=c.FONT_WEIGHT_BOLD),
            text="Collection Location",
        )
        self.label_collection_path_entry = tkinter.Label(
            self.group_collection,
            text="Directory Path :"
        )
        self.entry_collection_path = tkinter.Entry(
            self.group_collection,
            width=40,
        )
        self.browser_playlist_path = tkinter.Button(
            self.group_playlist,
            text="Change",
            width=6, height=1,
            relief=tkc.RAISED,
            command=lambda: self.open_file(self.entry_playlist_path)
        )
        self.browser_collection_path = tkinter.Button(
            self.group_collection,
            text="Change",
            width=6, height=1,
            relief=tkc.RAISED,
            command=lambda: self.open_directory(self.entry_collection_path)
        )
        self.group_console = tkinter.LabelFrame(
            self.control_panel,
            font=utils.tk_font(size=10, weight=c.FONT_WEIGHT_BOLD),
            text="Console Output",
        )
        self.textbox_console_output = SizedTextBox(
            self.group_console,
            height=100,
        )
        self.scale_console_text = tkinter.Scale(
            self,
            from_=8, to=14,
            resolution=2,
            orient=tkc.HORIZONTAL,
            showvalue=False,
            highlightbackground=c.COLOR_BLUE,
            variable=self.var_console_text_size,
            command=self.set_console_text_size,
        )
        self.btn_start_label = tkinter.Label(
            self.control_panel,
            text="",
            font=utils.tk_font(),
            width=10, height=1,
            bg=c.COLOR_LIGHT_GREY,
            relief=tkc.FLAT,
        )
        self.btn_start = tkinter.Button(
            self.control_panel,
            text="START",
            font=utils.tk_font(),
            width=8, height=1,
            bg=c.COLOR_GREEN,
            fg=c.COLOR_WHITE,
            relief=tkc.FLAT,
            command=lambda: self.collect_media(
                self.map_tracked_entries['playlist'].get('last'),
                self.map_tracked_entries['collection'].get('last')
            )
        )
        self.pack(
        )
        self.control_panel.pack(
            pady=(10, 0)
        )
        self.group_playlist.pack(
            fill=tkc.X
        )
        self.label_playlist_path_entry.grid(
            row=0, column=0,
            padx=(0, 0), pady=(0, 5)
        )
        self.entry_playlist_path.grid(
            row=0, column=1,
            padx=(37, 0), pady=(0, 3)
        )
        self.browser_playlist_path.grid(
            row=0, column=2,
            padx=(0, 0), pady=(0, 5)
        )
        self.group_collection.pack(
            fill=tkc.X,
            pady=(15, 0)
        )
        self.label_collection_path_entry.grid(
            row=0, column=0,
            padx=(0, 0), pady=(0, 5)
        )
        self.entry_collection_path.grid(
            row=0, column=1,
            padx=(7, 0), pady=(0, 3)
        )
        self.browser_collection_path.grid(
            row=0, column=2,
            padx=(0, 0), pady=(0, 5)
        )
        self.group_console.pack(
            fill=tkc.X,
            pady=(15, 0)
        )
        self.textbox_console_output = self.textbox_console_output.pack(
            fill=tkc.X,
            pady=(0, 5),
            padx=(5, 5)
        )
        self.scale_console_text.place(
            x=12, y=270
        )
        self.btn_start.place(
            x=320, y=273
        )
        self.grid(
            column=0, row=1,
            pady=27
        )

        self.update()

    def open_file(self, tk_entry):
        path = filedialog.askopenfilename()

        if not path is '':
            tk_entry.delete(0, tkc.END)
            tk_entry.insert(0, path)

    def open_directory(self, tk_entry):
        path = filedialog.askdirectory()

        if not path is '':
            tk_entry.delete(0, tkc.END)
            tk_entry.insert(0, path)

    def verify_path_playlist(self, path):
        file_name, ext = os.path.splitext(path)
        return os.path.exists(path) and ext == '.wpl'

    def console(self, msg, prefix=" >> ", end="\n", tag='', tag_start='insert-1c', tag_end='insert lineend+1c'):
        now = "[{}]".format(datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
        self.textbox_console_output.tag_add(tag, tag_start, tag_end)
        self.textbox_console_output.config(state=tkc.NORMAL)
        self.textbox_console_output.insert(tkc.END, now + prefix + msg + end)
        self.textbox_console_output.see(tkc.END)
        self.textbox_console_output.config(state=tkc.DISABLED)
        self.textbox_console_output.tag_remove(tag, 'insert lineend-1c')
        self.update_idletasks()

    def set_collection_entry(self, path):
        self.entry_collection_path.delete(0, tkc.END)
        self.entry_collection_path.insert(0, path)

    def set_playlist_entry(self, path):
        self.entry_playlist_path.delete(0, tkc.END)
        self.entry_playlist_path.insert(0, path)

    def set_console_text_size(self, event):
        self.textbox_console_output.config(
            font=utils.tk_font(size=self.var_console_text_size.get())
        )

    def set_tracked_entries_state(self, state=tkc.NORMAL):
        for _type, entry in self.map_tracked_entries.items():
            entry.get('widget').configure(state=state)
            entry.get('browser').configure(state=state)

    def on_done_collect_media(self):
        self.set_tracked_entries_state(state=tkc.NORMAL)
        self.state_ready_collect = c.STATE_READY
        self.console("done!", tag=c.TAG_TEXT_GREEN)
        #TODO: add logging
        self.console("logs available @ ...", tag=c.TAG_TEXT_ORANGE)

    def collect_media(self, path_playlist, dir_target):
        self.state_ready_collect = c.STATE_COLLECTING
        self.console("copying media...", tag=c.TAG_TEXT_ORANGE)
        self.root.alert_action_info(self.root.get_tip(c.TIP_RANDOM))
        media_collector = Collector(self.root, path_playlist, dir_target)
        media_collector.collect(callback=self.on_done_collect_media)

    def track_path_entries(self):
        if not self.state_ready_collect == c.STATE_COLLECTING:

            is_set_playlist = self.map_tracked_entries['playlist'].get('set')
            is_set_collection = self.map_tracked_entries['collection'].get('set')

            for _type, entry in self.map_tracked_entries.items():
                widget = entry.get('widget')
                verified = entry.get('verified')(widget.get())
                last = entry.get('last')
                browser = entry.get('browser')
                msg_path_state = '%s path verified @ "%s"'

                if verified:
                    widget.config(bg=c.COLOR_GREEN)
                    entry.update(set=True)
                    browser.config(text='Change')

                    if _type == 'playlist':
                        path_playlist = widget.get()
                        if last != path_playlist:
                            self.console(msg_path_state % (_type, path_playlist))
                            dir_playlist = os.path.dirname(path_playlist)
                            if not is_set_collection:
                                self.set_collection_entry(dir_playlist)
                            entry.update(last=path_playlist)

                    elif _type == 'collection':
                        dir_collection = widget.get()
                        if last != dir_collection:
                            self.console(msg_path_state % (_type, dir_collection))
                            entry.update(last=dir_collection)
                else:
                    widget.config(bg=c.COLOR_RED)
                    entry.update(set=False)
                    browser.config(text='Browse')

            if is_set_playlist and is_set_collection:
                if self.state_ready_collect != c.STATE_READY:
                    self.console("ready!", tag=c.TAG_TEXT_GREEN)
                    self.root.alert_action_info(self.root.get_tip(c.TIP_START), fg=c.COLOR_DARK_KNIGHT)
                    self.state_ready_collect = c.STATE_READY
            else:
                if self.state_ready_collect != c.STATE_NOT_READY:
                    self.console('not ready', tag=c.TAG_TEXT_RED)
                    self.root.alert_action_info(self.root.get_tip(c.TIP_BROWSE), fg=c.COLOR_DARK_KNIGHT)
                    self.state_ready_collect = c.STATE_NOT_READY

        self.root.after(100, self.track_path_entries)

    def track_collection_state(self):
        btn_start_state = tkc.DISABLED
        btn_start_color = c.COLOR_DARK_KNIGHT

        if self.state_ready_collect == c.STATE_NOT_READY:
            pass

        elif self.state_ready_collect == c.STATE_READY:
            btn_start_state = tkc.NORMAL
            btn_start_color = c.COLOR_GREEN

        elif self.state_ready_collect == c.STATE_COLLECTING:
            self.set_tracked_entries_state(state=tkc.DISABLED)

        self.btn_start.config(
            state=btn_start_state,
            bg=btn_start_color
        )

        #TODO: loading image

        self.root.after(50, self.track_collection_state)

    def track_console_output(self):
        pass


class RootFooterFrame(StyledFrame):
    def __init__(self, parent, **kwargs):
       StyledFrame.__init__(self, parent, **kwargs)

       self.init_ui()

    def init_ui(self):
        self.config(
            bg=c.COLOR_RED,
            height=40,
        )
        self.label_action_info = tkinter.Label(
            self,
            width=325,
            font=utils.tk_font(),
        )
        self.label_action_symbol = tkinter.Label(
            self,
            fg=c.COLOR_WHITE,
            bg=c.COLOR_BLUE,
            font=utils.tk_font(),
            height=40, width=6,
        )
        self.pack(
            side=tkc.BOTTOM,
            fill=tkc.X
        )

        self.refresh()

    def refresh(self):
        self.label_action_symbol.pack(
            in_=self,
            side=tkc.LEFT
        )
        self.label_action_info.pack(
            in_=self,
            side=tkc.LEFT,
            fill=tkc.BOTH
        )
        self.update()