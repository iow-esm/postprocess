import glob

def get_all_dirs_from_to(out_dir, from_date, to_date):

    dirs=[]

    for dir in glob.glob(out_dir + "/*"):
        date = dir.split("/")[-1]
        if not date.isnumeric() or len(date) != 8:
            continue

        if (int(date) >= from_date and int(date) <= to_date) or (from_date < 0 and to_date < 0):
            dirs.append(dir)
            
    return sorted(dirs)