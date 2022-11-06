import ffmpy
import os
import pandas as pd
import youtube_dl
import numpy as np
import cv2
import os
import pickle
import pandas as pd
import numpy as np
#from keras.models import load_model

def PredictLikeandView(vedio_input_arg):

    vedio_input = vedio_input_arg
    video_file_id=str(vedio_input.split(".")[0])

    # To extract Thumbnail
    thumbnail="InputVedios/Thumbnail/"+video_file_id+".jpg"
    #print(thumbnail)
    extractthumbnail = ffmpy.FFmpeg(inputs={vedio_input: None}, outputs={thumbnail: ['-ss', '01:01', '-vframes', '1']})
    #extractthumbnail = ffmpy.FFmpeg(inputs={vedio_input: None}, outputs={thumbnail: ['-vframes', '1']})
    #print(extractthumbnail)
    extractthumbnail.run()

    #sliced images
    output_base_dir= "InputVideo/SlicedImages"
    out_path = os.path.join(output_base_dir,'{}+%06d.jpg'.format(video_file_id)) #name slice images
    extractframes = ffmpy.FFmpeg(inputs={vedio_input: None}, outputs={out_path: ['-vf', 'fps=1']})
    #print(extractframes)
    extractframes.run()
    thumbnail=os.path.join(output_base_dir,video_file_id+"+000001.jpg")
    #print("thumb nail after reassigning")
    print(thumbnail)
    #Fetch metadata for vedio
    cap = cv2.VideoCapture(vedio_input)
    img_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    img_duration = frame_count/img_fps
    cap.release()
    print("img_fps"+str(img_fps))
    print("duration"+str(img_duration))
    #resize thumbnail
    thumnail_width = 224
    thumnail_height = 224
    dim = (thumnail_width, thumnail_height)

    pic_bgr_arry = cv2.imread(thumbnail)
    #print(pic_bgr_arry)
    resized_pic = cv2.resize(pic_bgr_arry, dim, interpolation=cv2.INTER_AREA)
    pic_rgb_arry = cv2.cvtColor(resized_pic, cv2.COLOR_BGR2RGB)

    width, height, fpss, durataion = thumnail_width, thumnail_height, img_fps, img_duration
    X_test_stats = np.array([width, height, fpss, durataion])

    #fetch image data thumbnail
    X_test_pic=np.array(thumbnail)

    #Sliced image data
    X_sliced_video_images=[]
    for filename in os.listdir(output_base_dir):
        f = os.path.join(output_base_dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            #print(f)
            X_sliced_video_images.append(f)

    X_sliced_video_images=np.array(X_sliced_video_images)

    like_count_predict=100
    view_count_predict=1000

    #load like count model
    loaded_like_model = load_model("SavedModels/CNN+LSTM_models_like_count")
    #Due to the model size, there does not exist the model file in the Git. 
    #Please download the model files from a public folder https://drive.google.com/drive/folders/1bIWz3Yhk4uU_Xlyy3rdFWr6k90WdBM9l?usp=share_link
    
    like_count_predict = loaded_like_model.predict([X_test_pic, X_test_stats, X_sliced_video_images])
    print('like_count_predict:'+str(like_count_predict))
 
    #load view count model
    loaded_view_model = load_model("SavedModels/CNN+LSTM_models_view_count")
    #Due to the model size, there does not exist the model file in the Git. 
    #Please download the model files from a public folder https://drive.google.com/drive/folders/1cB9nwoSLzOheF-ne1hlE6cptHok6L-Wz?usp=share_link
        
    view_count_predict = loaded_view_model.predict([X_test_pic, X_test_stats, X_sliced_video_images, like_count_predict])
    print('view_count_predict:'+str(view_count_predict))
    return like_count_predict,view_count_predict

#print(PredictLikeandView("-OXvzVt48DY+7+0.mp4"))
