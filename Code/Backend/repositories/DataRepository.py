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
    def read_all_devices():
        sql = "SELECT * FROM tblmeasurement"
        return Database.get_rows(sql)

    @staticmethod
    def read_all_sensors():
        sql = "SELECT * FROM tblmeasurement M JOIN tbldevice D ON M.DeviceId = D.DeviceId WHERE D.Type = 'Sensor'"
        return Database.get_rows(sql)

    @staticmethod
    def read_temperature():
        sql = "SELECT * FROM tblmeasurement WHERE ActionId = 'TEMP'"
        return Database.get_rows(sql)

    @staticmethod
    def read_humidity():
        sql = "SELECT * FROM tblmeasurement WHERE ActionId = 'HUM'"
        return Database.get_rows(sql)

    @staticmethod
    def read_moisture():
        sql = "SELECT * FROM tblmeasurement WHERE ActionId = 'MOIST'"
        return Database.get_rows(sql)

    @staticmethod
    def read_light():
        sql = "SELECT * FROM tblmeasurement WHERE ActionId = 'LIGHT'"
        return Database.get_rows(sql)

    @staticmethod
    def read_solenoid():
        sql = "SELECT * FROM tblmeasurement WHERE ActionId LIKE 'SOL%'"
        return Database.get_rows(sql)

    @staticmethod
    def read_latest_temperature():
        sql = "SELECT * FROM tblmeasurement WHERE ActionId = 'TEMP' ORDER BY DateTime DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def insert_measurement(actionId, deviceId, status, warning):
        sql = "INSERT INTO tblmeasurement (ActionId,DeviceId,Status,Warning) VALUES (%s,%s,%s,%s)"
        params = [actionId, deviceId, status, warning]
        return Database.execute_sql(sql, params)