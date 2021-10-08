#!/usr/bin/env python

import argparse
from uio_irreader.reader import DRIFTS, Transmission, ATR

reader_func = {
    'drifts' : DRIFTS,
    'trans' : Transmission,
    'atr' : ATR
}

def main():
    """[summary]
    """

    ### ADD YOUR PARSER ARGPASE HERE ####
    parser = argparse.ArgumentParser(prog='UiO IR Reader',

                    description='UiOs own python Opus IR spectrum converter. Uses the brukeropusreader package.'
                    )
    #INPUT OUTPUT
    parser.add_argument('-f', '--file', type=str, help="path to file to be converted.")
    parser.add_argument('-fo', '--format', choices=['drifts', 'trans', 'atr'], type=str, help='IR experiment type.')
    parser.add_argument('-o', '--out', type=str, help='file name for converte spectrum.')
    parser.add_argument('--meta', action='store_true', help='Show spectrum metadata.')

    # MODIFY Y-DATA
    parser.add_argument('-A', action="store_true", help='Convert to absorbance.')
    parser.add_argument('-T', action="store_true", help='Convert to transmission.')

    parser.add_argument('-R', action="store_true", help='Convert to reflectance.')
    parser.add_argument('-lgR', action="store_true", help='Convert to log reflectance.')
    parser.add_argument('-KM', action='store_true', help='Convert to Kubelka-Munk.')
    
    parser.add_argument('-ATR', action='store_true', help='Convert to ATR units.')
    
    # MODIFY X-data
    parser.add_argument('-m', '--microns', action='store_true', help='Convert to micro meters.')
    parser.add_argument('-w', '--wavenumbers', action='store_true', help='Convert to wavenumber.')

    #Plot Data
    parser.add_argument('-p', '--plot', action='store_true', help='Plot data.')
    
    args = parser.parse_args()
    args_dict = vars(args)

    #  PROGRAM

    ir_reader = reader_func[args_dict['format']]
    ir_data = ir_reader(directory=args.file)
    
    # CONVERSIONS
    if args.meta:
        print(ir_data)





    ## EVERYTHING ELSE

    # Check if plotting.
    if args.plot:
        ir_data.plot()


    #Save spectrum
    if args.out:
        ir_data.to_csv(args.out)    

    ####

    return


if __name__ == '__main__':
    main()