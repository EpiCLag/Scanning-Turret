#! /usr/bin/env python

#This will create a pgm file containing the image
#It will also remap the values
#All values will be reduced by the smallest one
def save_to_pgm(tab):
    #Open new file, nuking the old one
    output = open("output.pgm", "w")

    #Setting flags according to the pgm format
    #Format description: http://netpbm.sourceforge.net/doc/pgm.html

    output.write("P2\n")
    output.write(str( len(tab)))
    output.write(" ")
    output.write(str(len(tab[0])))


    #Finding the minimum and maximum
    #Max = 4 000 millimiter by the sensor
    themin = 4000
    themax = 0

    for line in tab:
        for pixel in line:
            if themin > pixel:
                themin = pixel
            if themax < pixel:
                themax = pixel

    #Max value:
    output.write('\n')
    output.write(str(themax - themin +1))
    output.write('\n')

    for line in tab:
        tmp = ''
        for pixel in line:
            #Offset the value
            tmpixel = (themax - themin)  - (pixel - themin)
            tmp =  tmp + str(tmpixel) + ' '
        tmp = tmp + '\n'
        output.write(tmp)

#Debug
if __name__ == "__main__":
    tab = [[0, 50],[100, 200]]
    save_to_pgm(tab)
