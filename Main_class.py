
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
        super().__init__(*args, **kwargs)

        self.control_y_value = 'reflectance'
        print('x-values: {}'.format(self.X_data))
        print('Y-values: {}'.format(self.Y_data))

        if self.IR_format != 'LRF':
            raise TypeError("Data is not in correct format. It is in LRF (DRIFTS)")
        




    def R_to_logR(self):

        if self.control_y_value != 'reflectance':
            raise TypeError("Data is not in correct format. Data is in {}.".format(self.control_x_value))



        y_value = self.IR_data[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = np.log(1/n)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from reflectace to log reflectance   ----
        
        """)

        

        self.control_y_value = 'log reflectance'
    


    def logR_to_R(self):

        if self.control_y_value != 'log recletcance':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)

        y_value = self.IR_data[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = 1/(10**n)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from log reflectance to reflectance   ----
        
        """)

      
        self.control_y_value = 'reflectance'



    def KM_to_R(self):

        if self.control_y_value != 'Kubelka Munk':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value) 


        y_value = self.IR_data[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = 1 + n - np.sqrt(2*n+n**2)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from Kubelka Munk to reflectance   ----
        
        """)
       
        self.control_y_value = 'reflectance'



    def R_to_KM(self):

        if self.control_y_value != 'recletcance':
            raise TypeError("Data is not in correct format. Data is in {}.").format(self.control_x_value)

        y_value = self.IR_data[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = (1-n)**2/(2*n)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from reflectance to Kubelka Munk   ----
        
        """)


        self.control_y_value = 'Kubelka Munk'




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



    def help():
        print(""""



        obj.to_csv()                                      Will save the data as a .CSV-file.

        obj.to_excel()                                    Will save the data as an .XLSX-file.

        obj.plot()                                        Will make a simplified plot for the data.


        obj.micro_meter_to_wave_number()                  Will change the x-axis format from micro meter to wave number.

        obj.wave_number_to_micro_meter()                  Will change the x-axis format from wave number to micro meter.
        

        obj.R_to_KM()                                     Will change the y-axis format to Kubelka Munk from reflectance.

        obj.KM_to_R()                                     Will change the y-axis format to reflectance from Kubelka Munk.

        obj.logR_to_R()                                   Will change the y-axis format to reflectance form log-reflectance.

        obj.R_to_logR()                                   Will change the y-axis format to log-reflectance from reflectance.
        
        """
        )








#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
class Transmission(IR_Reader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('x-values: {}'.format(self.X_data))
        print('Y-values: {}'.format(self.Y_data))


        if self.IR_format != 'AB':
            raise TypeError("Data is not in correct format. It is in AB (Transmission or ATR)")

        self.control_y_value = 'absorbance'



    def T_to_A(self):

        if self.control_y_value != 'transmission':
            raise TypeError("Data is not in correct format. Data is in {}.".format(self.control_x_value))

        ## Beer Lambert law
        y_value = self.IR_data[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = np.log10(1/n)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from transmission to absorbance   ----
        
        """)


        self.control_y_value = 'absorbance'



    def A_to_T(self):

        if self.control_y_value != 'absorbance':
            raise TypeError("Data is not in correct format. Data is in {}.".format(self.control_x_value))

        ## Beer Lambert law

        y_value = self.IR_data[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = 1/(10**n)
            new_y_value.append(x)
            i += 1
        
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from absorbance to transmission   ----
        
        """)

        self.control_y_value = 'transmission'
    


    def A_to_ATR(self):


        if self.control_y_value != 'ATR':
            raise TypeError("Data is not in correct format. Data is in {}.".format(self.control_x_value))
        

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
        new_y_value = []
        i = 0
        for n in y_value:
            x = n * (self.wave_number/1000)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from absorbance to ATR   ----
        
        """)



        self.control_y_value = 'ATR'
        


    def ATR_to_A(self):

        if self.control_y_value != 'ATR':
            raise TypeError("Data is not in correct format. Data is in {}.".format(self.control_x_value))
        

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
        new_y_value = []
        i = 0
        for n in y_value:
            x = n*(1000/self.wave_number)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from ATR to absorbance   ----
        
        """)
        

        self.control_y_value = 'absorbance'


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
            df.to_csv(r'{}/{}.csv'.format(self.result_path,self.file_name),header=False)
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

        

    def help():
        print(""""



        obj.to_csv()                                      Will save the data as a .CSV-file.

        obj.to_excel()                                    Will save the data as an .XLSX-file.

        obj.plot()                                        Will make a simplified plot for the data.


        obj.micro_meter_to_wave_number()                  Will change the x-axis format from micro meter to wave number.

        obj.wave_number_to_micro_meter()                  Will change the x-axis format from wave number to micro meter.
        

        obj.ATR_to_A()                                     Will change the y-axis format to ATR from absorption.

        obj.A_to_ATR()                                     Will change the y-axis format to absorption from ATR.

        obj.A_to_T()                                       Will change the y-axis format to transmission from absorption.

        obj.T_to_A()                                       Will change the y-axis format to absorption from transmission.
        
        """
        )



#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

class ATR(IR_Reader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('x-values: {}'.format(self.X_data))
        print('Y-values: {}'.format(self.Y_data))
        

        if self.IR_format != 'AB':
            raise TypeError("Data is not in correct format. It is in AB (Transmission or ATR)")

        self.control_y_value = 'absorbance'


    def T_to_A(self):

        if self.control_y_value != 'transmission':
            raise TypeError("Data is not in correct format. Data is in {}.".format(self.control_x_value))

        ## Beer Lambert law
        y_value = self.IR_data[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = np.log10(1/n)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from transmission to absorbance   ----
        
        """)


        self.control_y_value = 'absorbance'



    def A_to_T(self):

        if self.control_y_value != 'absorbance':
            raise TypeError("Data is not in correct format. Data is in {}.".format(self.control_x_value))

        ## Beer Lambert law

        y_value = self.IR_data[1]
        new_y_value = []
        i = 0
        for n in y_value:
            x = 1/(10**n)
            new_y_value.append(x)
            i += 1
        
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from absorbance to transmission   ----
        
        """)

        self.control_y_value = 'transmission'
    


    def A_to_ATR(self):


        if self.control_y_value != 'ATR':
            raise TypeError("Data is not in correct format. Data is in {}.".format(self.control_x_value))
        

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
        new_y_value = []
        i = 0
        for n in y_value:
            x = n * (self.wave_number/1000)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from absorbance to ATR   ----
        
        """)



        self.control_y_value = 'ATR'
        


    def ATR_to_A(self):

        if self.control_y_value != 'ATR':
            raise TypeError("Data is not in correct format. Data is in {}.".format(self.control_x_value))
        

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
        new_y_value = []
        i = 0
        for n in y_value:
            x = n*(1000/self.wave_number)
            new_y_value.append(x)
            i += 1
        
        self.IR_data[1] = np.array(new_y_value)
        print(self.IR_data[1])

        print("""
        
        ----   Data converted from ATR to absorbance   ----
        
        """)
        

        self.control_y_value = 'absorbance'




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


    def help():
        print(""""



        obj.to_csv()                                      Will save the data as a .CSV-file.

        obj.to_excel()                                    Will save the data as an .XLSX-file.

        obj.plot()                                        Will make a simplified plot for the data.


        obj.micro_meter_to_wave_number()                  Will change the x-axis format from micro meter to wave number.

        obj.wave_number_to_micro_meter()                  Will change the x-axis format from wave number to micro meter.
        

        obj.ATR_to_A()                                     Will change the y-axis format to ATR from absorption.

        obj.A_to_ATR()                                     Will change the y-axis format to absorption from ATR.

        obj.A_to_T()                                       Will change the y-axis format to transmission from absorption.

        obj.T_to_A()                                       Will change the y-axis format to absorption from transmission.
        
        """
        )







