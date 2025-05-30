# generated by AI to test stuff
# Python
import os
import glob
import time
import unittest
import subprocess

from services.tts_service import generate_audio
from services.manim_service import create_manim_video

# Import AudioSegment from pydub to check audio properties.
from pydub import AudioSegment


class TestTTSService(unittest.TestCase):
    def setUp(self):
        # Cleanup previous output file if exists.
        self.audio_file = "output.wav"
        if os.path.exists(self.audio_file):
            os.remove(self.audio_file)
    
    def test_generate_audio(self):
        sample_text = "This is a test narration for the TTS service."
        output_file = generate_audio(sample_text)
        # Check that the file was created and is non-empty.
        self.assertTrue(os.path.exists(output_file), "TTS output file was not created.")
        self.assertGreater(os.path.getsize(output_file), 0, "TTS output file is empty.")
        
        # Load the generated audio to check its duration and loudness.
        audio = AudioSegment.from_wav(output_file)
        self.assertGreater(audio.duration_seconds, 0, "TTS audio file has zero duration.")
        self.assertNotEqual(audio.dBFS, float("-inf"), "Generated audio is completely silent.")
        self.assertGreater(audio.dBFS, -35, "Audio seems too quiet; it may be silent.")
        
        # Leave the file on disk so it can be inspected.
        print(f"Test audio file saved at: {os.path.abspath(output_file)}")



class TestManimService(unittest.TestCase):
    def setUp(self):
        # Remove the generated video python file if it exists.
        self.manim_py = "generated_video.py"
        if os.path.exists(self.manim_py):
            os.remove(self.manim_py)
        # Remove previous output videos from Manim by searching the typical output folder.
        self.video_files = glob.glob("media/videos/generated_video/**/*.mp4", recursive=True)
        for f in self.video_files:
            os.remove(f)
    
    def test_create_manim_video_with_audio(self):
        # Create a dummy manim code that creates a scene lasting at least 5 seconds.
        dummy_code = """
from manim import *

class TestScene(Scene):
    def construct(self):
        self.wait(5)
"""
        video_data = {"output_file": "output.mp4", "manim_code": dummy_code}
        
        # Generate a TTS audio so we have an audio file for merging.
        audio_file = generate_audio("Test narration for merging with the Manim video.")
        self.assertTrue(os.path.exists(audio_file), "TTS audio file for merging was not created.")
        
        # Call the service that writes code, renders video, and merges audio using Manim.
        create_manim_video(video_data, dummy_code, audio_file=audio_file)
        
        # Allow enough time for Manim to finish rendering and merging.
        time.sleep(10)
        
        # Try to find the output video.
        video_paths = glob.glob("media/videos/generated_video/**/*.mp4", recursive=True)
        if not video_paths:
            # Fallback in case the output video is in the current directory.
            self.assertTrue(os.path.exists("output.mp4"), "No video file was produced by Manim.")
            # Add these additional test methods to your existing test classes:

            def test_generate_audio_empty_text(self):
                """Test TTS service with empty text input"""
                with self.assertRaises(ValueError):
                    generate_audio("")

            def test_generate_audio_long_text(self):
                """Test TTS with longer text input"""
                long_text = "This is a longer test narrative. " * 10
                output_file = generate_audio(long_text)
                self.assertTrue(os.path.exists(output_file))
                audio = AudioSegment.from_mp3(output_file)
                self.assertGreater(audio.duration_seconds, 5)
                os.remove(output_file)

            def test_create_manim_video_without_audio(self):
                """Test video creation without audio"""
                dummy_code = """
            class TestScene(Scene):
                def construct(self):
                    circle = Circle()
                    self.play(Create(circle))
                    self.wait(2)
            """
                video_data = {"output_file": "output.mp4", "manim_code": dummy_code}
                create_manim_video(video_data, dummy_code)
                
                time.sleep(5)
                video_paths = glob.glob("media/videos/generated_video/**/*.mp4", recursive=True)
                self.assertTrue(video_paths, "No video file was produced")
                
                for f in video_paths:
                    self.assertGreater(os.path.getsize(f), 0)
                    os.remove(f)

            def test_create_manim_video_invalid_code(self):
                """Test handling of invalid Manim code"""
                invalid_code = "This is not valid Python code"
                video_data = {"output_file": "output.mp4", "manim_code": invalid_code}
                with self.assertRaises(subprocess.CalledProcessError):
                    create_manim_video(video_data, invalid_code)

            def test_create_manim_video_with_text(self):
                """Test video creation with text elements"""
                code_with_text = """
            class TextScene(Scene):
                def construct(self):
                    text = Text("Hello World")
                    self.play(Write(text))
                    self.wait(2)
            """
                video_data = {"output_file": "output.mp4", "manim_code": code_with_text}
                create_manim_video(video_data, code_with_text)
                
                time.sleep(5)
                video_paths = glob.glob("media/videos/generated_video/**/*.mp4", recursive=True)
                self.assertTrue(video_paths)
                
                for f in video_paths:
                    self.assertGreater(os.path.getsize(f), 0)
                    os.remove(f)

            def test_audio_video_sync(self):
                """Test audio-video synchronization"""
                dummy_code = """
            class SyncScene(Scene):
                def construct(self):
                    circle = Circle()
                    self.play(Create(circle), run_time=3)
                    self.wait(2)
            """
                video_data = {"output_file": "output.mp4", "manim_code": dummy_code}
                audio_text = "This circle appears over three seconds and then waits for two more seconds."
                audio_file = generate_audio(audio_text)
                
                create_manim_video(video_data, dummy_code, audio_file=audio_file)
                
                time.sleep(10)
                video_paths = glob.glob("media/videos/generated_video/**/*.mp4", recursive=True)
                self.assertTrue(video_paths)
                
                # Clean up
                for f in video_paths:
                    os.remove(f)
                os.remove(audio_file)