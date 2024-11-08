import os
import tkinter as tk
import pandas as pd

import pandastable as pt

from idlelib.tooltip import Hovertip




#check if pandastable is "empty", or matches its initial dummy df
def is_empty_pt(ptdf):
	return (ptdf.count().tolist() == [0, 0, 0, 0, 0])

#add the .csv to filenames if not specified
def optional_add_file_extension(filename, file_extension=".csv"):
	#improvement - check for other ways that filename can be badly formed
	if not(filename.endswith(file_extension)):
		filename += file_extension
	return filename

# takes a string of a list of numbers, calculates the sum
def sum_points(points_list):
	points_list = points_list.strip("[]").split(", ")
	points_list = list(map(lambda x: float(x) if x != '' else 0, points_list))
	return sum(points_list)

# create a simple dummy df to load in when the GUI first starts
def generate_dummy_data():
	points_list = str([-20] * 35)
	dummy_data = {"name": ["Eleanor Shellstrop", "", ""],
						   "personality": ["[unkind]", "", ""], 
						   "points list": [points_list, "", ""]}
	return dummy_data






def run_window():

	# set up window and top frame

	window = tk.Tk()
	window.title("The Good Place Judgement Tool")
	window.configure(background="#65D46A")

	topFrame = tk.Frame(master=window, height=150, width=750) 

	# update the default/suggested export filename when the user imports a file
	# or passes judgement
	def update_export_filename():
		import_filename = importFileEntryBox.get()
		if toggle_med_place_var.get() == 1:
			threshold_values = (sinnerCutoffSlider1.get(), 
								sinnerCutoffSlider2.get())
			min_threshold_val, max_threshold_val = (min(threshold_values), 
													max(threshold_values))
			default_export_filename = import_filename.strip(".csv") + \
									  "_judged" + str(min_threshold_val) + "-" \
									  + str(max_threshold_val)
		else:
			default_export_filename = import_filename.strip(".csv") + "_judged"\
								  + str(sinnerCutoffSlider1.get())

		exportFileEntryBox.delete(0, tk.END)
		exportFileEntryBox.insert(0, default_export_filename)

		return

	##########################################
	# top left frame, import files
	##########################################

	topLeftFrame = tk.Frame(master=window, height=150, width=250, bg="#65D46A")
	topLeftFrame.grid(row=1, column=1)

	######################
	# HELP WINDOW
	######################
	def launch_help_window():
		help_window = tk.Tk()
		header_text = "How to use this GUI"
		help_header = tk.Label(master=help_window, text=header_text, 
							   font=("Arial", 14, "bold"))
		help_header.pack()

		help_text_frame = tk.Frame(master=help_window, height=500, width=300)
		help_text_frame.pack()

		help_p1 = "For more detailed help using this GUI, please consult the readme."
		help_p2 = "This tool is used to apply judgement to humans based on their numerical score."
		help_p3 = "To begin, type the name or path of a .csv file in the import filename box, \
then press the 'Import File' button to load the world file into the GUI."
		help_p4 = "Select the parameters you want to use above the Judge button. There is another \
help button to the right of the Judge button that explains all of these \
parameters. When you have selected your parameters, click the Judge button to \
apply judgement to the world file."
		help_p5 = "Judgement will add three new columns, the sum of points, the percentile of the \
sum of points, and the final judgement (Good Place, Bad Place, or Medium Place).\
The three table viewers at the bottom of the GUI will display a preview of the \
people going to each place."
		help_p6 = "You can use the export button in the top right to create a .csv file containing\
the calculations and judgements. The GUI will suggest an automatic export \
filename based on the input filename and the judgement parameters used, but you \
can enter any filename you prefer. Click the Export File button to create a .csv\
with the filename listed in the box."

		help_p1_label = tk.Label(master=help_text_frame, text=help_p1, 
								 wraplength=400, justify=tk.LEFT)
		help_p2_label = tk.Label(master=help_text_frame, text=help_p2, 
								 wraplength=400, justify=tk.LEFT)
		help_p3_label = tk.Label(master=help_text_frame, text=help_p3, 
								 wraplength=400, justify=tk.LEFT)
		help_p4_label = tk.Label(master=help_text_frame, text=help_p4, 
								 wraplength=400, justify=tk.LEFT)
		help_p5_label = tk.Label(master=help_text_frame, text=help_p5,
								 wraplength=400, justify=tk.LEFT)
		help_p6_label = tk.Label(master=help_text_frame, text=help_p6,
								 wraplength=400, justify=tk.LEFT)

		help_p1_label.pack()
		help_p2_label.pack()
		help_p3_label.pack()
		help_p4_label.pack()
		help_p5_label.pack()
		help_p6_label.pack()


		help_window.mainloop()

	# helpButton - launches the help window
	helpButton = tk.Button(master=topLeftFrame, text="?", command=launch_help_window, 
						   font=('arial', 18), bg="#000CFF", fg="white")
	helpButton.pack(side=tk.LEFT)

	helpButtontt = Hovertip(helpButton, " How to use this tool ")


	#################################
	# import file frame, top left
	#################################
	importFileFrame = tk.Frame(master=topLeftFrame, bg="#65D46A")
	importFileFrame.pack(side=tk.LEFT)

	importFileErrorLabel = tk.Label(master=importFileFrame,
									text="Import a file here to begin", 
									bg="#65D46A", fg="white", font=('bold'))
	importFileErrorLabel.pack()

	importFileEntryBox = tk.Entry(master=importFileFrame, font=('arial', 16))
	importFileEntryBox.pack(pady=5, padx=20)

	# import file function
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

	importFileButton = tk.Button(master=importFileFrame, text="Import File",
								 command=import_file, font=('arial', 14), 
								 fg="#19E722")
	importFileButton.pack(pady=5, padx=20)
	importFileButtontt = Hovertip(importFileButton, " Click this button to import the filename typed in the box ")


	##########################################
	# top mid frame, sinner cutoff slider(s)
	##########################################

	topMidFrame = tk.Frame(master=window, height=150, width=250, bg="#65D46A")
	topMidFrame.grid(row=1, column=2)

	sinnerCutoffSliderLabel = tk.Label(master=topMidFrame, text="Sinner Cutoff Slider",
									   font=('arial', 14, 'bold'), bg="#65D46A", fg="white")
	sinnerCutoffSliderLabel.pack()


	sinnerCutoffSlider1 = tk.Scale(master=topMidFrame, from_=0, to=100, length=200, 
								   orient="horizontal", font=('arial', 12))
	sinnerCutoffSlider1.set(50)
	sinnerCutoffSlider1.pack(pady=5, padx=20)

	secondSliderFrame = tk.Frame(master=topMidFrame, height=45, bg="#65D46A")
	secondSliderFrame.pack()

	sinnerCutoffSlider2 = tk.Scale(master=secondSliderFrame, from_=0, to=100, length=200, 
								   orient="horizontal", font=('arial', 12))
	sinnerCutoffSlider2.set(50)
	#sinnerCutoffSlider2.pack(pady=5, padx=20)

	# second sinnerCuttoffSlider starts invisible, is triggered when medium
	# place is toggled


	#########################
	# helper functions for medium place toggle
	#########################
	def hide_med_ptdf():
		med_place_hide_shape.grid(row=6, column=2)
		return

	def show_med_ptdf():
		med_place_hide_shape.grid_forget()
		return

	def turn_on_med_place():
		sinnerCutoffSlider2.pack()
		med_df_header.pack()
		ptdf_med.grid(row=1, column=1)
		show_med_ptdf()
		update_export_filename()
		return

	def turn_off_med_place():
		sinnerCutoffSlider2.pack_forget()
		med_df_header.pack_forget()
		hide_med_ptdf()
		update_export_filename()
		return

	toggle_med_place_var = tk.IntVar()

	def toggle_med_place():
		if toggle_med_place_var.get() == 0:
			turn_off_med_place()
		elif toggle_med_place_var.get() == 1:
			turn_on_med_place()
		return

	medPlaceButtonsFrame = tk.Frame(master=topMidFrame, bg="#65D46A")
	medPlaceButtonsFrame.pack()

	medPlaceCheckbutton = tk.Checkbutton(master=medPlaceButtonsFrame, text="Medium Place", 
										 variable=toggle_med_place_var, onvalue=1, offvalue=0, 
										 command=toggle_med_place, bg="#65D46A", fg="white",
										 activebackground="#65D46A", activeforeground="white",
										 selectcolor="black")
	medPlaceCheckbutton.pack()


	###############################################
	# judge function
	###############################################

	def judge():
		judged_people_df = ptdf_main.model.df

		#if df empty, or matches starter dummy data, can't judge
		dummy_df = pd.DataFrame(columns=["name", "personality", "points list"], 
								data=generate_dummy_data())
		
		if is_empty_pt(judged_people_df) or judged_people_df.equals(dummy_df):
			judgeErrorLabel.config(text="no data to judge")
			return
		
		#if data is good to judge, clear judge error label
		judgeErrorLabel.config(text="")

		#calculate sum of points
		judged_people_df["sum of points"] = judged_people_df["points list"].apply(sum_points)

		#calculate percentile based on sum of points
		judged_people_df["percentile"] = judged_people_df["sum of points"].rank(pct = True) * 100
		
		#if medium place active, judge is_good_or_bad_or_med
		if toggle_med_place_var.get() == 1:

			#get values from both threshold sliders
			sinnerCutoffThreshold1 = sinnerCutoffSlider1.get()
			sinnerCutoffThreshold2 = sinnerCutoffSlider2.get()

			def is_good_or_bad_or_med(points_percentile):
				# use slider values to set thresholds between good and medium place, 
				# and medium and bad place
				high_points_threshold = max([sinnerCutoffThreshold1, sinnerCutoffThreshold2])
				low_points_threshold = min([sinnerCutoffThreshold1, sinnerCutoffThreshold2])

				if high_points_threshold == low_points_threshold:
					judgeErrorLabel.config(text="To include a Medium Place, the two sliders \
												cannot have identical values")
					return
				else:
					judgeErrorLabel.config(text="")
					if points_percentile >= high_points_threshold:
						return "Good Place"
					elif points_percentile >= low_points_threshold:
						return "Medium Place"
					else:
						assert(points_percentile < low_points_threshold)
						return "Bad Place"
			judged_people_df["judgement"] = \
									judged_people_df["percentile"].apply(is_good_or_bad_or_med)

		#if medium place is not active, judge is_good_or_bad
		elif toggle_med_place_var.get() == 0:
			sinnerCutoffThreshold = sinnerCutoffSlider1.get()
			def is_good_or_bad(points_percentile):
				if points_percentile >= sinnerCutoffThreshold:
					return "Good Place"
				else:
					return "Bad Place"

			judged_people_df["judgement"] = judged_people_df["percentile"].apply(is_good_or_bad)

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

		if toggle_med_place_var.get() == 1:
			med_df = ptdf_main.model.df[["name", "percentile", "judgement"]]
			med_df = med_df[med_df["judgement"] == "Medium Place"]

			ptdf_med.model.df = med_df
			ptdf_med.redraw()

		#update default filename in export Entry box
		update_export_filename()


		return

	judge_button_frame = tk.Frame(master=topMidFrame, bg="#65D46A")
	judge_button_frame.pack()

	judgeButton = tk.Button(master=judge_button_frame, text="Judge", command=judge, bg="#AE1F00", 
						    font=('arial', 16, 'bold'))
	judgeButton.pack(side=tk.LEFT, padx=20)

	def launch_judge_help_window():
		judge_help_window = tk.Tk()

		judge_help_header_label = tk.Label(master=judge_help_window, text="Using the Judge Button")
		judge_help_header_label.pack()

		judge_help_text_p1 = "After importing a world file, you can click the Judge button to pass \
judgement."
		judge_help_text_p2 = "By default, the Medium Place is turned off, and you can only see one \
Sinner Cutoff Slider. Slide this to any value and press the Judge button to separate humans to the \
Good and Bad place based on that threshold."
		judge_help_text_p3 = "You can check the Medium Place checkbox to add the Medium Place as a \
third condition. If the Medium Place is active, you will have two Sinner Cutoff Sliders."
		judge_help_text_p4 = "With the Medium Place active, set the two Sinner Cutoff Sliders to \
different values. It will not judge if both sliders are set to the same value. You may set either \
value on either slider; both the low and high threshold can be on either the top or bottom slider."
		judge_help_text_p5 = "More parameters and modifiers for judgement coming soon!"

		judge_help_text_frame = tk.Frame(master=judge_help_window)
		judge_help_text_frame.pack()

		judge_help_label_p1 = tk.Label(master=judge_help_text_frame, text=judge_help_text_p1, wraplength=400, justify=tk.LEFT)
		judge_help_label_p1.pack()
		judge_help_label_p2 = tk.Label(master=judge_help_text_frame, text=judge_help_text_p2, wraplength=400, justify=tk.LEFT)
		judge_help_label_p2.pack()
		judge_help_label_p3 = tk.Label(master=judge_help_text_frame, text=judge_help_text_p3, wraplength=400, justify=tk.LEFT)
		judge_help_label_p3.pack()
		judge_help_label_p4 = tk.Label(master=judge_help_text_frame, text=judge_help_text_p4, wraplength=400, justify=tk.LEFT)
		judge_help_label_p4.pack()
		judge_help_label_p5 = tk.Label(master=judge_help_text_frame, text=judge_help_text_p5, wraplength=400, justify=tk.LEFT)
		judge_help_label_p5.pack()

		judge_help_window.mainloop()

	judgeHelpButton = tk.Button(master=judge_button_frame, text="?", bg="#f68383", 
								command=launch_judge_help_window, font=('arial', 12))
	judgeHelpButton.pack(side=tk.LEFT)

	judgeErrorLabel = tk.Label(master=topMidFrame, text="", bg="#65D46A", fg="white", font=('bold'))
	judgeErrorLabel.pack(pady=2)


	##########################################
	# top right frame, export files
	##########################################

	topRightFrame = tk.Frame(master=window, height=150, width=250, bg="#65D46A")
	topRightFrame.grid(row=1, column=3)

	exportFileErrorLabel = tk.Label(master=topRightFrame, text="", bg="#65D46A", fg="white", 
									font=('bold'))
	exportFileErrorLabel.pack()

	exportFileEntryBox = tk.Entry(master=topRightFrame, font=('arial', 16))
	exportFileEntryBox.pack(pady=5, padx=20)

	#######################
	# export file function
	#######################

	def export_file():
		export_filename = exportFileEntryBox.get()
		import_filename = importFileEntryBox.get()
		if import_filename != "":
			import_filename = optional_add_file_extension(import_filename)
			import_df = pd.read_csv(import_filename)
			#note - this wouldn't work correctly if the user had edited the import file box
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

	
	#export file button and tooltip
	exportFileButton = tk.Button(master=topRightFrame, text="Export File", command=export_file, 
								 font=('arial', 14), fg="#19E722")
	exportFileButton.pack(pady=5, padx=20)

	exportFileButtontt = Hovertip(exportFileButton, " press this button to export file with \
													  above name ")


	##########################################
	# top padding frame
	##########################################

	topPaddingFrame = tk.Frame(master=window, height=30, bg="#65D46A")
	topPaddingFrame.grid(row=2, column=1, columnspan=3)

	##########################################
	# mid frame, main df viewer
	##########################################

	midFrame = tk.Frame(master=window, height=250, width=1050, bg="#65D46A")
	midFrame.grid(row=3, column=1, columnspan=3)

	dummy_data = generate_dummy_data()
	
	dummy_df = pd.DataFrame(columns=["name", "personality", "points list"], data=dummy_data)

	ptdf_main = pt.Table(midFrame, width=1050, height=250, showstatusbar=True, editable=False)
	#improvement, maybe make a button that makes the df editable
	ptdf_main.model.df = dummy_df
	ptdf_main.show()
	ptdf_main.grid(row=1, column=1, columnspan=3)



	##########################################
	# bottom frame - preview dfs
	##########################################

	#bottom padding frame
	bottomPaddingFrame = tk.Frame(master=window, height=30, bg="#65D46A")
	bottomPaddingFrame.grid(row=4, column=1, columnspan=3)

	# bottomLeftHeaderFrame - contains header for bad place df
	bottomLeftHeaderFrame = tk.Frame(master=window, height=75, width=250, bg="#65D46A")
	bottomLeftHeaderFrame.grid(row=5, column=1)

	bad_df_header = tk.Label(master=bottomLeftHeaderFrame, text="Going to the Bad Place", 
							 font=('arial', 12, 'bold'), bg="#65D46A", fg="white")
	bad_df_header.pack()

	# bottomMidHeaderFrame - contains header for med place df
	bottomMidHeaderFrame = tk.Frame(master=window, height=25, width=250, bg="#65D46A")
	bottomMidHeaderFrame.grid(row=5, column=2)

	med_df_header = tk.Label(master=bottomMidHeaderFrame, text="Going to the Medium Place", 
							 font=('arial', 12, 'bold'), bg="#65D46A", fg="white")

	# bottomRightHeaderFrame - contains header for good place df
	bottomRightHeaderFrame = tk.Frame(master=window, height=27, width=250, bg="#65D46A")
	bottomRightHeaderFrame.grid(row=5, column=3)

	good_df_header = tk.Label(master=bottomRightHeaderFrame, text="Going to the Good Place", 
							  font=('arial', 12, 'bold'), bg="#65D46A", fg="white")
	good_df_header.pack()


	##########################################
	# bottom left frame, bad place preview df
	##########################################

	bottomLeftFrame = tk.Frame(master=window, height=100, width=250, bg="#65D46A")
	bottomLeftFrame.grid(row=6, column=1)

	ptdf_bad = pt.Table(bottomLeftFrame, height=100, width=250)
	pt.config.apply_options({'fontsize': 8, 'rowheight': 15}, ptdf_bad)
	ptdf_bad.show()
	ptdf_bad.grid(row=1, column=1)

	##########################################
	# bottom mid frame, medium place preview df
	##########################################

	bottomMidFrame = tk.Frame(master=window, height=100, width=250, bg="#65D46A")
	bottomMidFrame.grid(row=6, column=2)

	ptdf_med = pt.Table(bottomMidFrame, height=100, width=250)
	pt.config.apply_options({'fontsize': 8, 'rowheight': 15}, ptdf_med)
	ptdf_med.show()

	#use a canvas to hide the med place df when not in use
	med_place_hide_shape = tk.Canvas(master=window, bg="#65D46A", height=135, width=320)
	med_place_hide_shape.grid(row=6, column=2)

	#######################################
	# bottom right frame, good place preview df
	########################################

	bottomRightFrame = tk.Frame(master=window, height=100, width=250, bg="#65D46A")
	bottomRightFrame.grid(row=6, column=3)

	ptdf_good = pt.Table(bottomRightFrame, height=100, width=250)
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

Future Improvements:

modifiers (unforgiving god, children go to heaven)
-reformed go to heaven 
(compare second half of life to first half of life, or general upward trend for all or most of life)
-unreliable accountants
(some x% of judgements will be incorrect)

file explorer picker for import file (maybe, instead of file import and export buttons, create a file -> open menu up top)

"the good place" font

when (import filebox not empty) and (import filebox last edited), Enter to import file

cell width doesn't work on the pandastable. maybe consider a different widget. (or make my own?)

controlling where window appears - especially the help windows
https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens







"""