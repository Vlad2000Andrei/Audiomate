from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips, VideoFileClip
from os import remove, path

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

    def render_current_segment(self):
        filename = ".\\output\\temp_subfile_" + str(len(self.segments)) + ".mp4"
        print("Rendering partial output:",filename, "(total frames: ", len(self.current_segment_frames), ")")
        
        with ImageSequenceClip(self.current_segment_frames, self.fps) as video_clip:
            video_clip.write_videofile(filename, fps=self.fps)

        self.segments.append(filename)
        self.current_segment_frames.clear()

    def finalize(self, audio_file):
        to_delete = self.segments

        try:
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

            filename = "AudioMate Output - " + str(path.basename(audio_file)).split(".")[0] + ".mp4"
            result.write_videofile(".\\output\\" + filename, fps=self.fps)
        finally:
            for file in to_delete:
                remove(file)
    
