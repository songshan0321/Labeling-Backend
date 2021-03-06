# coding=utf-8
import os, sys
import tkFileDialog
import Tkinter as Tk
import ttk
from PIL import Image, ImageTk
import sqlite3  # Import the SQLite3 module
import csv
from datetime import datetime
import platform


class MainApplication(Tk.Tk):
	image = photo = []

	def __init__(self):
		Tk.Tk.__init__(self)
		self.path = Tk.StringVar()
		self.db_link = ""

		self.sql_create_table = """ CREATE TABLE IF NOT EXISTs attributes (
									participant_id      STRING,
									id                  INTEGER  PRIMARY KEY
																NOT NULL
																UNIQUE,
									file                STRING   NOT NULL
																UNIQUE,
									date                DATETIME,
									person              BOOLEAN  DEFAULT (0),
									home                BOOLEAN  DEFAULT (0),
									playground          BOOLEAN  DEFAULT (0),
									void_deck           BOOLEAN  DEFAULT (0),
									park                BOOLEAN  DEFAULT (0),
									public_space        BOOLEAN  DEFAULT (0),
									supermarket         BOOLEAN  DEFAULT (0),
									market              BOOLEAN  DEFAULT (0),
									food_court          BOOLEAN  DEFAULT (0),
									shop                BOOLEAN  DEFAULT (0),
									mall                BOOLEAN  DEFAULT (0),
									hospital            BOOLEAN  DEFAULT (0),
									clinic              BOOLEAN  DEFAULT (0),
									community_center    BOOLEAN  DEFAULT (0),
									senior              BOOLEAN  DEFAULT (0),
									religious           BOOLEAN  DEFAULT (0),
									transaction_ser     BOOLEAN  DEFAULT (0),
									fitness             BOOLEAN  DEFAULT (0),
									bus_stop            BOOLEAN  DEFAULT (0),
									mrt                 BOOLEAN  DEFAULT (0),
									walkway             BOOLEAN  DEFAULT (0),
									pedestrian_crossing BOOLEAN  DEFAULT (0),
									cycling_path        BOOLEAN  DEFAULT (0),
									street_lights       BOOLEAN  DEFAULT (0),
									traffic_lights      BOOLEAN  DEFAULT (0),
									street_signs        BOOLEAN  DEFAULT (0),
									trees               BOOLEAN  DEFAULT (0),
									furniture           BOOLEAN  DEFAULT (0),
									stairs              BOOLEAN  DEFAULT (0),
									ramps               BOOLEAN  DEFAULT (0),
									walk                BOOLEAN  DEFAULT (0),
									cycle               BOOLEAN  DEFAULT (0),
									bus                 BOOLEAN  DEFAULT (0),
									train               BOOLEAN  DEFAULT (0),
									car                 BOOLEAN  DEFAULT (0),
									drive               BOOLEAN  DEFAULT (0),
									sit                 BOOLEAN  DEFAULT (0),
									chat                BOOLEAN  DEFAULT (0),
									eat                 BOOLEAN  DEFAULT (0),
									shopping            BOOLEAN  DEFAULT (0),
									run                 BOOLEAN  DEFAULT (0),
									exercise            BOOLEAN  DEFAULT (0),
									not_useful          BOOLEAN  DEFAULT (0) 
								); """

		# Checkbutton width for different Operating System
		if platform.system() == 'Linux':
			self.cb_width = 120 # Checkbutton width
			self.image_width = 260
		elif platform.system() == 'Darwin': # OSX
			self.cb_width = 280
			self.image_width = 245
		elif platform.system() == 'Windows':
			self.cb_width = 300
			self.image_width = 260
		else:
			self.cb_width = 300 # Default checkbutton width
			self.image_width = 260

		self.cb_ls = []  # checkbox list: [(<Tkinter.Checkbutton instance>,<Tkinter.IntVar instance>),......]
		self.cb_data_ls = []  # checkbox data list: [(<Tkinter.Checkbutton instance>,1),......]
		self.file_ls = []  # image list: [(<Tkinter.Checkbutton instance>,<Tkinter.IntVar instance>),......]
		self.file_chosen_ls = []  # image data list: [<Tkinter.Checkbutton instance>,......]
		self.datetime_ls = []
		self.lbl_ls = ['person','home','playground','void_deck','park','public_space','supermarket','market','food_court','shop','mall','hospital','clinic','community_center','senior','religious','transaction_ser','fitness','bus_stop','mrt','walkway','pedestrian_crossing','cycling_path','street_lights','traffic_lights','street_signs','trees','furniture','stairs','ramps','walk','cycle','bus','train','car','drive','sit','chat','eat','shopping','run','exercise','not_useful']
		self.lbl_dict = {"Person": "person",
		                 "Home": "home",
		                 "Playground/Fitness corner (outdoor)": "playground",
		                 "Void deck": "void_deck",
		                 "Park": "park",
		                 "Open public space": "public_space",
		                 "Supermarket": "supermarket",
		                 "Dry/wet market": "market",
		                 "Restaurant/Food court/Coffee shop/Hawker center": "food_court",
		                 "Shop": "shop",
		                 "Mall/Shopping center": "mall",
		                 "Hospital": "hospital",
		                 "Polyclinic/Pharmacy": "clinic",
		                 "Community center/club": "community_center",
		                 "Senior activity/Daycare center": "senior",
		                 "Religious venue": "religious",
		                 "Transaction services (e.g. bank, post office)": "transaction_ser",
		                 "Indoor fitness facility (e.g. sports hall, gym, swimming pool)": "fitness",
		                 "Bus Stop/Interchange": "bus_stop",
		                 "MRT/LRT station": "mrt",
		                 "Covered walkway": "walkway",
		                 "Pedestrian crossing": "pedestrian_crossing",
		                 "Cycling path (seperated from footpath)": "cycling_path",
		                 "Street lights": "street_lights",
		                 "Traffic lights": "traffic_lights",
		                 "Street signs": "street_signs",
		                 "Trees/Grass": "trees",
		                 "Public furniture (e.g. benches, tables)": "furniture",
		                 "Stairs and level changes": "stairs",
		                 "Ramps": "ramps",
		                 "Walking": "walk",
		                 "Cycling": "cycle",
		                 "On a bus": "bus",
		                 "On a train": "train",
		                 "On a car (as a passenger)": "car",
		                 "Driving a car/vehicle": "drive",
		                 "Sitting": "sit",
		                 "Chatting": "chat",
		                 "Eating": "eat",
		                 "Shopping": "shopping",
		                 "Running": "run",
		                 "Other exercising activity": "exercise",
		                 "Not Useful": "not_useful"}

		self.title("Photo Labelling Software")
		# self.attributes('-fullscreen', True)
		self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
		self.geometry("%dx%d+0+0" % (self.w, self.h))
		self.grid_rowconfigure(2, weight = 1)
		self.grid_columnconfigure(0, weight = 1)
		
		# top_frame
		self.top_frame = Tk.Frame(self.master)
		self.top_frame.grid(row = 0, column = 0, columnspan=3, sticky="NW")
		# image frame
		self.image_frame = Tk.Frame(self.master)
		self.image_frame.grid(row = 1, column = 0, columnspan=3, rowspan=5, sticky="NSEW")
		# right_frame
		self.right_frame = Tk.Frame(self.master)
		self.right_frame.grid(row = 0, column = 3, rowspan=5, sticky="NSEW")

		self.canvas = Tk.Canvas(self.image_frame)
		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
		self.frame_in2 = Tk.Frame(self.canvas,width=self.image_frame.winfo_width(),height=self.image_frame.winfo_height())
		self.my_scrollbar = Tk.Scrollbar(self.image_frame, orient = "vertical", command = self.canvas.yview)
		self.canvas.configure(yscrollcommand = self.my_scrollbar.set)
		self.my_scrollbar.pack(side = "right", fill = "y")

		self.scroll_horizontal = Tk.Scrollbar(self.image_frame, orient="horizontal", command = self.canvas.xview)
		self.canvas.configure(xscrollcommand = self.scroll_horizontal.set)
		self.scroll_horizontal.pack(side = "bottom", fill ="x")
		self.canvas.pack(side="left")
		self.canvas.create_window((0, 0), window = self.frame_in2, anchor = 'nw')

		self.frame_in2.bind("<Configure>", self.my_canvas) 

		self.path_label = Tk.Label(self.top_frame, text = "Path  :   ").grid(row = 0, column = 0)
		self.entry = Tk.Entry(self.top_frame, textvariable = self.path, width = 30).grid(row = 0, column = 1)

		self.b1 = Tk.Button(self.top_frame, text = "Select", bg = "light gray", command = self.open_photo).grid(row = 0,column = 2, padx=2)
		self.b2 = Tk.Button(self.top_frame, text = "Update", bg = "SpringGreen2", command = self.update).grid(row = 0,column = 3, padx=2)
		self.b3 = Tk.Button(self.top_frame, text = "Show Labels", bg = "light gray", command = self.show_lbl).grid(row = 0, column = 4, padx=2)
		self.b4 = Tk.Button(self.top_frame, text = "Clear Checks", bg = "light gray", command = self.clear_check).grid(row = 0,column = 5, padx=2)
		self.b5 = Tk.Button(self.top_frame, text = "Clear Attribute", bg = "light gray", command = self.clear_atribute).grid(row = 0, column = 6, padx=2)
		self.b6 = Tk.Button(self.top_frame, text = "Export CSV", bg = "SpringGreen2", command = self.export_csv).grid(row = 0, column = 7, padx=2)

		self.var_msg = Tk.StringVar()
		self.msg_lbl = Tk.Label(self.top_frame, textvariable=self.var_msg, font=("Helvetica", 12)).grid(row = 1, column = 0, columnspan = 10)

		self.tag_labels = ttk.Notebook(self.right_frame)
		self.tag_labels.grid(sticky = "NSE")
		self.gen_tag_labels()

		self.image_frame.update()
		width = self.image_frame.winfo_width()
		print ("image_frame width = " + str(width))
		print ("System: %s"%platform.system())
		# print (self.cb_data_ls)

	def gen_tag_labels(self):
		general_tab = ttk.Frame(self.tag_labels)
		location_tab = ttk.Frame(self.tag_labels)
		activity_tab = ttk.Frame(self.tag_labels)
		others_tab = ttk.Frame(self.tag_labels)

		self.tag_labels.add(general_tab, text = "General")
		self.tag_labels.add(location_tab, text = "Location")
		self.tag_labels.add(activity_tab, text = "Activity")
		self.tag_labels.add(others_tab, text = "Others")

		# General Tab
		var = Tk.IntVar()
		person = Tk.Checkbutton(general_tab, text = "Person", variable = var)
		self.cb_ls.append((person, var))

		# Location Tab
		var = Tk.IntVar()
		home = Tk.Checkbutton(location_tab, text = "Home", variable = var)
		self.cb_ls.append((home, var))
		var = Tk.IntVar()
		playground = Tk.Checkbutton(location_tab, text = "Playground/Fitness corner (outdoor)", variable = var)
		self.cb_ls.append((playground, var))
		var = Tk.IntVar()
		voiddeck = Tk.Checkbutton(location_tab, text = "Void deck", variable = var)
		self.cb_ls.append((voiddeck, var))
		var = Tk.IntVar()
		park = Tk.Checkbutton(location_tab, text = "Park", variable = var)
		self.cb_ls.append((park, var))
		var = Tk.IntVar()
		publicspace = Tk.Checkbutton(location_tab, text = "Open public space", variable = var)
		self.cb_ls.append((publicspace, var))
		var = Tk.IntVar()
		supermarket = Tk.Checkbutton(location_tab, text = "Supermarket", variable = var)
		self.cb_ls.append((supermarket, var))
		var = Tk.IntVar()
		market = Tk.Checkbutton(location_tab, text = "Dry/wet market", variable = var)
		self.cb_ls.append((market, var))
		var = Tk.IntVar()
		foodplace = Tk.Checkbutton(location_tab, text = "Restaurant/Food court/Coffee shop/Hawker center",
		                           variable = var)
		self.cb_ls.append((foodplace, var))
		var = Tk.IntVar()
		shop = Tk.Checkbutton(location_tab, text = "Shop", variable = var)
		self.cb_ls.append((shop, var))
		var = Tk.IntVar()
		mall = Tk.Checkbutton(location_tab, text = "Mall/Shopping center", variable = var)
		self.cb_ls.append((mall, var))
		var = Tk.IntVar()
		hospital = Tk.Checkbutton(location_tab, text = "Hospital", variable = var)
		self.cb_ls.append((hospital, var))
		var = Tk.IntVar()
		clinic = Tk.Checkbutton(location_tab, text = "Polyclinic/Pharmacy", variable = var)
		self.cb_ls.append((clinic, var))
		var = Tk.IntVar()
		community = Tk.Checkbutton(location_tab, text = "Community center/club", variable = var)
		self.cb_ls.append((community, var))
		var = Tk.IntVar()
		seniorcenter = Tk.Checkbutton(location_tab, text = "Senior activity/Daycare center", variable = var)
		self.cb_ls.append((seniorcenter, var))
		var = Tk.IntVar()
		religion = Tk.Checkbutton(location_tab, text = "Religious venue", variable = var)
		self.cb_ls.append((religion, var))
		var = Tk.IntVar()
		services = Tk.Checkbutton(location_tab, text = "Transaction services (e.g. bank, post office)", variable = var)
		self.cb_ls.append((services, var))
		var = Tk.IntVar()
		indoors = Tk.Checkbutton(location_tab, text = "Indoor fitness facility (e.g. sports hall, gym, swimming pool)", variable = var)
		self.cb_ls.append((hospital, var))
		var = Tk.IntVar()
		bus_stop = Tk.Checkbutton(location_tab, text = "Bus Stop/Interchange", variable = var)
		self.cb_ls.append((bus_stop, var))
		var = Tk.IntVar()
		train_station = Tk.Checkbutton(location_tab, text = "MRT/LRT station", variable = var)
		self.cb_ls.append((train_station, var))
		var = Tk.IntVar()
		road = Tk.Checkbutton(location_tab, text = "Covered walkway", variable = var)
		self.cb_ls.append((road, var))
		var = Tk.IntVar()
		crossroad = Tk.Checkbutton(location_tab, text = "Pedestrian crossing", variable = var)
		self.cb_ls.append((crossroad, var))
		var = Tk.IntVar()
		cyclepath = Tk.Checkbutton(location_tab, text = "Cycling path (seperated from footpath)", variable = var)
		self.cb_ls.append((cyclepath, var))
		var = Tk.IntVar()
		streetlight = Tk.Checkbutton(location_tab, text = "Street lights", variable = var)
		self.cb_ls.append((streetlight, var))
		var = Tk.IntVar()
		trafficlight = Tk.Checkbutton(location_tab, text = "Traffic lights", variable = var)
		self.cb_ls.append((trafficlight, var))
		var = Tk.IntVar()
		streetsign = Tk.Checkbutton(location_tab, text = "Street signs", variable = var)
		self.cb_ls.append((streetsign, var))
		var = Tk.IntVar()
		trees = Tk.Checkbutton(location_tab, text = "Trees/Grass", variable = var)
		self.cb_ls.append((trees, var))
		var = Tk.IntVar()
		publicgoods = Tk.Checkbutton(location_tab, text = "Public furniture (e.g. benches, tables)", variable = var)
		self.cb_ls.append((publicgoods, var))
		var = Tk.IntVar()
		stairs = Tk.Checkbutton(location_tab, text = "Stairs and level changes", variable = var)
		self.cb_ls.append((stairs, var))
		var = Tk.IntVar()
		ramps = Tk.Checkbutton(location_tab, text = "Ramps", variable = var)
		self.cb_ls.append((ramps, var))

		# Activity Tab
		var = Tk.IntVar()
		walk = Tk.Checkbutton(activity_tab, text = "Walking", variable = var)
		self.cb_ls.append((walk, var))
		var = Tk.IntVar()
		cycle = Tk.Checkbutton(activity_tab, text = "Cycling", variable = var)
		self.cb_ls.append((cycle, var))
		var = Tk.IntVar()
		on_bus = Tk.Checkbutton(activity_tab, text = "On a bus", variable = var)
		self.cb_ls.append((on_bus, var))
		var = Tk.IntVar()
		on_train = Tk.Checkbutton(activity_tab, text = "On a train", variable = var)
		self.cb_ls.append((on_train, var))
		var = Tk.IntVar()
		on_car = Tk.Checkbutton(activity_tab, text = "On a car (as a passenger)", variable = var)
		self.cb_ls.append((on_car, var))
		var = Tk.IntVar()
		drive = Tk.Checkbutton(activity_tab, text = "Driving a car/vehicle", variable = var)
		self.cb_ls.append((drive, var))
		var = Tk.IntVar()
		sit = Tk.Checkbutton(activity_tab, text = "Sitting", variable = var)
		self.cb_ls.append((sit, var))
		var = Tk.IntVar()
		talk = Tk.Checkbutton(activity_tab, text = "Chatting", variable = var)
		self.cb_ls.append((talk, var))
		var = Tk.IntVar()
		eat = Tk.Checkbutton(activity_tab, text = "Eating", variable = var)
		self.cb_ls.append((eat, var))
		var = Tk.IntVar()
		shop = Tk.Checkbutton(activity_tab, text = "Shopping", variable = var)
		self.cb_ls.append((shop, var))
		var = Tk.IntVar()
		run = Tk.Checkbutton(activity_tab, text = "Running", variable = var)
		self.cb_ls.append((run, var))
		var = Tk.IntVar()
		others = Tk.Checkbutton(activity_tab, text = "Other exercising activity", variable = var)
		self.cb_ls.append((others, var))

		# Others_tab
		var = Tk.IntVar()
		useless = Tk.Checkbutton(others_tab, text = "Not Useful", variable = var)
		self.cb_ls.append((useless, var))

		for cb in self.cb_ls:
			cb[0].grid(sticky = "w")

	def my_canvas(self, event):
		self.canvas.configure(scrollregion = self.canvas.bbox("all"), width = self.frame_in2.winfo_width(), height=self.frame_in2.winfo_height())

	def open_photo(self):
		self.backup_path = self.path.get()
		path_ = tkFileDialog.askdirectory()
		self.var_msg.set("Importing images... This may take awhile =) ")
		self.path.set(path_)
		print("folder path: %s"%self.path.get())
		# handle error when user click 'cancel' button on the import image window
		if self.path.get() == '':
			self.var_msg.set("Please select an image folder.")
			print("Please select an image folder.")
			self.path.set(self.backup_path)
		else:
			self.file_ls = []  # image list: [(<Tkinter.Checkbutton instance>,<Tkinter.IntVar instance>),......]
			self.file_chosen_ls = []  # image data list: [<Tkinter.Checkbutton instance>,......]
			self.datetime_ls = []
			self.image = []
			self.photo = []
			# delete photos on GUI
			self.frame_in2.destroy()
			self.frame_in2 = Tk.Frame(self.canvas)
			# self.canvas.create_window((0, 0), window = self.frame_in2, anchor="center", height="25c", width="15c")
			# self.frame_in2.grid()
			self.canvas.create_window((0, 0), window = self.frame_in2, anchor = 'nw') 
			self.frame_in2.bind("<Configure>", self.my_canvas) 
			
			# Handle No. of rows of photos based on image frame width
			no_row = self.get_row()

			col = 0
			row = 0

			for file_name in os.listdir(self.path.get()):
				global image, photo
				if file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
					self.image.insert(0, Image.open(os.path.join(self.path.get(), file_name)).resize((self.image_width, int(self.image_width*0.75))))
					self.photo.insert(0, ImageTk.PhotoImage(self.image[0]))
					var = Tk.IntVar()
					c1 = Tk.Checkbutton(self.frame_in2, text = file_name, image = self.photo[0], variable = var, onvalue = 1, offvalue = 0, width = self.cb_width)
					c1.grid(row = row, column = col)
					# c1.pack()
					col += 1
					if col >= no_row:
						row += 1
						col = 0
					self.file_ls.append((c1, var))

			# handle no image folder
			if len(self.file_ls) == 0:
				self.var_msg.set("No jpg or jpeg file in %s."%self.path.get())
			else:
				self.var_msg.set("Imported " + str(len(self.file_ls)) + " images successfully from " + str(self.path.get()) + ".")
				self.db_name = self.getDbName(self.path.get())
				# Create directory if it is not exist
				if os.path.isdir("../database/data_" + self.db_name) == False:
					os.mkdir("../database/data_" + self.db_name, 0755)
					print "Path is created"

				self.db_link = "../database/data_" + self.db_name + "/" + self.db_name + '.db'
				with sqlite3.connect(self.db_link) as db:
					cur = db.cursor()
					# Create table if it is a new database
					if db is not None:
						self.create_table(db, self.sql_create_table) # only execute this line when db is a new database
						print ("Created a new database: %s" %self.db_name + '.db')
						self.var_msg.set("Created a new database: %s" %self.db_name + '.db')
					else:
						print("Error! cannot create the database connection.")
					
					for x in self.file_ls:
						f = x[0]
						name = f.cget("text")
						cur.execute("SELECT id FROM attributes WHERE file = (?)", (name,))
						row = cur.fetchall()
						# If picture is already recorded in database
						if len(row) != 0:
							f.configure(bg = "tomato")

	def update(self):
		self.update_file_chosen_ls()
		self.update_cb_data_ls()

		if len(self.file_chosen_ls) < 1:
			self.var_msg.set("Please choose at least one image")

		else:
			# update data to database
			try:  # if file not exist in database, add new row
				self.run_query("INSERT INTO attributes(file,date) VALUES (?,?)",
							(self.file_chosen_ls[0].cget("text"), self.datetime_ls[0]))
			except:  # if file exist in database, update it to all 0 first
				self.run_query(
					"UPDATE attributes SET person=0,home=0,playground=0,void_deck=0,park=0,public_space=0,supermarket=0,market=0,food_court=0,shop=0,mall=0,hospital=0,clinic=0,community_center=0,senior=0,religious=0,transaction_ser=0,fitness=0,bus_stop=0,mrt=0,walkway=0,pedestrian_crossing=0,cycling_path=0,street_lights=0,traffic_lights=0,street_signs=0,trees=0,furniture=0,stairs=0,ramps=0,walk=0,cycle=0,bus=0,train=0,car=0,drive=0,sit=0,chat=0,eat=0,shop=0,run=0,exercise=0,not_useful=0 WHERE file = (?)",
					(self.file_chosen_ls[0].cget("text"),))

			self.insert_row_data(self.cb_data_ls, 0)

			# Run if more than 1 picture being chosen
			if len(self.file_chosen_ls) >= 2:
				for j in range(1, len(self.file_chosen_ls)):
					try:  # if file not exist in database, add new row
						self.run_query("INSERT INTO attributes(file,date) VALUES (?,?)",
									(self.file_chosen_ls[j].cget("text"), self.datetime_ls[j]))
					except:  # if file exist in database, update it to all 0 first
						self.run_query(
							"UPDATE attributes SET person=0,home=0,playground=0,void_deck=0,park=0,public_space=0,supermarket=0,market=0,food_court=0,shop=0,mall=0,hospital=0,clinic=0,community_center=0,senior=0,religious=0,transaction_ser=0,fitness=0,bus_stop=0,mrt=0,walkway=0,pedestrian_crossing=0,cycling_path=0,street_lights=0,traffic_lights=0,street_signs=0,trees=0,furniture=0,stairs=0,ramps=0,walk=0,cycle=0,bus=0,train=0,car=0,drive=0,sit=0,chat=0,eat=0,shop=0,run=0,exercise=0,not_useful=0 WHERE file = (?)",
							(self.file_chosen_ls[j].cget("text"),))

					self.insert_row_data(self.cb_data_ls, j)

			# show feedback message
			msg = str(len(self.file_chosen_ls)) + " Images was labelled with "
			checked = False # A boolean represents if any label is checked
			for data in self.cb_data_ls:
				label = self.lbl_dict[data[0].cget("text")]
				k = data[1]  # k is a boolean
				if checked == False:
					if k == 1:
						msg = msg + label + ", "
						checked = True
				elif k == 1:
					msg = msg + label + ", "
			msg = msg[0:-2] + "."
			if checked == False:
				self.var_msg.set("Please choose at least one attribute")

			else:
				self.var_msg.set(msg)
				# add red color to image
				for x in self.file_ls:
					f = x[0]
					var = x[1]
					if var.get() == 1:
						f.configure(bg = "tomato")

				# clear img checks
				for x in self.file_ls:
					f = x[0]
					var = x[1]
					if var.get() == 1:
						var.set(0)

	def update_file_chosen_ls(self):
		# Take file_ls input and insert into file_chosen_ls
		self.file_chosen_ls = []
		self.datetime_ls = []
		for x in self.file_ls:
			f = x[0]
			var = x[1]
			if var.get() == 1:
				self.file_chosen_ls.append(f)
				self.datetime_ls.append(self.get_datetime(f))
		#print (self.file_chosen_ls)
		# print (self.datetime_ls)

	def update_cb_data_ls(self):
		# Take cb_data input and insert into cb_data_ls
		self.cb_data_ls = []
		for y in self.cb_ls:
			cb = y[0]
			var = y[1]
			if var.get() == 1:
				self.cb_data_ls.append((cb, 1))
			else:
				self.cb_data_ls.append((cb, 0))
		# print (self.cb_ls)
		# print (self.cb_data_ls)

	def insert_row_data(self, ls, n):
		# get data from data_ls and insert into SQL table
		for data in ls:
			label = self.lbl_dict[data[0].cget("text")]
			k = data[1]  # k is a boolean
			if k == 1:
				db = sqlite3.connect(self.db_link)
				cur = db.cursor()
				query_result = cur.execute("UPDATE attributes SET " + label + " = (?) WHERE file = (?)",
				                           (1, self.file_chosen_ls[n].cget("text"),))
				db.commit()

	def run_query(self, query, parameters = ()):
		with sqlite3.connect(self.db_link) as db:
			cur = db.cursor()
			query_result = cur.execute(query, parameters)
			db.commit()
		return query_result

	def show_lbl(self):
		# show label on GUI based on database
		self.update_file_chosen_ls()
		if len(self.file_chosen_ls) == 0:
			self.var_msg.set("No image is checked")
		elif len(self.file_chosen_ls) != 1:
			self.var_msg.set("Please only check 1 image to show labels")
		else:
			img = self.file_chosen_ls[0]
			name = img.cget("text")

			with sqlite3.connect(self.db_link) as db:
				cur = db.cursor()
				cur.execute("SELECT * FROM attributes WHERE file = (?)", (name,))
			row = cur.fetchall()
			if len(row) == 0:
				self.var_msg.set("Can't find "+ str(name) + " in database.")
			else:
				row = row[0][3:]
				msg = str(name) + ": "
				for i in range(len(row)):
					if row[i] == 1:
						msg = msg + str(self.lbl_ls[i]) + ', '
				msg = msg[0:-2] + "."
				self.var_msg.set(msg)

	def get_datetime(self, f):
		name = f.cget("text")  # 20000101_030548_000.jpg  -->  YYYY-MM-DD HH:MI:SS
		try:
			datetime = name[0:4] + "-" + name[4:6] + "-" + name[6:8] + " " + name[9:11] + ":" + name[11:13] + ":" + name[13:15]
		except:
			datetime = None
		return datetime

	def clear_atribute(self):
		for x in self.cb_ls:
			var = x[1]
			var.set(0)

	def clear_check(self):
		for y in self.file_ls:
			var = y[1]
			var.set(0)
		
	def get_row(self):
		# return No. of rows based on image frame width
		self.image_frame.update()
		width = self.image_frame.winfo_width()
		if width < 1350:
			no_row = 3
		else:
			no_row = 4

		return no_row

	def _on_mousewheel(self, event):
		self.canvas.yview_scroll(-1*(event.delta/120), "units")

	def export_csv(self):
		# reading the database generated by the labelling software
		db = sqlite3.connect(self.db_link)
		cursor = db.cursor()
		data = cursor.execute("SELECT * FROM attributes")  # select the values under attributes
		rows = cursor.fetchall()

		# save the database as a csv file for further application
		# Create directory if it is not exist
		if os.path.isdir("../database/data_" + self.db_name) == False:
			print("No directory called '../database/data_{0}' was found".format(self.db_name))
			self.var_msg.set("No directory called '../database/data_{0}' was found, cannot export csv.".format(self.db_name))
		with open('../database/data_{0}/{0}.csv'.format(self.db_name), 'w') as csv_file:
			writer = csv.writer(csv_file, delimiter = ',')
			writer.writerow(['participant_id','id','file','date','person','home','playground','void_deck','park','public_space','supermarket','market','food_court','shop','mall','hospital','clinic','community_center','senior','religious','transaction_ser','fitness','bus_stop','mrt','walkway','pedestrian_crossing','cycling_path','street_lights','traffic_lights','street_signs','trees','furniture','stairs','ramps','walk','cycle','bus','train','car','drive','sit','chat','eat','shopping','run','exercise','not_useful'])
			writer.writerows(rows)
		print ("Export to '../database/data_"+ self.db_name + "/" + self.db_name + ".csv' file successfully.")
		self.var_msg.set("Export to '../database/data_"+ self.db_name + "/" + self.db_name + ".csv' file successfully.")

	def create_table(self, db, create_table_sql):
		""" create a table from the create_table_sql statement
		:param conn: Connection object
		:param create_table_sql: a CREATE TABLE statement
		:return:
		"""
		try:
			cur = db.cursor()
			cur.execute(create_table_sql)
		except Error as e:
			print(e)

	def getDbName(self, path):
		index = path.rfind('/')
		return path[index+1:]

root = MainApplication()
root.mainloop()
