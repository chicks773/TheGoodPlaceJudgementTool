import tkinter as tk

import os
import pandas as pd

import pandastable as pt

from idlelib.tooltip import Hovertip



def is_empty_pt(ptdf):
	return (ptdf.count().tolist() == [0, 0, 0, 0, 0])

def optional_add_file_extension(filename, file_extension=".csv"):
	#improvement - check for other ways that filename can be badly formed
	if not(filename.endswith(file_extension)):
		filename += file_extension
	return filename

def sum_points(points_list):
	points_list = points_list.strip("[]").split(", ")
	points_list = list(map(lambda x: float(x), points_list))
	return sum(points_list)



def run_window():

	# set up window and top frame

	window = tk.Tk()
	window.title("The Good Place Judgement Tool")
	window.configure(background="#DAFFFE")

	topFrame = tk.Frame(master=window, height=150, width=750) 

	def update_export_filename():
		import_filename = importFileEntryBox.get()
		default_export_filename = import_filename.strip(".csv") + "_judged" + str(sinnerCutoffSlider.get())
		exportFileEntryBox.delete(0, tk.END)
		exportFileEntryBox.insert(0, default_export_filename)

		return

	##########################################
	# top left frame, import files
	##########################################

	topLeftFrame = tk.Frame(master=window, height=150, width=250)
	topLeftFrame.grid(row=1, column=1)

	importFileErrorLabel = tk.Label(master=topLeftFrame, text="")
	importFileErrorLabel.pack()

	importFileEntryBox = tk.Entry(master=topLeftFrame, font=('arial', 16))
	importFileEntryBox.pack(pady=5, padx=20)

	def import_file():
		filename = importFileEntryBox.get()
		filename = optional_add_file_extension(filename)
		if not os.path.isfile(filename):
			importFileErrorLabel.config(text="please enter valid import filename")
		else:
			importFileErrorLabel.config(text="")
			ptdf_main.importCSV(filename)
			ptdf_main.redraw()
			update_export_filename()
		return

	importFileButton = tk.Button(master=topLeftFrame, text="Import File", command=import_file, font=('arial', 14))
	importFileButton.pack(pady=5, padx=20)


	##########################################
	# top mid frame, sinner cutoff slider
	##########################################

	topMidFrame = tk.Frame(master=window, height=150, width=250)
	topMidFrame.grid(row=1, column=2)

	sinnerCutoffSliderLabel = tk.Label(master=topMidFrame, text="Sinner Cutoff Slider",font=('arial', 14))
	sinnerCutoffSliderLabel.pack()



	sinnerCutoffSlider = tk.Scale(master=topMidFrame, from_=0, to=100, length=200, orient="horizontal", font=('arial', 12))
	sinnerCutoffSlider.set(50)
	sinnerCutoffSlider.pack(pady=5, padx=20)



	def judge():
		judged_people_df = ptdf_main.model.df

		#if df empty, can't judge
		if is_empty_pt(judged_people_df):
			judgeErrorLabel.config(text="no data to judge")
			return
		
		judgeErrorLabel.config(text="")
		#calculate sum of points
		judged_people_df["sum of points"] = judged_people_df["points list"].apply(sum_points)

		#calculate percentile based on sum of points
		judged_people_df["percentile"] = judged_people_df["sum of points"].rank(pct = True) * 100
		
		sinnerCutoffThreshold = sinnerCutoffSlider.get()
		def is_good_or_bad(points_percentile):
			if points_percentile >= sinnerCutoffThreshold:
				return "Good Place"
			else:
				return "Bad Place"

		judged_people_df["judgement"] = judged_people_df["percentile"].apply(is_good_or_bad)
		#print(judged_people_df.head())

		ptdf_main.redraw()


		#create good and bad dfs

		good_df = ptdf_main.model.df[["name", "percentile", "judgement"]]
		good_df = good_df[good_df["judgement"] == "Good Place"]

		ptdf_good.model.df = good_df
		ptdf_good.redraw()

		bad_df = ptdf_main.model.df[["name", "percentile", "judgement"]]
		bad_df = bad_df[bad_df["judgement"] == "Bad Place"]

		ptdf_bad.model.df = bad_df
		ptdf_bad.redraw()

		#update default filename in export Entry box
		update_export_filename()


		return

	judgeButton = tk.Button(master=topMidFrame, text="Judge", command=judge, bg="#AE1F00", font=('arial', 16, 'bold'))
	judgeButton.pack(side=tk.LEFT, padx=20)

	judgeErrorLabel = tk.Label(master=topMidFrame, text="")
	judgeErrorLabel.pack(pady=2)

	judgeHelpButton = tk.Button(master=topMidFrame, text="?")
	judgeHelpButton.pack(side=tk.LEFT)
	#todo


	##########################################
	# top right frame, export files
	##########################################

	topRightFrame = tk.Frame(master=window, height=150, width=250)
	topRightFrame.grid(row=1, column=3)

	exportFileErrorLabel = tk.Label(master=topRightFrame, text="")
	exportFileErrorLabel.pack()

	exportFileEntryBox = tk.Entry(master=topRightFrame, font=('arial', 16))
	exportFileEntryBox.pack(pady=5, padx=20)

	def export_file():
		export_filename = exportFileEntryBox.get()
		import_filename = importFileEntryBox.get()
		if import_filename != "":
			filename = optional_add_file_extension(filename)
			import_df = pd.read_csv(import_filename)
		if export_filename == "":
			exportFileErrorLabel.config(text="Please enter a valid filename to use")
		else:
			if(not(export_filename.endswith(".csv"))):
				export_filename = export_filename + ".csv"

			df = ptdf_main.model.df
			#if df is empty, don't export
			if is_empty_pt(df):
				exportFileErrorLabel.config(text="no data to export")
			#don't export if df is unchanged from import file
			elif df.equals(import_df):
				exportFileErrorLabel.config(text="no change from import file to export")

			else:
				#check that filename doesn't already exist
				if(os.path.isfile(export_filename)):
					exportFileErrorLabel.config(text="File with that name already exists")
				else:
					df.to_csv(export_filename)
					exportFileErrorLabel.config(text="File exported successfully")

	exportFileButton = tk.Button(master=topRightFrame, text="Export File", command=export_file, font=('arial', 14))
	exportFileButton.pack(pady=5, padx=20)

	tt1 = Hovertip(exportFileButton, " press this button to export file with above name ")


	##########################################
	# top padding frame
	##########################################

	topPaddingFrame = tk.Frame(master=window, height=50)
	topPaddingFrame.grid(row=2, column=1, columnspan=3)


	##########################################
	# mid frame, main df viewer
	##########################################

	midFrame = tk.Frame(master=window, height=150, width=1050)
	midFrame.grid(row=3, column=1, columnspan=3)

	#dummy_df = pd.DataFrame(columns=["name", "personality", "points list"]) todo, this doesn't work

	ptdf_main = pt.Table(midFrame, width=1050, showtoolbar=True, showstatusbar=True)
	#ptdf_main.model.df = dummy_df
	ptdf_main.show()
	ptdf_main.grid(row=1, column=1, columnspan=3)



	##########################################
	# bottom frame
	##########################################


	bottomPaddingFrame = tk.Frame(master=window, height=50)
	bottomPaddingFrame.grid(row=4, column=1, columnspan=3)

	# bottomLeftHeaderFrame - contains header for bad place df
	bottomLeftHeaderFrame = tk.Frame(master=window, height=75, width=250)
	bottomLeftHeaderFrame.grid(row=5, column=1)

	bad_df_header = tk.Label(master=bottomLeftHeaderFrame, text="Going to the Bad Place", font=('arial', 12))
	bad_df_header.pack()

	# bottomRightHeaderFrame - contains header for good place df
	bottomRightHeaderFrame = tk.Frame(master=window, height=27, width=250)
	bottomRightHeaderFrame.grid(row=5, column=3)

	good_df_header = tk.Label(master=bottomRightHeaderFrame, text="Going to the Good Place", font=('arial', 12))
	good_df_header.pack()


	##########################################
	# bottom left frame, bad place preview df
	##########################################

	bottomLeftFrame = tk.Frame(master=window, height=150, width=250)
	bottomLeftFrame.grid(row=6, column=1)

	ptdf_bad = pt.Table(bottomLeftFrame, height=150, width=250)
	pt.config.apply_options({'fontsize': 8, 'rowheight': 15}, ptdf_bad)
	ptdf_bad.show()
	ptdf_bad.grid(row=1, column=1)

	bottomMidFrame = tk.Frame(master=window, height=150, width=250)
	bottomMidFrame.grid(row=6, column=2)

	#######################################
	# bottom right frame, good place preview df
	########################################

	bottomRightFrame = tk.Frame(master=window, height=150, width=250)
	bottomRightFrame.grid(row=6, column=3)

	ptdf_good = pt.Table(bottomRightFrame, height=150, width=250)
	pt.config.apply_options({'fontsize': 8, 'rowheight': 15}, ptdf_good)
	ptdf_good.show()
	ptdf_good.grid(row=1, column=1)






	window.mainloop()






	return




def __main__():
	run_window()
	return



if __name__ == "__main__":
	__main__()


"""
todo
	tooltips, pop out explanations
		pop out (?) next to judge button
		somewhere to put main Help button
		create some pdfs or images to be the pop out explanations

	medium place
	#maybe use this as a multi slider widget
	# https://github.com/MenxLi/tkSliderWidget

	maybe load in dummy database to start. or at least the correct headers.



"""


"""

improvements:

modifiers (unforgiving god, children go to heaven)

file explorer picker for import file

"the good place" font

when (import filebox not empty) and (import filebox last edited), Enter to import file

maybe, instead of file import and export buttons, create a file -> open menu up top (like most windows)

cell width doesn't work on the pandastable. maybe consider a different widget. (or make my own?)







"""