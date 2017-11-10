from tkinter import *
import requests
import xmltodict
import webbrowser

#Opmaak van de GUI
font_text = ('Helvetica', 55, 'bold')
yellow = '#fed633'
blue = '#333399'

#Tkinter GUI's
root = Tk()
root.configure(width=1400, height=500, background=yellow)
root.title('NS Hoofdpagina')

# Zodra de gebruiker klikt op de knop om vertrektijden te bekijken, wordt het hoofdscherm vergroot zodat de zoekbalk te zien is.
def zoekbalk():
    root.configure(width=1400, height=700, background=yellow)

# Hier wordt het vertrekschema aangemaakt elke keer als deze functie wordt aangeroepen.
def vertrekschema():
    global root2
    root2 = Tk()
    root2.configure(height=955, width=840, background='white')
    root2.title('NS Vertrekschema')
    Label(root2, text='Vertrektijd', font=('Helvetica', 12, 'bold'), foreground='black', background='white').place(x=5, y=10)
    Label(root2, text='Vertraging', font=('Helvetica', 12, 'bold'), foreground='black', background='white').place(x=110, y=10)
    Label(root2, text='Bestemming', font=('Helvetica', 12, 'bold'), foreground='black', background='white').place(x=220, y=10)
    Label(root2, text='Spoor', font=('Helvetica', 12, 'bold'), foreground='black', background='white').place(x=400, y=10)
    Label(root2, text='Soort', font=('Helvetica', 12, 'bold'), foreground='black', background='white').place(x=460, y=10)
    Label(root2, text='Via', font=('Helvetica', 12, 'bold'), foreground='black', background='white').place(x=550, y=10)
    Button(root2, text='Sluiten', font=('Helvetica', 10), foreground='black', command=lambda: root2.destroy()).place(x=780, y=0)

# Code voor de knop die de NS site opent.
ns_site = 'https://www.ns.nl/'
def OpenNsSite(ns_site):
    webbrowser.open_new(ns_site)

# Sluit de GUI's af, hierna zal het script ook afsluiten.
def stoppen():
    root.destroy()
    try:
        root2.destroy()
    except:
        None

# Hier wordt een popup bericht gemaakt, deze wordt aangeroepen als de gebruiker een ongeldig station invoert.
def popup_bericht():
    popupbericht = Toplevel()
    popupbericht.wm_title("Foutmelding")
    popupbericht.configure(width=250, height=150)
    l = Label(popupbericht, text="Dit station bestaat niet.\n Probeer het opnieuw.", font=('Helvetica', 14))
    l.place(x=25, y=30)
    b = Button(popupbericht, text="Ok", command=popupbericht.destroy, font=('Helvetica', 14))
    b.place(x=100, y=100)

# De main code voor het hele proces dat de stations zoekt en alle informatie print.
def openvertrekschema(station):
    # Verbinden met API
    username = 'mark.vanmanen@student.hu.nl'
    password = 'uFoczwG8LsttBU8saXxvVEybDJG6LNp39Q7_SCzniijV18aA_wBR4w'
    url = 'https://webservices.ns.nl/ns-api-avt?station=' + station
    response = requests.get(url, auth=(username, password))
    vertrekXML = xmltodict.parse(response.text)

    # Elke trein + plus informatie van die trein komt 30 pixels onder de vorige te staan.
    var_y = 30

    # Er wordt gekeken of ActueleVertrekTijden in de xmltodict staat, die zal er bij elk station ALTIJD staan, behalve als het station niet bestaat.
    # Oftewel dit kijkt ernaar of de gebruiker wel daadwerkelijk een bestaand station heeft ingevuld.
    if 'ActueleVertrekTijden' in vertrekXML:
        vertrekschema()

        # Doormiddel van een for loop gaat hij elke trein af in het lijstje en laat dat in het schema zien.
        for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            if 'RouteTekst' in vertrek:
                Label(root2, text=vertrek['VertrekTijd'][11:16], font=('Helvetica', 12), anchor='w', foreground='black', background='white').place(x=5, y=var_y)
                try:
                    Label(root2, text=vertrek['VertrekVertragingTekst'], font=('Helvetica', 12, 'bold'), anchor='w', foreground='red', background='white').place(x=110, y=var_y)
                except:
                    None
                Label(root2, text=vertrek['EindBestemming'], font=('Helvetica', 12), anchor='w', foreground='black', background='white').place(x=220, y=var_y)
                Label(root2, text=vertrek['TreinSoort'], font=('Helvetica', 12), anchor='w', foreground='black', background='white').place(x=460, y=var_y)
                Label(root2, text=vertrek['RouteTekst'], font=('Helvetica', 12), anchor='w', foreground='black', background='white').place(x=550, y=var_y)
                if vertrek['VertrekSpoor']['@wijziging'] == 'true':
                    Label(root2, text=vertrek['VertrekSpoor']['#text'], font=('Helvetica', 12), anchor='w',foreground='red', background='white').place(x=400, y=var_y)
                else:
                    Label(root2, text=vertrek['VertrekSpoor']['#text'], font=('Helvetica', 12), anchor='w',foreground='black', background='white').place(x=400, y=var_y)
                var_y += 20
            elif 'RouteTekst' not in vertrek:
                Label(root2, text=vertrek['VertrekTijd'][11:16], font=('Helvetica', 12), anchor='w', foreground='black', background='white').place(x=5, y=var_y)
                try:
                    Label(root2, text=vertrek['VertrekVertragingTekst'], font=('Helvetica', 12, 'bold'), anchor='w', foreground='red', background='white').place(x=110, y=var_y)
                except:
                    None
                Label(root2, text=vertrek['EindBestemming'], font=('Helvetica', 12), anchor='w', foreground='black', background='white').place(x=220, y=var_y)
                Label(root2, text=vertrek['VertrekSpoor']['#text'], font=('Helvetica', 12), anchor='w', foreground='black', background='white').place(x=400, y=var_y)
                Label(root2, text=vertrek['TreinSoort'], font=('Helvetica', 12), anchor='w', foreground='black', background='white').place(x=460, y=var_y)
                var_y += 20
    # Als het station niet bestaat ontstaat een popup met een foutmelding, zodra de gebruiker deze wegklikt kan er opnieuw gezocht worden naar een station.
    else:
        popup_bericht()

#Invoer balkje
station = StringVar()
invoerStation = Entry(root, textvariable=station, font=('Helvetica', 15))
invoerStation.place(x=555, y=560)

#Inhoud van de hoofdpagina
Label(root, text='Beste reiziger, welkom bij de NS.', font=font_text, foreground=blue, background=yellow).place(x=150, y=50)
Label(root, text='Gemaakt door: Mark van Manen, Xandra Mentink, Floris Roest, Thijs Rijders en Stef Bos.', font=('Helvetica', 10), foreground='black', background=yellow).place(x=0, y=0)
Label(root, text='Versie 2.1', font=('Helvetica', 12, 'bold'), foreground='black', background=yellow).place(x=1320, y=675)
Label(root, text='Voer het station in:', font=('Helvetica', 15), foreground='black', background=yellow).place(x=580, y=530)

#Knoppen
knopWebsite = Button(master=root, text='Open website van de NS', background=blue, foreground='white', font=('Helvetica', 15, 'bold'), command=lambda: OpenNsSite(ns_site))
knopSluiten = Button(master=root, text='Venster sluiten', background=blue,foreground='white', font=('Helvetica', 15, 'bold'), command=lambda: stoppen())
knopVertrektijden = Button(master=root, text='Vertrektijden bekijken', background=blue, foreground='white', font=('Helvetica', 15, 'bold'), command=lambda: zoekbalk())
knopZoeken = Button(master=root, text='zoeken', background=blue, foreground='white', font=('Helvetica', 12), command=lambda: openvertrekschema(station.get()))
knopWebsite.place(x=300, y=300)
knopSluiten.place(x=600, y=300)
knopVertrektijden.place(x=800, y=300)
knopZoeken.place(x=630, y=590)

root.mainloop()

try:
    root2.mainloop()
except:
    None
