import cv2
import numpy as np


if __name__ == '__main__':
    def callback(*arg):
        print (arg)

    def createPath( img ):
        h, w = img.shape[:2]
        return np.zeros((h, w, 3), np.uint8)

    cv2.namedWindow( "result" )

    cap = cv2.VideoCapture("C:/hui10.mp4")
    colors = ['red', 'green', 'blue'] # список цветов, которые необходимо определить

    # диапазоны HSV для каждого цвета (в данном примере для красного, зеленого и синего)
    hsv_min = {'red': np.array((0, 100, 100), np.uint8),
               'green': np.array((40, 70, 70), np.uint8),
               'blue': np.array((100, 70, 70), np.uint8)}

    hsv_max = {'red': np.array((10, 255, 255), np.uint8),
               'green': np.array((80, 255, 255), np.uint8),
               'blue': np.array((130, 255, 255), np.uint8)}

    last_coords = {} # словарь для хранения последних координат каждого цвета
    path_color = {'red': (0, 0, 255),
                  'green': (0, 255, 0),
                  'blue': (255, 0, 0)}

    flag, img = cap.read()
    path = createPath(img)

    while True:
        flag, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )

        for color in colors:
            thresh = cv2.inRange(hsv, hsv_min[color], hsv_max[color])
            moments = cv2.moments(thresh, 1)
            dM01 = moments['m01']
            dM10 = moments['m10']
            dArea = moments['m00']

            if dArea > 100:
                x = int(dM10 / dArea)
                y = int(dM01 / dArea)
                cv2.circle(img, (x, y), 10, path_color[color], -1)

                if last_coords.get(color) is not None:
                    cv2.line(path, last_coords[color], (x, y), path_color[color], 5)
                last_coords[color] = (x, y)

        img = cv2.add( img, path)

        cv2.imshow('result', img)

        ch = cv2.waitKey(5)
        if ch == 27:
            break

    cap.release()
    cv2.destroyAllWindows()