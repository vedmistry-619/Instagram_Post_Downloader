from tkinter import *
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import os,cv2,json
import requests
import urllib.request

def Object():
	label = Label(root,text = "URL",backgroung = "black")
	label.grid(row = 0,column =0, padx = 5,pady = 5)

	root.urlEntry = Entry(root , width = 30 , textvariable = instaURL)
	root.urlEntry.grid(row = 0, column = 1, columnspan = 3, padx = 0, pady = 5)

	download = Button(root , text = "Download", command = _download, highlightbackground = "red")
	download.grid(row = 0, column = 3, padx = 5, pady = 5)

	root.result = Label(root, text = "Results", background = "white")
	root.result.grid(row = 1, column = 5, padx= 5, pady = 1)

	root.downloadlabel = Label(root, textvariable = downloadtext , background = "deepskyblue4")
	root.downloadlabel.grid(row = 2, column = 0, columnspan = 2, padx = 5 , pady = 5)

	root.previewLabel = Label(root, text = "Preview", background = "deepskyblue4")
	root.previewLabel.grid(row = 3, column = 0, padx= 5, pady = 5)





def _download():
	download_path = "What is your destiantion path folder??"
	posts = requests.get(instaURL.get())

	soup = BeautifulSoup(posts.content,'html parser')
	script = soup.find('script', text.re.compile('window._sharedData'))

	jsonn = script.text.split('=', 1)[1].rstrip(;)

	data = json.loads(jsonn)
	base_data = data['entry_data']['Post_page'][0]['graphql']['shortcode_media']
	typename = base_data['__typename']

if typename == "GraphImage":
	display_url = base_data['display-url']
	file_name = base_data['taken_at_timestamp']
	download_p = download_path + str(file_name) = ".jpg"

	if not os.path.exists(download_p):
		urllib.request.urlretrieve(display_url , download_p)

		image = Image.open(download_p)
		image = image.resize((100,100), Image.ANTIALIAS)
		image = ImageTk.PhotoImage(image)

		imgLabel = Label(root)
		imgLabel.grid(row = 4, column = 0, padx= 1, pady = 1)
		imgLabel.config(image=image)
		imgLabel.photo = image

		prev_t = downloadtext.get()
		new_t = prev_t + "\n" + str(file_name) + ".jpg DOWNLOADED"
		root.downloadlabel.grid(row = 2, column = 0, columnspan = 2, padx = 1 , pady = 1)
		downloadtext.set(new_t)

	else:
		prev_t = downloadtext.get()
		new_t = prev_t + "\n" + str(file_name) + ".jpg EXISTING"
		root.downloadlabel.grid(row = 2, column = 0, columnspan = 2, padx = 1 , pady = 1)
		downloadtext.set(new_t)

elif typename == "GraphVideo":
	video_url = base_data['video_url']
	file_name = base_data['taken_at_timestamp']
	download_p = download_path +str(file_name) + ".mp4"

	if not os.path.exists(download_p):
		urllib.request.urlretrieve(video_url,download_p)
		vid = cv2.VideoCapture(download_p)
		ret,frame = vid.read()
		
		video_icon = download_path + "/Video Icons/" + str(file_name) + ".jpg"
		cv2.imwrite(video_icon,frame)
		icon = Image.open(video_icon)
		icon = icon.resize((100,100), Image.ANTIALIAS)
		icon = ImageTk.PhotoImage(icon)

		imgLabel = Label(root)
		imgLabel.grid(row = 4, column = 0, padx = 1 , pady = 1)
		imgLabel.config(image=icon)
		imgLabel.photo = icon

		prev_t = downloadtext.get()
		new_t = prev_t + "\n" + str(file_name) + ".mp4 DOWNLOADED"
		root.downloadlabel.grid(row = 2, column = 0, columnspan = 2, padx = 1 , pady = 1)
		downloadtext.set(new_t)

	else:
		prev_t = downloadtext.get()
		new_t = prev_t + "\n" + str(file_name) + ".mp4 EXISTING"
		root.downloadlabel.grid(row = 2, column = 0, columnspan = 2, padx = 1 , pady = 1)
		downloadtext.set(new_t)
		root.downloadlabel.config(text = str(file_name) + ".mp4 ALREADY DOWNLOADED")

elif typename == "GraphSidecar":
	shortcode = base_data['shortcode']
	response = requests.get(f"https://www.instagram.com/p/"+ shortcode + "/?__a=1").json()
	post_n = 1; i = 0

	for edge in response['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
		file_name = response['graphql']['shortcode_media']['taken_at_timestamp']
		download_p = download_path + str(file_name) + "-" + str(post_n)
		is_video = edge['node']['is_video']

		if not is_video:
			display_url = ['edge']['display_url']
			download_p += ".jpg"

			if not os.path.exists(download_p):
				urllib.request.urlretrieve(display_url, download_p)

				image = Image.open(download_p)
				image = image.resize(100,100), Image.ANTIALIAS
				image = ImageTk.PhotoImage(image)

				imgLabel = Label(root)
				imgLabel.grid(row = 4, column = i, padx = 1 , pady = 1)
				imgLabel.config(image=image)
				imgLabel.photo = image

				prev_t = downloadtext.get()
				new_t = prev_t + "\n" + str(file_name) + "-" + str(post_n) + ".jpg DOWNLOADED"
				root.downloadlabel.grid(row = 2, column = 0, columnspan = 2, padx = 1 , pady = 1)
				downloadtext.set(new_t)
				i+=1

			else:
				prev_t = downloadtext.get()
				new_t = prev_t + "\n" + str(file_name) + "-" + str(post_n) + ".jpg EXISTS"
				root.downloadlabel.grid(row = 2, column = 0, columnspan = 2, padx = 1 , pady = 1)
				downloadtext.set(new_t)

		else:
						video_url = edge['node']['video_url']
			download_p += ".mp4"

			if not os.path.exists(download_p):
				urllib.request.urlretrieve(video_url, download_p)

				vid = cv2.VideoCapture(download_p)
				ret,frame = vid.read()
		
				video_icon = download_path + "/Video Icons/" + str(file_name) + ".jpg"
				cv2.imwrite(video_icon,frame)
				icon = Image.open(video_icon)
				icon = icon.resize((100,100), Image.ANTIALIAS)
				icon = ImageTk.PhotoImage(icon)

				imgLabel = Label(root)
				imgLabel.grid(row = 4, column = i, padx = 1 , pady = 1)
				imgLabel.config(image=image)
				imgLabel.photo = image

				prev_t = downloadtext.get()
				new_t = prev_t + "\n" + str(file_name) + "-" + str(post_n) + ".mp4 DOWNLOADED"
				root.downloadlabel.grid(row = 2, column = 0, columnspan = 2, padx = 1 , pady = 1)
				downloadtext.set(new_t)
				i+=1

			else:
				prev_t = downloadtext.get()
				new_t = prev_t + "\n" + str(file_name) + "-" + str(post_n) + ".mp4 EXISTS"
				root.downloadlabel.grid(row = 2, column = 0, columnspan = 2, padx = 1 , pady = 1)
				downloadtext.set(new_t)

		post_n += 1



root = tk.Tk()

root.geometry("600x400")
root.title("Insta Downloader")
root.config(background = "black")

instaURL = StringVar()
downloadtext = StringVar()

CreateWidgets()

root.mainloop()


