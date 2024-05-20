
# Football Analysis Web Application Using Deep Learning and Computer Vision

## University of Science - VNUHCM
## Final Project - Introduction to Machine Learning - 21KHDL1

## Team Information
| Name              | ID       |
|-------------------|----------|
| Trần Nguyên Huân  | 21127050 |
| Doãn Anh Khoa   | 21127076 |
| Nguyễn Minh Quân   | 21127143 |
| Nguyễn Phát Đạt   | 21127240 |

## Project Objective
Develop an automated football analysis web application that provides useful insights to aid in strategic decision-making.

## Project Progress
Utilizing Streamlit to develop a web application for player detection, tracking goalkeepers, referees, the ball, and visualizing data through a tactical map.

## Key Features
1. Detect players, referees, and the ball.
2. Predict the teams of the players.
3. Estimate the positions of players and the ball on a tactical map.
4. Track the ball.

## Usage Instructions
Steps to use the application:
1. Upload a video for analysis using the `Browse Files` button below.
2. Enter the names of the teams corresponding to the uploaded video in the text fields.
3. Select a frame where players and goalkeepers from both teams can be identified.
4. Choose the colors of the players and goalkeepers for each team corresponding to the selected frame (you can adjust the team colors in the fields below if not satisfied).
5. Go to the `Tùy chỉnh Tham Số và Nhận diện` tab, adjust the parameters, and choose annotation options. (Default parameters are recommended)
6. Run Detection!
7. If you select the `Lưu kết quả` option, the saved video can be found in the `outputs` folder.

##  Flow Chart
The process from uploading the input video to the various functionalities is illustrated in the flow chart below.

![Flow Chart](https://github.com/knightstark7/FootBall-Analytics-with-Deep-Learning-and-Computer-Vision/blob/main/FlowChart.png)