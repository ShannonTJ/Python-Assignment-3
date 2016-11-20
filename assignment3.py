#Shannon TJ 10101385
#This program equalizes an image's color distribution to maximize its contrast

from SimpleGraphics import *

#Store numeric constants in variables
NUM_VALUES = 256

#Compute red, green, blue histograms for an image
#Parameters: An image
#Returns: Three lists (histograms), each containing 256 values
def histogram(img):
  #Create three empty lists, one for red, one for green, one for blue
  red_list = []
  for i in range(NUM_VALUES):
    red_list.append(0)
  green_list = []
  for i in range(NUM_VALUES):
    green_list.append(0)
  blue_list = []
  for i in range(NUM_VALUES):
    blue_list.append(0)
  for x in range(getWidth(img)):
    for y in range(getHeight(img)):
      #Get the amount of red, green, blue from each pixel
      r, g, b = getPixel(img, x, y)
      #Increment the amount of red, green, blue in their respective lists
      red_list[r] = red_list[r] + 1
      green_list[g] = green_list[g] + 1
      blue_list[b] = blue_list[b] + 1
  return red_list, green_list, blue_list

#Compute a cumulative histogram from a non-cumulative histogram
#Parameters: A histogram
#Returns: A list (cumulative histogram) containing 256 values
def c_histogram(histogram):
  #Create an empty list
  c_list = []
  for i in range(NUM_VALUES):
    c_list.append(0)
  #Store a histogram in the empty list
  for i in range(NUM_VALUES):
    c_list[i] = c_list[i] + histogram[i]
  #Compute values for the cumulative histogram
  c_list[0] = c_list[0] + 0
  i = 1
  while i <= NUM_VALUES - 1:
    c_list[i] = c_list[i-1] + histogram[i]
    i = i + 1
  return c_list

#Display a histogram and cumulative histogram
#Parameters: The histogram to display, the cumulative histogram to display, the x-coordinate of the upper left corner, the y-coordinate of the upper left corner, the color that will be used to draw the histogram
#Returns: The histogram drawn as a bar graph and the cumulative histogram drawn as a line graph
def d_histogram(histogram, c_histogram, x, y, color):
  #Find the maximum values in the non-cumulative and cumulative histograms
  max = 0 
  max_2 = 0
  for i in range(NUM_VALUES):
    if histogram[i] > max:
      max = histogram[i]
    if c_histogram[i] > max_2:
      max_2 = c_histogram[i]
  i = 0
  y_3 = 0
  while i <= NUM_VALUES - 1:
    for l in range(x, x + NUM_VALUES):
      #Display the histogram
      y_1 = ((histogram[i] / max) * NUM_VALUES)
      setColor(color)
      display_hist = line(l, y + (NUM_VALUES - y_1), l, y + NUM_VALUES)
      #Display the cumulative histogram
      y_2 = ((c_histogram[i] / max_2) * NUM_VALUES)
      setColor("black")
      display_c_hist = line(l, y+(NUM_VALUES-y_2), l-1, y+(NUM_VALUES-y_3))
      i = i + 1
      y_3 = y_2
  return display_hist, display_c_hist

#Modify an image by equalizing its histogram
#Parameters: An image, the image's red cumulative histogram, the image's green  cumulative histogram, the image's blue cumulative histogram 
#Returns: A modified copy of the original image that has an equalized histogram
def eq_histogram(img, r_c_histogram, g_c_histogram, b_c_histogram):
  #Compute the total number of pixels in the image
  num_pixels = getWidth(img) * getHeight(img)
  #Create a new image with the same dimensions as the original image
  new_image = createImage(getWidth(img), getHeight(img))  
  for x in range(getWidth(img)):
    for y in range(getHeight(img)):
      #Get the amount of red, green, blue from each pixel  
      r, g, b = getPixel(img, x, y)
      #Compute the equalized red, green, blue values
      new_r = int((r_c_histogram[r] / num_pixels) * (NUM_VALUES - 1))
      new_g = int((g_c_histogram[g] / num_pixels) * (NUM_VALUES - 1))
      new_b = int((b_c_histogram[b] / num_pixels) * (NUM_VALUES - 1))
      #Store a pixel containing the  equalized red, green, blue values in the         new image
      putPixel(new_image, x, y, new_r, new_g, new_b)
  return new_image

def main():

  #Resize the window 
  resize(4 * NUM_VALUES, 2 * NUM_VALUES)

  #Prompt the user to upload an image
  input_img = input("Enter the name of an image you want to upload:")
  print("Loading and displaying image...")
  img = loadImage(input_img)

  #Display the image
  drawImage(img, 0, 0)
  print("Computing histograms...")

  #Compute histograms
  red_list, green_list, blue_list = histogram(img)
  print("Computing cumulative histograms...")

  #Compute cumulative histograms
  c_red_list = c_histogram(red_list)
  c_green_list = c_histogram(green_list)
  c_blue_list = c_histogram(blue_list)
  print("Displaying histograms...")

  #Display histograms
  r_d_histogram = d_histogram(red_list,c_red_list,NUM_VALUES,0,"red")
  g_d_histogram = d_histogram(green_list,c_green_list,2 * NUM_VALUES,0,"green")
  b_d_histogram = d_histogram(blue_list,c_blue_list,3 * NUM_VALUES,0,"blue")
  print("Equalizing image...")

  #Create and display the equalized image
  eq_img = eq_histogram(img, c_red_list, c_green_list, c_blue_list)
  drawImage(eq_img, 0,  NUM_VALUES)
  print("Computing equalized histograms...")

  #Compute equalized histograms
  eq_redlist, eq_greenlist, eq_bluelist = histogram(eq_img)

  #Compute cumulative equalized histograms
  c_eq_redlist = c_histogram(eq_redlist)
  c_eq_greenlist = c_histogram(eq_greenlist)
  c_eq_bluelist = c_histogram(eq_bluelist)
  print("Displaying equalized histograms...")
  
  #Display cumulative equalized histograms
  d_histogram(eq_redlist, c_eq_redlist, NUM_VALUES, NUM_VALUES, "red")
  d_histogram(eq_greenlist, c_eq_greenlist, 2 * NUM_VALUES, NUM_VALUES, "green")
  d_histogram(eq_bluelist, c_eq_bluelist, 3 * NUM_VALUES, NUM_VALUES, "blue")

#Call the main function
main()
