from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, TextClip

def createVideoOfListOfClips(clips):
    final_clips = []

    for clip in clips:
        video = VideoFileClip("downloads/" + clip['channel'] + '/' + clip['slug'] + '.mp4')
        title = TextClip(clip['channel'] + ': ' + clip['title'], font='Amiri-regular', color='white', fontsize=42).set_duration(8)
        title_mov = title.set_pos((0.05,0.9), relative=True)

        # Create video object with text
        final_clip = CompositeVideoClip([video, title_mov])
        final_clips.append(final_clip)

    # Add clips together
    finished = concatenate_videoclips(final_clips, method='compose')

    # Render video
    finished.write_videofile("result.mp4", fps=30)