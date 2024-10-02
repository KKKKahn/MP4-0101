import cv2
import numpy as np

# 打开视频文件
cap = cv2.VideoCapture('your_video.mp4')  # 替换为你的视频路径，

# 设置每个“字符块”的大小
block_size = 10  # 字符块的大小
font_scale = 0.4  # 字体大小
font = cv2.FONT_HERSHEY_SIMPLEX  # 字体样式

# 获取视频的宽高并转换为整数
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))  # 获取帧率

# 定义用于保存视频的 VideoWriter，输出为 .mp4 格式
output_filename = 'output_video_with_saturation_and_full_resolution.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 设置编码器为 MP4
out = cv2.VideoWriter(output_filename, fourcc, fps, (original_width, original_height))

# 创建全屏窗口
cv2.namedWindow('Color-Based Binary Text Display', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Color-Based Binary Text Display', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 调整饱和度的参数，值越高饱和度越强，默认是1.0
saturation_factor = 2  # 你可以调整这个值来增强饱和度

while True:
    ret, frame = cap.read()  # 读取视频帧
    if not ret:
        break

    # 增强颜色的饱和度
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 提高饱和度通道值，通过saturation_factor进行放大
    s_channel = hsv_frame[:, :, 1].astype(np.float32)
    s_channel = s_channel * saturation_factor
    s_channel = np.clip(s_channel, 0, 255).astype(np.uint8)
    hsv_frame[:, :, 1] = s_channel

    # 将HSV转回BGR
    saturated_frame = cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2BGR)

    # 获取原始帧的宽高（不再缩小尺寸）
    height, width = saturated_frame.shape[:2]

    # 转为灰度图像以计算亮度
    gray = cv2.cvtColor(saturated_frame, cv2.COLOR_BGR2GRAY)

    # 创建一个空白画布用于显示字符
    canvas = np.ones((height, width, 3), dtype=np.uint8) * 180

    # 使用 NumPy 矩阵操作加速计算平均颜色和亮度
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # 获取每个 block_size x block_size 的像素块
            block = saturated_frame[y:y + block_size, x:x + block_size]

            # 确保中心像素的计算不超出边界
            center_y = min(y + block_size // 2, height - 1)
            center_x = min(x + block_size // 2, width - 1)

            fg_color = saturated_frame[center_y, center_x]

            # 获取该块的平均亮度
            avg_brightness = np.mean(gray[y:y + block_size, x:x + block_size])

            # 根据平均亮度决定是 0 还是 1
            char = '1' if avg_brightness > 128 else '0'

            # 绘制字符
            text_position = (x, y + block_size - 2)  # 调整字符的位置
            cv2.putText(canvas, char, text_position, font, font_scale, fg_color.tolist(), 1, cv2.LINE_AA)

    # 在窗口中显示带有字符的画布
    cv2.imshow('Color-Based Binary Text Display', canvas)

    # 将带有字符的帧写入视频
    out.write(canvas)

    # 按下 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# 释放资源
cap.release()
out.release()  # 关闭 VideoWriter
cv2.destroyAllWindows()
