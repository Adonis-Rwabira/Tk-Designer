from tkinter import PanedWindow, Event
from tkinter.ttk import Style, Separator, Treeview
from customtkinter import*
from PIL import Image
from pathlib import Path
import idlelib.colorizer as ic
import idlelib.percolator as ip
from inspect import signature
import re


class TK_Designer(CTk):
    def __init__(self):
        super().__init__()
        
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, minsize=100)
        self.rowconfigure(0, minsize=60)
        self.rowconfigure(2, weight=1)
        
        width = 600
        
        set_appearance_mode("dark")
        
        # set_default_color_theme("green")
        # deactivate_automatic_dpi_awareness()
        # self.configure(fg_color=("white", "black"))
        
        self.folder = Path(__file__).parent
        
        # self.geometry(f"{width}x{self.winfo_screenheight()}+{self.winfo_screenwidth()-width+600}+0")
        
        # self.attributes("-topmost", True) # -alpha, -transparentcolor, -disabled, -fullscreen, -toolwindow, or -topmost
        self.after(100, lambda: self.wm_state("zoomed"))
        
        self.title("TK Designer")
        
        self.menu_principal = CTkFrame(self, fg_color=("grey97", "grey5"), corner_radius=0)
        self.menu_principal.grid(columnspan=3, sticky=NSEW)
        
        self.menu_principal.rowconfigure(0, weight=1)
        self.menu_principal.columnconfigure(0, weight=1)
        self.menu_principal.columnconfigure(1, weight=1)
        self.menu_principal.columnconfigure(2, weight=1)
        
        menu1 = CTkFrame(self.menu_principal, fg_color='transparent')
        menu1.grid(sticky=W, padx=5)
        
        menu2 = CTkFrame(self.menu_principal, fg_color='transparent')
        menu2.grid(row=0, column=1, pady=3)
        
        menu3 = CTkFrame(self.menu_principal, fg_color="transparent")
        menu3.grid(row=0, column=2, sticky=E, padx=5)
        
        for i in ("Fichier", "Edition", "Affichage", "Exécution", "Aide"): CTkButton(menu1, fg_color=self.menu_principal._fg_color, hover_color=("grey85", "grey15"), text=i, text_color=("black", "grey80"), width=0).pack(side=LEFT, padx=2)
        
        self.file_title = CTkLabel(menu2, fg_color=self.menu_principal._fg_color, text="Sans titre.py", text_color=("black", "white"), width=0)
        self.file_title.pack(side=RIGHT, padx=2)
        
        for i in ["play", "pause", "stop", "replay", "undo", "redo", "theme"]:
            CTkButton(menu3,text="", fg_color=menu3._fg_color, hover_color=("grey90", "grey15"), image=CTkImage(Image.open((self.folder / "Images" / (i+".png")).as_posix()), Image.open((self.folder / "Images" / (i+"_dark.png")).as_posix())), width=0, command=(lambda: (set_appearance_mode("Dark" if get_appearance_mode() == "Light" else "Light"), self.change_code_theme())) if i == "theme" else None).pack(side=LEFT, pady=2)
        
        self.style = Style()
        self.style.configure("TSeparator", background=self._apply_appearance_mode(("grey80", "black")))
        Separator(self, orient=HORIZONTAL).grid(columnspan=3, sticky=EW)
        
        self.list_widgets = CTkScrollableFrame(self, fg_color=("grey97", "grey8"), corner_radius=0, orientation=VERTICAL, border_width=1, border_color=("grey80", "grey20"), width=170)
        self.list_widgets.grid(sticky=NSEW, pady=0)
        self.list_widgets._scrollbar.configure(width=10)
        self.list_widgets._scrollbar.grid(padx=1)
        
        container = CTkFrame(self.list_widgets, fg_color="transparent")
        container.pack(pady=10)
        
        arrow = CTkButton(container, text=" Selection", fg_color=("gray80", "gray20"), text_color=("grey10", "grey80"), corner_radius=10, hover=True, hover_color=("grey90", "grey15"), image=CTkImage(Image.open((self.folder / "Images" / "Selection.png").as_posix()), Image.open((self.folder / "Images" / "Selection_dark.png").as_posix())), compound=LEFT, anchor=W)
        arrow.pack(anchor=W, fill=X, pady=[0, 5])
        arrow.bind("<ButtonRelease>", self.change_selection)
        
        
        CTkLabel(container, text="CONTAINERS", font=("", 14, "bold"), text_color=("grey20", "grey60")).pack(pady=2)
        
        for widget in ["Tabview", "Textbox", "Canvas", "Frame", "ScrollableFrame"]:
            widget = CTkButton(container, fg_color="transparent", text=" "*2+widget, text_color=("grey10", "grey80"), corner_radius=10, font=("Yu Ghothic UI Semilight", 13), hover=True, hover_color=("grey90", "grey15"), image=CTkImage(Image.open((self.folder / "Images" / (widget+".png")).as_posix()), Image.open((self.folder / "Images" / (widget+"_dark.png")).as_posix())), compound=LEFT, anchor=W)
            widget.pack(anchor=W, fill=X)
            widget.bind("<ButtonRelease>", self.change_selection)
        
        CTkLabel(container, text="WIDGETS", font=("", 14, "bold"), text_color=("grey20", "grey60")).pack(pady=[20, 10])
        
        for widget in ["Label", "Button", "Entry", "ComboBox", "RadioButton", "CheckBox", "Switch", "Slider", "ProgressBar", "Scrollbar", "OptionMenu"]:
            widget = CTkButton(container, fg_color="transparent", text=" "*2+widget, text_color=("grey10", "grey80"), corner_radius=10, font=("Yu Ghothic UI Semilight", 13), hover=True, hover_color=("grey90", "grey15"), image=CTkImage(Image.open((self.folder / "Images" / (widget+".png")).as_posix()), Image.open((self.folder / "Images" / (widget+"_dark.png")).as_posix())), compound=LEFT, anchor=W)
            widget.pack(anchor=W, fill=X)
            widget.bind("<ButtonRelease>", self.change_selection)
        
        
        self.view = CTkFrame(self, fg_color="transparent", corner_radius=8)
        self.view.grid(row=2, column=1, sticky=NSEW)
        
        self.list_options = CTkScrollableFrame(self, label_text="Button", label_font=("", 15, "bold"), label_anchor=S, label_fg_color="transparent", label_text_color=("grey10", "grey80"), fg_color=("grey97", "grey8"), corner_radius=0, orientation=VERTICAL, border_width=1, border_color=("grey80", "grey20"), width=210)
        self.list_options.grid(row=2, column=2, sticky=NSEW)
        self.list_options._scrollbar.configure(width=12)
        self.list_options._scrollbar.grid(padx=1)
        
        self.list_options.columnconfigure(0, minsize=120, weight=1)
        self.list_options.columnconfigure(1, weight=1)
        
        CTkLabel(self.list_options, text="Master", font=("", 12)).grid(padx=10, sticky=S)
        CTkComboBox(self.list_options, border_width=0, fg_color=("grey90", "grey14"), font=("", 12), button_color=("grey90", "grey14"), height=24).grid(row=0, column=1, padx=5, pady=[20, 0])
        
        CTkLabel(self.list_options, text="Name", font=("", 12)).grid(padx=10)
        CTkEntry(self.list_options, border_width=0, fg_color=("grey90", "grey14"), font=("", 12, "bold"), height=22).grid(row=1, column=1, padx=5, pady=10, sticky=EW)
        
        self.style.configure("L.TSeparator", background=self._apply_appearance_mode(("grey90", "grey0")))
        Separator(self.list_options, orient=HORIZONTAL, style="L.TSeparator").grid(columnspan=2, sticky=EW, pady=10)
         
        CTkLabel(self.list_options, text="Appearence", font=("", 12, "bold")).grid(padx=20, columnspan=2, sticky=W)
        CTkButton(self.list_options, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "down.png").as_posix()), Image.open((self.folder / "Images" / "down_dark.png").as_posix())), width=0).grid(row=3, column=1, sticky=E)
       
        container = CTkFrame(self.list_options, corner_radius=0, fg_color="transparent")
        container.grid(sticky=EW, columnspan=2, padx=15, pady=10)
        
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
       
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "width.png").as_posix()), Image.open((self.folder / "Images" / "width_dark.png").as_posix()))).grid(sticky=W)
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=0, column=0, pady=5, sticky=E)
        
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "height.png").as_posix()), Image.open((self.folder / "Images" / "height_dark.png").as_posix()))).grid(padx=10, row=0, column=1, sticky=W)
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=0, column=1, sticky=E)
        
        
        CTkLabel(container, text="Border", font=("", 12)).grid(sticky=W, columnspan=2)
       
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "border_radius.png").as_posix()), Image.open((self.folder / "Images" / "border_radius_dark.png").as_posix()))).grid(sticky=W, pady=[0, 10])
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=2, column=0, sticky=E)
        
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "border_width.png").as_posix()), Image.open((self.folder / "Images" / "border_width_dark.png").as_posix()))).grid(padx=10, row=2, column=1, sticky=W)
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=2, column=1, sticky=E)
        
        container2 = CTkFrame(container, corner_radius=0, fg_color="transparent")
        container2.grid(columnspan=2, pady=[10, 10], sticky=W)
        
        CTkButton(container2, text="", border_width=.5, corner_radius=3, fg_color=ThemeManager.theme["CTkButton"]["border_color"], width=20, height=20).pack(side=LEFT, padx=10)
        CTkLabel(container2, text=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["border_color"])[1:], font=("", 11)).pack(side=LEFT, padx=[5, 20])
        CTkButton(container2, text="", border_width=.5, corner_radius=3, fg_color=ThemeManager.theme["CTkButton"]["border_color"][::-1], width=20, height=20).pack(side=LEFT, padx=10)
        CTkLabel(container2, text=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["border_color"][::-1])[1:], font=("", 11)).pack(side=LEFT)
        
        
        CTkLabel(container, text="Backgroud", font=("", 12)).grid(sticky=W, columnspan=2)
       
        container2 = CTkFrame(container, corner_radius=0, fg_color="transparent")
        container2.grid(columnspan=4, pady=[5, 10], sticky=W)
        
        CTkButton(container2, text="", border_width=.5, corner_radius=3, fg_color=ThemeManager.theme["CTkButton"]["fg_color"], width=20, height=20).pack(side=LEFT, padx=10)
        CTkLabel(container2, text=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"])[1:], font=("", 11)).pack(side=LEFT, padx=[5, 10])
        CTkButton(container2, text="", border_width=.5, corner_radius=3, fg_color=ThemeManager.theme["CTkButton"]["fg_color"][::-1], width=20, height=20).pack(side=LEFT, padx=10)
        CTkLabel(container2, text=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"][::-1])[1:], font=("", 11)).pack(side=LEFT)
        
        
        CTkLabel(container, text="Hover", font=("", 12)).grid(sticky=W, columnspan=2)
       
        container2 = CTkFrame(container, corner_radius=0, fg_color="transparent")
        container2.grid(columnspan=4, pady=5, sticky=W)
        
        CTkButton(container2, text="", border_width=.5, corner_radius=3, fg_color=ThemeManager.theme["CTkButton"]["hover_color"], width=20, height=20).pack(side=LEFT, padx=10)
        CTkLabel(container2, text=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["hover_color"])[1:], font=("", 11)).pack(side=LEFT, padx=[5, 10])
        CTkButton(container2, text="", border_width=.5, corner_radius=3, fg_color=ThemeManager.theme["CTkButton"]["hover_color"][::-1], width=20, height=20).pack(side=LEFT, padx=10)
        CTkLabel(container2, text=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["hover_color"][::-1])[1:], font=("", 11)).pack(side=LEFT)
    
    
        Separator(self.list_options, orient=HORIZONTAL, style="L.TSeparator").grid(columnspan=2, sticky=EW, pady=10)
         
        CTkLabel(self.list_options, text="Text", font=("", 12, "bold")).grid(padx=20, columnspan=2, sticky=W)
        CTkButton(self.list_options, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "down.png").as_posix()), Image.open((self.folder / "Images" / "down_dark.png").as_posix())), width=0).grid(padx=10, row=6, column=1, sticky=E)
       
        container = CTkFrame(self.list_options, corner_radius=0, fg_color="transparent")
        container.grid(sticky=EW, columnspan=2, padx=15)
        
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "font2.png").as_posix()), Image.open((self.folder / "Images" / "font2_dark.png").as_posix()))).grid(sticky=W, pady=10)
        CTkComboBox(container, border_width=0, fg_color=("grey90", "grey14"), font=("", 12), button_color=("grey90", "grey14"), height=24).grid(sticky=EW, row=0, column=0, columnspan=2, padx=[60, 10])
        

        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "uppercase.png").as_posix()), Image.open((self.folder / "Images" / "uppercase_dark.png").as_posix()), (24, 24))).grid(pady=5, sticky=W)
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=1, column=0, padx=[60, 30], sticky=E)
        
        container2 = CTkFrame(container, corner_radius=0, fg_color="transparent")
        container2.grid(row=1, column=1)
        
        CTkLabel(container2, text="", image=CTkImage(Image.open((self.folder / "Images" / "bold.png").as_posix()), Image.open((self.folder / "Images" / "bold_dark.png").as_posix()))).pack(side=LEFT)
        CTkLabel(container2, text="", image=CTkImage(Image.open((self.folder / "Images" / "italic.png").as_posix()), Image.open((self.folder / "Images" / "italic_dark.png").as_posix()))).pack(side=LEFT)
        CTkLabel(container2, text="", image=CTkImage(Image.open((self.folder / "Images" / "underline.png").as_posix()), Image.open((self.folder / "Images" / "underline_dark.png").as_posix()))).pack(side=LEFT)
        CTkLabel(container2, text="", image=CTkImage(Image.open((self.folder / "Images" / "overstrike2.png").as_posix()), Image.open((self.folder / "Images" / "overstrike2_dark.png").as_posix()))).pack(side=LEFT)
        
        
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "spacing.png").as_posix()), Image.open((self.folder / "Images" / "spacing_dark.png").as_posix()))).grid(pady=5, sticky=W)
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=2, column=0, padx=[60, 30], sticky=E)
        
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "align_left.png").as_posix()), Image.open((self.folder / "Images" / "align_left_dark.png").as_posix()), (20, 20))).grid(row=2, column=1, sticky=W)
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "align_center.png").as_posix()), Image.open((self.folder / "Images" / "align_center_dark.png").as_posix()))).grid(row=2, column=1)
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "align_left.png").as_posix()), Image.open((self.folder / "Images" / "align_left_dark.png").as_posix()))).grid(row=2, column=1, sticky=E)
        
        
        container2 = CTkFrame(container, corner_radius=0, fg_color="transparent")
        container2.grid(columnspan=2, pady=10, sticky=W)
        
        CTkButton(container2, text="", border_width=.5, corner_radius=3, fg_color=ThemeManager.theme["CTkButton"]["text_color"], width=20, height=20).pack(side=LEFT, padx=10)
        CTkLabel(container2, text=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["text_color"])[1:], font=("", 11)).pack(side=LEFT, padx=[5, 10])
        CTkButton(container2, text="", border_width=.5, corner_radius=3, fg_color=ThemeManager.theme["CTkButton"]["text_color"][::-1], width=20, height=20).pack(side=LEFT, padx=10)
        CTkLabel(container2, text=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["text_color"][::-1])[1:], font=("", 11)).pack(side=LEFT)


        CTkLabel(container, text="Anchor", font=("", 12)).grid(sticky=W, columnspan=2)
     
        container2 = CTkFrame(container, corner_radius=0, fg_color="transparent", border_width=1, border_color=("grey80", "grey20"))
        container2.grid(columnspan=2, pady=10)
        
        container2.columnconfigure(0, weight=1)
        container2.columnconfigure(1, weight=1)
        container2.columnconfigure(2, weight=1)
        
        container2.rowconfigure(0, weight=1)
        container2.rowconfigure(1, weight=1)
        container2.rowconfigure(2, weight=1)
        
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "top_left.png").as_posix()), Image.open((self.folder / "Images" / "top_left_dark.png").as_posix())), width=0).grid(row=0, column=0, padx=2, pady=2)
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "top_align.png").as_posix()), Image.open((self.folder / "Images" / "top_align_dark.png").as_posix())), width=0).grid(row=0, column=1, padx=2, pady=2)
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "top_right.png").as_posix()), Image.open((self.folder / "Images" / "top_right_dark.png").as_posix())), width=0).grid(row=0, column=2, padx=2, pady=2)
        
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "left_align.png").as_posix()), Image.open((self.folder / "Images" / "left_align_dark.png").as_posix())), width=0).grid(row=1, column=0, padx=2, pady=2)
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "recenter.png").as_posix()), Image.open((self.folder / "Images" / "recenter_dark.png").as_posix())), width=0).grid(row=1, column=1, padx=2, pady=2)
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "right_align.png").as_posix()), Image.open((self.folder / "Images" / "right_align_dark.png").as_posix())), width=0).grid(row=1, column=2, padx=2, pady=2)

        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "bottom_left.png").as_posix()), Image.open((self.folder / "Images" / "bottom_left_dark.png").as_posix())), width=0).grid(row=2, column=0, padx=2, pady=2)
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "bottom_align.png").as_posix()), Image.open((self.folder / "Images" / "bottom_align_dark.png").as_posix())), width=0).grid(row=2, column=1, padx=2, pady=2)
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "bottom_right.png").as_posix()), Image.open((self.folder / "Images" / "bottom_right_dark.png").as_posix())), width=0).grid(row=2, column=2, padx=2, pady=2)
        
        
        Separator(self.list_options, orient=HORIZONTAL, style="L.TSeparator").grid(columnspan=2, sticky=EW, pady=10)
        
        CTkLabel(self.list_options, text="Image", font=("", 12, "bold")).grid(padx=20, columnspan=2, sticky=W)
        CTkButton(self.list_options, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "down.png").as_posix()), Image.open((self.folder / "Images" / "down_dark.png").as_posix())), width=0).grid(padx=10, row=6, column=1, sticky=E)
       
        container = CTkFrame(self.list_options, corner_radius=0, fg_color="transparent")
        container.grid(sticky=EW, columnspan=2, padx=15)
        
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "width.png").as_posix()), Image.open((self.folder / "Images" / "width_dark.png").as_posix()))).grid(sticky=W)
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=0, column=0, pady=[10, 5], sticky=E)
        
        CTkLabel(container, text="", image=CTkImage(Image.open((self.folder / "Images" / "height.png").as_posix()), Image.open((self.folder / "Images" / "height_dark.png").as_posix()))).grid(padx=10, row=0, column=1, sticky=W)
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=0, column=1, sticky=E)        
        
        
        CTkLabel(container, text="Compound", font=("", 12)).grid(sticky=W, columnspan=2)
     
        container2 = CTkFrame(container, corner_radius=0, fg_color="transparent", border_width=1, border_color=("grey80", "grey20"))
        container2.grid(columnspan=2, pady=10)
        
        container2.columnconfigure(0, weight=1)
        container2.columnconfigure(1, weight=1)
        container2.columnconfigure(2, weight=1)
        
        container2.rowconfigure(0, weight=1)
        container2.rowconfigure(1, weight=1)
        container2.rowconfigure(2, weight=1)
        
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "align_start.png").as_posix()), Image.open((self.folder / "Images" / "align_start_dark.png").as_posix())), width=0).grid(row=0, column=1, padx=2, pady=2)
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "align_justify_flex_start.png").as_posix()), Image.open((self.folder / "Images" / "align_justify_flex_start_dark.png").as_posix())), width=0).grid(row=1, column=0, padx=2, pady=2)
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "align_justify_flex_end.png").as_posix()), Image.open((self.folder / "Images" / "align_justify_flex_end_dark.png").as_posix())), width=0).grid(row=1, column=2, padx=2, pady=2)
        CTkButton(container2, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "align_end.png").as_posix()), Image.open((self.folder / "Images" / "align_end_dark.png").as_posix())), width=0).grid(row=2, column=1, padx=2, pady=2)
       
        
        Separator(self.list_options, orient=HORIZONTAL, style="L.TSeparator").grid(columnspan=2, sticky=EW, pady=10)
         
        CTkLabel(self.list_options, text="Position", font=("", 12, "bold")).grid(padx=20, columnspan=2, sticky=W)
        CTkButton(self.list_options, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "down.png").as_posix()), Image.open((self.folder / "Images" / "down_dark.png").as_posix())), width=0).grid(padx=10, row=9, column=1, sticky=E)
       
        container = CTkFrame(self.list_options, corner_radius=0, fg_color="transparent")
        container.grid(sticky=EW, columnspan=2, padx=15)
        
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
       
        CTkLabel(container, text="Place", font=("", 12)).grid(sticky=W, columnspan=2)
       
        container2 = CTkFrame(container, corner_radius=0, fg_color="transparent")
        container2.grid(columnspan=2, padx=15, pady=5)

        CTkLabel(container2, text="x").pack(padx=[0, 20], side=LEFT)
        CTkEntry(container2, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).pack(side=LEFT)
        
        CTkLabel(container2, text="y").pack(padx=[30, 20], side=LEFT)
        CTkEntry(container2, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).pack(side=LEFT)
        
        
        CTkLabel(container, text="relx").grid(pady=5, sticky=W)
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=2,column=0, sticky=E)
        
        CTkLabel(container, text="rely").grid(row=2, column=1, padx=[15, 0], sticky=W)
        CTkEntry(container, justify=CENTER, border_width=0, fg_color=("grey90", "grey14"), height=22, width=50).grid(row=2, column=1, sticky=E)
        
        
        Separator(self.list_options, orient=HORIZONTAL, style="L.TSeparator").grid(columnspan=2, sticky=EW, pady=10)
         
        CTkLabel(self.list_options, text="Children manage", font=("", 12, "bold")).grid(padx=20, columnspan=2, sticky=W)
        CTkButton(self.list_options, text="", fg_color="transparent", hover_color=("grey80", "grey20"), image=CTkImage(Image.open((self.folder / "Images" / "down.png").as_posix()), Image.open((self.folder / "Images" / "down_dark.png").as_posix())), width=0).grid(row=12, column=1, sticky=E)
       
        container = CTkFrame(self.list_options, corner_radius=0, fg_color="transparent")
        container.grid(sticky=EW, columnspan=2, padx=15)
        
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        
        
        
        # CONTENEUR DU MILIEU
        
        self.view.columnconfigure(0, weight=1)
        self.view.rowconfigure(1, weight=1)
        
        
        view_switch = CTkSegmentedButton(self.view, values=[str(i)*5 for i in range(5)])
        view_switch.grid(pady=10)
        
        self.app_frame= CTkFrame(self.view, corner_radius=0, fg_color="transparent", border_width=.5, border_color=("gray80", "gray20"))
        self.app_frame.grid(sticky=NSEW)
        
        
        # Lier l'événement de clic à la fonction d'ajout de widget
        self.app_frame.bind("<Button-1>", self.create_widget)

        # Lier l'événement de pression de la touche "Delete" à la fonction de suppression du widget
        self.app_frame.bind("<Delete>", self.delete_widget)
        
        # Initialisation de la variable pour les boutons radio
        self.selection = arrow
        
        # Variable pour les widgets de la fenetre
        self.widget = self.app_frame
        self.deleting = True
        self.updating = False
        self.poo = True
        self.file = ""
        self.sep = ["(\n\t\t\t", ",\n\t\t\t", "\n\t\t)"]
        self.defauts = {}
        self.widgets_list = {}
        self.all_children = {self.app_frame: {"nom": "App", "classe": "CTk", "children": {}}}
        
        # Le canvas pour afficher les éléments de rédimensionnenent
        self.canvas =  CTkCanvas(border=0, relief=FLAT)
        
        # Dessin du cadre entourant le widget
        self.canvas.create_rectangle(0, 0, 0, 0, outline="blue1", width=1, dash=1, tag="rectangle")

        # Afficage des points de rédimensionnenent
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_NW", "size_nw_se", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_N", "sb_v_double_arrow", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_NE", "size_ne_sw", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_W", "sb_h_double_arrow", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_SE", "size_nw_se", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_S", "sb_v_double_arrow", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_SW", "size_ne_sw", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_E", "sb_h_double_arrow", "points"))

        self.canvas.tag_bind("canvas", "<1>", self.create_widget)
        self.canvas.tag_bind("points", "<Leave>", lambda e: self.canvas.configure(cursor="arrow"))
        self.canvas.tag_bind("points", "<Enter>", lambda e: self.canvas.configure(cursor=self.canvas.gettags("current")[1]))

        # Lier l'événement de  redimensionnement des widgets
        self.canvas.tag_bind("points", "<1>", lambda e: exec("self.start_x, self.start_y = self.winfo_pointerxy()", {"self": self}))
        self.canvas.tag_bind("points", "<B1-Motion>", self.resize_widget)
        #self.canvas.tag_bind("points", "<ButtonRelease>", self.update_position_code)
        
        
        # FRAME DES OPTIONS

        self.Splitter = PanedWindow(
            self.view,
            orient=VERTICAL,
            background=self._apply_appearance_mode(self._fg_color),
        )
        
        #self.Splitter.pack(fill=BOTH, padx=5, pady=5)
        
        code_Frame = CTkFrame(
            self.Splitter,
            fg_color=self.view._fg_color,
            bg_color=self._fg_color,
            corner_radius=0,
            border_width=0
        )
        
        self.view_bar = CTkSegmentedButton(
            code_Frame,
            border_width=0,
            corner_radius=0,
            fg_color=("gray90", "gray10"),
            #unselected_color=self.bar_Frame._fg_color,
            #selected_color=code_Frame._fg_color,
            #selected_hover_color=code_Frame._fg_color,
            unselected_hover_color=("white", "gray30"),
            text_color=("black", "white"),
            font=("Calibri", 16),
            command=lambda v: ...,
            values=["code" , "fenetre"],
            height=42,
        )
        
        self.Splitter.add(code_Frame, height=self.winfo_screenheight())

        self.code_Text = CTkTextbox(
            code_Frame,
            width = self.winfo_screenwidth()-280,
            height=self.winfo_screenheight()-80,
            corner_radius=0,
            border_width=0,
            border_color=("black", "gray0"),
            font=("Consolas", 13),
            fg_color=self.cget("fg_color"),
            #selectbackground=self._apply_appearance_mode(("light sky blue", "gray20")),
            #selectforeground="",
            text_color=("black", "white"),
            tabs="24p",
            undo=True,
            maxundo=-1,
            wrap="word"
        )
        
        self.code_Text.insert(0.0, open(__file__).read())

        self.code_Text.pack(padx=[20, 5], pady=[5, 0])
        self.code_Text._textbox.tag_configure("widget")
        self.code_Text._y_scrollbar.configure(width=6)
        
        self.code_Text.bind("Control-Z", lambda e: self.code_Text.edit_undo())
        self.code_Text.bind("Control-Y", lambda e: self.code_Text.edit_redo())
        
        self.code_Text.bind("<KeyRelease-Return>", lambda e: self.code_Text.insert(INSERT, "\t\t", self.code_Text.tag_names("current")[-1]))
        
        self.cdg = ic.ColorDelegator()
        self.cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat().pattern, re.S)
        self.cdg.idprog = re.compile(r'\s+(\w+)', re.S)
        
        self.highlighted_textbox = ip.Percolator(self.code_Text._textbox)
        self.highlighted_textbox.insertfilter(self.cdg)

        #self.highlighted_textbox.redir.register("insert", self.check_text_insertion)
        #self.highlighted_textbox.redir.register("delete", self.check_text_delete)
        
        self.change_code_theme()

        self.message_Frame = CTkFrame(
            self.Splitter,
            corner_radius=0,
            border_width=0,
            border_color="black",
            fg_color=self.list_widgets.cget("fg_color")
        )

        self.msg_box_bar = CTkSegmentedButton(
            self.message_Frame,
            corner_radius=10,
            fg_color=self.message_Frame._fg_color,
            unselected_color=self.message_Frame._fg_color,
            selected_color=self.message_Frame._fg_color,
            selected_hover_color=("white", "gray20"),
            unselected_hover_color=("white", "gray20"),
            text_color=("black", "white"),
            font=("Arial", 12),
            height=30,
            #variable=bt_var
        )
        
        self.msg_box_bar.pack(side=TOP, anchor=NE)

        for i, widget in enumerate(list(self.msg_box_bar.children.values())[1:]): widget.configure(text_color=[("black", "green4"), ("red", "red3")][i], font=("Arial", [14, 12][i]),)

        self.message_box = CTkTextbox(
            self.message_Frame,
            corner_radius=0,
            border_width=0,
            width = self.winfo_screenwidth()-280,
            height=self.winfo_screenheight()-80,
            font=("Consolas", 14),
            fg_color=self.list_widgets.cget("fg_color"),
            #electbackground=self._apply_appearance_mode(("LightSkyBlue", "gray35")),
            state="disabled"
        )
        
        self.message_box.pack(fill=X)
        #self.message_box.tag_configure("error", foreground=self._apply_appearance_mode(("red", "red1")))
        self.Splitter.add(self.message_Frame, minsize=0)

        self.style.configure("S.TSeparator", background=self._apply_appearance_mode(("grey80", "grey20")))
        separator = Separator(
            self.Splitter,
            orient=HORIZONTAL,
            style="S.TSeparator"
        )

        separator.place(x=-5, y=-5, height=2)

        verify = lambda: self.after(100, verify) if self.Splitter.identify(self.winfo_pointerx() - self.Splitter.winfo_rootx(), self.winfo_pointery() - self.Splitter.winfo_rooty()) else (self.style.configure("S.TSeparator", background=self._apply_appearance_mode(("grey80", "grey20"))), separator.place_forget(), self.message_box_height.set(self.Splitter.sash_coord(0)[1]))
        self.Splitter.bind("<Motion>", lambda e: self.Splitter.identify(e.x, e.y) and (separator.place(dict(zip(("x", "y", "relwidth"), list(self.Splitter.sash_coord(0))+[1]))), self.style.configure("S.TSeparator", background=self._apply_appearance_mode(("grey80", "grey20"))), self.after(100, verify)))\
            
    def change_selection(self, e: Event):
        self.selection.configure(fg_color="transparent", hover_color=("gray90", "gray15"))
        self.selection = e.widget.master
        self.selection.configure(fg_color=("gray80", "gray20"), hover_color=("gray80", "gray20"))
    
    def create_widget(self, e: Event): # Fonction pour ajouter le widget sélectionné à l'emplacemen du clic
        classe = "CTk" + self.selection.cget("text").strip()
        
        if "Selection" not in classe: # and not self.canvas.winfo_ismapped():
            parent = e.widget.master if isinstance(e.widget, CTkCanvas) else e.widget
            
            x, y = e.x, e.y
            
            widget = eval(classe)(parent) # = getattr(globals()[classe])(parent)
            
            # Obtenir la signature de la méthode __init__
            arguments = signature(widget.__init__).parameters
            
            nom = classe.removeprefix("CTk") + str(max([int(w["nom"][len(classe.removeprefix("CTk")):] or 0) for w in self.all_children.values() if w["classe"] == classe] or [0]) +1)

            if any(i == "text" for i in arguments.keys()): widget.configure(text=nom)
              
            widget.place_configure(x=x, y=y)
            
            # self.Tree.insert(parent, END, widget, image=package.capitalize()+classe+"_ico", text=f" {nom}", tag=(nom, "widget"))
            #self.Tree.insert(parent, END, widget, image="Window", text=f" {nom}", tag=(nom, "widget"))

            if any(i == "state" for i in arguments.keys()): widget.configure(state="disabled")
            if any(i == "text_color_disabled" for i in arguments.keys()): widget.configure(text_color_disabled=widget.cget("text_color"))
            
            place_info = {key: value for key, value in widget.place_info().items() if key in "x y width height"}
            #place_info.update({"width": widget.winfo_width(), "height": widget.winfo_height()})
            
            self.all_children[widget] = self.all_children[parent]["children"][widget] = {
                "nom": nom,
                "classe": classe,
                "parent": parent,
                "options": {},
                "children": {},
                "position": place_info
            }
            
            return
            
            items = {key: value for key, value in items if value and value != self.defauts[package+"."+classe][key] and (str(value).isnumeric() and int(value) or not str(value).isnumeric())}.items()
            parent_name = ("self" if self.poo else self.all_children[self.app_frame]["nom"]) if parent == self.app_frame else ("self." if self.poo else "")+self.all_children[parent]["nom"]

            text = ("\n\t\tself." if self.poo else "\n")+nom+" = "+(package+"." if package in ("ttk", "Pmw") else "")+classe+(self.sep[0] if items else "(")+parent_name+(self.sep[1] if items else "")
            text += self.sep[1].join([key+"="+str("\""+str(value)+"\"" if not ((value.isnumeric() or value[1:].isnumeric()) and int(value)) else value) for key, value in items if value])+(self.sep[2] if items else ")")+"\n"+("\n" if items else "")
            
            self.highlighted_textbox.insert(self.limite[0], text, tags=(nom, "widget"))
            
            text = ("\t\tself." if self.poo else "")+nom+".place("
            text += ", ".join([key+"="+str(value) for key, value in place_info.items()])+")\n"

            self.highlighted_textbox.insert(nom+".last", text, tags=(nom, nom+".pos", "widget"))

            
            self.limite = self.code_Text.index(f"{nom}.last"), nom

            # Actualisation de l'affichage
            self.update_idletasks()
            
            # Lier l'événement de déplacement du widget
            widget.bind("<B1-Motion>", self.move_widget)
            widget.bind("<Button-1>", lambda e: self.select_widget(e.widget) if self.selection.get() == "arrow" else self.create_widget(e))
            widget.bind("<ButtonRelease>", self.update_position_code)
            widget.bind("<Delete>", self.delete_widget)

            # Selection du widget pour modification
            self.select_widget(widget)

            # Réinitialiser le sélécteur
            # self.selection.set("arrow")

        elif self.widget != self.app_frame and e.widget in (self.app_frame, self.canvas) and len(self.canvas.gettags("current")) <= 2: # Déselection du widget en supprimmant le rectangle te les points de redimensionnement
            
            self.canvas.place_forget()
            self.resizing = False

            if any(i == "cursor" for i in arguments.keys()): self.widget.configure(cursor="arrow")

            #self.code_Text.tag_configure(self.widgets_list[self.app_frame]["children"][self.widget]["nom"], background="")
            #self.code_Text.tag_config(self.widgets_list[self.app_frame]["nom"], background=self.code_Text._textbox["selectbackground"])

            #self.code_Text.see((self.code_Text.index(f"{self.widgets_list[self.app_frame]['nom']}.first")))
            
            #self.Tree.selection_set(self.app_frame)
            
            self.widget = self.app_frame
            #self.update_options_Frame()

    def select_widget(self, widget, resizing=False):
        # Récupération de la position de la souris pour le déplacement du widget
        self.start_x, self.start_y = self.winfo_pointerxy()

        if "cursor" in self.widget.keys(): widget.configure(cursor="fleur")

        x, y, width, height = widget.winfo_x()-4, widget.winfo_y()-4, widget.winfo_width()+10, widget.winfo_height()+10
        
        self.canvas.configure(bg=widget.master["bg"])
        self.canvas.place(in_=widget.master, x=-2, y=-2, relwidth=1.1, relheight=1.1)

        color = "black" if all([i >= 32896 for i in self.winfo_rgb(self.canvas["bg"])]) else "white"
        self.canvas.itemconfigure("points", fill=color, outline=color)
        
        # Dessin du cadre entourant le widget
        self.canvas.coords("rectangle", (x, y, x+width, y+height))
        
        # Afficage des points de rédimensionnenent
        self.canvas.coords("point_NW", (x-2, y-2, x+2, y+2))
        self.canvas.coords("point_N", (x+(width/2)-2, y-2, x+(width/2)+2, y+2))
        self.canvas.coords("point_NE", (x+width-2, y-2, x+width+2, y+2))
        self.canvas.coords("point_E", (x+width-2, y+(height/2)-2, x+width+2, y+(height/2)+2))
        self.canvas.coords("point_SE", (x+width-2, y+height-2, x+width+2, y+height+2))
        self.canvas.coords("point_S", (x+(width/2)-2, y+height-2, x+(width/2)+2, y+height+2))
        self.canvas.coords("point_SW", (x-2, y+height-2, x+2, y+height+2))
        self.canvas.coords("point_W", (x-2, y+(height/2)-2, x+2, y+(height/2)+2))

        self.code_Text.see(float(self.code_Text.index(f"{self.all_children[widget]['nom']}.first"))+10)
        
        if not resizing and self.widget != widget:
            self.Tree.selection_set(widget)
            self.Tree.see(widget)

            # Dans le text
            #self.code_Text.tag_configure(self.widgets_list[self.app_frame]["children"][self.widget]["nom"], background="")
            #self.code_Text.tag_configure(self.widgets_list[self.app_frame]["children"][widget]["nom"], background=self.code_Text._textbox["selectbackground"])

            self.widget = widget
            self.update_options_Frame()

    def delete_widget(self, e): # Fonction pour supprimer le widget sélectionné
        if self.widget != self.app_frame:
            if askyesno("Suppresion", f"Voulez-vous supprimez {self.all_children[self.widget]['nom']} ?"):
                # Suppression du texte correspondant
                widget_opts_dict = self.all_children[self.widget]
                package = widget_opts_dict["package"]
                
                self.modules_opts[package][1] -= 1

                if package != "tkinter":
                    if not self.modules_opts[package][1]:
                        self.deleting = True
                        self.code_Text.delete(f"{package}.import.first", f"{package}.import.last")

                a, b = self.code_Text.tag_ranges(widget_opts_dict["nom"])
                self.deleting = True
                self.code_Text.delete(a, b)

                if widget_opts_dict["nom"] == self.limite[1]:
                    self.limite = a, widget_opts_dict["nom"]
                    self.code_Text.tag_delete(self.limite[1])

                self.Tree.delete(self.widget)

                # TO DO: Recursion delete
                for widget in widget_opts_dict["children"]: widget.destroy()
                
                self.all_children[widget_opts_dict["parent"]]["children"].pop(self.widget)
                self.all_children.pop(self.widget)
                self.widget.destroy()

                self.canvas.place_forget()
                self.resizing = False
            
                self.widget = self.app_frame
                self.update_options_Frame()

        else: self.bell()

    def resize_widget(self, e): # Rédimensionner le widget en maintenant le clic gauche de la souris
        if self.widget != self.app_frame:
            delta_x, delta_y = e.x_root - self.start_x, e.y_root - self.start_y

            if abs(delta_x) >= 5 or abs(delta_y) >= 5:

                if "E" in e.widget.gettags(CURRENT)[0]:
                    self.widget.place_configure(width=int(self.widget.winfo_width() + delta_x))

                elif "W" in e.widget.gettags(CURRENT)[0]:
                    self.widget.place_configure(x=self.widget.winfo_x() + delta_x, width=int(self.widget.winfo_width()) - delta_x)

                if "S" in e.widget.gettags(CURRENT)[0]:
                    self.widget.place_configure(height=int(self.widget.winfo_height() + delta_y))

                elif "N" in e.widget.gettags(CURRENT)[0]:
                    self.widget.place_configure(y=self.widget.winfo_y() + delta_y, height=int(self.widget.winfo_height()) - delta_y)

                # Enregistrement de la nouvelle position de la souris
                self.start_x, self.start_y = self.winfo_pointerxy()

                # déplacer aussi le rectangle de rédimensionnement
                self.update_idletasks()
                self.select_widget(self.widget, True)
                self.update_position_code(e)
   
    def move_widget(self, e): # Fonction déplacer le widget dans la fénêtre
        if self.widget != self.app_frame:
            delta_x, delta_y = e.x_root - self.start_x, e.y_root - self.start_y

            if abs(delta_x) >= 5 or abs(delta_y) >= 5:
                x, y = int(self.widget.place_info()["x"]) + delta_x, int(self.widget.place_info()["y"]) + delta_y
                self.widget.place_configure(x=x, y=y)

                # déplacer aussi le rectangle de redimensionnement
                self.update_idletasks()
                self.select_widget(self.widget, True)

                # Enregistrement de la nouvelle position de la souris
                self.start_x, self.start_y = self.winfo_pointerxy()

    def change_code_theme(self):
        self.style.configure("TSeparator", background=self._apply_appearance_mode(("grey80", "black")))
        self.style.configure("L.TSeparator", background=self._apply_appearance_mode(("grey90", "grey0")))
        self.style.configure("S.TSeparator", background=self._apply_appearance_mode(("grey80", "grey20")))
        
        self.cdg.tagdefs['MYGROUP'] = {'foreground': self._apply_appearance_mode(('#7F7F7F', "gray60"))}

        # These five lines are optional. If omitted, default colours are used.
        self.cdg.tagdefs['COMMENT'] = {'foreground': self._apply_appearance_mode(('#dd0000', "#dd0000")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}
        self.cdg.tagdefs['KEYWORD'] = {'foreground': self._apply_appearance_mode(('#ff7700', "#569CD6")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}
        self.cdg.tagdefs['BUILTIN'] = {'foreground': self._apply_appearance_mode(('#900090', "#ff00ff")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}
        self.cdg.tagdefs['STRING'] = {'foreground': self._apply_appearance_mode(('#00aa00', "#02ff02")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}
        self.cdg.tagdefs['DEFINITION'] = {'foreground': self._apply_appearance_mode(('#0000ff', "#5e5eff")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}
        
        self.cdg.config_colors()
    
if __name__ == '__main__': TK_Designer().mainloop()
    