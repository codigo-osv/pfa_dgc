from string import upper

from functions import psycodb
from psycopg2.extensions import AsIs


def isPassengerCar(strVehicle):
    return upper(strVehicle) in ['AMBULANCIA','CAMIONETA','TAXI/REMIS','AUTO']


def isPassengerTransport(strVehicle):
    return upper(strVehicle) in ['TRANSPORTE ESCOLAR','TRANSPORTE PUBLICO','OMNIBUS / MINIBUS']


def isCargoTransport(strVehicle):
    return upper(strVehicle) in ['TRANSPORTE DE CARGAS / GRUA','CAMION','AUTOBOMBA','UTILITARIO','VEHICULO RURAL']


def isPedestrian(strVehicle):
    return upper(strVehicle) in ['PEATON','PATINETA']


def isBicycle(strVehicle):
    return upper(strVehicle) in ['BICICLETA']


def isMotoCycle(strVehicle):
    return upper(strVehicle) in ['MOTO','CUATRICICLO']


def isHorseman(strVehicle):
    return upper(strVehicle) in ['TRACCION A SANGRE']


def isTrain(strVehicle):
    return upper(strVehicle) in ['TREN / SUBTE','TRANVIA']


def isNoData(strVehicle):
    return strVehicle in [None,'','NULL','sin datos','no hay datos']


def isOther(strVehicle):
    return not (isPassengerCar(strVehicle) | isPassengerTransport(strVehicle) | isCargoTransport(strVehicle) |\
           isPedestrian(strVehicle) | isBicycle(strVehicle) | isMotoCycle(strVehicle) |\
            isHorseman(strVehicle) | isTrain(strVehicle) | isNoData(strVehicle))


def vehicleTypeRecoded(strVehicle):
    res = 'NULL'
    if isNoData(strVehicle): pass
    elif isPassengerTransport(strVehicle): res = 'transportePasajeros'
    elif isCargoTransport(strVehicle): res = 'transporteCarga'
    elif isPedestrian(strVehicle): res = 'peaton'
    elif isBicycle(strVehicle): res = 'bicicleta'
    elif isMotoCycle(strVehicle): res = 'moto'
    elif isHorseman(strVehicle): res = 'traccionASangre'
    elif isTrain(strVehicle): res = 'tren'
    elif isPassengerCar(strVehicle): res = 'automovil'
    elif isOther(strVehicle): res = 'otro'
    return res


def vehicleTypeForCollisions(strVehicle):
    res = 'NULL'
    if isNoData(strVehicle): pass
    elif upper(strVehicle) in ['AUTO','TRANSPORTE DE CARGAS / GRUA','AMBULANCIA',
                               'CAMIONETA','TAXI/REMIS','VEHICULO RURAL','TRANSPORTE PUBLICO',
                               'VEHICULO RURAL','TRANSPORTE ESCOLAR','AUTOBOMBA','CAMION',
                               'UTILITARIO','OMNIBUS / MINIBUS']:
        res = 'vehiculo'
    elif upper(strVehicle) in ['MOTO','CUATRICICLO']: res = 'moto'
    elif upper(strVehicle) in ['PEATON','PATINETA']: res = 'peaton'
    elif upper(strVehicle) in ['BICICLETA']: res = 'bicicleta'
    elif upper(strVehicle) in ['TRACCION A SANGRE']: res = 'traccionASangre'
    elif upper(strVehicle) in ['TREN / SUBTE','TRANVIA']: res = 'tren'
    return res


def isVehicleForCollisions(strVehicle):
    res = False
    if isPassengerCar(strVehicle) | isPassengerTransport(strVehicle) |\
            isCargoTransport(strVehicle) | isMotoCycle(strVehicle):
        res = True
    return res


def collisionType(tuplIDAccAndVehicTpList):
    res = 'NULL'
    participants = participantsForCollisionType(tuplIDAccAndVehicTpList[1])
    if participants.__len__() < 2:
        pass
    elif (participants.count('vehiculo') + participants.count('moto')) > 2:
        res = 'multiple'
    elif participants.count('vehiculo') == 2:
        res = 'vehiculo - vehiculo'
    elif ('vehiculo' in participants) and ('moto' in participants):
        res = 'vehiculo - moto'
    elif ('vehiculo' in participants) and ('peaton' in participants):
        res = 'vehiculo - peaton'
    elif ('vehiculo' in participants) and ('bicicleta' in participants):
        res = 'vehiculo - bicicleta'
    elif ('vehiculo' in participants) and ('traccionASangre' in participants):
        res = 'vehiculo - traccionASangre'
    elif participants.count('moto') == 2:
        res = 'moto - moto'
    elif ('moto'  in participants) and ('peaton' in participants):
        res = 'moto - peaton'
    elif ('moto'  in participants) and ('bicicleta' in participants):
        res = 'moto - bicicleta'
    elif ('moto'  in participants) and ('traccionASangre' in participants):
        res = 'moto - traccionASangre'
    elif participants.count('bicicleta') == 2:
        res = 'bicicleta - bicicleta'
    elif ('bicicleta' in participants) and ('peaton' in participants):
        res = 'bicicleta - peaton'
    elif 'tren' in participants:
        res = 'tren'
    else:
        res = 'otro'
    return (tuplIDAccAndVehicTpList[0], res)


def participantsForCollisionType(vehicLst):
    res = []
    for vehic in vehicLst:
        recodedVehicle = vehicleTypeForCollisions(vehic)
        if not isNoData(recodedVehicle):
            res.append(recodedVehicle)
    return res


def ageRange(intAge):
    res = 'NULL'
    if (intAge>=0) & (intAge<5): res = 1
    elif (intAge>=5) & (intAge<15): res = 2
    elif (intAge>=15) & (intAge<25): res = 3
    elif (intAge>=25) & (intAge<35): res = 4
    elif (intAge>=35) & (intAge<45): res = 5
    elif (intAge>=45) & (intAge<55): res = 6
    elif (intAge>=55) & (intAge<65): res = 7
    elif (intAge>=65) & (intAge<75): res = 8
    elif (intAge>=75) & (intAge<150): res = 9
    return res


def genAgeRange(strNewColName):
    #preconditions: destination num column exists in the database, num column edad exists, column id is pk.
    cur = psycodb.cursor()
    cur.execute("select id from victimas;")
    ids = sorted([x[0] for x in cur.fetchall()])
    for id in ids:
        cur.execute("select edad from victimas where id = %s;", (id,))
        ageR = ageRange(cur.fetchone()[0])
        cur.execute("update victimas set %s = %s where id = %s;", (AsIs(strNewColName),AsIs(ageR),id))
        psycodb.commit()


def genVehicleTypeRecoded(strNewColName):
    #preconditions: destination text column exists in the database, text column tipo exists, column id is pk.
    cur = psycodb.cursor()
    cur.execute("select id from victimas;")
    ids = sorted([x[0] for x in cur.fetchall()])
    for id in ids:
        cur.execute("select tipo from victimas where id = %s;", (id,))
        newType = vehicleTypeRecoded(cur.fetchone()[0])
        cur.execute("update victimas set %s = %s where id = %s;", (AsIs(strNewColName),newType,id))
        psycodb.commit()