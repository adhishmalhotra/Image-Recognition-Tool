import os
import numpy as np
from barcode import Code128
from barcode.writer import ImageWriter
import PIL
from scipy.spatial import distance
import matplotlib.pyplot as plt

#function for reversing an array because we might need to reverse projection 2 with angle 45 degree and projection 4 with angle 135 degree
def Reverse(lst):
    return [ele for ele in reversed(lst)]
#this is the function for 1st projection
#when projection angle is 0 degrees
def p1(): 
    projectionArr = []
    sum = 0
    m,n = 28,28
    for row in range(m):
        for col in range(n): 
            sum += imgArray2d[row][col]
        projectionArr.append(sum)
        sum = 0
    return projectionArr
#when the projection angle is 45 degrees
def p2():
    projectionArr = []
    m,n = 28,28
    for col in range(n-1, 0, -1):
        sum = 0
        count = 0 
        row = 0
        if (col == n-1):
            pass
        
        while(row + count<m and col + count<n):
            sum+=imgArray2d[row+count][col+count]
            count+=1
        projectionArr.append(sum)
    for row in range (1, m-1):
        sum=0
        count=0
        col=0
        if(row == m-1):
            pass
        while(row+count<m and col+count<n):
            sum+=imgArray2d[row+count][col+count]
            count+=1
        projectionArr.append(sum)
    return projectionArr
#when projection angle is 90 degrees
def p3():
    projectionArr = []
    sum = 0
    m,n = 28,28
    for row in range(m):
        for col in range(n): 
            sum += imgArray2d[col][row]
        projectionArr.append(sum)
        sum = 0
    return projectionArr
#when projection angle is 135 degrees
def p4(): 
    projectionArr = []
    m,n = 28,28
    for col in range (n-1, 0, -1): 
        count = 0
        sum = 0
        row = n-1
        if (col == n-1):
            pass
        while(row - count< m and col + count< n):
            sum += imgArray2d[row-count][col+count]
            count +=1
        projectionArr.append(sum)
    for row in range (m-1, 0, -1):
        sum = 0
        count = 0
        col = 0
        if (row == 0): 
            pass
        while(row - count <m and col+count <n and row - count>=0):
            sum += imgArray2d[row-count][col+count]
            count += 1
        projectionArr.append(sum)
    return projectionArr
#calculating the threshold for each projection and storing it in an array
def threshold_calculator(arr, size):
    thArray = []
    sum = 0
    avg = 0
    for i in range(size):
        sum+=arr[i]
    avg = sum/size
    for i in range(size):
        if(arr[i]<avg):
            thArray.append(0)
        elif(arr[i]>avg):
            thArray.append(1)
    return thArray
def BarcodeGenerator():
    directory = 'MNIST_DS'
    table = []
    for subdir, dirs, files in os.walk(directory):
        col = []
        for file in files:
            img = PIL.Image.open(os.path.join(subdir, file))
            image_sequence = img.getdata()
            #1d array out here for the image 
            imgArray = np.array(image_sequence)
            #changing that 1d array into 2d array with row = col = 28
            global imgArray2d
            imgArray2d = np.reshape(imgArray, (28,28))
            projection1 = p1()
            projection2 = p2()
            projection3 = p3()
            projection4 = p4()
            Th_p1 = threshold_calculator(projection1, len(projection1))
            Th_p2 = threshold_calculator(projection2, len(projection2))
            Th_p3 = threshold_calculator(projection3, len(projection3))
            Th_p4 = threshold_calculator(projection4, len(projection4))
            RBC = np.concatenate((Th_p4, Th_p3, Th_p2, Th_p1))
            col.append(RBC)
        table.append(col)
    return table

table = BarcodeGenerator()

#explanatory example
#this is an example which can be used to calculate the hamming distance 
#dist = distance.hamming(table[1][0], table[1][1])
#print(dist) 

def SearchAlgorithm(barCodeArray):
    #so we'd have to run two loops
    #the outer loop is supposed to go over all the elements in the table (the image is being passed as an argument so we can search it)
    #the inner loop shall do the same thing that is, going over all the elements in the table (but this time its for comparison)
    #the inner loop must do the following computations: -
    #1 calculate the hamming distance between the image which has been passed from the outer loop and the image which is being iterated in the inner loop
    #2 return the image with the lowest hamming distance
    #3check if the image lies in the same subfolder, if it does increase the hit rate by 1 otherwise not
    ham = 0
    imgClass = 0
    hit = 0
    img1Row = 0
    img1Col =0
    img2Row = 0
    img2Col = 0
    for i in range(1, len(barCodeArray)):
        for j in range(len(barCodeArray[i])):
            
            #assign the image being searched for some value of the table array
            imgSearch = barCodeArray[i][j]
            img1Row = i
            img1Col = j
            shortest = len(imgSearch)
            for x in range(1, len(barCodeArray)):
                for y in range(len(barCodeArray[x])):
                    #assign the image being compared some value of the table array
                    imgCompare = barCodeArray[x][y]
                    ham = distance.hamming(imgSearch, imgCompare)
                    if(ham!=0 and ham<shortest):
                        shortest = ham
                        img2Row = x
                        img2Col = y
                        imgClass = x
                    else: 
                        pass
            # the smallest hamming distance for the image being searched for will be stored in "least"
            imgOne = plt.imread('MNIST_DS/' + str(img1Row-1) + '/' + 'img_' + str(img1Col) + '.jpg')
            imgTwo = plt.imread('MNIST_DS/' + str(img2Row-1) + '/' + 'img_' + str(img2Col) + '.jpg')
            plt.subplot(2,2,1)
            plt.imshow(imgOne)
            plt.subplot(2,2,2)
            plt.imshow(imgTwo)
            plt.show()
            if(i == imgClass):
                hit+=1     
    return hit

def main():
    print("The accuracy of the program is:" + str(SearchAlgorithm(table)) + "%")

if __name__ == "__main__":
    main()
        

