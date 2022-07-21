from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips, VideoFileClip

class RenderGroup:

    def __init__(self, height, width, fps, max_clip_size):
        self.fps = fps
        self.segments = []
        self.current_segment_frames = []
        self.frames_per_segment = int(max_clip_size / (height * width * 3))
        print("Max clip size:", max_clip_size, "| Max frames per subclip: ", self.frames_per_segment)
        
    def add_frame(self, frame):
        self.current_segment_frames.append(frame)
        
        if len(self.current_segment_frames) == self.frames_per_segment:
            self.render_current_segment()
            self.current_segment_frames.clear()

    def render_current_segment(self):
        filename = ".\\output\\temp_subfile_" + str(len(self.segments)) + ".mp4"
        print("Rendering partial output:",filename, "(total frames: ", len(self.current_segment_frames), ")")
        
        with ImageSequenceClip(self.current_segment_frames, self.fps) as video_clip:
            video_clip.write_videofile(filename, fps=self.fps)

        self.segments.append(filename)

    def finalize(self, audio_file):
        if not len(self.current_segment_frames) == 0:
            self.render_current_segment()
        
        result = VideoFileClip(self.segments[0], audio=False)
        self.segments = self.segments[1:]
        
        for segment in self.segments:
            video_seg = VideoFileClip(segment, audio=False)
            result = concatenate_videoclips((result, video_seg), method="chain")

        audio = AudioFileClip(audio_file)
        audio.cutout(result.duration, audio.duration)
        result.audio = audio
        result.write_videofile("OUPUT.mp4", fps=self.fps)
        
def render_image_sequence(images, fps, music_path):
    video_clip = ImageSequenceClip(images, fps)
    audio = AudioFileClip(music_path)
    audio.cutout(video_clip.duration, audio.duration)
    video_clip.audio = audio
    video_clip.write_videofile("Final - sky high 1080p60.mp4", fps=fps)

