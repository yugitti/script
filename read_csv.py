import time
import csv
from memory_profiler import profile
import pandas as pd

# PATH = "./classes/class-descriptions.csv"
PATH_CLASS = "./classes/class-descriptions.csv"
PATH_ANNOT = "./annotations/validation/annotations-human.csv"
PATH_OUT_ANNOT_FACE = "./annotations/validation/annotations-face.csv"
PATH_IMAGE_URL = "./images/validation/images.csv"
PATH_OUT_IMAGE_URL = "./images/train/images-face.csv"


HEADER = ['ImageID','Subset','OriginalURL','OriginalLandingURL','License','AuthorProfileURL','Author','Title','OriginalSize','OriginalMD5','Thumbnail300KURL']
MOUTH_ID = '/m/0283dt1'
EYE_ID = '/m/014sv8'
FACE_ID = '/m/0dzct'
HUMAN_ID = '/m/01g317'

def myTime(func):
    import functools
    import datetime
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.today()
        result = func(*args, **kwargs)
        end = datetime.datetime.today()
        return end - start
    return wrapper


def get_class_name():
    read = pd.read_csv(PATH_CLASS)
    temp = read[read['name'].str.contains('Human|Face|Eye|Mouth')]
    print temp

# @myTime
# @profile
def get_label1(read):
    temp = read[read['LabelName'].str.contains('%s|%s|%s'%(FACE_ID,EYE_ID,MOUTH_ID))]
    print temp.shape
    return temp
# @myTime
# @profile
def get_label2(read, SEARCH_ID):
    # temp = read.query('LabelName==@FACE_ID | LabelName==@EYE_ID | LabelName==@MOUTH_ID | LabelName==@ ')
    temp = read.query('LabelName==@SEARCH_ID')
    # print temp.shape
    return temp
# @myTime
# @profile
def get_label3(read):
    temp = read[(read['LabelName'] == FACE_ID)|(read['LabelName'] == EYE_ID)|(read['LabelName'] == MOUTH_ID)]
    print temp.shape
    return temp

def get_matach_imageID(df_word, df_target):
    col = df_word.columns
    df = pd.DataFrame(columns=col)
    hit_count = 0
    for k, a in enumerate(df_word.itertuples()):
        image_id = a[1]

        if not (df_target.query('ImageID==@image_id')).empty:
            df = df.append(df_word.iloc[k])
            # hit_count += 1
            # if (hit_count % 100 == 0):
            #     print hit_count

    return df


def get_imageID2():
    read = pd.read_csv(PATH_ANNOT)
    col = read.columns
    human = pd.DataFrame(columns=col)
    print "get duplicate"
    a = read.duplicated(subset='ImageID')
    ind = []
    hit_count = 0

    print "get index"
    for i, aa in enumerate(a):
        if (aa == False):
            ind.append(i)
    sf = read['LabelName']

    print "start query"
    for k, top_id in enumerate(ind):
        if (k != len(ind) - 1):
            temp = sf[top_id: ind[k + 1]]
            temp2 = temp.str.contains('%s|%s|%s|%s'%(HUMAN_ID,FACE_ID,EYE_ID,MOUTH_ID)).value_counts(sort=False)
            if (len(temp2) == 4):
                human = human.append(read.iloc[top_id])
                hit_count += 1
                if(hit_count%100 == 0):
                    print hit_count

    human_opt_id = pd.DataFrame(human['ImageID'], columns=['ImageID'])
    print human_opt_id.shape
    return human_opt_id


# @profile
def get_imageID():
    read = pd.read_csv(PATH_ANNOT)
    col = read.columns
    human = pd.DataFrame(columns=col)
    person = get_label2(read, HUMAN_ID)
    face = get_label2(read, FACE_ID)
    eye = get_label2(read, EYE_ID)
    mouth = get_label2(read, MOUTH_ID)

    print person.shape
    print face.shape
    print eye.shape
    print mouth.shape

    print "mouth shape is %d" %mouth.shape[0]
    temp = get_matach_imageID(mouth, eye)
    print "mouth w/ eye shape is %d" % temp.shape[0]
    temp = get_matach_imageID(temp, face)
    print "mouth w/ eye&face shape is %d" % temp.shape[0]
    human = get_matach_imageID(temp, person)
    print "person w/ mouth&eye&face shape is %d" % human.shape[0]

    human_opt = human.drop_duplicates(subset='ImageID')

    # for a in human_opt.itertuples():
    #     print a[1]
    human_opt_id = pd.DataFrame(human_opt['ImageID'], columns=['ImageID'])
    print human_opt_id.shape
    # print human_opt_id[0:10]
    return human_opt_id

# @profile
def get_imageURL(id_table):
    # df = pd.Series()
    df = pd.DataFrame(columns=HEADER)
    print type(df)
    count = 0
    hit_count = 0

    reads = pd.read_csv(PATH_IMAGE_URL, chunksize=10000)
    i = 1
    for read in reads:
        print "no %d" %i
        i = i + 1
        for k, a in enumerate(read.itertuples()):
            image_id = a[1]
            # print image_id
            temp = id_table.query('ImageID==@image_id')
            if not temp.empty:
                df = df.append(read.iloc[k])
                index = temp.index
                id_table.drop(index)
                hit_count += 1
                if(hit_count%100 == 0):
                    print hit_count

    print df.shape
    return df


if __name__ == '__main__':

    # get_class_name()
    human_id = get_imageID()
    image_human_id = get_imageURL(human_id)
    human_id.to_csv(PATH_OUT_ANNOT_FACE, index=False)
    image_human_id.to_csv(PATH_OUT_IMAGE_URL, index=False)



