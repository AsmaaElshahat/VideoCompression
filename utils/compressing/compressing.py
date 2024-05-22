from ffmpeg import FFmpeg, Progress

class VideoCompressing():
    def __init__(self,ip_file_name, op_file_name):
        self.ip_file_name = ip_file_name
        self.op_file_name = op_file_name

    def compressing_process(self):
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(self.ip_file_name)
            .output(
                self.op_file_name,
                {"codec:v": "libx264"},
                vf="scale=1280:-1",
                preset="veryslow",
                crf=24,
            )
        )

        @ffmpeg.on("progress")
        def time_to_terminate(progress: Progress):
            print(progress)

        ffmpeg.execute()