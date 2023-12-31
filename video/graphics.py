import numpy as np
import matplotlib.pyplot as plt
from random import randint
from PIL import Image, ImageDraw
from video.rendering import RenderGroup



PATH = "audio_samples/underwaterbeats_delete.wav"
HEIGHT = None
WIDTH = None

def create_canvas(height, width, bgcolor = None, custom_background = None) -> np.array:    
    global HEIGHT
    global WIDTH
    
    if custom_background == None:
        HEIGHT = height
        WIDTH = width

        # Create blank black background of chosen size
        return Image.new("RGB", (WIDTH, HEIGHT), bgcolor)
    else:
        # Open the image
        custom_background = Image.open(custom_background)
        # Convert to numpy array
        custom_background = np.array(custom_background)
        
        # Load the size
        HEIGHT = custom_background.shape[0]
        WIDTH = custom_background.shape[1]
        
        # Log size to console
        print("Custom height: ", HEIGHT, "| Custom width: ", WIDTH)
        
        return custom_background

def ffts_to_heights (max_height, ffts):
    # Prepare the arguments
    max_height = int(max_height)
    ffts = np.array(ffts)

    # Convert from fft amplitudes to bar heights
    max_val = ffts.max()
    if (max_val == 0):
        return ffts

    heights = ffts / max_val    # Normalize
    heights = heights * max_height  # Scale to max height

    return heights    

def smoothen_heigths(heights, n = 5):
    result = np.array(heights)
    for i in range(n, len(heights)-n):
        for j in range(len(heights[i])):
            sum = 0
            for k in range(i-n, i+n):
                sum += heights[k][j]
            mean = sum / (n * 2 + 1)
            result[i][j] = mean

    return result #normalize(result)


def create_frames(ffts :np.array, fps, smoothing, spacing, bar_color, height = 480, width = 640, custom_background = None, bgcolor = None):

    background = create_canvas(height, width, bgcolor, custom_background)

    render_group = RenderGroup(HEIGHT, WIDTH, fps, 10e9)

    heights = ffts_to_heights(HEIGHT, ffts)
    heights = smoothen_heigths(heights, smoothing)
    heights = heights * 3

    frame_num = 1
    for frame in heights:
        frame_background = Image.fromarray(background)
        
        draw_bars(frame_background, frame, spacing, bar_color)
        render_group.add_frame(np.array(frame_background))

        print_progress_bar(iteration=frame_num, total=len(heights), decimals=2, prefix="Generating Animation")
        frame_num += 1
    
    return render_group

def draw_bars(background, heights, spacing, bar_color):
    global WIDTH
    global HEIGHT

    drawing = ImageDraw.Draw(background)
    
    bar_count = len(heights)    # The number of bars
    total_spacing = spacing * (bar_count + 1)   # The total width of all the "spacing" in pixels
    total_bar = WIDTH - total_spacing   # the total width of all the bars in pixels
    bar_width = int(total_bar / bar_count)   # the width of each bar in pixels (rounded down)
    padding_left_right = (WIDTH - total_bar - total_spacing) / 2 # Leftover space from rounding errors to be added before the first and after the last bar
    if padding_left_right < 0:
        padding_left_right = 0


    if bar_width == 0:
        print("[ERROR] Too much spacing selected for the width of the frame. No room for bars. Please increase frame width or decrease spacing.")
        exit()

    x_pos = spacing + padding_left_right + (bar_width / 2)
    y_bottom = HEIGHT

    for bar in heights:
        drawing.line((x_pos, y_bottom, x_pos, HEIGHT - bar), bar_color, bar_width)
        x_pos = x_pos + bar_width + spacing


def sample_frames(count, ffts):
    indexes = [randint(0, len(ffts)-1)  for i in range(count)]
    for i in indexes:
        print("Sample number", i, "| Values: ",ffts[i])
        plt.bar(range(len(ffts[i])-1), ffts[i][1:])
        plt.show()

# Print iterations progress
def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()