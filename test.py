import mimetypes

mime_type, encoding = mimetypes.guess_type("./message/audio/hello.mp3")
print(mime_type)  # Output: application/pdf