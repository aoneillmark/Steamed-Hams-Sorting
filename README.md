# Steamed Hams Frequency Sorter

This repository contains a Python script that sorts the scenes of the "Steamed Hams" video by the dominant frequency of the audio in each scene. The script utilizes the `moviepy` library to handle video and audio data, and `scipy` for audio processing and frequency analysis.

## File Structure

The repository is organized as follows:

- `Code/`: Contains the Python script `sorting_by_frequency.py`.
- `Data/`: Contains the input video file.
- `Results/`: Contains the output sorted video and frequency plot.

## How It Works

The script operates through the following steps:

1. The video is loaded, and the audio is extracted.
2. The audio is divided into chunks of a specified length.
3. The dominant frequency of each chunk is determined using the Fast Fourier Transform (FFT).
4. The video scenes corresponding to each audio chunk are sorted by the dominant frequency.
5. The sorted video scenes are reassembled into a new video.

## Usage

To use the script, instantiate the `VideoSorter` class from `sorting_by_frequency.py` with the filename of the video and the desired chunk length in seconds:

```python
from sorting_by_frequency import VideoSorter
video_sorter = VideoSorter("path_to_video.mp4", chunk_length=1.0)
video_sorter.sort_video_by_frequency()
```

## Results

- The sorted video is saved as `Results/sorted_video.mp4`.
- A plot of the dominant frequency of each chunk after sorting is saved as `Results/sorted_frequencies.png`.

### Frequency Plot

![Frequency Plot](https://github.com/aoneillmark/Steamed-Hams-Sorting/blob/main/Results/original_frequencies.png?raw=true)

### Sorted Video

You can view the sorted video by [clicking here](https://github.com/aoneillmark/Steamed-Hams-Sorting/blob/main/Results/sorted_video.mp4) to download it. Github doesn't support viewing files this large in browser, unfortunately.


## Dependencies

This script requires the following Python libraries:

- `moviepy`
- `scipy`
- `numpy`
- `matplotlib`

You can install these dependencies using pip:

```bash
pip install moviepy scipy numpy matplotlib
```

## Note

The chunk length must be chosen such that the total duration of the audio is exactly divisible by the chunk length. If an invalid chunk length is chosen, the script will suggest valid lengths close to the chosen length.