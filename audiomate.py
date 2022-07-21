from ingest.preprocessing import prepare
from video.graphics import create_frames

PATH = "input/elektronimia_sky_high.wav"
BG = "audio_samples/dummy_bg_3.jpg"
FPS = 60

class UserOptions:

    def __init__(self):
        self.audio_path = None
        self.background_path = None
        self.fps = 30
        self.height = None
        self.width = None
        self.bg_color = None
        self.bar_color = None
        self.spacing = 5
        self.bar_count = None
        self.bar_height = None
        self.animation_smoothing = None

    def prompt_all(self):
        self.prompt_music()
        self.prompt_background()
        self.prompt_bar_color()
        self.prompt_fps()
        self.prompt_bar_count()
        self.prompt_spacing()
        self.prompt_smoothing()
        self.prompt_bar_height()

        self.print_separator()
        print("Thank you, setup complete. Starting...")
        self.print_separator()
        return

    def prompt_music(self):
        self.print_separator()
        print("Please enter the name of the audio file you would like to process. The audio file must be in the \"input\" folder.")
        ans = input("> File name (including extension):  ")
        self.audio_path = "./input/" + ans.strip()
    
    def prompt_background(self):
        self.print_separator()
        use_custom = self.get_yes_no("Would you like to use an image as a background?")

        if use_custom:
            print("Please enter the name of the image file you would like to use. The file must be in the \"input\" folder.")
            ans = input("> File name (including extension):  ")
            self.background_path = "./input/" + ans.strip()
        else:
            self.bg_color = self.get_rgb("Please enter a background color to use. (RGB format) ")
            self.height = self.get_int("Please enter the height of the video (vertical pixels): ", 100, 10000)
            self.width = self.get_int("Please enter the width of the video (horizontal pixels): ", 100, 10000)

    def prompt_bar_color(self):
        self.print_separator()
        self.bar_color = self.get_rgb("Please enter a color for the animated bars. (RGB format) ")

    def prompt_fps(self):
        self.print_separator()
        self.fps = self.get_int("Please enter the framerate of the video (FPS): ", 1, 500)

    def prompt_bar_count(self):
        self.print_separator()
        self.bar_count = self.get_int("Please enter the number of animated bars you want. (default is 30): ", 1, int(self.width / 3))

    def prompt_spacing(self):
        self.print_separator()
        self.spacing = self.get_int("Please enter the amount of horizontal spacing between the bars. Adding more spacing will make the bars narrower. (default spacing is 5 pixels): ", 0, 100)

    def prompt_bar_height(self):
        self.print_separator()
        self.bar_height = self.get_int("Please enter the height of the animated bars. (Default is 3)", 0, 10)
    
    def prompt_smoothing(self):
        self.print_separator()
        self.animation_smoothing = self.get_int("Please enter the amount of smoothing to apply to the animcation.\n Higher numbers make the animation more fluid. Lower numbers make it more chaotic but more responsive to the music.\n Higher framerates might require more smoothing. (Default is 8)", 1, 100)


    def get_yes_no(self, text):
        while True:
            ans = input(text + " [ Y / N ]  ").lower().strip()
            if ans == 'y':
                return True
            elif ans == 'n':
                return False
            
    def get_rgb(self, text):
        print(text)
        r = self.get_int("RED ", 0, 255)
        g = self.get_int("GREEN ", 0, 255)
        b = self.get_int("BLUE ", 0, 255)
        return (r,g,b)

    def get_int(self, text, min, max):
        while True:
            ans = input(text + " (a whole number between " + str(min) + " and " + str(max) + ") :  ")
            
            try:
                ans = int(ans)
            except:
                print("Please enter a whole number between ", min, "and", max)
                continue
            
            if ans > max:
                print("Number too large. Max allowed is", max)
            elif ans < min:
                print("Number too small. Min allowed is", min)
            else:
                return ans

    def print_separator(self):
        print("-----------------------------------")

def main():
    op = UserOptions()
    op.prompt_all()

    ffts = prepare(file_path = op.audio_path, 
                    fps = op.fps, 
                    bars_per_frame = op.bar_count)

    renderer = create_frames(ffts = ffts, 
                            fps = op.fps, 
                            smoothing = op.animation_smoothing, 
                            spacing = op.spacing, 
                            bar_color = op.bar_color,
                            height = op.height,
                            width = op.width,
                            custom_background = op.background_path,
                            bgcolor = op.bg_color)


    renderer.finalize(audio_file = op.audio_path)
    return 0


main()