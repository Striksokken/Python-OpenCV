import cv2
import numpy as np
import platform

def invisible_green_screen():
    cap = cv2.VideoCapture(0)
    background = None

    # Fang baggrunden (første 30 frames)
    for i in range(30):
        ret, background = cap.read()
        if not ret:
            print("Kunne ikke læse baggrund.")
            return
    print("Baggrund registreret!")

    lower_green = np.array([35, 50, 50])   # Nedre grænse for grøn
    upper_green = np.array([85, 255, 255]) # Øvre grænse for grøn

    # Check operativsystem
    current_os = platform.system()

    if current_os == "Windows":
        # Brug pyvirtualcam på Windows
        import pyvirtualcam
        with pyvirtualcam.Camera(width=background.shape[1], height=background.shape[0], fps=30) as cam:
            print(f"Virtuelt kamera '{cam.device}' startet.")
            print(f"Platform: {current_os}")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Fjern grøn farve
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_frame, lower_green, upper_green)
                mask_inv = cv2.bitwise_not(mask)

                fg_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
                bg_part = cv2.bitwise_and(background, background, mask=mask)
                result = cv2.addWeighted(fg_part, 1, bg_part, 1, 0)

                # Send til virtuelt kamera
                cam.send(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
                cam.sleep_until_next_frame()

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    elif current_os == "Darwin":  # macOS
        print(f"Platform: {current_os} - Brug OBS Virtual Camera")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Fjern grøn farve
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_frame, lower_green, upper_green)
            mask_inv = cv2.bitwise_not(mask)

            fg_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
            bg_part = cv2.bitwise_and(background, background, mask=mask)
            result = cv2.addWeighted(fg_part, 1, bg_part, 1, 0)

            # Vis resultatet i et vindue
            cv2.imshow("Green Screen Effect", result)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    else:
        print(f"Operativsystem '{current_os}' ikke understøttet.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    invisible_green_screen()
