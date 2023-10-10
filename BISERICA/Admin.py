import tkinter as tk
from tkinter import messagebox
import re
from tkinter import simpledialog
import fileinput
from reportlab.pdfgen import canvas
import datetime
import os


class FuneralApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Program pentru cimitir")
        self.state("zoomed")  # maximize the window
        self.resizable(False, False)
        self.create_widgets()
        self.counter = 0  # initialize the counter to zero
        self.load_counter()  # load the counter from the file
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.text_area = tk.Text(self)
        self.text_area.pack(side="top", fill="both", expand=True)
        # Display the entire data in the Text widget with line numbers
        scrollbar = tk.Scrollbar(self.text_area, command=self.text_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=scrollbar.set)
        with open("data.txt", "r") as f:
            content = f.readlines()
            self.text_area.delete("1.0", tk.END)
            for i, line in enumerate(content):
                line_number = i + 1
                self.text_area.insert(tk.END, f"{line_number:<5}{line}")

        self.text_area.configure(state="disabled")


    def on_closing(self):
        if messagebox.askokcancel("Warning", "Esti sigur ca vrei sa parasesti programul?"):
            self.destroy()

    def load_counter(self):
        try:
            with open("contor.txt", "r") as f:
                content = f.read().strip()
                if content:
                    self.counter = int(content)
        except FileNotFoundError:
            pass

    def save_counter(self):
        with open("contor.txt", "w") as f:
            f.write(str(self.counter))

    def increment_counter(self):
        self.counter += 1
        self.save_counter()

    def create_widgets(self):
        # Create the top frame for the title
        title_frame = tk.Frame(self)
        title_frame.pack(side="top", fill="x", pady=0)

        

        # Create the left frame for the name and date input
        input_frame = tk.Frame(self)
        input_frame.pack(side="left", fill="both", padx=50, pady=50)

        # Create a label for the deceased name
        name_label = tk.Label(input_frame, text="Numele decedatei/ului:", font=("Arial", 11))
        name_label.pack(pady=5)

        # Create an entry widget for the deceased name
        self.name_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.name_entry.pack(pady=5)

        # Create a label for the funeral date and time
        date_label = tk.Label(input_frame, text="Data si timpul pentru inmormantare:", font=("Arial", 11))
        date_label.pack(pady=5)

        # Create an entry widget for the funeral date and time
        self.date_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.date_entry.pack(pady=5)

        # Create a label for the deceased's adress
        adress_label = tk.Label(input_frame, text="Adresa decedatei/ului:", font=("Arial", 11))
        adress_label.pack(pady=5)

        # Create an entry widget for the deceased's adress
        self.adress_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.adress_entry.pack(pady=5)

        # Create a label for the deceased's number
        number_label = tk.Label(input_frame, text="Numarul de locuri:", font=("Arial", 11))
        number_label.pack(pady=5)

        # Create an entry widget for the deceased's number
        self.number_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.number_entry.pack(pady=5)

        # Create a label for the deceased's cash
        cash_label = tk.Label(input_frame, text="Taxa:", font=("Arial", 11))
        cash_label.pack(pady=5)

        # Create an entry widget for the deceased's cash
        self.cash_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.cash_entry.pack(pady=5)

        # Create a label for the deceased's cash (paid)
        cash_paid_label = tk.Label(input_frame, text="Taxa platita:", font=("Arial", 11))
        cash_paid_label.pack(pady=5)

        # Create an entry widget for the deceased's cash (paid)
        self.cash_paid_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.cash_paid_entry.pack(pady=5)

        # Create a label for the deceased's spawn
        spawn_label = tk.Label(input_frame, text="Locul inmormantarii:", font=("Arial", 11))
        spawn_label.pack(pady=5)

        # Create an entry widget for the deceased's spawn
        self.spawn_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.spawn_entry.pack(pady=5)





        # Create a button to save the data
        save_button = tk.Button(input_frame, text="Salvare", font=("Arial", 11), command=self.save)
        save_button.pack(pady=10)

        # Create a button to exit the program
        exit_button = tk.Button(input_frame, text="Exit", font=("Arial", 11), command=self.exit_program)
        exit_button.pack(pady=10)

        # Create the right frame for the search and modify options
        options_frame = tk.Frame(self)
        options_frame.pack(side="right", fill="both", padx=50, pady=50)

        # Create a label for the search input
        search_label = tk.Label(options_frame, text="Cauta persoane:", font=("Arial", 17))
        search_label.pack(pady=10)

        # Create an entry widget for the search text input
        self.search_entry = tk.Entry(options_frame, font=("Arial", 11))
        self.search_entry.pack(pady=5)

        # Create a button to search for funeral data
        search_button = tk.Button(options_frame, text="Cauta", font=("Arial", 11), command=self.search)
        search_button.pack(pady=10)

        # Create a label to display the search results
        self.search_results = tk.Label(options_frame, font=("Arial", 11))
        self.search_results.pack(pady=10)

        # Create a button to modify the data
        modify_button = tk.Button(options_frame, text="Modifica date", font=("Arial", 11), command=self.modify_data)
        modify_button.pack(pady=10)

        # Create a button to delete the data
        modify_button = tk.Button(options_frame, text="Sterge date", font=("Arial", 11), command=self.modify_data_delete)
        modify_button.pack(pady=10)

        # Create a button to erase all input fields
        clear_button = tk.Button(input_frame, text="Clear", font=("Arial", 11), command=self.clear_fields)
        clear_button.pack(pady=10)

        # Create a button to import dates from file.txt to data.txt
        import_button = tk.Button(options_frame, text="Import", font=("Arial", 11), command=lambda: self.import_btn("file.txt"))
        import_button.pack(pady=5)

        # create a button to export the data
        export_button = tk.Button(input_frame, text="Export all data", font=("Arial", 11), command=self.export_data)
        export_button.pack(pady=10)

        # create a button to export the filtered data
        export_filter_button = tk.Button(options_frame, text="Export filter data", font=("Arial", 11), command=self.export_filter_data)
        export_filter_button.pack(pady=10)


    def exit_program(self):
        if messagebox.askokcancel("Exit Program", "Esti sigur ca vrei sa parasesti programul?"):
            self.destroy()

    def save(self):
        # Get the name and date input values
        name = self.name_entry.get()
        date = self.date_entry.get()
        adress = self.adress_entry.get()
        number = self.number_entry.get()
        cash = self.cash_entry.get()
        cash_paid = self.cash_paid_entry.get()
        spawn = self.spawn_entry.get()

        # Check if any fields are empty
        if not all((name, date, adress, number, cash, cash_paid, spawn)):
            messagebox.showwarning("Empty Fields", "Toate campurile trebuie completate!")
            return 

        # Write the data to a file
        with open("data.txt", "a") as file:
            file.write(f"{name}, {date}, {adress}, {number}, {cash}, {cash_paid}, {spawn}\n")

        # Clear the input fields
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.adress_entry.delete(0, tk.END)
        self.number_entry.delete(0, tk.END)
        self.cash_entry.delete(0, tk.END)
        self.cash_paid_entry.delete(0, tk.END)
        self.spawn_entry.delete(0, tk.END)

        # Display the entire data in the Text widget with line numbers
        self.text_area.configure(state="normal")
        with open("data.txt", "r") as f:
            content = f.readlines()
            self.text_area.delete("1.0", tk.END)
            for i, line in enumerate(content):
                line_number = i + 1
                self.text_area.insert(tk.END, f"{line_number:<5}{line}")
        self.text_area.configure(state="disabled")

        self.increment_counter()  # increment the counter and save the updated value

        messagebox.showinfo("Data Saved", "Datele s-au salvat corect!")

        return 

    
    '''
    def search(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Eroare la cautare", "Va rugam sa introduceti un nume pentru a cauta!")
            return

        found = False
        results = ""
        with open("data.txt", "r") as file:
            for i, line in enumerate(file):
                if re.search(search_term, line):
                    results += f"Linia {i+1}: {line}"
                    found = True
        
        if found:
            self.search_results.config(text=results)
        else:
            self.search_results.config(text="Nu s-au gasit rezultate.")
            messagebox.showwarning("Eroare la cautare", "Nu s-au gasit rezultate.")
    '''
    def search(self):
        search_term = self.search_entry.get()
        query = self.search_entry.get() #.lower()
        if not search_term:
            messagebox.showwarning("Eroare la cautare", "Va rugam sa introduceti un nume pentru a cauta!")
            return

        found = False
        results = ""
        with open("data.txt", "r") as file:
            for i, line in enumerate(file):
                if re.search(search_term, line) and query in line: # and query in line.lower()
                    results += f"Linia {i+1}: {line}"
                    found = True
        #            
        if not results:
            messagebox.showinfo("Niciun rezultat", f"Nu s-a gasit niciun rezultat pentru '{query}'.")
            return

        '''
        # Create a new window to display the search results
        search_results_window = tk.Toplevel(self)
        search_results_window.title(f"Rezultatele cautarii pentru: '{query}'")

        # Create a text widget to display the search results
        search_results_text = tk.Text(search_results_window, font=("Arial", 11))
        search_results_text.pack(expand=True, fill="both")

        # Insert each match into the text widget
        for result in results.splitlines():
            search_results_text.insert("end", result + "\n")


        # Disable editing in the text widget
        search_results_text.config(state="disabled")
        #
        '''

        if found:
            self.search_results.config(text=results)
        else:
            self.search_results.config(text="Nu s-au gasit rezultate.")
            messagebox.showwarning("Eroare la cautare", "Nu s-au gasit rezultate.")

        def save_results(results):
            # specify the folder path where you want to save the PDF file
            folder_path = "Exporturi"

            # create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            filename = f"search_results_for_{query}.txt" #datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            #filename = canvas.Canvas(f"search_results_{query}.pdf")
            #filename = os.path.join(folder_path, f"{query}.pdf")
            #pdf_file = canvas.Canvas(filename)

            with open(os.path.join(folder_path, filename), "w") as file:
                file.write(results)
            messagebox.showinfo("Salvare reusita", f"Rezultatele au fost salvate in fisierul {filename}.")

        # Create a new window to display the search results
        search_results_window = tk.Toplevel(self)
        search_results_window.title(f"Rezultatele cautarii pentru: '{query}'")

        # Create a text widget to display the search results
        search_results_text = tk.Text(search_results_window, font=("Arial", 11))
        search_results_text.pack(expand=True, fill="both")

        # Insert each match into the text widget
        for result in results.splitlines():
            search_results_text.insert("end", result + "\n")

        # Add a button to save the search results
        save_button = tk.Button(search_results_window, text="Salveaza rezultatele", command=lambda: save_results(results))
        save_button.pack(pady=10)
    '''
    def search(self):
        query = self.search_entry.get().lower()
        results = []
        with open("data.txt", "r") as f:
            for line in f:
                if query in line.lower():
                    results.append(line.strip())

        if not results:
            messagebox.showinfo("No results", f"No results found for '{query}'.")
            return

        # Create a new window to display the search results
        search_results_window = tk.Toplevel(self)
        search_results_window.title(f"Search results for '{query}'")

        # Create a text widget to display the search results
        search_results_text = tk.Text(search_results_window, font=("Arial", 11))
        search_results_text.pack(expand=True, fill="both")

        # Insert each match into the text widget
        for result in results:
            search_results_text.insert("end", result + "\n")

        # Disable editing in the text widget
        search_results_text.config(state="disabled")
    '''


    def modify_data(self):
        # Open the data file for reading
        with open("data.txt", "r") as file:
            data = file.readlines()

        # Prompt the user for the line number to be modified
        line_num = tk.simpledialog.askinteger("Modificare date registru", "Introdu linia pe care vrei sa o modifici (incepand de la 1):")

        if line_num is not None and line_num > 0 and line_num <= len(data):
            # Prompt the user for the new data
            new_data = tk.simpledialog.askstring("Modificare date registru", "Introdu noi date pentru linia {}: ".format(line_num))

            if new_data:
                # Replace the specified line with the new data
                data[line_num-1] = new_data + "\n"

                # Write the updated data to the file
                with open("data.txt", "w") as file:
                    file.writelines(data)

                # Update the search results label
                self.search_results.config(text="Data modificata!")
            else:
                self.search_results.config(text="Te rog sa introduci noi date.")
        else:
            self.search_results.config(text="Numar de linie invalid.")

        # Display the entire data in the Text widget with line numbers
        self.text_area.configure(state="normal")
        with open("data.txt", "r") as f:
            content = f.readlines()
            self.text_area.delete("1.0", tk.END)
            for i, line in enumerate(content):
                line_number = i + 1
                self.text_area.insert(tk.END, f"{line_number:<5}{line}")
        self.text_area.configure(state="disabled")

    def modify_data_delete(self):
        # Open the data file for reading
        with open("data.txt", "r") as file:
            data = file.readlines()

        # Prompt the user for the line number to be modified
        line_num = simpledialog.askinteger("Modificare date registru", "Introdu linia pe care vrei sa o stergi:")

        # Check if the line number is valid
        if line_num is not None and 0 < line_num <= len(data):
            # Remove the line from the data list
            removed_line = data.pop(line_num - 1)

            # Open the data file for writing
            with open("data.txt", "w") as file:
                # Write the modified data to the file
                file.write("".join(data))

            # Decrement the save counter
            self.counter -= 1
            self.save_counter()

            # Show a message box with the removed line
            messagebox.showinfo("Date sterse", f"Linia introdusa a fost stearsa:\n\n{removed_line.strip()}")
        else:
            # Show an error message if the line number is not valid
            messagebox.showerror("Eroare", "Numarul de linie invalid.")

        # Display the entire data in the Text widget with line numbers
        self.text_area.configure(state="normal")
        with open("data.txt", "r") as f:
            content = f.readlines()
            self.text_area.delete("1.0", tk.END)
            for i, line in enumerate(content):
                line_number = i + 1
                self.text_area.insert(tk.END, f"{line_number:<5}{line}")
        self.text_area.configure(state="disabled")

    def clear_fields(self):
        # Clear the text in the name and date entry widgets
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        # Clear the text in the search entry widget
        self.search_entry.delete(0, tk.END)
        # Clear the text in the search results label
        self.search_results.config(text="")
        self.adress_entry.delete(0, tk.END)
        self.number_entry.delete(0, tk.END)
        self.cash_paid_entry.delete(0, tk.END)
        self.cash_entry.delete(0, tk.END)
        self.spawn_entry.delete(0, tk.END)

    def import_dates(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()

        with open("data.txt", "a") as f:
            for line in lines:
                f.write(line.strip() + "\n")

    '''
    def import_btn(self, file_name):
        try:
            with open(file_name, "r") as file:
                data = file.read().strip()
                with open("data.txt", "a") as outfile:
                    outfile.write(data + "\n")
                messagebox.showinfo("Data Imported", "Datele s-au importat cu succes!")
            # Increment the counter and save the updated value
            self.increment_counter()
            
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "Fisierul nu a fost gasit!")
    '''
    def import_btn(self, file_name):
        try:
            # Open the file.txt and read its content
            with open(file_name, 'r') as file:
                file_data = file.read()

            # Add newline character to the end of each line
            file_data = file_data.replace('\r\n', '\n').replace('\r', '\n')
            file_data = file_data.rstrip()  # remove any trailing whitespace

            # Write the data to data.txt
            with open('data.txt', 'a') as f:
                f.write(file_data)
                f.write('\n')  # add a new line character at the end of the file

            with open(file_name, "r") as file:
                lines = file.readlines()
                num_lines = len(lines)
                self.counter += num_lines
                self.save_counter()
                messagebox.showinfo("Import", f"{num_lines} date au fost importate cu succes!")
        except FileNotFoundError:
            messagebox.showerror("Error", "Fisierul nu a fost gasit.")

        # Display the entire data in the Text widget with line numbers
        self.text_area.configure(state="normal")
        with open("data.txt", "r") as f:
            content = f.readlines()
            self.text_area.delete("1.0", tk.END)
            for i, line in enumerate(content):
                line_number = i + 1
                self.text_area.insert(tk.END, f"{line_number:<5}{line}")
        self.text_area.configure(state="disabled")

    def export_data(self):
        # specify the folder path where you want to save the PDF file
        folder_path = "Exporturi"

        # create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # create a new PDF file
        pdf_file = canvas.Canvas(os.path.join(folder_path, "export_data.pdf"))
        #pdf_file = canvas.Canvas("Exports/export_data.pdf")

        # open the data.txt file and read the contents
        with open("data.txt", "r") as f:
            data = f.read().splitlines()

        # write the data to the PDF file
        y = 750
        for line in data:
            pdf_file.drawString(100, y, line)
            y -= 12  # move to the next line

        # save and close the PDF file
        pdf_file.save()

        messagebox.showinfo("Data Exported", "Datele s-au exportat corect!")

    def export_filter_data(self):
        pass

    def display_results_window(self):
        results_window = tk.Toplevel(self)
        results_window.title("Search Results")
        results_window.geometry("400x400")
        results_text = tk.Text(results_window, font=("Arial", 11))
        results_text.pack(fill="both", expand=True)
        results_text.insert("end", self.search_results["text"])
        results_text.configure(state="disabled")


if __name__ == "__main__":
    app = FuneralApp()
    app.mainloop()