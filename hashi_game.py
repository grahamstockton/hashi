from tkinter.constants import INSIDE, X
from hashi_generator import Island
import tkinter

# thx to https://stackoverflow.com/questions/16523128/resizing-tkinter-frames-with-fixed-aspect-ratio for help with this function
def set_tkinter_aspect(content_frame, pad_frame, aspect_ratio):

    def enforce_aspect_ratio(event):
        desired_width = event.width
        desired_height = int(event.width / aspect_ratio)

        # if desired_height is too big, make height the larger dimension
        if desired_height > event.height:
            desired_height = event.height
            desired_width = int(event.height * aspect_ratio)

        # place in frame
        content_frame.place(in_=pad_frame, anchor="nw", 
            width=desired_width, height=desired_height)

    pad_frame.bind("<Configure>", enforce_aspect_ratio)

def main():
    WIDTH = 10

    # root instance
    root = tkinter.Tk()

    # set the default font
    root.option_add("*font", "Helvetica, 16")

    # window title and starting width
    root.title("Hashiwokakero")
    root.geometry("800x600")

    ###############################################################
    ################## Grid objects for game board ################
    ###############################################################
    # Create frames for game and buttons
    game_board_outer_frame = tkinter.Frame(root)
    game_board_inner_frame = tkinter.Frame(game_board_outer_frame)

    # place those frames in root, using set_tkinter_aspect to lock aspect ratio
    game_board_outer_frame.place(relheight=1, relwidth=.8, x=0, y=0)
    set_tkinter_aspect(game_board_inner_frame, game_board_outer_frame, aspect_ratio=1)

    # Populate with width*width buttons
    for i in range(WIDTH):
        for j in range(WIDTH):
            new_button = tkinter.Button(game_board_inner_frame, border=1)
            new_button.place(relx=i/WIDTH, rely = j/WIDTH)

    ###############################################################
    ################## Buttons for button_frame ###################
    ###############################################################
    # create button frame and inner frame and anchor it to left
    button_frame = tkinter.Frame(root)
    button_frame.place(height=800, relwidth=.2, relx=.8, rely=.4)

    # button to check answer
    check_button = tkinter.Button(button_frame, text="Check Solution", height=1, background="Gainsboro")
    check_button.place(y=0)

    # button to generate a new game
    new_game_button = tkinter.Button(button_frame, text="New Puzzle", height=1, background="Gainsboro")
    new_game_button.place(y=50)

    # Slider for number of rows
    width_slider = tkinter.Scale(button_frame, from_=8, to=20, length=165, orient="horizontal", label="Number of rows", background="Gray90")
    width_slider.place(y=100)

    # Run main loop of application
    root.mainloop()

if __name__ == '__main__':
    main()