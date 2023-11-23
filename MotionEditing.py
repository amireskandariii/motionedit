# By Amir Eskandari
# filepath was changed to its original value for your convenience

import Quaternions as Q
import Animation as A
import BVH as BVH
import numpy as np

'''relocate anim so that it starts from start_pos'''


def relocate(anim, start_pos):
    delta_pos = start_pos - anim.positions[0, 0]
    anim.positions[:, 0] += delta_pos
    return anim


'''rotate anim, so that it starts in different facing direction, delta_q is quaternion'''


def rotate_root(anim, delta_q):
    anim.rotations[:, 0] = delta_q * anim.rotations[:, 0]
    transform = np.repeat(delta_q.transforms(), anim.shape[0], axis=0)
    for f in range(0, anim.shape[0]):
        anim.positions[f, 0] = np.matmul(transform[f], anim.positions[f, 0])
    return anim


'''naively put anim2 at the end of anim1, not smooth, with teleportation issue'''


def concatenate_naive(anim1, anim2):
    anim1.rotations = Q.Quaternions(
        np.vstack((anim1.rotations.qs, anim2.rotations.qs)))
    anim1.positions = np.vstack((anim1.positions, anim2.positions))
    return anim1


'''NOTE 
for motion editing, only change anim.rotations and anim.positions
no need to change the skeleton, which is anim.orients and anim.offsets
'''

def concatenate(anim1, anim2):
    # we will first reorient anim2 to the last frame of anim1 by rotating the root
    # then we will relocate anim2 to the last frame of anim1 by translating the root
    # the we will interpolate 20 frames between the last frame of anim1 and first frame of anim2 to make the transition smooth
    # we use slerp to interpolate the joints' rotations and lerp to interpolate the joints' positions
    # then we will concatenate anim1 and anim2 by stacking their rotations and positions
    concatenated = anim1
    delta_q = anim1.rotations[-1, 0] * -anim2.rotations[0, 0]
    anim2 = rotate_root(anim2, delta_q)
    anim2 = relocate(anim2, anim1.positions[-1, 0])
    for i in range(20):
        
        w = (i+1)/20
        f = 534 + (i+1)
        inter_q = Q.Quaternions.slerp(anim1.rotations[-1,:], anim2.rotations[0,:], np.array([w]*31))
        concatenated.rotations = Q.Quaternions(np.vstack((anim1.rotations.qs, [inter_q.qs])))

        inter_p = w * anim1.positions[-1, :] + (1 - w) * anim2.positions[0, :]
        inter_p = np.reshape(inter_p, (1, 31, 3))
        concatenated.positions = np.vstack((anim1.positions, inter_p))
    concatenated.rotations = Q.Quaternions(np.vstack((anim1.rotations.qs, anim2.rotations.qs)))
    concatenated.positions = np.vstack((anim1.positions, anim2.positions))
    return concatenated


def splice(anim1, anim2):
    # first we will choose the right arm rotations of anim2 
    # then scale it to frame length of anim1 
    # then we will replace the right arm of anim1 with the right arm of anim2
    # indices of the joints were found by printing the joint names in line 90 and 91
    right_arm = anim2.rotations[:, 24:31]
    right_arm = np.repeat(right_arm, 2, axis=0)
    right_arm = right_arm[:anim1.shape[0], :]
    anim1.rotations[:, 24:31] = right_arm
    return anim1


'''load the walking motion'''

filepath = 'C:/Users/Amir/Desktop/CAS 737/Assignment 2/'

filename_walk = filepath + '16_11.bvh'
anim_walk, joint_names_walk, frametime_walk = BVH.load(filename_walk)

# for i in range(len(joint_names_walk)):
#     print(i, joint_names_walk[i])

'''load the waving motion'''
filename_wave = filepath + '141_16.bvh'
anim_wave, joint_names_wave, frametime_wave = BVH.load(filename_wave)

# '''simple editing'''
# anim_rotated = rotate_root(anim_walk, Q.Quaternions.from_euler(np.array([0, 90, 0])))
# filename_rotated = filepath + 'rotated.bvh'
# BVH.save(filename_rotated, anim_rotated, joint_names_walk, frametime_walk)

# anim_concat_naive = concatenate_naive(anim_walk, anim_wave)
# filename_concat_naive = filepath + 'concat_naive.bvh'
# BVH.save(filename_concat_naive, anim_concat_naive, joint_names_walk, frametime_walk)
# print('DONE!')


'''splice the waving motion into the walking motion'''
anim_splice = splice(anim_walk, anim_wave)
filename_splice = filepath + 'result_spliced.bvh'
BVH.save(filename_splice, anim_splice, joint_names_walk, frametime_walk)
print('SPLICE DONE!')


# we will reread the motions, because we have modified it in the previous step and I don't know why it doesn't work if we don't do this...
filename_wave = filepath + '141_16.bvh'
anim_wave, joint_names_wave, frametime_wave = BVH.load(filename_wave)
filename_walk = filepath + '16_11.bvh'
anim_walk, joint_names_walk, frametime_walk = BVH.load(filename_walk)

'''concatenate the two motions'''
anim_concat = concatenate(anim_walk, anim_wave)
filename_concat = filepath + 'result_concatenated.bvh'
BVH.save(filename_concat, anim_concat, joint_names_walk, frametime_walk)
print('CONCAT DONE!')