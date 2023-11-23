# Motion Capture BVH Editing

This Python script allows users to splice and concatenate two motion capture files in BVH format. Other editing operations will be added in the future.

File's description:

- `BVH.py` - parsing *.bvh file, read and write animations in bvh file format.
- `Animation.py` - describing motions loaded from bvh file.
- `Quaternion.py` - rotation representation and its related code and conversion to matrix representation as well.

## Features

- **Splicing**: Extract a specific frame range from one BVH file and add it to another BVH file.
- **Concatenation**: Seamlessly merge two BVH files' motion sequences into one.

## Requirements

- Python 3.x
- numpy
- BVH files for processing

## Installation

1. Clone the repository `git clone https://github.com/amireskandariii/motionedit.git`.
2. Navigate to the project directory.
3. Install requirements with `pip install -r requirements.txt` or `pip3 install -r requirements.txt`.

## Usage

0.I. Update the `file_path` variable in `MotionEditing.py` to the directory containing the BVH files on line 83.
0.II. Update the file names in `MotionEditing.py` on line 85 and 92 to the desired BVH files. 
1. Run `python MotionEditing.py` or `python3 MotionEditing.py` in the terminal.
2. Edited BVH files will be saved in the same directory as the original BVH files named as `result_spliced.bvh` and `result_concatenated.bvh`


## Notes

- Ensure both BVH files have identical skeletal structures and frame rates for successful concatenation.
- The output BVH files will contain the specified frames or merged motion sequences based on the operation.


## Examples

The motion capture files for experiment are:
- `test/16_11.bvh` - from CMU Motion Capture Dataset, walking straight then turning left
- `test/141_16.bvh` - from CMU Motion Capture Dataset, right arm waving

The edited files are::
- `test/result_concatenated.bvh` - concatenation of the two files, a new animation that smoothly connects two animations where the character is walking straight, turning left, **then** waving right arm.
- `test/result_spliced.bvh` - splicing of `16_11.bvh` and `141_16.bvh`, a new animation that is a combination of the two files where the character is walking straight, turning left, **while** waving right arm.

To visualize the bvh motions, you can use the online bvh player at
[online BVH player](http://lo-th.github.io/olympe/BVH_player.html)


