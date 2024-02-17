import moviepy.editor as mp
from scipy.fft import fft
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


class VideoSorter:
    def __init__(self, filename, chunk_length=1):
        self.filename = filename
        self.chunk_length = chunk_length  # Length of audio chunks in seconds
        self.video = mp.VideoFileClip(filename)
        self.sample_rate = None
        self.audio_chunks = []
        self.video_clips = []
        self.dominant_frequencies = []
    
        if not self.validate_chunk_length(chunk_length):
            print(f"Error: The chosen chunk length {chunk_length} seconds is not valid.")
            self.suggest_chunk_lengths(chunk_length)
            raise ValueError(f"Invalid chunk length: {chunk_length} seconds. Please choose a valid length.")

    def extract_audio(self):
        self.audio = self.video.audio
        self.sample_rate, _ = wavfile.read('Results/extracted_audio.wav')
        self.audio.write_audiofile("Results/extracted_audio.wav")

    def process_audio(self):
        rate, data = wavfile.read('Results/extracted_audio.wav')
        if data.ndim == 2:  # Convert stereo to mono if necessary
            data = np.mean(data, axis=1)
        self.sample_rate = rate
        chunk_size = int(self.sample_rate * self.chunk_length)
        total_chunks = len(data) // chunk_size

        for i in range(total_chunks):
            start_index = int(i * chunk_size)
            end_index = int((i + 1) * chunk_size)
            chunk = data[start_index:end_index]

            if len(chunk) != chunk_size:
                continue
            yf = fft(chunk)
            # Only consider the first half of the FFT result for real signals
            xf = np.linspace(0.0, rate / 2, len(chunk) // 2)
            abs_yf = np.abs(yf[:len(chunk) // 2])
            index = np.argmax(abs_yf)
            # Ensure index is within the bounds of xf
            dominant_frequency = xf[index] if index < len(xf) else 0
            self.dominant_frequencies.append(dominant_frequency)
            self.video_clips.append(self.video.subclip(i * self.chunk_length, (i + 1) * self.chunk_length))

    def sort_chunks(self):
        sorted_indices = np.argsort(self.dominant_frequencies)
        self.video_clips = [self.video_clips[i] for i in sorted_indices]
        self.dominant_frequencies.sort()  # Sorting frequencies for plotting

    def reassemble_video(self):
        final_clip = mp.concatenate_videoclips(self.video_clips)
        final_clip.write_videofile("Results/sorted_video.mp4")

    def plot_frequencies(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.dominant_frequencies, marker='o', linestyle='-', color='blue')
        plt.title('Dominant Frequency of Each Chunk After Sorting')
        plt.xlabel('Chunk Index')
        plt.ylabel('Frequency (Hz)')
        plt.grid(True)
        plt.savefig("Results/sorted_frequencies.png")
        plt.show()

    def validate_chunk_length(self, chunk_length):
        try:
            rate, data = wavfile.read('Results/extracted_audio.wav')
        except FileNotFoundError:
            print("Audio file not found. Please extract audio first.")
            return False

        self.sample_rate = rate  # Update sample rate here as well
        total_duration = len(data) / rate
        total_chunks = total_duration / chunk_length
        return total_chunks.is_integer()
    
    def suggest_chunk_lengths(self, chosen_length):
        rate, data = wavfile.read('Results/extracted_audio.wav')
        total_duration = len(data) / rate
        print("Suggested chunk lengths close to your choice:")

        # Find and suggest lengths that are closest to the chosen length
        # First, calculate a range of acceptable lengths based on the chosen length
        min_length = max(0.01, chosen_length - 0.05)  # Ensure minimum length is not negative or too small
        max_length = chosen_length + 0.05  # Allow a range above the chosen length

        acceptable_lengths = []
        for i in range(1, 500):  # Increased range for finer granularity
            test_length = i * 0.01  # Test lengths in smaller increments
            if min_length <= test_length <= max_length:
                total_chunks = total_duration / test_length
                if total_chunks.is_integer():
                    acceptable_lengths.append((test_length, int(total_chunks)))

        # Sort acceptable lengths based on their closeness to the chosen length
        acceptable_lengths.sort(key=lambda x: abs(x[0] - chosen_length))

        # Display the top 5 closest lengths
        for length, chunks in acceptable_lengths[:5]:
            print(f"{length} seconds: {chunks} chunks (Total duration: {chunks * length} seconds)")

        if not acceptable_lengths:
            print("No chunk lengths very close to your choice were found. Consider choosing a new length based on your audio's total duration.")

    def sort_video_by_frequency(self):
        print("Extracting audio...")
        self.extract_audio()

        # Validate chunk length with actual audio data
        if not self.validate_chunk_length(self.chunk_length):
            print(f"Error: The chosen chunk length {self.chunk_length} seconds is not valid.")
            self.suggest_chunk_lengths(self.chunk_length)
            raise ValueError(f"Invalid chunk length: {self.chunk_length} seconds. Please choose a valid length.")
        
        print("Processing audio...")
        self.process_audio()
        print("Sorting chunks...")
        self.sort_chunks()
        print("Plotting frequencies...")
        self.plot_frequencies()
        print("Reassembling and exporting video...")
        self.reassemble_video()



####################
# Code Execution
video_sorter = VideoSorter("Data/Steamed Hams.mp4", chunk_length=0.01) # 0.01 seconds
video_sorter.sort_video_by_frequency()
