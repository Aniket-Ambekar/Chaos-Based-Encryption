
# Video Encryption Decryption

# imported necessary library
import tkinter
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import numpy as np
from cv2 import *
from moviepy.editor import *
from skimage import img_as_float
from tqdm import tqdm
from matplotlib import pyplot as plt

# function to select file
def open_file():
    global filename
    filename = filedialog.askopenfilename(title="Select file")
    # print(filename)
    path_text.delete("1.0", "end")
    path_text.insert(END, filename)

# Video encryption function

def encrypt_fun():
    # Video capture
    cam = cv2.VideoCapture(filename)
    
    # Frame rate
    x = int(cam.get(cv2.CAP_PROP_FPS))
    
    # Frame width and height
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # VideoWriter to save encrypted video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('encrypted_video.mp4', fourcc, x, (width, height))
    
    # Get the total number of frames
    total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # running the loop
    for _ in tqdm(range(total_frames), desc="Processing frames", total=total_frames):
        ret, frame = cam.read()
        if ret:
            # Process and encrypt frame
            frame_encrypted = img_as_float(frame)
            mu, sigma = 0, 0.01   # Reduce sigma to decrease noise
            noise = np.random.normal(mu, sigma, frame_encrypted.shape)
            frame_encrypted = frame_encrypted + noise
            frame_encrypted = np.clip(frame_encrypted, 0, 1) * 255
            
            # Save encrypted frame
            out.write(frame_encrypted.astype(np.float32))
            
        else:
            break
    
    # Release the resources
    cam.release()
    out.release()
    cv2.destroyAllWindows()

# Decryption function
def decrypt_fun():
    # Video capture
    cam = cv2.VideoCapture('encrypted_video.mp4')
    
    # Frame rate
    x = int(cam.get(cv2.CAP_PROP_FPS))
    
    # Frame width and height
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # VideoWriter to save decrypted video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('decrypted_video.mp4', fourcc, x, (width, height))
    
    # Get the total number of frames
    total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # running the loop
    for _ in tqdm(range(total_frames), desc="Processing frames", total=total_frames):
        ret, frame = cam.read()
        if ret:
            # Process and decrypt frame
            frame_decrypted = img_as_float(frame)
            mu, sigma = 0, 0.1   # Reduce sigma to decrease noise
            noise = np.random.normal(mu, sigma, frame_decrypted.shape)
            frame_decrypted = frame_decrypted - noise
            frame_decrypted = np.clip(frame_decrypted, 0, 1) * 255
            
            # Save decrypted frame
            out.write(frame_decrypted.astype(np.float32))
            
        else:
            break
    
    # Release the resources
    
    cam.release()
    out.release()
    cv2.destroyAllWindows()
    decrypt_save()
# function to reset the video to original video and show preview of that
def compare_frames():
    global filename
    source = cv2.VideoCapture(filename)
    source2 = cv2.VideoCapture('decrypted_video.mp4')

    # save a frame from the original video
    ret, img = source.read()
    cv2.imwrite('original_frame.jpg', img)

    # save a frame from the decrypted video
    ret2, img2 = source2.read()
    cv2.imwrite('decrypted_frame.jpg', img2)

    # close the videos
    source.release()
    source2.release()

    # read the saved frames and compute the histogram
    original_img = cv2.imread('original_frame.jpg')
    original_img_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    original_hist = cv2.calcHist([original_img_gray], [0], None, [256], [0, 256])

    decrypted_img = cv2.imread('decrypted_frame.jpg')
    decrypted_img_gray = cv2.cvtColor(decrypted_img, cv2.COLOR_BGR2GRAY)
    decrypted_hist = cv2.calcHist([decrypted_img_gray], [0], None, [256], [0, 256])

    # plot the histograms
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(original_hist)
    plt.title('Original Frame Histogram')

    plt.subplot(1, 2, 2)
    plt.plot(decrypted_hist)
    plt.title('Decrypted Frame Histogram')

    plt.show()

def decrypt_save():
    
    source = cv2.VideoCapture(filename)
    width = int(source.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    # creating the output video
    out = cv2.VideoWriter('decrypted_video.mp4', codec, 30.0, (width, height))

    # running the loop
    while True:
        # extracting the frames
        ret, img = source.read()
        if not ret:
            break
        # displaying the video
        cv2.imshow("Decrypted Video", img)
        # saving the frame to the output video
        out.write(img)
        # exiting the loop
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    # releasing the resources
    source.release()
    out.release()
    cv2.destroyAllWindows()


window1 = tk.Tk()
window1.title("VIDEO ENCRYPTION DECRYPTION")

# top label
start1 = tk.Label(text = "VIDEO  ENCRYPTION\nDECRYPTION", font=("Arial", 55, "underline"), fg="magenta") # same way bg
start1.place(x = 120, y = 10)

lbl2 = tk.Label(text="Selected Video", font=("Arial", 30),fg="brown")  # same way bg
lbl2.place(x=80, y=220)

path_text = tk.Text(window1, height=3, width=37, font=("Arial", 30), bg="light yellow", fg="orange",borderwidth=2, relief="solid")
path_text.place(x=80, y = 270)

# Select Button
selectb=Button(window1, text="ENCRYPT VIDEO",command=encrypt_fun,  font=("Arial", 25), bg = "orange", fg = "blue")
selectb.place(x = 120, y = 450)

# Select Button
selectb=Button(window1, text="DECRYPT VIDEO",command=decrypt_fun,  font=("Arial", 25), bg = "orange", fg = "blue")
selectb.place(x = 550, y = 450)

# Select Button
selectb=Button(window1, text="SELECT",command=open_file,  font=("Arial", 25), bg = "light green", fg = "blue")
selectb.place(x = 80, y = 580)

# Get Images Button
getb=Button(window1, text="COMPARE",command=compare_frames,  font=("Arial", 25), bg = "yellow", fg = "blue")
getb.place(x = 420, y = 580)


def exit_win1():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window1.destroy()

# Get Images Button
getb=Button(window1, text="EXIT",command=exit_win1,  font=("Arial", 25), bg = "red", fg = "blue")
getb.place(x = 780, y = 580)

window1.protocol("WM_DELETE_WINDOW", exit_win1)
window1.mainloop()
