# Build Code Nimble

To build from source you need to clone this repo:
`git clone https://github.com/HojdaAdelin/CodeNimble.git`

1. You need to download these libraries:
    - customtkinter
    - tkinter
    - CTkMenuBar
    - CTkTable
    - Pywinstyles
    ```sh
    pip install customtkinter
    pip install tkinter
    pip install CTkMenuBar
    pip install CTkTable
    pip install pywinstyles
    pip install black
    ```

2. Fiind the source of the custom tkinter library
It should be like this: `C:/Users/{user}/AppData/Local/Programs/Python/Python311/Lib/site-packages/customtkinter` and copy this

3. Put the custom tkinter source in the [build-file](build_info/build.md) in "[Path to customtkinter library]"

4. Open a CMD in the Code Nimble source folder and run the code from [build-file](build_info/build.md)

5. Open the dist folder created in the source and run CodeNimble.exe from the CodeNimble folder