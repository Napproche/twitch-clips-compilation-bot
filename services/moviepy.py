from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, TextClip

import constants

def createVideoOfListOfClips(clips, output):
    final_clips = []

    for clip in clips:
        video = VideoFileClip(constants.DOWNLOAD_LOCATION + clip['channel'] + '/' + clip['slug'] + '.mp4')
        title = TextClip(clip['channel'] + ': ' + clip['title'], font='Amiri-regular', color='white', fontsize=55).set_duration(8)
        title_mov = title.set_pos((0.05,0.8), relative=True)

        # Create video object with text
        final_clip = CompositeVideoClip([video, title_mov]).resize( (1280,720) )
        final_clips.append(final_clip)

        # Remove from memory
        del title
        del video
        del final_clip

    # Add clips together
    finished = concatenate_videoclips(final_clips, method='compose')

    # Render video
    finished.write_videofile(output, fps=30)