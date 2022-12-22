import csv
import datetime as dt
import numpy as np
import os
import pandas as pd
import sqlite3

def dbSetup(dbName):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
        CREATE TABLE consoles
        (
            console_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            console_name VARCHAR NOT NULL
        );''')
    
    cursor.execute('''
        CREATE TABLE platforms
        (
            platform_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            platform_name VARCHAR NOT NULL,
            description VARCHAR,
            console INTEGER REFERENCES consoles(console_id) NOT NULL
        );''')
    
    cursor.execute('''
        CREATE TABLE software_series
        (
            software_series_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            series_name VARCHAR NOT NULL,
            description VARCHAR,
            parent_series INTEGER REFERENCES software_series(software_series_id)
        );''')

    cursor.execute('''
        CREATE TABLE bundles
        (
            bundle_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            bundle_name VARCHAR NOT NULL,
            description VARCHAR
        );''')
    
    cursor.execute('''
        CREATE TABLE softwares
        (
            software_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            software_name VARCHAR NOT NULL,
            software_edition VARCHAR,
            platform INTEGER REFERENCES platforms(platform_id) NOT NULL,
            legal BOOLEAN NOT NULL DEFAULT(1),
            error BOOLEAN NOT NULL DEFAULT(0),
            shame BOOLEAN NOT NULL DEFAULT(0),
            date_acquired DATE,
            cost DECIMAL NOT NULL DEFAULT(0),
            value DECIMAL NOT NULL DEFAULT(0),
            series INTEGER REFERENCES software_series(software_series_id),
            bundle INTEGER REFERENCES bundles(bundle_id)
        );''')

    cursor.execute('''
        CREATE TABLE software_digital
        (
            software_digital_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            software INTEGER REFERENCES softwares(software_id) UNIQUE NOT NULL,
            file_size_bytes DECIMAL,
            directory VARCHAR,
            platform_software_identifier VARCHAR
        );''')

    cursor.execute('''
        CREATE TABLE software_time
        (
            software_time_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            software INTEGER REFERENCES softwares(software_id) UNIQUE NOT NULL,
            spent_mins DECIMAL NOT NULL DEFAULT(0),
            completionist_mins DECIMAL
        );''')

    cursor.execute('''
        CREATE TABLE software_achievements
        (
            software_achievement_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            software INTEGER REFERENCES softwares(software_id) UNIQUE NOT NULL,
            earned INTEGER NOT NULL DEFAULT(0),
            total INTEGER NOT NULL DEFAULT(1)
        );''')

    cursor.execute('''
        CREATE TABLE states
        (
            state_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            state_name VARCHAR UNIQUE NOT NULL,
            description VARCHAR
        );''')

    cursor.execute('''
        CREATE TABLE media_types
        (
            media_type_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            platform INTEGER REFERENCES platforms(platform_id) NOT NULL,
            media_type_name VARCHAR NOT NULL,
            description VARCHAR,
            length_mm DECIMAL,
            width_mm DECIMAL,
            height_mm DECIMAL
        );''')

    cursor.execute('''
        CREATE TABLE software_physical
        (
            software_physical_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            software INTEGER REFERENCES softwares(software_id) UNIQUE NOT NULL,
            got_state INTEGER REFERENCES states(state_id) NOT NULL,
            current_state INTEGER REFERENCES states(state_id) NOT NULL,
            media_type INTEGER REFERENCES media_types(media_type_id)-- NOT NULL
        );''')

    cursor.execute('''
        CREATE TABLE addons
        (
            addon_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            software INTEGER REFERENCES softwares(software_id) NOT NULL,
            date_acquired DATE,
            cost DECIMAL NOT NULL DEFAULT(0),
            value DECIMAL NOT NULL DEFAULT(0),
            file_size_bytes DECIMAL,
            directory VARCHAR
        );''')

    cursor.execute('''
        CREATE TABLE boxes
        (
            box_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            box_name VARCHAR NOT NULL,
            description VARCHAR,
            got_state INTEGER REFERENCES states(state_id) NOT NULL,
            current_state INTEGER REFERENCES states(state_id) NOT NULL,
            date_acquired DATE,
            cost DECIMAL NOT NULL DEFAULT(0),
            value DECIMAL NOT NULL DEFAULT(0),
            bundle INTEGER REFERENCES bundles(bundle_id)
        );''')

    cursor.execute('''
        CREATE TABLE digital_platforms
        (
            digital_platform_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            digital_platform_name VARCHAR NOT NULL,
            description VARCHAR,
            platform INTEGER REFERENCES platforms(platform_id),
            file_size_bytes DECIMAL,
            directory VARCHAR
        );''')

    cursor.execute('''
        CREATE TABLE hardware_types
        (
            hardware_type_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            type_name VARCHAR NOT NULL
        );''')

    cursor.execute('''
        CREATE TABLE hardwares
        (
            hardware_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            hardware_name VARCHAR NOT NULL,
            description VARCHAR,
            serial_number VARCHAR,
            date_acquired DATE,
            error BOOLEAN NOT NULL DEFAULT(0),
            console INTEGER REFERENCES consoles(console_id),
            got_state INTEGER REFERENCES states(state_id) NOT NULL,
            current_state INTEGER REFERENCES states(state_id) NOT NULL,
            cost DECIMAL NOT NULL DEFAULT(0),
            value DECIMAL NOT NULL DEFAULT(0),
            hardware_type INTEGER REFERENCES hardware_types(hardware_type_id) NOT NULL,
            bundle INTEGER REFERENCES bundles(bundle_id)
        );''')

    cursor.execute('''
        CREATE TABLE paper_materials
        (
            material_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            material_name VARCHAR NOT NULL,
            description VARCHAR,
            got_state INTEGER REFERENCES states(state_id) NOT NULL,
            current_state INTEGER REFERENCES states(state_id) NOT NULL,
            date_acquired DATE,
            cost DECIMAL NOT NULL DEFAULT(0),
            value DECIMAL NOT NULL DEFAULT(0),
            bundle INTEGER REFERENCES bundles(bundle_id)
        );''')

    cursor.execute('''
        CREATE TABLE ttl_series
        (
            ttl_series_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            ttl_series_name VARCHAR NOT NULL,
            software_series INTEGER REFERENCES software_series(software_series_id)-- NOT NULL
        );''')

    cursor.execute('''
        CREATE TABLE ttl_types
        (
            ttl_type_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            type_name VARCHAR NOT NULL,
            ttl_series INTEGER REFERENCES ttl_series(ttl_series_id) NOT NULL
        );''')

    cursor.execute('''
        CREATE TABLE toys_to_life
        (
            ttl_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            ttl_name VARCHAR NOT NULL,
            ttl_edition VARCHAR,
            ttl_type INTEGER REFERENCES ttl_types(ttl_type_id) NOT NULL,
            legal BOOLEAN NOT NULL DEFAULT(1),
            error BOOLEAN NOT NULL DEFAULT(0),
            date_acquired DATE,
            got_state INTEGER REFERENCES states(state_id) NOT NULL,
            current_state INTEGER REFERENCES states(state_id) NOT NULL,
            cost DECIMAL NOT NULL DEFAULT(0),
            value DECIMAL NOT NULL DEFAULT(0),
            bundle INTEGER REFERENCES bundles(bundle_id)
        );''')

    cursor.execute('''
        CREATE TABLE ttl_software_types
        (
            ttl_software_type_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            ttl_series INTEGER REFERENCES ttl_series(ttl_series_id) NOT NULL,
            ttl_software_type_name VARCHAR NOT NULL,
            description VARCHAR
        );''')

    cursor.execute('''
        CREATE TABLE ttl_compatabilities
        (
            ttl_compatability_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            ttl INTEGER REFERENCES toys_to_life(ttl_id) NOT NULL,
            ttl_software_type INTEGER REFERENCES ttl_software_types(ttl_software_type_id) NOT NULL
        );''')

    cursor.execute('''
        CREATE TABLE ttl_software_compatabilities
        (
            ttl_software_compatability_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            software INTEGER REFERENCES softwares(software_id),
            ttl_software_type INTEGER REFERENCES ttl_software_tyeps(ttl_software_type_id) NOT NULL
        );''')

    command = 'INSERT INTO states (state_name, description) VALUES (?,?);'
    for pair in [("0", "Broken in some form or fashion"), ("S", "Sealed"), ("FS", "Factory Sealed"),
                 ("U1", "Un-appraised 1/10: Bad condition"), ("U2", "Un-appraised: 2/10"),
                 ("U3", "Un-appraised 3/10"), ("U4", "Un-appraised 4/10"),
                 ("U5", "Un-appraised 5/10"), ("U6", "Un-appraised 6/10"),
                 ("U7", "Un-appraised 7/10"), ("U8", "Un-appraised 8/10"),
                 ("U9", "Un-appraised 9/10: Near mint condition"),
                 ("U10", "Un-appraised 10/10: Basically mint condition"), ("M", "Missing")]:
        cursor.execute(command, (pair[0], pair[1],))

    connection.commit()
    connection.close()

def selectFromDBOrInsert(cursor, select, selectParams, insert, insertParams):
    cursor.execute(select, selectParams)
    result = cursor.fetchall()
    if (len(result) == 1):
        return result[0][0]
    elif (len(result) < 1):
        cursor.execute(insert, insertParams)
        return selectFromDBOrInsert(cursor, select, selectParams, insert, insertParams)

def checkDBForConsole(cursor, console):
    return selectFromDBOrInsert(cursor, 'SELECT console_id FROM consoles WHERE console_name = ?;',
                                (console,), 'INSERT INTO consoles (console_name) VALUES (?);',
                                (console,))

def checkDBForPlatform(cursor, platform, console):
    consoleId = checkDBForConsole(cursor, console)
    return selectFromDBOrInsert(cursor, 'SELECT platform_id FROM platforms WHERE platform_name ' +
                                '= ? AND console = ?;', (platform, consoleId,),
                                'INSERT INTO platforms (platform_name, console) VALUES (?,?);',
                                (platform, consoleId,))

def checkDBForHardwareType(cursor, hardware):
    return selectFromDBOrInsert(cursor, 'SELECT hardware_type_id FROM hardware_types WHERE ' +
                                'type_name = ?;', (hardware,),
                                'INSERT INTO hardware_types (type_name) VALUES (?);', (hardware,))

def checkDBForTTLSeries(cursor, ttlSeries):
    return selectFromDBOrInsert(cursor, 'SELECT ttl_series_id FROM ttl_series WHERE ' +
                                'ttl_series_name = ?;', (ttlSeries,),
                                'INSERT INTO ttl_series (ttl_series_name) VALUES (?);',
                                (ttlSeries,))

def checkDBForTTLType(cursor, ttlType, ttlSeries):
    ttlSeriesId = checkDBForTTLSeries(cursor, ttlSeries)
    return selectFromDBOrInsert(cursor, 'SELECT ttl_type_id FROM ttl_types WHERE type_name = ' +
                                '? AND ttl_series = ?;', (ttlType, ttlSeriesId,),
                                'INSERT INTO ttl_types (type_name, ttl_series) VALUES (?,?);',
                                (ttlType, ttlSeriesId,))

def checkDBForState(cursor, state):
    params = ()
    if (state == ''):
        params = ('U1',)
    elif (state == '11'):
        params = ('FS',)
    elif (state == '-1'):
        params = ('M',)
    elif (state != '-1' and state != '0' and state != '11'):
        params = ('U' + state,)
    else:
        params = (state,)
    cursor.execute('SELECT state_id FROM states WHERE state_name = ?;', params)
    result = cursor.fetchall()
    if (len(result) == 1):
        return result[0][0]

def addSoftwareToDB(cursor, row):
    def addSoftwarePhysical():
        if (row[21] != '' and row[21] != '-1'):
            cursor.execute('SELECT software_id FROM softwares WHERE software_name  = ? ' +
                           'AND software_edition = ? AND platform = ?;',
                           (row[0], row[1], platformId,))
            softwareId = cursor.fetchall()[0][0]
            cursor.execute('INSERT INTO software_physical (software, got_state, ' +
                           'current_state) VALUES (?,?,?);',
                           (softwareId, checkDBForState(cursor, row[20]),
                            checkDBForState(cursor, row[21]),))

    def addSoftwareDigital():
        if (row[2] != '' or row[7] != '' or row[8] != ''):
            platId = None
            size = None
            location = None
            if (row[2] != ''):
                platId = row[2]
            if (row[7] != ''):
                size = row[7]
            if (row[8] != ''):
                location = row[8]
            cursor.execute('INSERT INTO software_digital (software, file_size_bytes, ' +
                           'directory, platform_software_identifier) VALUES (?,?,?,?);',
                           (softwareId, size, location, platId,))

    def addSoftwareAchievements():
        if (row[4] != ''):
            cursor.execute('INSERT INTO software_achievements (software, earned, total) ' +
                           'VALUES (?,?,?);', (softwareId, row[3], row[4],))

    def addSoftwareTime():
        if ((row[5] != '' and row[5] != '0') or row[6] != ''):
            spent = None
            comp = None
            if (row[6] != ''):
                comp = row[6]
                spent = 0
            if (row[5] != '' and row[5] != '0'):
                spent = row[5]
            cursor.execute('INSERT INTO software_time (software, spent_mins, ' +
                           'completionist_mins) VALUES (?,?,?);', (softwareId, spent, comp,))

    platformId = checkDBForPlatform(cursor, row[-2], row[-1])
    if ((row[15] != '' and row[15] != '-1')  or (row[18] != '' and row[18] != '-1')):
        bundleName = row[0] + ' - ' + row[1] + ' - ' + row[-1] + ' - ' + row[-2]
        cursor.execute('INSERT INTO bundles (bundle_name) VALUES (?);', (bundleName,))
        cursor.execute('SELECT bundle_id FROM bundles WHERE bundle_name = ?;', (bundleName,))
        bundleId = cursor.fetchall()[0][0]
        if (bundleId > 0):
            cursor.execute('INSERT INTO softwares (software_name, software_edition, value, ' +
                           'cost, legal, error, shame, date_acquired, bundle, platform) ' +
                           'VALUES (?,?,?,?,?,?,?,?,?,?);',
                           (row[0], row[1], row[9], row[10], row[11], row[12], row[13],
                            row[len(row)-3], bundleId, platformId,))
            if (row[15] != '' and row[15] != '-1'):
                cursor.execute('INSERT INTO boxes (box_name, got_state, current_state, ' +
                               'bundle, date_acquired) VALUES (?,?,?,?,?);',
                               (row[0] + ' - ' + row[-1], checkDBForState(cursor, row[14]),
                                checkDBForState(cursor, row[15]), bundleId,
                                row[len(row)-3],))
            elif (row[15] != '11'):
                if (row[18] != '' and row[18] != '-1'):
                    cursor.execute('INSERT INTO paper_materials (material_name, ' +
                                   'got_state, current_state, bundle, date_acquired) ' +
                                   'VALUES (?,?,?,?,?);',
                                   (row[0] + ' - ' + row[-1], checkDBForState(cursor, row[17]),
                                    checkDBForState(cursor, row[18]), bundleId,
                                    row[len(row)-3],))
                addSoftwarePhysical()
                
    else:
        cursor.execute('INSERT INTO softwares (software_name, software_edition, value, ' +
                        'cost, legal, error, shame, date_acquired, platform) ' +
                        'VALUES (?,?,?,?,?,?,?,?,?);',
                        (row["game_name"], row["game_edition"], row["value"], row["cost"],
                         row["legal"], row["error"], row["_shame"],
                        row["date_acquired"], platformId,))
        addSoftwarePhysical()

    cursor.execute('SELECT software_id FROM softwares WHERE software_name  = ? AND ' +
                   'software_edition = ? AND platform = ?;', (row[0], row[1], platformId,))
    softwareId = cursor.fetchall()[0][0]
    addSoftwareDigital()
    addSoftwareAchievements()
    addSoftwareTime()

def addHardwareToDB(cursor, row):
    consoleId = checkDBForConsole(cursor, row[len(row)-1])
    hardwareTypeId = checkDBForHardwareType(cursor, row[2])
    if ((row[6] != '' and row[6] != '-1') or (row[9] != '' and row[9] != '-1')):
        bundleName = row[0] + ' - ' + row[1]
        cursor.execute('INSERT INTO bundles (bundle_name) VALUES (?);', (bundleName,))
        cursor.execute('SELECT bundle_id FROM bundles WHERE bundle_name = ?;', (bundleName,))
        bundleId = cursor.fetchall()[0][0]
        if (bundleId > 0):
            got = checkDBForState(cursor, row[11])
            current = checkDBForState(cursor, row[12])
            if (row[6] == '11'):
                got = checkDBForState(cursor, '10')
                current = checkDBForState(cursor, '10')
            else:
                if (row[6] != '' and row[6] != '-1'):
                    cursor.execute('INSERT INTO boxes (box_name, got_state, ' +
                                   'current_state, bundle, date_acquired) VALUES ' +
                                   '(?,?,?,?,?);',
                                   (row[0], checkDBForState(cursor, row[5]),
                                    checkDBForState(cursor, row[6]), bundleId,
                                    row[len(row)-3],))
                if (row[9] != '' and row[9] != '-1'):
                    cursor.execute('INSERT INTO paper_materials (material_name, ' +
                                   'got_state, current_state, bundle, date_acquired) ' +
                                   'VALUES (?,?,?,?,?);',
                                   (row[0], checkDBForState(cursor, row[8]),
                                    checkDBForState(cursor, row[9]), bundleId,
                                    row[len(row)-3]))
            cursor.execute('INSERT INTO hardwares (hardware_name, serial_number, ' +
                           'date_acquired, error, console, got_state, current_state, ' +
                           'cost, value, hardware_type, bundle) VALUES (?,?,?,?,?,?,?,?,' +
                           '?,?,?);',
                           (row[0], row[1], row[len(row)-3], row[len(row)-2], consoleId,
                            got, current, row[4], row[3], hardwareTypeId, bundleId,))
    else:
        cursor.execute('INSERT INTO hardwares (hardware_name, serial_number, ' +
                       'date_acquired, error, console, got_state, current_state, cost, ' +
                       'value, hardware_type) VALUES (?,?,?,?,?,?,?,?,?,?);',
                       (row[0], row[1], row[len(row)-3], row[len(row)-2], consoleId,
                        checkDBForState(cursor, row[11]), checkDBForState(cursor, row[12]),
                        row[4], row[3], hardwareTypeId,))

def addTTLToDB(cursor, row):
    ttlTypeId = checkDBForTTLType(cursor, row[1], row[15])
    if ((row[5] != '' and row[5] != '-1') or (row[8] != '' and row[8] != '-1')):
        bundleName = row[0] + ' - ' + row[1] + ' - ' + row[15]
        cursor.execute('INSERT INTO bundles (bundle_name) VALUES (?);', (bundleName,))
        cursor.execute('SELECT bundle_id FROM bundles WHERE bundle_name = ?;', (bundleName,))
        bundleId = cursor.fetchall()[0][0]
        if (bundleId > 0):
            got = checkDBForState(cursor, row[10])
            current = checkDBForState(cursor, row[11])
            if (row[5] == '11'):
                got = checkDBForState(cursor, '10')
                current = checkDBForState(cursor, '10')
            else:
                if (row[5] != '' and row[5] != '-1'):
                    cursor.execute('INSERT INTO boxes (box_name, got_state, ' +
                                   'current_state, bundle, date_acquired) VALUES ' +
                                   '(?,?,?,?,?);',
                                   (bundleName, checkDBForState(cursor, row[4]),
                                    checkDBForState(cursor, row[5]), bundleId,
                                    row[len(row)-3],))
                if (row[8] != '' and row[8] != '-1'):
                    cursor.execute('INSERT INTO paper_materials (material_name, ' +
                                   'got_state, current_state, bundle, date_acquired) ' +
                                   'VALUES (?,?,?,?,?);',
                                   (row[1] + ' ' + row[15] + ' ' + row[16],
                                    checkDBForState(cursor, row[7]),
                                    checkDBForState(cursor, row[8]), bundleId,
                                    row[len(row)-3]))
            cursor.execute('INSERT INTO toys_to_life (ttl_name, ttl_edition, ttl_type, legal, ' +
                       'error, date_acquired, got_state, current_state, cost, value, ' +
                       'bundle) VALUES (?,?,?,?,?,?,?,?,?,?,?);',
                       (row[0], '', ttlTypeId, '1', row[14], row[13], got, current, row[3],
                        row[2], bundleId,))
    else:
        cursor.execute('INSERT INTO toys_to_life (ttl_name, ttl_edition, ttl_type, legal, ' +
                       'error, date_acquired, got_state, current_state, cost, value) ' +
                       'VALUES (?,?,?,?,?,?,?,?,?,?);',
                       (row[0], '', ttlTypeId, '1', row[14], row[13],
                        checkDBForState(cursor, row[10]), checkDBForState(cursor, row[11]),
                        row[3], row[2],))

def importFromXLSX(cursor, xl_name):
    xl_file = pd.read_excel(xl_name, header=0, index_col=None, keep_default_na=False)
    df = pd.DataFrame({'' : []})
    
    if (xl_name == "Games.xlsx"):
        xl_file[xl_file["game_name"].str.strip().astype(bool)]
        df = xl_file.astype({"game_name":str, "game_edition":str, "steam_id":str,
                             "achieve_earned":str, "achieve_total":str, "playtime":str,
                             "completion":str, "file_size":str, "file_name":str, "value":str,
                             "cost":str, "legal":bool, "error":bool, "_shame":bool,
                             "box_got_state":str, "box_current_state":str, "box_modified":bool,
                             "materials_got_state":str, "materials_current_state":str,
                             "materials_modified":bool, "media_got_state":str,
                             "media_current_state":str, "media_modified":bool,
                             "date_acquired":str, "platform":str, "console":str})
    elif(xl_name == "Hardware.xlsx"):
        xl_file[xl_file["hardware_name"].str.strip().astype(bool)]
        df = xl_file.astype({"hardware_name":str, "serial":str, "hardware_type":str, "value":str, "cost":str,
                             "box_got_state":str, "box_current_state":str, "box_modified":bool,
                             "materials_got_state":str, "materials_current_state":str, "materials_modified":bool,
                             "hardware_got_state":str, "hardware_current_state":str, "hardware_modified":bool,
                             "date_aquired":str, "error":bool, "console":str})
    elif(xl_name == "ToysToLife.xlsx"):
        xl_file[xl_file["toy_name"].str.strip().astype(bool)]
        df = xl_file.astype({"toy_name":str, "item_type":str, "value":str, "cost":str, "box_got_state":str,
                             "box_current_state":str, "box_modified":bool, "materials_got_state":str,
                             "materials_current_state":str, "materials_modified":bool, "toy_got_state":str,
                             "toy_current_state":str, "toy_modified":bool, "date_aquired":str, "error":bool,
                             "series":str, "game":str})
        
    if (not df.empty):
        for index,row in df.iterrows():
            if (xl_name == "Games.xlsx"):
                addSoftwareToDB(cursor, row)
            elif(xl_name == "Hardware.xlsx"):
                addHardwareToDB(cursor, row)
            elif(xl_name == "ToysToLife.xlsx"):
                addTTLToDB(cursor, row)

if __name__ == '__main__':
    old = "base.db"
    new = "data.db"
    if not os.path.exists(new):
        if not os.path.exists(old):
            dbSetup(old)
        os.system('copy ' + old + ' ' + new)

    connection = sqlite3.connect(new)
    cursor = connection.cursor()
	
    importFromXLSX(cursor, "Games.xlsx")
    importFromXLSX(cursor, "Hardware.xlsx")
    importFromXLSX(cursor, "ToysToLife.xlsx")
    
    connection.commit()
    connection.close()
