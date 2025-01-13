from django.shortcuts import render, redirect
import qrcode
import numpy as np
import cv2
from io import BytesIO
from urllib.parse import urlparse
import base64


def qr_generator_scanner(request):
    qr_image = None
    scanned_text = None

    if request.method == "POST":
        # Check if it's a QR code generation request
        if "generate" in request.POST:
            url = request.POST.get("url", "")
            if url:
                # Generate the QR code
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image(fill="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                qr_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Check if it's a QR code scanning request
        elif "scan" in request.POST:
            uploaded_file = request.FILES.get("qr_image", None)
            if uploaded_file:
                # Read uploaded image using OpenCV
                file_bytes = BytesIO(uploaded_file.read())
                file_bytes.seek(0)
                img = cv2.imdecode(
                    np.frombuffer(file_bytes.read(), np.uint8), cv2.IMREAD_COLOR
                )

                # Use OpenCV's QRCodeDetector to decode the QR code
                detector = cv2.QRCodeDetector()
                data, bbox, _ = detector.detectAndDecode(img)

                if data:
                    # Validate if the decoded data is a valid URL
                    parsed_url = urlparse(data)
                    if parsed_url.scheme and parsed_url.netloc:
                        return redirect(data)  # Redirect to the scanned URL
                    else:
                        scanned_text = f"Scanned Data: {data}"
                else:
                    scanned_text = "No QR code detected or invalid QR code."

    return render(
        request,
        "home.html",
        {"qr_image": qr_image, "scanned_text": scanned_text},
    )
