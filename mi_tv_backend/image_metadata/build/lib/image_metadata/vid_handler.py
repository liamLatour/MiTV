import ffmpeg
from os.path import join, isdir, splitext, abspath, basename, exists
from os import listdir, mkdir
import click
import subprocess

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
            whole_vid = ffmpeg.input(join(path, name))
            vid = whole_vid.video
            aud = whole_vid.audio

            if width > self._compression_width:
                new_height = int(self._compression_width * height / width)
                if new_height % 2 != 0:
                    new_height -= 1

                vid = ffmpeg.filter(vid, "scale", self._compression_width, new_height)

            whole_vid = ffmpeg.output(aud, vid, base + ".webm", format="webm", vcodec="libvpx-vp9", acodec="libopus", framerate=30, crf=30)
            whole_vid = ffmpeg._ffmpeg.global_args(whole_vid, "-hide_banner")
            whole_vid = ffmpeg._ffmpeg.global_args(whole_vid, "-loglevel", "error")

            click.echo("Converting... ", nl=False)

            args = ffmpeg.compile(whole_vid)
            try:
                args[args.index("0:a")] = "0:a?"
            except:
                click.echo("Issue when trying to map audio stream!")

            self.run_ffmpeg(whole_vid, args)

        if not exists(base + ".jpg"):
            click.echo("Thumbnail... ", nl = False)

            thumb = ffmpeg.input(file)
            thumb = ffmpeg.filter(thumb, "scale", 500, -2)
            thumb = ffmpeg.output(thumb, base + ".jpg", vframes=1)
            thumb = ffmpeg._ffmpeg.global_args(thumb, "-hide_banner")
            thumb = ffmpeg._ffmpeg.global_args(thumb, "-loglevel", "error")

            ffmpeg.run(thumb)

        click.echo("Done!")

    def run_ffmpeg(self, stream_spec, args = None, cmd='ffmpeg',
        capture_stdout=False,
        capture_stderr=False,
        input=None,
        quiet=False,
        overwrite_output=False,
        cwd=None,
    ):
        process = self.run_ffmpeg_async(
            stream_spec,
            args,
            cmd,
            pipe_stdin=input is not None,
            pipe_stdout=capture_stdout,
            pipe_stderr=capture_stderr,
            quiet=quiet,
            overwrite_output=overwrite_output,
            cwd=cwd,
        )
        
        out, err = process.communicate(input)
        retcode = process.poll()

        if retcode:
            raise Exception("ffmpeg", out, err)
        return out, err

    def run_ffmpeg_async(self, stream_spec, args = None, cmd = "ffmpeg",
        pipe_stdin=False,
        pipe_stdout=False,
        pipe_stderr=False,
        quiet=False,
        overwrite_output=False,
        cwd=None,
    ):

        if args is None:
            args = ffmpeg.compile(stream_spec, cmd, overwrite_output=overwrite_output)

        stdin_stream = subprocess.PIPE if pipe_stdin else None
        stdout_stream = subprocess.PIPE if pipe_stdout else None
        stderr_stream = subprocess.PIPE if pipe_stderr else None
        if quiet:
            stderr_stream = subprocess.STDOUT
            stdout_stream = subprocess.DEVNULL
        return subprocess.Popen(
            args,
            stdin=stdin_stream,
            stdout=stdout_stream,
            stderr=stderr_stream,
            cwd=cwd,
        )