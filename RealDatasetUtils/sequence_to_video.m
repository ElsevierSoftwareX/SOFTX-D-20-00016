% sequence_to_video.m
% @author: giuseppecanto
% Transform a sequence of images to a video

% Config parameter(s)
input_folder = 'cam01';
output_video_path = 'cam01/video';

%% Set output video
outputVideo = VideoWriter(output_video_path, 'MPEG-4');
outputVideo.FrameRate = 30;

% Start measuring time
tic;

% Open video stream
open(outputVideo)

% Iterate over the images
for ii = 0:299
   ii
   img = imread(['cam01/soccer_arc_cam01-f000' num2str(ii,'%03d') '.png']);
   writeVideo(outputVideo,img)
end

% Close output stream
close(outputVideo)

% Stop measuring time
elapsed = toc;

%% Show feedback and performance analysis to the user
msg = ['Operation completed in ' num2str(elapsed,'%.1f') ' s.'];
f = msgbox(msg);