import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Vayyar():
    # Class that gets the filename, xmin, xmax, ymin, ymax of the wanted location

    def __init__(self, filename, x_min, x_max, y_min, y_max):
        self.filename = filename
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    # This function organizes the file data inside pandas dataframe based on the wanted location inputs
    def dataframe(self):
        file = pd.read_csv(self.filename, sep="\t", header=None)
        # Dataframe columns:
        # Process_frame - contains frame number
        # FPS = contains average of last 1 frame per second
        # X_num - contains the X coordinates from the log file, same for y and Z
        # No_t_id - contains the frame without target (target = 0)
        Process_frame = np.array([])
        FPS = []
        FPS_No_t_id = []
        Process_Frame_No_t_id = np.array([])
        X_num = []
        Y_num = []
        Z_num = []
        data = file[0]
        for line in range(len(data) - 3):  # -3 because of comparison to 3 rows after process frame line
            if ("interrupt" in data[line]) & (
                    "t_id" in data[line + 3]):  # if I have the x,y,z coordinates of the target
                # Split is splitting according to spaces
                # Need to know if there are suspicoius places - if so, add try & catch
                Process_frame = np.append(Process_frame, [int(s) for s in data[line].split() if
                                                          s.isdigit()])  # add current process frame to dataframe
                FPS.append(data[line + 1].split()[-1])  # Add current average FPS to dataframe
                X_num.append(data[line + 3].split()[1])  # Add current X coordinate to dataframe
                Y_num.append(data[line + 3].split()[2])  # Add current Y coordinate to dataframe
                Z_num.append(data[line + 3].split()[3])  # Add current Z coordinate to dataframe
            elif ("interrupt" in data[line]) & (
                    "t_id" not in data[line + 3]):  # If I don't have the x,y,z coordinates of the target
                FPS_No_t_id.append(data[line + 1].split()[-1])  # add current FPS without target
                np.append(Process_Frame_No_t_id,
                          [int(s) for s in data[line].split() if s.isdigit()])  # add current frame without target

        df = pd.DataFrame(list(zip(Process_frame.astype(int), FPS, X_num, Y_num, Z_num)),
                          columns=['Process_frame', 'FPS', 'X_num', 'Y_num',
                                   'Z_num'])  # Create dataframe with relevant columns
        df['FPS'] = df['FPS'].str[4:].astype(
            float)  # Frame per second, 4 is to remove "FPS=" (could use different methods, depends on definition)
        df['X_num'] = df['X_num'].str[2:].astype(float)  # x coordinate, 2 is to remove "x="
        df['Y_num'] = df['Y_num'].str[2:].astype(float)
        df['Z_num'] = df['Z_num'].str[2:].astype(float)
        # Below -> find when target location is on wanted location
        target_df = df[(df['X_num'] <= self.x_max) & (df['X_num'] >= self.x_min) & (df['Y_num'] <= self.y_max) & (
                df['Y_num'] >= self.y_min)]
        self.df = df
        self.target_df = target_df

    def time_on_target(self): # This function calcaulates and prints the time the target spent on the given location
        time_on_target = len(self.target_df) / self.target_df['FPS'].mean()
        print(time_on_target, 'Seconds')

    def visualize(self): # This function presents a plot of the X,Y coordinates based on frame, and marks the frames with the target on the given location
        plt.plot(self.df['Process_frame'], self.df['X_num'], label="All frames_X")
        plt.plot(self.df['Process_frame'], self.df['Y_num'], label="All frames_Y")
        plt.plot(self.target_df['Process_frame'], self.target_df['X_num'], 'go')
        plt.plot(self.target_df['Process_frame'], self.target_df['Y_num'], 'go', label="Target frames")
        plt.legend(loc="upper left")
        plt.xlabel("Frame number")
        plt.ylabel("X and Y coordinates")
        plt.title('X,Y coordinates vs frame number')
        plt.show()


data = Vayyar("tracker_log.log", -0.5, 0, 1.8, 2.4)  # filename and chair coordinates
data.dataframe()
data.time_on_target()
data.visualize()
