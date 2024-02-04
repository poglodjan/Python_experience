import numpy as np
import cv2
import matplotlib.pyplot as plt

def zmniejsz_jasnosc(img, factor=0.5):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_hsv[:,:,2] = np.clip(img_hsv[:,:,2] * factor, 0, 255)
    return cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

def zwieksz_kontrast(img, alpha=1.5, beta=0):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def wizualizuj_histogram(img, title):
    color = ('b','g','r')
    for i,col in enumerate(color):
        hist = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(hist,color = col)
        plt.xlim([0,256])
    plt.title(title)
    plt.show()

img1 = cv2.imread("astronom.png")
img2 = cv2.imread("zadanie_6.01.png")

print(img1.shape)
print(img2.shape)

width, height = 183, 275
img2_resized = cv2.resize(img2, (width, height))

img2_processed = zmniejsz_jasnosc(img2_resized, factor=0.7)
img2_processed = zwieksz_kontrast(img2_processed, alpha=1.5, beta=30)

wizualizuj_histogram(img1, 'Histogram - Obraz 1')
wizualizuj_histogram(img2_resized, 'Histogram - Obraz 2 (Po zmianie rozmiaru)')
wizualizuj_histogram(img2_processed, 'Histogram - Obraz 2 (Po przetworzeniu)')

combined = np.hstack((img1, img2_resized, img2_processed))

cv2.imshow("Combined Images", combined)
cv2.waitKey()
cv2.destroyAllWindows()
