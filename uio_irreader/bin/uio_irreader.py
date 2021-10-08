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
    parser.add_argument('-o', '--out', type=str, help='file name and save as csv.')
    parser.add_argument('--out_excel', type=str, help='file name and save as excel file.')
    parser.add_argument('--meta', action='store_true', help='Show spectrum metadata.')

    # MODIFY Y-DATA
    parser.add_argument('-c', '--convert', type=str, choices=['A', 'T', 'R', 'lgR', 'KM'], help='Convert spectrum data to desired unit.')
    
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

    # CONVERT Y-DATA
    if args.convert == 'A':
        ir_data.to_A()
    elif args.convert == 'T':
        ir_data.to_T()
    elif args.convert == 'R':
        ir_data.to_R()
    elif args.convert == 'lgR':
        ir_data.to_lgR()
    elif args.convert == 'KM':
        ir_data.to_KM()

    # CONVERT X-DATA
    if args.microns:
        ir_data.wave_number_to_micro_meter()
    
    if args.wavenumbers:
        ir_data.micro_meter_to_wave_number()

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
    if args.out_excel:
        ir_data.to_excel(args.out_excel)
    ####

    return


if __name__ == '__main__':
    main()