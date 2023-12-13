import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import cv2
class VideoFrameSplitter:
    def __init__(self, root):
        self.root = root
        self.root.title("视频分割工具")

        # 输入视频路径
        self.video_path_label = tk.Label(root, text="输入视频路径:")
        self.video_path_label.grid(row=0, column=0, sticky=tk.E)

        self.video_path_entry = tk.Entry(root, width=50)
        self.video_path_entry.grid(row=0, column=1)

        self.browse_video_button = tk.Button(root, text="浏览", command=self.browse_video)
        self.browse_video_button.grid(row=0, column=2)

        # 保存图片路径
        self.save_path_label = tk.Label(root, text="保存图片路径:")
        self.save_path_label.grid(row=1, column=0, sticky=tk.E)

        self.save_path_entry = tk.Entry(root, width=50)
        self.save_path_entry.grid(row=1, column=1)

        self.browse_save_button = tk.Button(root, text="浏览", command=self.browse_save)
        self.browse_save_button.grid(row=1, column=2)

        # 视频分割参数
        self.interval_label = tk.Label(root, text="分割间隔帧数:")
        self.interval_label.grid(row=2, column=0, sticky=tk.E)

        self.interval_entry = tk.Entry(root,width=10)
        self.interval_entry.grid(row=2, column=1, sticky=tk.W)

        # 图片命名格式
        self.format_label = tk.Label(root, text="命名前缀（空为/）:")
        self.format_label.grid(row=3, column=0, sticky=tk.E)

        self.format_entry = tk.Entry(root,width=10)
        self.format_entry.grid(row=3, column=1, sticky=tk.W)

        # 命名宽度
        self.width_label = tk.Label(root, text="命名数字宽度:")
        self.width_label.grid(row=4, column=0, sticky=tk.E)

        self.width_entry = tk.Entry(root,width=10)
        self.width_entry.grid(row=4, column=1, sticky=tk.W)

        # 图片格式
        self.type_label = tk.Label(root, text="图片格式(png,jpg...):")
        self.type_label.grid(row=5, column=0, sticky=tk.E)

        self.type_entry = tk.Entry(root, width=10)
        self.type_entry.grid(row=5, column=1, sticky=tk.W)

        # 开始编号
        self.start_label = tk.Label(root, text="命名开始编号:")
        self.start_label.grid(row=6, column=0, sticky=tk.E)

        self.start_entry = tk.Entry(root, width=10)
        self.start_entry.grid(row=6, column=1, sticky=tk.W)

        # 分割按钮
        self.split_button = tk.Button(root, text="开始分割", command=self.split_video)
        self.split_button.grid(row=7, column=1)

    def browse_video(self):
        video_path = filedialog.askopenfilename(title="选择视频文件", filetypes=[("视频文件", "*.mp4;*.avi")])
        self.video_path_entry.delete(0, tk.END)
        self.video_path_entry.insert(0, video_path)

    def browse_save(self):
        save_path = filedialog.askdirectory(title="选择保存路径")
        self.save_path_entry.delete(0, tk.END)
        self.save_path_entry.insert(0, save_path)

    def split_video(self):
        video_path = self.video_path_entry.get()
        save_path = self.save_path_entry.get()
        interval = int(self.interval_entry.get())
        format_str = self.format_entry.get()
        width = self.width_entry.get()
        type = self.type_entry.get()
        start = int(self.start_entry.get())

        if video_path and save_path and interval > 0 and format_str and width and type and start:
            self.split_frames(video_path, save_path, interval, format_str, width ,type, start)
            tk.messagebox.showinfo("完成", "视频分割完成！")
        else:
            tk.messagebox.showerror("错误", "请填写完整的信息")

    def split_frames(self, video_path, save_path, interval, format_str, width, type, start):
        video_capture = cv2.VideoCapture(video_path)
        success, image = video_capture.read()
        count = 0

        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)

        while success:
            if count % interval == 0:
                if format_str == '/':
                    image_name = save_path / "{:0{}d}.{}".format(count // interval +start, width, type)
                else:
                    image_name = save_path / "{}_{:0{}d}.{}".format(format_str, count // interval +start, width ,type)
                cv2.imwrite(str(image_name), image)
            success, image = video_capture.read()
            count += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoFrameSplitter(root)
    root.mainloop()
