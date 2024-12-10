import cv2
import numpy as np

def invisible_green_screen():
    cap = cv2.VideoCapture(0)  # Start webcam
    background = None

    # Fang baggrunden
    print("Fanger baggrund... Stå væk fra kameraet i 2 sekunder.")
    for i in range(30):  # Fang de første 30 frames som baggrund
        ret, background = cap.read()
        if not ret:
            print("Kunne ikke læse baggrund.")
            return
    print("Baggrund registreret!")

    # HSV-værdier for grøn (kan justeres)
    lower_green = np.array([35, 50, 50])   # Nedre grænse for grøn
    upper_green = np.array([85, 255, 255]) # Øvre grænse for grøn

    while True:
        ret, frame = cap.read()  # Læs nyt billede fra webcam
        if not ret:
            break

        # Konverter BGR til HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Skab maske for grøn farve
        mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        mask_inv = cv2.bitwise_not(mask)

        # Erstat grøn farve med baggrunden
        fg_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
        bg_part = cv2.bitwise_and(background, background, mask=mask)
        result = cv2.add(fg_part, bg_part)

        # Vis resultat i et OpenCV-vindue
        cv2.imshow("Green Screen Effect", result)

        # Afslut med 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    invisible_green_screen()
