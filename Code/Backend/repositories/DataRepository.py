from .Database import Database

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens


    @staticmethod
    def read_all_measurements():
        sql = "SELECT DateTime, ActionId, Status, Warning FROM tblmeasurement"
        return Database.get_rows(sql)

    @staticmethod
    def read_all_sensordata():
        sql = "SELECT M.DateTime, M.ActionId, M.Status, M.Warning FROM tblmeasurement M JOIN tbldevice D ON M.DeviceId = D.DeviceId WHERE D.Type = 'Sensor'"
        return Database.get_rows(sql)


    @staticmethod
    def read_temperature():
        sql = "SELECT DateTime, Status, Warning FROM tblmeasurement WHERE ActionId = 'TEMP' ORDER BY DateTime DESC"
        return Database.get_rows(sql)

    @staticmethod
    def read_humidity():
        sql = "SELECT DateTime, Status, Warning FROM tblmeasurement WHERE ActionId = 'HUM' ORDER BY DateTime DESC"
        return Database.get_rows(sql)

    @staticmethod
    def read_moisture():
        sql = "SELECT DateTime, Status, Warning FROM tblmeasurement WHERE ActionId = 'MOIST' ORDER BY DateTime DESC"
        return Database.get_rows(sql)

    @staticmethod
    def read_light():
        sql = "SELECT * FROM tblmeasurement WHERE ActionId = 'LIGHT' ORDER BY DateTime DESC"
        return Database.get_rows(sql)

    @staticmethod
    def read_solenoid():
        sql = "SELECT * FROM tblmeasurement WHERE ActionId LIKE 'SOL%' ORDER BY DateTime DESC"
        return Database.get_rows(sql)


    @staticmethod
    def read_latest_30_temperature():
        sql = "SELECT M.Status, W.Message AS Warning FROM tblmeasurement M LEFT JOIN tblwarning W ON M.Warning = W.WarningId WHERE M.ActionId = 'TEMP' ORDER BY M.DateTime DESC LIMIT 30"
        return Database.get_one_row(sql)

    @staticmethod
    def read_latest_30_humidity():
        sql = "SELECT Status FROM tblmeasurement WHERE ActionId = 'HUM' ORDER BY DateTime DESC LIMIT 30"
        return Database.get_one_row(sql)

    @staticmethod
    def read_latest_30_moisture():
        sql = "SELECT M.Status, W.Message AS Warning FROM tblmeasurement M LEFT JOIN tblwarning W ON M.Warning = W.WarningId WHERE M.ActionId = 'MOIST' ORDER BY M.DateTime DESC LIMIT 30"
        return Database.get_one_row(sql)

    @staticmethod
    def read_latest_30_light():
        sql = "SELECT Status FROM tblmeasurement WHERE ActionId = 'LIGHT' ORDER BY DateTime DESC LIMIT 30"
        return Database.get_one_row(sql)

    @staticmethod
    def read_latest_30_solenoid():
        sql = "SELECT DateTime, Warning FROM tblmeasurement WHERE ActionId LIKE 'SOL%' ORDER BY DateTime DESC LIMIT 30"
        return Database.get_one_row(sql)


    @staticmethod
    def read_latest_temperature():
        sql = "SELECT M.Status, W.Message AS Warning FROM tblmeasurement M LEFT JOIN tblwarning W ON M.Warning = W.WarningId WHERE M.ActionId = 'TEMP' ORDER BY M.DateTime DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def read_latest_humidity():
        sql = "SELECT Status FROM tblmeasurement WHERE ActionId = 'HUM' ORDER BY DateTime DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def read_latest_moisture():
        sql = "SELECT M.Status, W.Message AS Warning FROM tblmeasurement M LEFT JOIN tblwarning W ON M.Warning = W.WarningId WHERE M.ActionId = 'MOIST' ORDER BY M.DateTime DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def read_latest_light():
        sql = "SELECT Status FROM tblmeasurement WHERE ActionId = 'LIGHT' ORDER BY DateTime DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def read_latest_solenoid():
        sql = "SELECT DateTime, Warning FROM tblmeasurement WHERE ActionId LIKE 'SOL%' ORDER BY DateTime DESC LIMIT 1"
        return Database.get_one_row(sql)


    @staticmethod
    def insert_measurement(actionId, deviceId, status, warning):
        sql = "INSERT INTO tblmeasurement (ActionId,DeviceId,Status,Warning) VALUES (%s,%s,%s,%s)"
        params = [actionId, deviceId, status, warning]
        return Database.execute_sql(sql, params)