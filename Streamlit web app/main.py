import tempfile
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import cv2
from ultralytics import YOLO
from detection import create_colors_info, detect
import base64

# @st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():
    img = get_img_as_base64("image.jpg")
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://img.freepik.com/free-photo/happy-birthday-soccer-themed_23-2149695896.jpg?t=st=1714831432~exp=1714835032~hmac=777a583b35362058c5e0f95855129eb2bb30ced0ef393a2b8a1e128e52fd896b&w=826");
    background-size: 100%;
    # background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }}

    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{img}");
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """
    st.set_page_config(page_title="Web AI Phân Tích Bóng Đá", layout="wide", initial_sidebar_state="expanded")
    # st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("Nhận diện Cầu thủ Bóng đá với Dự đoán Đội & Bản đồ Chiến thuật")



    ## Thiết lập Sidebar
    # st.sidebar.markdown('---')






    # Load the YOLOv8 players detection model
    model_players = YOLO("../models/Yolo8L Players/weights/best.pt")
    # Load the YOLOv8 field keypoints detection model
    model_keypoints = YOLO("../models/Yolo8M Field Keypoints/weights/best.pt")

    
    ## Thiết lập Trang
    tab1, tab2, tab3 = st.tabs(["Tải lên video", "Tùy chỉnh Tham Số và Nhận diện", "Thông tin nhóm và web"])
    with tab1:
        st.subheader('Cách Sử Dụng?', divider='blue')
        st.markdown("""
                    1. Tải lên một video để phân tích, sử dụng nút "Browse Files" bên dưới.
                    2. Nhập tên đội tương ứng với video đã tải lên vào các trường văn bản.
                    3. Chọn một khung hình (thứ tự của frame) mà ở đó cầu thủ và thủ môn từ cả hai đội có thể được nhận diện.
                    4. Chọn màu của cầu thủ và thủ môn của mỗi đội tương ứng với khung nhận diện ở trên mà bạn cho là phù hợp nhất (bạn có thể tùy chình lại màu đội ở các ô bên dưới nếu chưa hài lòng).
                    5. Chuyển đến tab "Tùy chỉnh Tham Số và Nhận diện", điều chỉnh các tham số và chọn các tùy chọn chú thích. (Tham số mặc định được đề xuất)
                    6. Chạy Phát hiện!
                    7. Nếu chọn tùy chọn "Lưu kết quả", video đã lưu có thể được tìm thấy trong thư mục "outputs"
                    """)
        st.subheader(":red[Chỉ hoạt động với các video từ Camera Chiến thuật]")
        st.write('\n')
        
        t2col1, t2col2 = st.columns([1,1])
        with t2col1:
            demo_selected = st.radio(label="Chọn Video Demo có sẵn", options=["Demo 1 (France vs Switzerland)", "Demo 2 (Chelsea vs ManCity)"], horizontal=True)
            # st.subheader("Tải lên Video")
            st.write('\n')
            st.write('\n')
            # st.markdown('---')
            # st.info('✨ Hỗ trợ các video theo định dạng 📷 - MP4, MOV, AVI, M4V, ASF 😉')
            # st.write('\n')
            input_vide_file = st.file_uploader('Tải lên một tệp video', type=['mp4','mov', 'avi', 'm4v', 'asf'])
            tempf = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
            st.write('\n')
            st.write('\n')
            demo_vid_paths={
                "Demo 1 (France vs Switzerland)":'./demo_vid_1.mp4',
                "Demo 2 (Chelsea vs ManCity)":'./demo_vid_2.mp4'
            }
            demo_vid_path = demo_vid_paths[demo_selected]
            demo_team_info = {
                "Demo 1 (France vs Switzerland)":{"team1_name":"France",
                        "team2_name":"Switzerland",
                        "team1_p_color":'#1E2530',
                        "team1_gk_color":'#F5FD15',
                        "team2_p_color":'#FBFCFA',
                        "team2_gk_color":'#B1FCC4',
                        },
                "Demo 2 (Chelsea vs ManCity)":{"team1_name":"Chelsea",
                        "team2_name":"Manchester City",
                        "team1_p_color":'#29478A',
                        "team1_gk_color":'#DC6258',
                        "team2_p_color":'#90C8FF',
                        "team2_gk_color":'#BCC703',
                        }
            }
            selected_team_info = demo_team_info[demo_selected]

            team1_name = st.text_input(label='Nhập Tên Đội Thứ Nhất', value=selected_team_info["team1_name"])
            team2_name = st.text_input(label='Nhập Tên Đội Thứ Hai', value=selected_team_info["team2_name"])

            
        
            
        with t2col2:
            # st.title("Cài đặt Chính")
            if not input_vide_file:
                tempf.name = demo_vid_path
                demo_vid = open(tempf.name, 'rb')
                demo_bytes = demo_vid.read()

                st.text('Demo video')
                st.video(demo_bytes)
            else:
                tempf.write(input_vide_file.read())
                demo_vid = open(tempf.name, 'rb')
                demo_bytes = demo_vid.read()
                st.text('Input video')
                st.video(demo_bytes)



        st.markdown('---')
        # st.sidebar.markdown('---')
            
        # st.markdown('---')


        t1col1, t1col2 = st.columns([1,1])
        with t1col1:
            cap_temp = cv2.VideoCapture(tempf.name)
            frame_count = int(cap_temp.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_nbr = st.slider(label="Chọn thứ tự khung hình tương ứng trong video", min_value=1, max_value=frame_count, step=1, help="Select frame to pick team colors from")
            cap_temp.set(cv2.CAP_PROP_POS_FRAMES, frame_nbr)
            success, frame = cap_temp.read()
            with st.spinner('Phát hiện cầu thủ trong khung hình được chọn.'):
                results = model_players(frame, conf=0.7)
                bboxes = results[0].boxes.xyxy.cpu().numpy()
                labels = results[0].boxes.cls.cpu().numpy()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detections_imgs_list = []
                detections_imgs_grid = []
                padding_img = np.ones((80,60,3),dtype=np.uint8)*255
                for i, j in enumerate(list(labels)):
                    if int(j) == 0:
                        bbox = bboxes[i,:]                         
                        obj_img = frame_rgb[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
                        obj_img = cv2.resize(obj_img, (60,80))
                        detections_imgs_list.append(obj_img)
                detections_imgs_grid.append([detections_imgs_list[i] for i in range(len(detections_imgs_list)//2)])
                detections_imgs_grid.append([detections_imgs_list[i] for i in range(len(detections_imgs_list)//2, len(detections_imgs_list))])
                if len(detections_imgs_list)%2 != 0:
                    detections_imgs_grid[0].append(padding_img)
                concat_det_imgs_row1 = cv2.hconcat(detections_imgs_grid[0])
                concat_det_imgs_row2 = cv2.hconcat(detections_imgs_grid[1])
                concat_det_imgs = cv2.vconcat([concat_det_imgs_row1,concat_det_imgs_row2])
            st.write("Cầu thủ đã được phát hiện")
            value = streamlit_image_coordinates(concat_det_imgs, key="numpy")
            #value_radio_dic = defaultdict(lambda: None)
            st.markdown('---')
            radio_options =[f"{team1_name} Player color", f"{team1_name} GK color",f"{team2_name} Player color", f"{team2_name} GK color"]
            active_color = st.radio(label="Chọn màu đội mà bạn muốn từ ảnh ở trên", options=radio_options, horizontal=True,
                                    help="Chọn màu đội mà bạn muốn chọn và nhấp vào ảnh ở trên để chọn màu. Các màu sẽ được hiển thị trong các hộp dưới đây.")
            if value is not None:
                picked_color = concat_det_imgs[value['y'], value['x'], :]
                st.session_state[f"{active_color}"] = '#%02x%02x%02x' % tuple(picked_color)
            st.write("Các ô màu dưới đây có thể được sử dụng để điều chỉnh màu đã chọn.")
            cp1, cp2, cp3, cp4 = st.columns([1,1,1,1])
            with cp1:
                hex_color_1 = st.session_state[f"{team1_name} Player color"] if f"{team1_name} Player color" in st.session_state else selected_team_info["team1_p_color"]
                team1_p_color = st.color_picker(label=' ', value=hex_color_1, key='t1p')
                st.session_state[f"{team1_name} Player color"] = team1_p_color
            with cp2:
                hex_color_2 = st.session_state[f"{team1_name} GK color"] if f"{team1_name} GK color" in st.session_state else selected_team_info["team1_gk_color"]
                team1_gk_color = st.color_picker(label=' ', value=hex_color_2, key='t1gk')
                st.session_state[f"{team1_name} GK color"] = team1_gk_color
            with cp3:
                hex_color_3 = st.session_state[f"{team2_name} Player color"] if f"{team2_name} Player color" in st.session_state else selected_team_info["team2_p_color"]
                team2_p_color = st.color_picker(label=' ', value=hex_color_3, key='t2p')
                st.session_state[f"{team2_name} Player color"] = team2_p_color
            with cp4:
                hex_color_4 = st.session_state[f"{team2_name} GK color"] if f"{team2_name} GK color" in st.session_state else selected_team_info["team2_gk_color"]
                team2_gk_color = st.color_picker(label=' ', value=hex_color_4, key='t2gk')
                st.session_state[f"{team2_name} GK color"] = team2_gk_color
        st.markdown('---')


        
            

        with t1col2:
            extracted_frame = st.empty()
            extracted_frame.image(frame, use_column_width=True, channels="BGR")

        
        colors_dic, color_list_lab = create_colors_info(team1_name, st.session_state[f"{team1_name} Player color"], st.session_state[f"{team1_name} GK color"],
                                                     team2_name, st.session_state[f"{team2_name} Player color"], st.session_state[f"{team2_name} GK color"])

    # with tab2:



    with tab2:
        t2col1, t2col2 = st.columns([1,1])
        with t2col1:
            player_model_conf_thresh = st.slider('Ngưỡng Tin cậy Phát hiện Cầu thủ', min_value=0.0, max_value=1.0, value=0.6)
            
        with t2col2:
            keypoints_displacement_mean_tol = 7
            
            keypoints_model_conf_thresh = st.slider('Ngưỡng Tin cậy Phát hiện Điểm chính trên Sân', min_value=0.0, max_value=1.0, value=0.7)
            detection_hyper_params = {
                0: player_model_conf_thresh,
                1: keypoints_model_conf_thresh,
                2: keypoints_displacement_mean_tol
            }
            num_pal_colors = 3
        st.write("Các tùy chọn đánh dấu:")
        bcol21t, bcol22t = st.columns([1,1])
        with bcol21t:
            show_k = False
            show_p = st.toggle(label="Hiển thị nhận diện cầu thủ", value=True)
        with bcol22t:
            show_pal = True
            show_b = st.toggle(label="Hiển thị đường đi quả bóng", value=True)
        plot_hyperparams = {
            0: show_k,
            1: show_pal,
            2: show_b,
            3: show_p
        }
        st.markdown("---")
        save_output = st.checkbox(label='Lưu kết quả', value=False)
        if save_output:
            output_file_name = st.text_input(label='Tên tệp (Tùy ý)', placeholder='Nhập tên tệp video kết quả.')
        else:
            output_file_name = None
        st.markdown("---")

        
        # bcol1, bcol2 = st.columns([1,1])
        # with bcol1:
        #     nbr_frames_no_ball_thresh = st.number_input("Ball track reset threshold (frames)", min_value=1, max_value=10000,
        #                                              value=30, help="After how many frames with no ball detection, should the track be reset?")
        #     ball_track_dist_thresh = st.number_input("Ball track distance threshold (pixels)", min_value=1, max_value=1280,
        #                                                 value=100, help="Maximum allowed distance between two consecutive balls detection to keep the current track.")
        #     max_track_length = st.number_input("Maximum ball track length (Nbr. detections)", min_value=1, max_value=1000,
        #                                                 value=35, help="Maximum total number of ball detections to keep in tracking history")
        #     ball_track_hyperparams = {
        #         0: nbr_frames_no_ball_thresh,
        #         1: ball_track_dist_thresh,
        #         2: max_track_length
        #     }
            
        nbr_frames_no_ball_thresh = 30
        ball_track_dist_thresh = 100
        max_track_length = 35
        ball_track_hyperparams = {
            0: nbr_frames_no_ball_thresh,
            1: ball_track_dist_thresh,
            2: max_track_length
        }
        # with bcol2:

        # st.markdown('---')
        bcol21, bcol22, bcol23, bcol24 = st.columns([1.5,1,1,1])
        with bcol21:
            st.write('')
        with bcol22:
            ready = True if (team1_name == '') or (team2_name == '') else False
            start_detection = st.button(label='Bắt đầu nhận diện', disabled=ready)
        with bcol23:
            stop_btn_state = True if not start_detection else False
            stop_detection = st.button(label='Dừng nhận diện', disabled=stop_btn_state)
        with bcol24:
            st.write('')


    stframe = st.empty()
    cap = cv2.VideoCapture(tempf.name)
    status = False

    if start_detection and not stop_detection:
        st.toast(f'Bắt đầu nhận diện!')
        status = detect(cap, stframe, output_file_name, save_output, model_players, model_keypoints,
                         detection_hyper_params, ball_track_hyperparams, plot_hyperparams,
                           num_pal_colors, colors_dic, color_list_lab)
    else:
        try:
            # Release the video capture object and close the display window
            cap.release()
        except:
            pass
    if status:
        st.toast(f'Hoàn tất nhận diện!')
        cap.release()
    with tab3:
        st.header('Đồ án cuối kì Nhập môn học máy')
        st.header('21KHDL1 - VNU - HCMUS')
        st.subheader('Thông tin các thành viên:', divider='blue')
        member_info = [
            {"Tên": "Trần Nguyên Huân", "MSSV": "21127050"},
            {"Tên": "Doãn Anh Khoa", "MSSV": "21127076"},
            {"Tên": "Nguyễn Minh Quân", "MSSV": "21127143"},
            {"Tên": "Nguyễn Phát Đạt", "MSSV": "21127240"}
        ]
        member_df = pd.DataFrame(member_info)

        # Display the DataFrame as a table with larger width and without index column
        st.write(member_df, width='100%', index=False)

        st.subheader('Các chức năng chính:', divider='blue')
        st.markdown("""
                    1. Nhận diện cầu thủ, trọng tài và bóng.
                    2. Dự đoán đội cầu thủ.
                    3. Ước tính vị trí của cầu thủ và quả bóng trên bản đồ chiến thuật.
                    4. Theo dõi quả bóng.
                    """)


if __name__=='__main__':
    try:
        main()
    except SystemExit:
        pass