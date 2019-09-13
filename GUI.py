
import Teleportation
from tkinter import *

def get_entry_fields():
    number_of_players = e1.get()
    isnumeric = number_of_players.isnumeric()
    int_nop = int(number_of_players)
    small_value = (int_nop < 10)

    if isnumeric:
        if small_value:
            result = Tk()
            result.title("Results")
            result.geometry("850x500")
            result_title = Label(result, text = "Results").pack()
            many_players = Teleportation.run(int_nop,100)
            msg = Message(result, text = many_players)
            msg.pack()
            msg.config(aspect=600)
        else: 
            warning = Tk()
            warning.title("WARNING")
            warning.geometry("300x100")
            many_players="High numbers of players will take up significant amount of computation time"
            msg = Message(warning, text = many_players)
            msg.pack()
            msg.config(aspect=600)
            Button(warning, text='continue', command=get_entry).pack()
            Button(warning, text='QUIT', command=warning.quit).pack()
    else:
        error = Tk()
        error.title("ERROR")
        error.geometry("300x100")
        many_players="You must enter a numerical value"
        msg = Message(error, text = many_players)
        msg.pack()
        msg.config(aspect=600)
        Button(error, text='QUIT', command=error.quit).pack()		


def get_entry(int_nop):
    print(int_nop)
			
   
fenster = Tk()
fenster.title("Communications Game")
fenster.geometry("1500x1000")
logo = PhotoImage(file="logo.gif")
w1 = Label(fenster, image=logo).pack(side="left")
label = Label(fenster, text = "Communications Game Hackathon ETHZ")
label.place(x = 750, y = 50) #Anordnung durch Place-Manager 
rules="Rules: Each player is assigned an arbitrary float number. The total of all numbers will add up to an integer. Every player can send a classical 2 bit value to its neighbour. Determine whether the total is an even or odd number."
msg1 = Message(fenster, text = rules)
msg1.place(x=450, y=100)
msg1.config(aspect=500)
strategy="Each players has two qubits. One qubit is entangled with the qubit of his predecessor, the other one is entangled with the qubit of his successor. The float number that the first player is assigned will then be embedded in the phase of state of the qubit. Via quantum teleportation, the state will be transported to the qubit of the next player. The next player will then rotate the phase by the number he was assigned. The last player will either measure a |1> or |0> state."
msg2 = Message(fenster, text = strategy)
msg2.place(x=450, y=250)
msg2.config(aspect=300)
frame = Frame(fenster)
frame.pack()
##button = Button(frame, text="QUIT", command=frame.quit)
##button.pack(side=LEFT)


Label(fenster, text="Number of Players").place(x = 450, y =600)
#Label(fenster, text="Last Name").place(x = 450, y =170)

e1 = Entry(fenster)
#e2 = Entry(fenster)

e1.place(x = 750, y =600)
#e2.place(x = 560, y =170)

Button(fenster, text='Quit', command=fenster.quit).place(x = 770, y =900)
Button(fenster, text='Compute', command=get_entry_fields).place(x = 1200, y =600)



fenster.mainloop()


