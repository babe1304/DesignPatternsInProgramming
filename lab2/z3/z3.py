def mymax(iterable, key=lambda x: x):
    max_x=max_key=None

    for x in iterable:
        if  max_x == None or key(x) > max_key:
            max_x = x
            max_key = key(x)
    return max_x

if __name__=="__main__":
    maxint = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
    print(maxint)

    maxchar = mymax("Suncana strana ulice")
    print(maxchar)

    maxstring = mymax([
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"])
    print(maxstring)

    D = {'burek':8, 'buhtla':5, 'kifla':7, 'krafna':6}
    maxdict = mymax(D, key=D.get)
    print(maxdict)

    maxtup = mymax([('Dominik', 'Babić'), ('Siniša', 'Šegvić'), ('Florijan', 'Sandalj')])
    print(maxtup)
