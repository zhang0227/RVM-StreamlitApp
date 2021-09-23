
from re import I
import streamlit as st
import os
import argparse
import torch
import shutil



def add_model_args(parser):

    parser.add_argument('--variant', type=str, default="mobilenetv3",
                        choices=['mobilenetv3', 'resnet50'])
    parser.add_argument('--checkpoint', type=str,
                        default="rvm_mobilenetv3.pth")
    parser.add_argument('--input-resize', type=int, default=None, nargs=2)
    parser.add_argument('--output-composition', type=str,
                        default="composition.mp4")
    parser.add_argument('--output-alpha', type=str, default="alpha.mp4")
    parser.add_argument('--output-foreground', type=str,
                        default="foreground.mp4")
    parser.add_argument('--output-type', type=str,
                        default="video", choices=['video', 'png_sequence'])
    parser.add_argument('--output-video-mbps', type=int, default=4)
    parser.add_argument('--seq-chunk', type=int, default=1)
    parser.add_argument('--num-workers', type=int, default=0)
    parser.add_argument('--disable-progress', action='store_true')


    parser.add_argument('--device', type=str)
    parser.add_argument('--downsample-ratio', type=float)
    parser.add_argument('--input-source', type=str)

    return parser


if __name__ == '__main__':

    st.title('RVM Streamlit App')

    
    parser = argparse.ArgumentParser()
    add_model_args(parser)

    opt = parser.parse_args()
    print(opt)

    # check device
    if torch.cuda.is_available():
        opt.device = "cuda"
    else:
        opt.device = "cpu"

    source = ("HD", "4K")
    source_index = st.sidebar.selectbox("选择输入", range(
        len(source)), format_func=lambda x: source[x])

    uploaded_file = st.sidebar.file_uploader("上传视频", type=['mp4'])
    if uploaded_file is not None:

        is_valid = True
        with st.spinner(text='资源加载中...'):
            st.sidebar.video(uploaded_file)
            with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        opt.input_source = f'data/videos/{uploaded_file.name}'
        print(uploaded_file)
        if source_index == 0:
            opt.downsample_ratio = 0.25
        else:
            opt.downsample_ratio = 0.125
    else:
        is_valid = False



    if is_valid:
        print('valid')
        output_path = os.path.join("result",uploaded_file.name.split(".")[0])
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        
        
        if st.button('开始转换'):
            
            from inference import convert
            
            convert(opt)
            
            st.text("composition video:")
            st.video(str("composition.mp4"))
            st.text("alpha video:")
            st.video(str("alpha.mp4"))
            st.text("foreground video:")
            st.video(str("foreground.mp4"))
            st.balloons()
            
            shutil.move("composition.mp4", os.path.join(output_path))
            shutil.move("alpha.mp4", os.path.join(output_path))
            shutil.move("foreground.mp4", os.path.join(output_path))

