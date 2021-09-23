import glob
import os
import subprocess


def gen_output_path(INPUT_VIDEO):
    # Generate output path

    dirname = os.path.dirname(INPUT_VIDEO)
    basename_without_ext = os.path.splitext(os.path.basename(INPUT_VIDEO))[0]
    #print(dirname, basename_without_ext)
    OUTPUT_COMP  = os.path.join(dirname, basename_without_ext + "_ecs_comp.MP4")
    OUTPUT_ALPHA = os.path.join(dirname, basename_without_ext + "_ecs_alpha.MP4")
    #print (OUTPUT_COMP, OUTPUT_ALPHA)
    return OUTPUT_COMP, OUTPUT_ALPHA


def run_rvm_cmd(INPUT_VIDEO):

    # Generate output path
    OUTPUT_COMP, OUTPUT_ALPHA = gen_output_path(INPUT_VIDEO)
    print ("INPUT_VIDEO:", INPUT_VIDEO)
    print ("OUTPUT_COMP:", OUTPUT_COMP)
    print ("OUTPUT_ALPHA:", OUTPUT_ALPHA)

    # run RVM_cmd
    result = subprocess.call(["python3", "inference.py",
                            "--variant", "resnet50",
                            "--checkpoint", "rvm_resnet50.pth",
                            "--device", "cuda",
                            "--input-source", INPUT_VIDEO,
                            "--output-type", "video",
                            #"--downsample-ratio", "0.4",
                            "--output-composition", OUTPUT_COMP,
                            "--output-alpha", OUTPUT_ALPHA,
                            "--output-video-mbps", "4",
                            "--seq-chunk", "1"])
    return result


if __name__ == '__main__':
    

    FILES_DIR = "/data2/20210803_Sancyoku_user_data"
    #FILES_DIR = "./test_sancyoku"

    # test_list = [*glob.glob(os.path.join(FILES_DIR, '**', '*.MOV'), recursive=True)]
    # print(test_list, len(test_list))

    # Get All File Path
    file_list = sorted([*glob.glob(os.path.join(FILES_DIR, '**', '*.MOV'), recursive=True),
                        *glob.glob(os.path.join(FILES_DIR, '**', '*.mp4'), recursive=True)])
    #print(file_list, len(file_list))

    #Loop
    for idx, video_file in enumerate(file_list):
        print(idx, "/", len(file_list))
        result = run_rvm_cmd(video_file)




