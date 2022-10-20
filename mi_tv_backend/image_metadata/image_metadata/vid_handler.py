import ffmpeg
from os.path import join, isdir, splitext, abspath, basename, exists
from os import listdir, mkdir
import click

class Videos():
    small_dir_name = ".vid_small"
    supported_formats = ["mp4", "avi", "mov", "webm", "wmv", "mkv", "flv"]

    _compression_width = 640

    def __init__(self):      
        pass

    def run(self, paths):
        for path in paths:
            assert isdir(path)

            self.parse_vids(path)
        
    def parse_vids(self, path):
        if self.small_dir_name in basename(path):
            return

        for f in listdir(path):
            _path = join(path, f)

            if isdir(_path):
                self.parse_vids(_path)
                continue

            if splitext(f)[-1][1:] in self.supported_formats:
                if not self.small_dir_name in listdir(path):
                    mkdir(join(path, self.small_dir_name))

                click.echo("Treating " + f + " : ", nl=False)
                self.treat_vid(abspath(path), f)
            
    def treat_vid(self, path, name):
        file = join(path, name)
        base = splitext(join(path, self.small_dir_name, name))[0]

        click.echo("Parsing... ", nl=False)

        probe = ffmpeg.probe(file)
        video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
        width = int(video_stream["width"])
        height = int(video_stream["height"])

        if not exists(base + ".webm"):
            file = ffmpeg.input(join(path, name))
            vid = ffmpeg.video
            aud = ffmpeg.video

            if width > self._compression_width:
                new_height = int(self._compression_width * height / width)
                if new_height % 2 != 0:
                    new_height -= 1

                vid = ffmpeg.filter(vid, "scale", self._compression_width, new_height)

            file = ffmpeg.output(aud, vid, base + ".webm", format="webm", vcodec="libvpx-vp9", acodec="libopus", framerate=30, crf=30)
            file = ffmpeg._ffmpeg.global_args(file, "-hide_banner")
            file = ffmpeg._ffmpeg.global_args(file, "-loglevel", "error")

            click.echo("Converting... ", nl=False)

            ffmpeg.run(file)

        if not exists(base + ".jpg"):
            click.echo("Thumbnail... ", nl = False)

            thumb = ffmpeg.input(file)
            thumb = ffmpeg.filter(thumb, "scale", 500, -2)
            thumb = ffmpeg.output(thumb, base + ".jpg", vframes=1)
            thumb = ffmpeg._ffmpeg.global_args(thumb, "-hide_banner")
            thumb = ffmpeg._ffmpeg.global_args(thumb, "-loglevel", "error")

            ffmpeg.run(thumb)

        click.echo("Done!")