from tools.condb import db



dbaas = db('192.168.122.101', 'test', 4007, 'dbaas', '123456')
print(dbaas.ReadFromPgsql('select 1;'))