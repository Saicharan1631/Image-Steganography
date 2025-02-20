
# Image Steganography

A Python-based image steganography tool that hides and retrieves secret messages inside images using the LSB (Least Significant Bit) technique. The tool comes with a user-friendly GUI built using Tkinter and ttkbootstrap.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Testing and Compatibility](#testing-and-compatibility)
- [Contributing](#contributing)
  

## Features

- Encode secret messages into images.
- Decode hidden messages from images.
- Uses a secret key for message security.
- Simple and intuitive GUI with ttkbootstrap styling.
- Supports PNG images.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Saicharan1631/Image-Steganography.git
   ```
2. Navigate to the project directory:
   ```bash
   cd image-steganography
   ```
3. Install dependencies:
   ```bash
   pip install Pillow ttkbootstrap
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. **Encoding a message:**
   - Select an image.
   - Enter a secret message.
   - Provide a secret key.
   - Specify an output file name and encode.

3. **Decoding a message:**
   - Select an encoded image.
   - Enter the secret key.
   - Retrieve the hidden message.

## Example

### Encoding:
1. Open the application.
2. Click **Browse** to select an image (e.g., `example.png`).
3. Enter a secret message (e.g., `"This is a secret!"`).
4. Provide a secret key (e.g., `"mysecretkey123"`).
5. Specify an output file name (e.g., `encoded_image.png`).
6. Click **Encode** to save the encoded image.

### Decoding:
1. Open the application.
2. Click **Browse** to select the encoded image (e.g., `encoded_image.png`).
3. Enter the secret key (e.g., `"mysecretkey123"`).
4. Click **Decode** to retrieve the hidden message.

## Screenshots

### Encoding a Message
![Encoding Example](screenshots/encode_example.png)

### Decoding a Message
![Decoding Example](screenshots/decode_example.png)

## Technologies Used

- **Python** - Main programming language.
- **Tkinter** - GUI framework.
- **ttkbootstrap** - Enhanced styling for Tkinter.
- **Pillow** - Image processing.

## Testing and Compatibility

- **Python Version**: Compatible with Python 3.8 and above.
- **Platforms**: Tested on Windows, macOS, and Linux.
- **Dependencies**: Ensure all dependencies are installed using ` Pillow , ttkbootstrap`.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

