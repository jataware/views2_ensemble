import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--start_date', default="483")
parser.add_argument('--end_date', default="520")
args = parser.parse_args()
print("start_date", args.start_date, "end_date", args.end_date)


nameofcsv = "storage/predictions/views_sb_ensemble_script_start=" + str(args.start_date) +"_end="+str(args.end_date)+ ".csv"

print('csv_name', nameofcsv)
time.sleep(2)



