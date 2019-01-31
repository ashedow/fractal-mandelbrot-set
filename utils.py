def fractal_calc(x, y):
    """Berechnet den Wert an der Position (x,y). Zurückgegeben
       wird ein Wert zwischen 0 für eindeutige Konvergenz und
       255 für eindeutige Divergenz. Werte zwischen 0 und 255
       geben den Grad der Divergenz an und bilden damit einen
       Divergenzkoeffizienten."""
    # Beginn der Lösung
    c = x + y*1j
    z = 0
    for i in range(256):
        z = z*z + c
        if abs(z) > 2:
            return i
    return 255