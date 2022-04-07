
try:
    import brukeropusreader as opus
except ImportError:
    print(f"Install brukeropusreader to read OPUS raw files")

import os as os
from typing import Type
import pandas as pd
import numpy as np


class IR_Reader():

    def __init__(self,*args,**kwargs):

        # self.directory = str(input("Enter the wavenumber (to abort write 'END'):")=
        self.directory = kwargs.get('directory',r'place holder')
        
        # self.opus_data = opus.read_file(self.directory)
        


        try:
            self.opus_data = opus.read_file(self.directory)

        except: 
            raise ImportError("A directory was not given")

        
        ## meta data
        self.IR_Date = self.opus_data["ScRf Data Parameter"]["DAT"]
        self.IR_Detector = self.opus_data["Optik"]["DTC"]
        self.IR_intrument = self.opus_data["Instrument"]["INS"]
        self.IR_format = self.opus_data["Acquisition"]["PLF"]
        self.IR_expr_name = self.opus_data["Sample"]["SNM"]
        self.IR_expr_program = self.opus_data["Sample"]["SFM"]
        self.IR_aperture = self.opus_data["Optik"]["APT"]
        self.IR_number_of_scans = self.opus_data["Acquisition"]["NSS"]


        ## y-values
        self.X_data = self.opus_data.get_range('AB')
        self.Y_data = self.opus_data['AB'][0:len(self.X_data)]
        self.IR_data = []
        self.IR_data.append(self.X_data) 
        self.IR_data.append(self.Y_data)
        
        ## used to keep track of the data format of the x-values
        self.control_x_value = 0

    def __repr__(self):
        return "IR_Reader('{}')'".format(self.directory)

    def __str__(self):
        return '''  Directory:  {}  

                    Date:                   {} 
                    Experiment name:        {}  
                    Experiment progarm:     {}  
                    No. of scans:           {} 
                    Data format:            {} 
                    Detector:               {} 
                    Arpeture:               {}  
                    Intstrument:            {}'''.format(self.directory,self.IR_Date,self.IR_expr_name,self.IR_expr_program,self.IR_number_of_scans,self.IR_format,self.IR_Detector,self.IR_aperture,self.IR_intrument)



        
    def __len__(self):
        return len(self.Y_data)


    


    





#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

class DRIFTS(IR_Reader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.control_y_value = 'log reflectance'
        

        if self.IR_format != 'LRF':
            if self.IR_format != 'RFL':
                raise TypeError("Data is not in correct format. It needs to be in log reflectance (LRF) or reflectance (RFL) --- (DRIFTS mode)")

        #Defining the formate for control value        
        if self.IR_format == 'LRF': 
            self.control_y_value = 'log reflectance'
        if self.IR_format == 'RFL':   
            self.control_y_value = 'reflectance'

    def values(self):
        print('x-values: {}'.format(self.X_data))
        print('Y-values: {}'.format(self.Y_data))
        


    #Y_DATA change
    def to_R(self):
        if self.control_y_value == 'reflectance':
            #NO CONVERSION NEEDED         
            pass
        elif self.control_y_value == 'log recletcance':
            self.IR_data = DRIFTS.lgR_R(self.IR_data)

        elif self.control_y_value == 'Kubelka Munk':
                 self.IR_data = DRIFTS.KM_R(self.IR_data)

        self.control_y_value = 'reflectance'



    def to_lgR(self):
        if self.control_y_value == 'log recletcance':
            #NO CONVERSION NEEDED         
            pass
        elif self.control_y_value == 'Kubelka Munk':
            self.IR_data = DRIFTS.KM_R(self.IR_data)
            self.IR_data = DRIFTS.R_lgR(self.IR_data)

        elif self.control_y_value == 'recletcance':
            self.IR_data = DRIFTS.R_lgR(self.IR_data)
                 
        self.control_y_value = 'log recletcance'
        


    def to_KM(self):
        if self.control_y_value == 'Kubelka Munk':
            #NO CONVERSION NEEDED         
            pass
        elif self.control_y_value == 'log recletcance':
            self.IR_data = DRIFTS.lgR_R(self.IR_data)
            self.IR_data = DRIFTS.R_KM(self.IR_data)

        elif self.control_y_value == 'recletcance':
            self.IR_data = DRIFTS.R_KM(self.IR_data)
                 
        self.control_y_value = 'Kubelka Munk'




    @staticmethod
    def R_lgR(y):
        y_value = y[1]
        new_y_value = []
        i = 0

        for n in y_value:
            x = np.log(1/n)
            new_y_value.append(x)
            i += 1
        
        y[1] = np.array(new_y_value)
        return y

    @staticmethod
    def R_KM(y):
        y_value =y[1]
        new_y_value = []
        i = 0

        for n in y_value:
            x = (1-n)**2/(2*n)
            new_y_value.append(x)
            i += 1
        
        y[1] = np.array(new_y_value)
        return y
    
    @staticmethod
    def lgR_R(y):
        y_value = y[1]
        new_y_value = []
        i = 0

        for n in y_value:
            x = 1/(10**n)
            new_y_value.append(x)
            i += 1

        y[1] = np.array(new_y_value)
        return y


    @staticmethod
    def KM_R(y):
        y_value = y[1]
        new_y_value = []
        i = 0

        for n in y_value:
            x = 1 + n - np.sqrt(2*n+n**2)
            new_y_value.append(x)
            i += 1
        
        y[1] = np.array(new_y_value)   
        return y




    #X_DATA change
    def wave_number_to_micro_meter(self):

        if self.control_x_value != 0:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")

        x_value = self.IR_data[0]
        new_x_value = []
        i = 0
        for n in x_value:
            x = (1/n*10**7)/1000
            new_x_value.append(x)
            i += 1
        
        self.IR_data[0] = np.array(new_x_value)
        print(self.IR_data[0])

        print("""
        
        ----   x-axis converted to micro meter   ----
        
        """)

        self.control_x_value = 1   
    


    def micro_meter_to_wave_number(self):

        if self.control_x_value != 1:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")


        x_value = self.IR_data[0]
        new_x_value = []
        i = 0
        for n in x_value:
            x = (1000/n)/(10**7)
            new_x_value.append(x)
            i += 1
        
        self.IR_data[0] = np.array(new_x_value)
        print(self.IR_data[0])

        print("""
        
        ----   x-axis converted to wave number   ----
        """)

        self.control_x_value = 0



    #OTHER
    def plot(self):
        try:
            import matplotlib.pyplot as plt

            print("Plotting Stectra")
            plt.plot(self.IR_data[0],self.IR_data[-1])
            plt.show()

        except ImportError:
            print(f"Install matplotlib to plot spectra")



    def to_csv(self, outname=None):
        x = self.IR_data[0]
        y = self.IR_data[1]

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      



        def loop_func_2(): 
            inp = input("Enter the result file directory (.csv):") 
        
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp



        if not outname:
            self.file_name = loop_func_2()
            try:
                df.to_csv(self.file_name, header=None, index=False)
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')
        else:
            try:
                df.to_csv(outname, header=None, index=False)
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')




    def to_excel(self, outname=None):
        x = self.IR_data[0]
        y = self.IR_data[1]
        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      


        def loop_func_2(): 
            inp = input("Enter the result file directory (.xlsx):") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp



        if not outname:
            self.file_name = loop_func_2()
            try:
                df.to_excel(self.file_name, header=None, index=False)
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work') 
        else:
            try:
                df.to_excel(outname, sheet_name='Sheet1')
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')



    def data(self):
        return self.IR_data

    def help(self):
        print("""



        obj.to_csv()                                      Will save the data as a .CSV-file.

        obj.to_excel()                                    Will save the data as an .XLSX-file.

        obj.plot()                                        Will make a simplified plot for the data.

        obj.data()                                        Will return the values (x,y, = obj.data()) 


        obj.micro_meter_to_wave_number()                  Will change the x-axis format from micro meter to wave number.

        obj.wave_number_to_micro_meter()                  Will change the x-axis format from wave number to micro meter.
        

        obj.to_KM()                                       Will change the y-axis format to Kubelka Munk.

        obj.to_R()                                        Will change the y-axis format to reflectance.

        obj.to_lgR()                                     Will change the y-axis format to log-reflectance.
        
        """
        )








#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
class Transmission(IR_Reader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        if self.IR_format != 'AB':
            raise TypeError("Data is not in correct format. It needs to be in AB (Transmission or ATR)")

        self.control_y_value = 'absorbance'

    def values(self):
        print('x-values: {}'.format(self.X_data))
        print('Y-values: {}'.format(self.Y_data))



    #Y_DATA change
    def to_A(self):
        if self.control_y_value == 'absorbance':
            #NO CHANGE NEEDED
            pass

        elif self.control_y_value == 'transmission':
            self.IR_data = Transmission.T_A(self.IR_data)


        self.control_y_value = 'absorbance'


    def to_T(self):
        if self.control_y_value == 'transmission':
            #NO CHANGE NEEDED
            pass

        elif self.control_y_value == 'absorbance':
            self.IR_data = Transmission.A_T(self.IR_data)


        self.control_y_value = 'transmission'
        


 



    @staticmethod
    def T_A(y):
        y_value = y[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = np.log10(1/n)
            new_y_value.append(x)
            i += 1
        
        y[1] = np.array(new_y_value) 
        return y



    @staticmethod
    def A_T(y):
        y_value = y[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = 1/(10**n)
            new_y_value.append(x)
            i += 1
        
        y[1] = np.array(new_y_value)
        return y

 





    #X_DATA change
    def wave_number_to_micro_meter(self):

        if self.control_x_value != 0:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")

        x_value = self.IR_data[0]
        new_x_value = []
        i = 0
        for n in x_value:
            x = (1/n*10**7)/1000
            new_x_value.append(x)
            i += 1
        
        self.IR_data[0] = np.array(new_x_value)
        print(self.IR_data[0])

        print("""
        
        ----   x-axis converted to micro meter   ----
        
        """)

        self.control_x_value = 1   
    


    def micro_meter_to_wave_number(self):

        if self.control_x_value != 1:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")


        x_value = self.IR_data[0]
        new_x_value = []
        i = 0
        for n in x_value:
            x = (1000/n)/(10**7)
            new_x_value.append(x)
            i += 1
        
        self.IR_data[0] = np.array(new_x_value)
        print(self.IR_data[0])

        print("""
        
        ----   x-axis converted to wave number   ----
        
        """)

        self.control_x_value = 0



    #OTHER
    def plot(self):
        try:
            import matplotlib.pyplot as plt

            print("Plotting Sectra")
            plt.plot(self.IR_data[0],self.IR_data[-1])
            plt.show()

        except ImportError:
            print(f"Install matplotlib to plot spectra")



    def to_csv(self, outname=None):
        x = self.IR_data[0]
        y = self.IR_data[1]

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      


        def loop_func_2(): 
        
            inp = input("Enter the result file directory (.csv):") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
                            
        if not outname:
            self.file_name = loop_func_2()
            try:
                df.to_csv(self.file_name, header=None, index=False)
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')
        else:
            try:
                df.to_csv(outname, header=None, index=False)
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')




    def to_excel(self, outname=None):
        x = self.IR_data[0]
        y = self.IR_data[1]
        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      


        def loop_func_2(): 
        
            inp = input("Enter the result file directory (.xlsx):") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp

        if not outname:
            self.file_name = loop_func_2()
            try:
                df.to_excel(self.file_name, header=None, index=False)
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')
        else:
            try:
                df.to_excel(outname, sheet_name='Sheet1')
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')

        

    def data(self):
        return self.IR_data

    def help(self):
        print("""



        obj.to_csv()                                      Will save the data as a .CSV-file.

        obj.to_excel()                                    Will save the data as an .XLSX-file.

        obj.plot()                                        Will make a simplified plot for the data.

        obj.data()                                        Will return the values (x,y, = obj.data()) 


        obj.micro_meter_to_wave_number()                  Will change the x-axis format from micro meter to wave number.

        obj.wave_number_to_micro_meter()                  Will change the x-axis format from wave number to micro meter.
        


        obj.to_T()                                        Will change the y-axis format to transmission.

        obj.to_A()                                        Will change the y-axis format to absorption.
        
        """
        )



#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

class ATR(IR_Reader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        if self.IR_format != 'AB':
            raise TypeError("Data is not in correct format. It needs to be in AB (Transmission or ATR)")

        self.control_y_value = 'absorbance'

    def values(self):
        print('x-values: {}'.format(self.X_data))
        print('Y-values: {}'.format(self.Y_data))



    #Y_DATA change
    def to_A(self):
        if self.control_y_value == 'absorbance':
            #NO CHANGE NEEDED
            pass

        elif self.control_y_value == 'transmission':
            self.IR_data = Transmission.T_A(self.IR_data)


        self.control_y_value = 'absorbance'


    def to_T(self):
        if self.control_y_value == 'transmission':
            #NO CHANGE NEEDED
            pass

        elif self.control_y_value == 'absorbance':
            self.IR_data = Transmission.A_T(self.IR_data)


        self.control_y_value = 'transmission'
        






    @staticmethod
    def T_A(y):
        y_value = y[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = np.log10(1/n)
            new_y_value.append(x)
            i += 1
        
        y[1] = np.array(new_y_value) 
        return y



    @staticmethod
    def A_T(y):
        y_value = y[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = 1/(10**n)
            new_y_value.append(x)
            i += 1
        
        y[1] = np.array(new_y_value)
        return y

 


 

    #X_DATA change
    def wave_number_to_micro_meter(self):

        if self.control_x_value != 0:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")

        x_value = self.IR_data[0]
        new_x_value = []
        i = 0
        for n in x_value:
            x = (1/n*10**7)/1000
            new_x_value.append(x)
            i += 1
        
        self.IR_data[0] = np.array(new_x_value)
        print(self.IR_data[0])

        print("""
        
        ----   x-axis converted to micro meter   ----
        
        """)

        self.control_x_value = 1   
    



    def micro_meter_to_wave_number(self):

        if self.control_x_value != 1:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")


        x_value = self.IR_data[0]
        new_x_value = []
        i = 0
        for n in x_value:
            x = (1000/n)/(10**7)
            new_x_value.append(x)
            i += 1
        
        self.IR_data[0] = np.array(new_x_value)
        print(self.IR_data[0])

        print("""

        ----   x-axis converted to wave number   ----

        """)

        self.control_x_value = 0



    #OTHER
    def plot(self):
        try:
            import matplotlib.pyplot as plt

            print("Plotting AB")
            plt.plot(self.IR_data[0],self.IR_data[-1])
            plt.show()

        except ImportError:
            print(f"Install matplotlib to plot spectra")


    

    def to_csv(self, outname=None):
        x = self.IR_data[0]
        y = self.IR_data[1]

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      


        def loop_func_2(): 
        
            inp = input("Enter the result file directory (.csv):") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
                            
        if not outname:
            self.file_name = loop_func_2()
            try:
                df.to_csv(self.file_name, header=None, index=False)
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')
        else:
            try:
                df.to_csv(outname, header=None, index=False)
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')




    def to_excel(self, outname=None):
        x = self.IR_data[0]
        y = self.IR_data[1]
        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      


        def loop_func_2(): 
        
            inp = input("Enter the result file directory (.xlsx):") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp

        if not outname:
            self.file_name = loop_func_2()
            try:
                df.to_excel(self.file_name, header=None, index=False)
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')
        else:
            try:
                df.to_excel(outname, sheet_name='Sheet1')
            except:
                raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')


    def data(self):
        return self.IR_data


    def help(self):
        print("""



        obj.to_csv()                                      Will save the data as a .CSV-file.

        obj.to_excel()                                    Will save the data as an .XLSX-file.

        obj.plot()                                        Will make a simplified plot for the data.

        obj.data()                                        Will return the values (x,y, = obj.data()) 


        obj.micro_meter_to_wave_number()                  Will change the x-axis format from micro meter to wave number.

        obj.wave_number_to_micro_meter()                  Will change the x-axis format from wave number to micro meter.
        

        obj.to_KM()                                       Will change the y-axis format to Kubelka Munk.

        obj.to_R()                                        Will change the y-axis format to reflectance.

        obj.to_lgR()                                     Will change the y-axis format to log-reflectance.
        
        """
        )









