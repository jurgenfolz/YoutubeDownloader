import yt_dlp
import os
from ttkthemes import ThemedTk
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import re
import math
import threading


class Downloader:
    
    def __init__(self,theme):
        self.theme=theme
        self.application_path = os.path.dirname(os.path.abspath(__file__))
    
    def progress_hook(self,d):
        #Verify if the download is finished
        if d['status'] == 'downloading':
            prog_string=d['_percent_str']
            prog_string = d['_percent_str'].replace('%', '')  # Remove the '%' character
            prog_float = float(prog_string)  # Convert the string to a float
            prog_int = math.floor(prog_float)  # Convert the float to an integer, rounding down
            self.main_window.after_idle(self.write, f"\nDownload progress: {d['_percent_str']}")
            self.main_window.after_idle(self.progress.set, prog_int)
        elif d['status'] == 'finished':
            self.write(f"\n✅ Done.",tag='green')
            
    def download_as_video(self,url,output_dir,format):
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'ffmpeg_location': f'{self.application_path}\\ffmpeg\\bin',
            'merge_output_format': format,
            'progress_hooks': [self.progress_hook],
            'no_color': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_as_audio(self,url,output_dir):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'ffmpeg_location': f'{self.application_path}\\ffmpeg\\bin',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [self.progress_hook],
            'no_color': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    # region Main GUI
    def main_gui(self):
        self.main_window = ThemedTk(theme=self.theme)
        self.main_window.title("Youtube Downloader")  # Title
        self.main_window.geometry("500x400+50+50")  # size
        self.main_window.resizable(0, 0)
        self.main_window.iconbitmap(self.application_path + "\\images\\logo.ico")  # icon
        # >>>Frame:
        
        
        self.main_frame = ttk.Frame(self.main_window, padding=10)
        self.main_frame.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor="n")
        
        self.build_widgets()
        

        self.main_window.lift()
        self.main_window.mainloop()
    
    def build_widgets(self):
        style = ttk.Style(self.main_frame)
        style.configure("title.TLabel", justify=tk.CENTER)
        
        logo_size=(30,20) #logo size
        yt_logo = Image.open(self.application_path + "\\images\\youtubelogo.png") #logo path
        yt_logo = yt_logo.resize(logo_size) #resize logo
        self.logo = ImageTk.PhotoImage(yt_logo) #convert logo to tkinter image

        logo_mk_label = ttk.Label(self.main_frame, image=self.logo, style="title.TLabel",text="Youtube Downloader",compound="left") #create label with logo
        logo_mk_label.config(anchor="center") #center the label
        logo_mk_label.place(relx=0, rely=0, relwidth=1, relheight=0.1) #place the label
        
        
        url_label = ttk.Label(self.main_frame, text="URL") #create label
        url_label.place(relx=0, rely=0.11,relheight=0.08,relwidth=.1)#place the label
        
        self.url_entry = ttk.Entry(self.main_frame) #create entry
        self.url_entry.place(relx=0.11, rely=0.11,relheight=0.08,relwidth=0.89) #place the entry
        
        out_label = ttk.Label(self.main_frame, text="Output") #create label
        out_label.place(relx=0, rely=0.19,relheight=0.08,relwidth=.1) #place the label
        
        self.output_dir_entry = ttk.Entry(self.main_frame) #create entry
        self.output_dir_entry.place(relx=0.11, rely=0.2,relheight=0.08,relwidth=0.79) #place the entry
        self.output_dir_entry.insert(0, self.application_path) #set the default value
        
        self.folder_btn = ttk.Button(self.main_frame, text="📁", command=self.select_folder) #button to select folder
        self.folder_btn.place(relx=0.91, rely=0.2,relheight=0.08,relwidth=0.09) #place the button
        
        
        values = ['Video (.mp4)', 'Video (.mkv)', 'Audio (.mp3)'] # Define the values for the combobox
        self.combo_box = ttk.Combobox(self.main_frame, values=values) # Create the combobox
        
        form_label = ttk.Label(self.main_frame, text="Format") #create label
        form_label.place(relx=0, rely=0.29,relheight=0.08,relwidth=.1) #place the label
        
        self.combo_box.set('Video (.mp4)') # Set the default value
        self.combo_box.place(relx=0.11, rely=0.29,relheight=0.08,relwidth=.69) #place the combobox
        
        self.download_btn = ttk.Button(self.main_frame, text="Download", command=self.download) #create button
        self.download_btn.place(relx=0.81, rely=0.29,relheight=0.08,relwidth=.19) #place the button
        
        
        self.text_area = tk.Text(self.main_frame)
        self.text_area.place(relx=0, rely=0.38,relheight=0.56,relwidth=1) #place the text area
        
        fontsize = 10
        font = f"Calibri {fontsize} normal roman"
        self.text_area["font"] = font
        self.text_area["border"] = "1"
        
        self.progress = tk.DoubleVar()  # Create a DoubleVar to hold progress
        self.progressbar = ttk.Progressbar(self.main_frame, variable=self.progress, maximum=100)  # Create a Progressbar that uses progress
        self.progressbar.place(relx=0, rely=0.95, relwidth=1, relheight=0.05) #place the progressbar
       
    def select_folder(self):
        folder=filedialog.askdirectory() #open file dialog
        if folder: #if folder is selected
            self.output_dir_entry.delete(0, tk.END) #delete the entry
            self.output_dir_entry.insert(0, folder) #insert the folder path
           
    def download(self):
        self.delete_text() #clear the text area
        go_ahead_download = True #flag to check if the download can proceed
        
        url = self.url_entry.get() #get the url from the entry
        is_valid = self.validate_youtube_url(url) #validate the url
        self.write(f"URL: {url}") #write the url to the text area
        #write the validation result to the text area

        if not is_valid:
            self.write(f"\nValid URL: {is_valid}",tag="red")
            tk.messagebox.showerror("Error", "Invalid URL")
            go_ahead_download=False
        else:
            self.write(f"\nValid URL: {is_valid}",tag="green")
        
        output_dir = self.output_dir_entry.get()
        if not os.path.isdir(output_dir):
            self.write(f"\nInvalid output folder",tag="red")
            tk.messagebox.showerror("Error", "Invalid output folder")
            go_ahead_download=False
        
            
        if go_ahead_download:
            self.write(f"\nStarting download...")
            if self.combo_box.get() == 'Video (.mp4)':
                threading.Thread(target=self.download_as_video,args=(url,output_dir,'mp4')).start()
            elif self.combo_box.get() == 'Video (.mkv)':
                threading.Thread(target=self.download_as_video,args=(url,output_dir,'mkv')).start()
            elif self.combo_box.get() == 'Audio (.mp3)':
                threading.Thread(target=self.download_as_audio,args=(url,output_dir)).start()
            else:
                pass
    
    def write(self,text,tag="black"):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert("end", f"{text}", tag)
        self.text_area.tag_config("black", foreground="black")
        self.text_area.tag_config("red", foreground="red")
        self.text_area.tag_config("green", foreground="green")
        self.text_area.tag_config("yellow", foreground="#d17402")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        
    def delete_text(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
    @staticmethod
    def validate_youtube_url(url):
        youtube_regex = (
            r"(https?://)?(www\.)?"
            "(youtube|youtu|youtube-nocookie)\.(com|be)/"
            "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
        )

        youtube_match = re.match(youtube_regex, url)
        return youtube_match is not None  # Return True if the URL is a valid YouTube URL, False otherwise
    
    # endregion
        
if __name__ == '__main__': 
    d=Downloader(theme='arc')
    d.main_gui()