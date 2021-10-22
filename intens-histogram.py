import cv2
import numpy
import math
import matplotlib.pyplot as plt
import pickle
import time
import progressbar

#------------------------------------------------------------------------
#                               Progress Bar 
#------------------------------------------------------------------------- 

widgets = [' [', progressbar.Timer(format= 'elapsed time: %(elapsed)s'), '] ',
                 progressbar.Bar('|'),' (', progressbar.ETA(), ') ',
          ]

#------------------------------------------------------------------------
#                       Convert RGB to Gray-Scale 
#-------------------------------------------------------------------------

#read rgb image
def gray_conversion(img):
    gray_scale = img.copy()
    row,col,_=img.shape
    print("Image ",row," x ",col,end='\t')
    #average weights 
    R,G,B = 76.245,149.685,29.071                           

    #converts original RGB image into gray-scale using avg weights 

    for i in range(row):
        for j in range(col):
            b = img[i][j][0]*B
            g = img[i][j][1]*G
            r = img[i][j][2]*R
            gray_scale[i][j]  = (r+b+g)/255
    return gray_scale

#-------------------------------------------------------------------------
#                       Read Intensity Values 
#-------------------------------------------------------------------------

#get pix values store in dictionary
#if pixel value already exists tally it
def read_intensity_values(img, channel=0):   
    row,col,_=img.shape
    intensity_vals = {}
    for i in range(row):
        for j in range(col):
            color = int(img[i][j][channel])
            if color in intensity_vals:
                intensity_vals[color]+=1
            else:
                intensity_vals[color]=1
    return intensity_vals

#-------------------------------------------------------------------------
#                       Compute Probability Density 
#-------------------------------------------------------------------------
# print(intensity_vals)
def compute_pr_density(img, intensity_vals):
    row, col, _ = img.shape
    # compute probability density funciton p(rk)=nk/MN
    MN = row*col
    prk = {}
    for k in intensity_vals:
        prk[k]=(intensity_vals.get(k)/MN)
    return prk
   
#-------------------------------------------------------------------------
#                       Compute Cumulative Distribution  
#-------------------------------------------------------------------------

def compute_cumulative_dis(prk):
    sum, s, frequencies = 0, {}, []
    tones = len(prk)-1

    for k in prk:
        sum += prk.get(k)
        if(sum*tones - int(sum*tones)>=.5):
            s[k]= math.ceil(sum*tones)
        else:
            s[k]=int(sum*tones)
    return s

#-------------------------------------------------------------------------
#                               Plot Histogram 
#-------------------------------------------------------------------------

# Plot RGB Original Histogram 
def plot_histogram(r_prk, g_prk, b_prk,gr_prk,):
    r_x,g_x,b_x,gr_x = [],[],[],[]

    # #get index of prk
    # for i in range(len(r_prk)):
    #     r_x.append(i)
    # for i in range(len(g_prk)):
    #     g_x.append(i)
    # for i in range(len(b_prk)):
    #     b_x.append(i)
    # for i in range(len(gr_prk)):
    #     gr_x.append(i)

    #red
    plt.subplot(141)
    plt.bar(r_prk.keys(),r_prk.values(),color='r')
    plt.xlabel('rk')
    plt.ylabel('Probability(rk)')
    plt.title('Red')

    #green
    plt.subplot(142)
    plt.bar(g_prk.keys(),g_prk.values(),color='g' )
    plt.xlabel('rk')
    plt.ylabel('Probability(rk)')
    plt.title('Green')

    #blue
    plt.subplot(143)
    plt.bar(b_prk.keys(),b_prk.values(),color='b' )
    plt.xlabel('rk')
    plt.ylabel('Probability(rk)')
    plt.title('Blue')

    #gray
    plt.subplot(144)
    plt.bar(gr_prk.keys(),gr_prk.values(),color='k' )
    plt.xlabel('rk')
    plt.ylabel('Probability(rk)')
    plt.title('Gray')

    #show plots
    plt.tight_layout()
    plt.show()

#-------------------------------------------------------------------------
#                       Display Histogram-Equalized image 
#-------------------------------------------------------------------------

# need to map the prk -> sval pass as dictionary s
def convert_equalized_gray(gray,s):
    enhanced_gray = gray.copy()
    row,col,_ = gray.shape

    #make list of colors 
    colors = []
    for i in s:
        colors.append(i)

    g_bar = progressbar.ProgressBar(max_value=row, widgets=widgets).start()
    #compare every pix and map with closest s value
    for i in range(row):
        g_bar.update(i)
        for j in range(col):
            for k in s:
                if int(k) == int(gray[i][j][0]):
                    enhanced_gray[i][j] = colors[s[k]]
                    break
    return enhanced_gray

#-------------------------------------------------------------------------
#                       Dump Pickle File 
#-------------------------------------------------------------------------
def dump(img, newimg):
    db = {"gray": img, "enhanced_gray": newimg}

    # for writing binary mode 
    dbfile = open('examplePickle', 'wb')     
    db = pickle.dump(db,dbfile)
    dbfile.close()

#-------------------------------------------------------------------------
#                              Main
#-------------------------------------------------------------------------

if __name__ == "__main__":
    #read img
    # rgb = cv2.imread("html/img/Image-1.bmp")
    rgb = cv2.imread("html/img/bright.jpg") 
    # rgb = cv2.imread("html/img/dark.jpg")
    gray = rgb.copy()

    #convert to gray
    gray = gray_conversion(rgb)

    #read intensity values 
    b_intensity = read_intensity_values(rgb)
    g_intensity = read_intensity_values(rgb,1)
    r_intensity = read_intensity_values(rgb,2)
    gr_intensity = read_intensity_values(gray)

    #compute prk (probability density )
    #FIX THE FREQUENCIES 
    b_prk = compute_pr_density(rgb,b_intensity)
    g_prk = compute_pr_density(rgb,g_intensity)
    r_prk = compute_pr_density(rgb,r_intensity)
    gr_prk = compute_pr_density(gray,gr_intensity)

    #compute s val (cumulative distribution)
    # b_s = compute_cumulative_dis(b_prk)
    # g_s = compute_cumulative_dis(g_prk)
    # r_s = compute_cumulative_dis(r_prk)
    gr_s = compute_cumulative_dis(gr_prk)

    #plot histogram
    plot_histogram(r_intensity, g_intensity, b_intensity,gr_s)

    #display histogram equalized image
    enhanced_gray = convert_equalized_gray(gray,gr_s)

    #display image comparisions 
    cv2.imshow("RGB",rgb)
    cv2.imshow("Gray",gray)
    cv2.imshow("Enhanced Gray Scale", enhanced_gray)
    cv2.waitKey(0)

    #dump 
    #dump(gray, enhanced_gray)
    


    
