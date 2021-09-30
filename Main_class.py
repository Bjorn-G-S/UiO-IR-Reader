
try:
    from brukeropusreader import read_file
except ImportError:
    print(f"Install brukeropusreader to read OPUS raw files")

import os as os
from typing import Type
import pandas as pd
import numpy as np


class IR_Reader():

    def __init__(self,*args,**kwargs):

        self.directory = kwargs.get('directory', False)



        try:
            self.opus_data = read_file(self.directory)

        except: 
            raise ImportError("A directory was not given")


        ## meta data
        self.IR_Date = self.opus_data["ScRf Data Parameter"]["DAT"]
        self.IR_Detector = self.opus_data["Optik"]["DTC"]
        self.IR_intrument = self.opus_data["Instrument"]["INS"]
        self.IR_format = self.opus_data["Acquisition"["PLF"]]
        self.IR_expr_name = self.opus_data["Sample"]["SNM"]
        self.IR_expr_program = self.opus_data["Sample"]["SFM"]
        self.IR_aperture = self.opus_data["Optik"]["APT"]
        self.IR_number_of_scans = self.opus_data["Acquisition"]["NSS"]


        ## y-values
        self.AB_data = self.opus_data.get_range('AB')

        self.IR_data = (self.opus_data.get_rage('0'), self.opus_data['AB'][0:len[self.AB_data]])

        ## used to keep track of the data format of the x-values
        self.control_x_value = 0

    def __repr__(self):
        return "IR_Reader('{}')'".format(self.directory)

    def __str__(self):
        return 'Directory: {} - Date: {} - Experiment name: {} - Experiment progarm: {} - No. of scans: {} - Data format: {} - Detector: {} - Arpeture: {} - Intstrument: {}'.format(self.directory,self.IR_Date,self.IR_expr_name,self.IR_expr_program,self.IR_number_of_scans,self.IR_format,self.IR_Detector,self.IR_format,self.IR_intrument)

    def __len__(self):
        return '{}'.format(len(self.opus_data['AB'][0:len[self.AB_data]]))


    def help():
        print(""""
        
        
        
        
        
        
        """
        )


    





#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

class DRIFTS(IR_Reader):

    def __init__(self, *args, **kwargs):
        super(self).__init__(self,*args, **kwargs)


    
    if self.IR_format != 'LRF':
        raise TypeError("Data is not in correct format")
        

    self.control_y_value = 'recletcance'



    def R_to_logR(self):

        if self.control_y_value != 'recletcance':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)

        y_value = self.IR_data[1]
        new_y_value = np.log(1/y_value)
        self.IR_data[1] = new_y_value
        print("Data converted from reflectace to log reflectance")

        self.control_y_value = 'log reflectance'
    


    def logR_to_R(self):

        if self.control_y_value != 'log recletcance':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)

        y_value = self.IR_data[1]
        new_y_value = 1/(10**y_value)
        self.IR_data[1] = new_y_value
        print("Data converted from log reflectance to reflectance")

        self.control_y_value = 'reflectance'



    def KM_to_R(self):

        if self.control_y_value != 'Kubelka Munk':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value) 

        y_value = self.IR_data[1]
        new_y_value = 1 + y_value - np.sqrt(2*y_value+y_value**2)
        self.IR_data[1] = new_y_value
        print("Data converted from Kubelka Munk to reflectance")

        self.control_y_value = 'reflectance'



    def R_to_KM(self):

        if self.control_y_value != 'recletcance':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)

        y_value = self.IR_data[1]
        new_y_value = (1-y_value)**2/(2*y_value)
        self.IR_data[1] = new_y_value
        print("Data converted from reflectance to Kubelka Munk")

        self.control_y_value = 'Kubelka Munk'




    def wave_number_to_micro_meter(self):

        if self.control_x_value != 0:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")

        x_value = self.IR_data[0]
        new_x_value = (1/x_value*10**7)/1000
        self.IR_data[0] = new_x_value
        print("x-axis converted to micro meter")

        self.control_x_value = 1   
    

    def micro_meter_to_wave_number(self):

        if self.control_x_value != 1:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")

        x_value = self.IR_data[0]
        new_x_value = (1000/x_value)/(10**7)
        self.IR_data[0] = new_x_value
        print("x-axis converted to wave number")

        self.control_x_value = 0


    def plot(self):
        try:
            import matplotlib.pyplot as plt

            print("Plotting AB")
            plt.plot(self.IR_data[0],self.IR_data[-1])
            plt.show()

        except ImportError:
            print(f"Install matplotlib to plot spectra")



    def to_csv(self):
        x = self.IR_data[0]
        y = self.IR_data[1]

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      

        def loop_func_1(): 
        
            inp = input("Enter the result directory:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
        
        self.result_path = loop_func_1() 

        def loop_func_2(): 
        
            inp = input("Enter the result file name:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
                            
        self.file_name = loop_func_2() 

        
        try:
            df.to_csv(r'{}/{}.csv'.format(self.result_path,self.file_name))
        except:
            raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')


    def to_excel(self):
        x = self.IR_data[0]
        y = self.IR_data[1]

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      

        def loop_func_1(): 
        
            inp = input("Enter the result directory:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
        
        self.result_path = loop_func_1() 

        def loop_func_2(): 
        
            inp = input("Enter the result file name:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
                            
        self.file_name = loop_func_2() 

        try:
            df.to_excel(r'{}/{}.xlsx'.format(self.result_path,self.file_name), sheet_name='Sheet1')
        except:
            raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')











#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
class Transmission(IR_Reader):

    def __init__(self, *args, **kwargs):
        super(self).__init__(self,*args, **kwargs)



    if self.IR_format != 'AB':
        raise TypeError("Data is not in correct format")

    self.control_y_value = 'absorbance'



    def T_to_A(self):

        if self.control_y_value != 'transmission':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)

        ## Beer Lambert law
        y_value = self.IR_data[1]
        new_y_value = np.log10(1/y_value)
        self.IR_data[1] = new_y_value
        print("Data converted from transmission to absorbance")

        self.control_y_value = 'absorbance'



    def A_to_T(self):

        if self.control_y_value != 'absorbance':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)

        ## Beer Lambert law
        y_value = self.IR_data[1]
        new_y_value = 1/(10**y_value)
        self.IR_data[1] = new_y_value
        print("Data converted from absorbance to transmission")

        self.control_y_value = 'transmission'
    


    def A_to_ATR(self):


        if self.control_y_value != 'ATR':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)
        

        def func(self,check):
            while check == True:
                try:
                    wave_number = input("Enter the wavenumber (to abort write 'END'):")
                    self.wave_number = float(wave_number)      # this will raise a ValueError if s can't be made into an float
                    break 
                except ValueError:
                    if self.wave_number == 'END':
                        break
                    try:
                        int(self.wave_number)    # will raise another ValueError if s can't be made into a float
                        print("You must enter an floating point number, rather than a integer.")
                        func(True)
                    except ValueError:
                        print("You must enter a number.")
                        func(True)
                

        func(True)
        
        y_value = self.IR_data[1]
        new_y_value = y_value * (self.wave_number(True)/1000)
        self.IR_data[1] =  new_y_value
        print("Data converted from absorbance to ATR")

        self.control_y_value = 'ATR'
        


    def ATR_to_A(self):

        if self.control_y_value != 'ATR':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)
        

        def wave_number(check):
            while check == True:
                try:
                    x = input("Enter the wave number:")
                    x = float(x)      # this will raise a ValueError if s can't be made into an float
                    check = False

                except ValueError:
                    try:
                        int(x)    # will raise another ValueError if s can't be made into a float
                        print("You must enter an floating point number, rather than a integer.")
                        wave_number(True)
                    except ValueError:
                        print("You must enter a number.")
                        wave_number(True)
            

        y_value = self.IR_data[1]
        new_y_value = y_value*(1000/wave_number(True))
        self.IR_data[1] =  new_y_value
        print("Data converted from ATR to absorbance")

        self.control_y_value = 'absorbance'


    def wave_number_to_micro_meter(self):

        if self.control_x_value != 0:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")

        x_value = self.IR_data[0]
        new_x_value = (1/x_value*10**7)/1000
        self.IR_data[0] = new_x_value
        print("x-axis converted to micro meter")

        self.control_x_value = 1   
    


    def micro_meter_to_wave_number(self):

        if self.control_x_value != 1:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")

        x_value = self.IR_data[0]
        new_x_value = (1000/x_value)/(10**7)
        self.IR_data[0] = new_x_value
        print("x-axis converted to wave number")

        self.control_x_value = 0

    def plot(self):
        try:
            import matplotlib.pyplot as plt

            print("Plotting AB")
            plt.plot(self.IR_data[0],self.IR_data[-1])
            plt.show()

        except ImportError:
            print(f"Install matplotlib to plot spectra")



    def to_csv(self):
        x = self.IR_data[0]
        y = self.IR_data[1]

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      

        def loop_func_1(): 
        
            inp = input("Enter the result directory:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
        
        self.result_path = loop_func_1() 

        def loop_func_2(): 
        
            inp = input("Enter the result file name:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
                            
        self.file_name = loop_func_2() 

        try:
            df.to_csv(r'{}/{}.csv'.format(self.result_path,self.file_name))
        except:
            raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')



    def to_excel(self):
        x = self.IR_data[0]
        y = self.IR_data[1]

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      

        def loop_func_1(): 
        
            inp = input("Enter the result directory:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
        
        self.result_path = loop_func_1() 

        def loop_func_2(): 
        
            inp = input("Enter the result file name:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
                            
        self.file_name = loop_func_2() 

        try:
            df.to_excel(r'{}/{}.xlsx'.format(self.result_path,self.file_name), sheet_name='Sheet1')
        except:
            raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')

        





#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

class ATR(IR_Reader):

    def __init__(self, *args, **kwargs):
        super(self).__init__(self,*args, **kwargs)

        

    if self.IR_format != 'AB':
        raise TypeError("Data is not in correct format")

    self.control_y_value = 'absorbance'


    def T_to_A(self):

        if self.control_y_value != 'transmission':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)

        ## Beer Lambert law
        y_value = self.IR_data[1]
        new_y_value = np.log10(1/y_value)
        self.IR_data[1] = new_y_value
        print("Data converted from transmission to absorbance")

        self.control_y_value = 'absorbance'

        

    def A_to_T(self):

        if self.control_y_value != 'absorbance':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)

        ## Beer Lambert law
        y_value = self.IR_data[1]
        new_y_value = 1/(10**y_value)
        self.IR_data[1] = new_y_value
        print("Data converted from absorbance to transmission")

        self.control_y_value = 'transmission'



    def A_to_ATR(self):

        if self.control_y_value != 'ATR':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)
        

        def func(self,check):
            while check == True:
                try:
                    wave_number = input("Enter the wavenumber (to abort write 'END'):")
                    self.wave_number = float(wave_number)      # this will raise a ValueError if s can't be made into an float
                    break 
                except ValueError:
                    if self.wave_number == 'END':
                        break
                    try:
                        int(self.wave_number)    # will raise another ValueError if s can't be made into a float
                        print("You must enter an floating point number, rather than a integer.")
                        func(True)
                    except ValueError:
                        print("You must enter a number.")
                        func(True)
                

        func(True)
        
        y_value = self.IR_data[1]
        new_y_value = y_value * (self.wave_number(True)/1000)
        self.IR_data[1] =  new_y_value
        print("Data converted from absorbance to ATR")

        self.control_y_value = 'ATR'



    def ATR_to_A(self):

        if self.control_y_value != 'ATR':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)
        

        def func(self,check):
            while check == True:
                try:
                    wave_number = input("Enter the wavenumber (to abort write 'END'):")
                    self.wave_number = float(wave_number)      # this will raise a ValueError if s can't be made into an float
                    break 
                except ValueError:
                    if self.wave_number == 'END':
                        break
                    try:
                        int(self.wave_number)    # will raise another ValueError if s can't be made into a float
                        print("You must enter an floating point number, rather than a integer.")
                        func(True)
                    except ValueError:
                        print("You must enter a number.")
                        func(True)
        

        func(True)    

        y_value = self.IR_data[1]
        new_y_value = y_value*(1000/self.wave_number)
        self.IR_data[1] =  new_y_value
        print("Data converted from ATR to absorbance")

        self.control_y_value = 'absorbance'



    def wave_number_to_micro_meter(self):

        if self.control_x_value != 0:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")

        x_value = self.IR_data[0]
        new_x_value = (1/x_value*10**7)/1000
        self.IR_data[0] = new_x_value
        print("x-axis converted to micro meter")

        self.control_x_value = 1   
    


    def micro_meter_to_wave_number(self):

        if self.control_x_value != 1:
            raise TypeError("The x-values are allready in micrometers. try 'IR_reader.micro_meter_to_wave_number()'")

        x_value = self.IR_data[0]
        new_x_value = (1000/x_value)/(10**7)
        self.IR_data[0] = new_x_value
        print("x-axis converted to wave number")

        self.control_x_value = 0



    def plot(self):
        try:
            import matplotlib.pyplot as plt

            print("Plotting AB")
            plt.plot(self.IR_data[0],self.IR_data[-1])
            plt.show()

        except ImportError:
            print(f"Install matplotlib to plot spectra")


    
    def to_csv(self):
        x = self.IR_data[0]
        y = self.IR_data[1]

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      

        def loop_func_1(): 
        
            inp = input("Enter the result directory:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
        
        self.result_path = loop_func_1() 

        def loop_func_2(): 
        
            inp = input("Enter the result file name:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
                            
        self.file_name = loop_func_2() 

        try:
            df.to_csv(r'{}/{}.csv'.format(self.result_path,self.file_name))
        except:
            raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')


    def to_excel(self):
        x = self.IR_data[0]
        y = self.IR_data[1]

        data = {'x': x, 'y': y}
        df = pd.DataFrame(data,columns=['x','y'])      

        def loop_func_1(): 
        
            inp = input("Enter the result directory:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
        
        self.result_path = loop_func_1() 

        def loop_func_2(): 
        
            inp = input("Enter the result file name:") 
                
            if inp is float:   # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            elif inp is int:  # will raise another ValueError if s can't be made into a float
                raise ValueError("You must enter an string, not an integer or floated point number.")
                
            else:
                inp = r'{}'.format(inp)
                return inp
                            
        self.file_name = loop_func_2() 

        try:
            df.to_excel(r'{}/{}.xlsx'.format(self.result_path,self.file_name), sheet_name='Sheet1')
        except:
            raise TypeError('The file name and/or directory is nor corret (does not exist or dones work')










