from flask import Flask, render_template, request, redirect, url_for, send_file
from openpyxl import Workbook, load_workbook

app = Flask(__name__)

table = []

new_file = 0
file = 0

def process(table,file):
    print("#######################")
    print(table)
    if(table[0]==""):
        return file
    if(table[0]!=""):
        wb = load_workbook(file)
        ws=wb.get_sheet_by_name('PRACOWNICY')
        ws.append(table)
        wb.save(file)
    return file    

def get_file_from_html(file):
    wb = load_workbook(file)
    return wb


@app.route("/", methods=["POST", "GET"])
def form():
    if request.method == "POST":

        file = request.form["file"]
        user = request.form["name"]
        table.append(user)
        pion = request.form["pion"]
        table.append(pion)
        departament= request.form["dep"]
        table.append(departament)
        zespol= request.form["zesp"]
        table.append(zespol)
        stan= request.form["stan"]
        table.append(stan)
        etat= request.form["liczba_etat"]
        table.append(etat)
        czy= request.form["czy_pracuje"]
        table.append(czy)
        rozp= request.form["rozp"]
        table.append(rozp)
        zak= request.form["zak"]
        table.append(zak)

        new_file = process(table,file)
        table.clear()
        path = new_file

        return send_file(new_file,as_attachment=True)

    else: 
        return render_template("test.html")


print(table)

if __name__ == "__main__":
    app.run()

