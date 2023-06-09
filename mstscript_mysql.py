# import sqlite3
# print('Started')
import psycopg2
# print('psycopg2 imported')



connection = psycopg2.connect(host="localhost",
    database="dms_2022_3",
    user="postgres",
    password="root")
# print('Connection success')
cursor = connection.cursor()
# print(connection)
try:

    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Download Log', 'download-log' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='download-log'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Project Menu', 'project-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='project-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'User Menu', 'user-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='user-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Dashboard View', 'dashboard-view' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='dashboard-view'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Masters Main Menu', 'masters-main-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='masters-main-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Customer Menu', 'customer-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='customer-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Product Type Menu', 'product-type-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='product-type-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Product Menu', 'product-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='product-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Item Menu', 'item-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='item-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Main Menu', 'drone-main-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-main-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone List Menu', 'drone-list-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-list-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Category List', 'category-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='category-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Category Delete', 'category-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='category-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Category Add', 'category-add' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='category-add'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Category Update', 'category-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='category-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Product Edit', 'product-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='product-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Product Update', 'product-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='product-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Customer List', 'customer-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='customer-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Customer Edit', 'customer-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='customer-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Customer Update', 'customer-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='customer-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Customer Add', 'customer-add' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='customer-add'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Customer Save', 'customer-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='customer-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Type List', 'drone-type-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-type-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Type Add', 'drone-type-add' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-type-add'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Type Save', 'drone-type-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-type-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Type Edit', 'drone-type-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-type-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Type Update', 'drone-type-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-type-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Product Type List', 'product-type-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='product-type-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Product Type Add', 'product-type-add' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='product-type-add'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Product Type Delete', 'product-type-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='product-type-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Product Type Edit', 'product-type-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='product-type-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Product Type Update', 'product-type-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='product-type-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Item List', 'item-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='item-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Item Add', 'item-add' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='item-add'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Item Save', 'item-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='item-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Item Edit', 'item-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='item-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Item Update', 'item-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='item-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Item Delete', 'item-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='item-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone List', 'drone-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Add', 'drone-add' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-add'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Save', 'drone-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Edit', 'drone-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Update', 'drone-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Delete', 'drone-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'User List', 'user-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='user-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Add User', 'add-user' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='add-user'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Delete User', 'delete-user' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='delete-user'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Edit User', 'edit-user' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='edit-user'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Login Avm', 'login-avm' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='login-avm'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Group List', 'group-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='group-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Add Group', 'add-group' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='add-group'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Delete Group', 'delete-group' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='delete-group'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Edit Group', 'edit-group' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='edit-group'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Permission Group List', 'permission-group-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='permission-group-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Permission List', 'permission-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='permission-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Add Permission', 'add-permission' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='add-permission'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Delete Permission', 'delete-permission' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='delete-permission'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Edit Permission', 'edit-permission' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='edit-permission'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Role List', 'role-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='role-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Add Role', 'add-role' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='add-role'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Delete Role', 'delete-role' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='delete-role'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Edit Role', 'edit-role' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='edit-role'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Delete', 'drone-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-delete'); ''')

    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Edit Role', 'edit-role' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='edit-role'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Purpose List', 'purpose-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='purpose-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Purpose Delete', 'purpose-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='purpose-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Purpose Save', 'purpose-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='purpose-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Purpose Update', 'purpose-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='purpose-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Purpose Edit', 'purpose-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='purpose-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'State List', 'state-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='state-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'State Delete', 'state-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='state-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'State Save', 'state-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='state-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'State Update', 'state-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='state-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'State Edit', 'state-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='state-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Country List', 'country-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='country-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Country Delete', 'country-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='country-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Country Save', 'country-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='country-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Country Update', 'country-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='country-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Country Edit', 'country-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='country-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Log Fields Template List', 'log-fields-template-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='log-fields-template-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Log Fields Template Delete', 'log-fields-template-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='log-fields-template-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Log Fields Template Add', 'log-fields-template-add' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='log-fields-template-add'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Log Fields Template Save', 'log-fields-template-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='log-fields-template-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Log Fields Template Update', 'log-fields-template-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='log-fields-template-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Log Fields Template Edit', 'log-fields-template-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='log-fields-template-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Activate', 'drone-activate' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-activate'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Configuration', 'drone-configuration' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-configuration'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Settings List', 'settings-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='settings-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Settings Save', 'settings-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='settings-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Settings Edit', 'settings-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='settings-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Settings Update', 'settings-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='settings-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Settings Delete', 'settings-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='settings-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Item Activate', 'item-activate' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='item-activate'); ''')

    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Item Activate', 'item-activate' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='item-activate'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT '', '' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code=''); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Type Menu', 'drone-type-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-type-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Purpose Menu', 'purpose-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='purpose-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Log Fields Template Menu', 'log-fields-template-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='log-fields-template-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Settings Menu', 'settings-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='settings-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Country Menu', 'country-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='country-menu'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'State Menu', 'state-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='state-menu'); ''')

    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Reson List', 'reson-list' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='reson-list'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Reson Save', 'reson-save' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='reson-save'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Reson Edit', 'reson-edit' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='reson-edit'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Reson Update', 'reson-update' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='reson-update'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Reson Delete', 'reson-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='reson-delete'); ''')
    cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Reson Menu', 'reson-menu' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='reson-menu'); ''')

    cursor.execute('''INSERT INTO dms_group (name, description) SELECT 'Admin Group', 'Admin Group' WHERE NOT EXISTS (SELECT 1 FROM dms_group WHERE name='Admin Group'); ''')
    cursor.execute('''INSERT INTO dms_group (name, description) SELECT 'User Group', 'User Group' WHERE NOT EXISTS (SELECT 1 FROM dms_group WHERE name='User Group'); ''')
    cursor.execute('''INSERT INTO dms_group (name, description) SELECT 'Staff Group', 'Staff Group' WHERE NOT EXISTS (SELECT 1 FROM dms_group WHERE name='Staff Group'); ''')

    cursor.execute('''INSERT INTO dms_roles (name, description) SELECT 'Customer Admin', 'Customer Admin' WHERE NOT EXISTS (SELECT 1 FROM dms_roles WHERE name='Customer Admin'); ''')
    cursor.execute('''INSERT INTO dms_roles (name, description) SELECT 'Customer User', 'Customer User' WHERE NOT EXISTS (SELECT 1 FROM dms_roles WHERE name='Customer User'); ''')
    cursor.execute('''INSERT INTO dms_roles (name, description) SELECT 'Staff Role', 'Staff Role' WHERE NOT EXISTS (SELECT 1 FROM dms_roles WHERE name='Staff Role'); ''')
    cursor.execute('''INSERT INTO dms_roles (name, description) SELECT '', '' WHERE NOT EXISTS (SELECT 1 FROM dms_roles WHERE name=''); ''')

    cursor.execute('''UPDATE dms_transaction_logs	SET trans_type='New' WHERE trans_type = 'new';''')
    cursor.execute('''UPDATE dms_transaction_logs	SET trans_type='Allocated' WHERE trans_type = 'allocated';''')
    cursor.execute('''UPDATE dms_products	SET trans_type='New' WHERE trans_type = 'new';''')
    cursor.execute('''UPDATE dms_products	SET trans_type='Allocated' WHERE trans_type = 'allocated';''')

    cursor.execute('''UPDATE dms_product_types	SET type='Camera' WHERE type = 'camera';''')
    cursor.execute('''UPDATE dms_product_types	SET type='Battery' WHERE type = 'battery';''')
    cursor.execute('''UPDATE dms_product_types	SET type='Remote Control' WHERE type = 'rc';''')
    cursor.execute('''UPDATE dms_product_types	SET type='Sensor' WHERE type = 'sensor';''')
    cursor.execute('''UPDATE dms_product_types	SET type='Flight Controller' WHERE type = 'fc';''')
    cursor.execute('''UPDATE dms_product_types	SET type='QGC' WHERE type = 'qgc';''')
    cursor.execute('''UPDATE dms_product_types	SET type='Frame' WHERE type = 'frame';''')

    cursor.execute('''UPDATE dms_drone_status	SET type='Drone' WHERE type = 'drone';''')
    cursor.execute('''UPDATE dms_drone_status	SET type='Item' WHERE type = 'item';''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'checklist', '{   "rules":[      {         "id":1,         "val":"No Flying in Red zone"      },      {         "id":2,         "val":"No Flying in Adverse weather"      }   ],   "maintanence":[      {         "id":3,         "val":"Preflight Checking"      },      {         "id":4,         "val":"Location Checking"      },      {         "id":5,         "val":"Camera/Sensor Checking"      }   ],   "approval":[      {         "id":6,         "val":"Verified Maintanence"      },      {         "id":7,         "val":"Verified Location"      },      {         "id":8,         "val":"Verified Pilot"      }   ]}','checklist' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='checklist'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'additional_features', '	{"wing_span":{"type":"string","label": "Wing Span"},"flying_time":{"type":"string","label": "Flying Time"},"wheel_base":{"type":"list","label": "Wheel Base","allowed":[1,2,3,4,5,6,7,8,9,10]},"motors_used":{"type":"string","label": "No of Motors"},"max_speed":{"type":"string","label": "Max Speed"},"flight_control":{"type":"string","label": "Flight Control"},"payload_capacity":{"type":"string","label": "Payload Capacity"},"weight":{"type":"string","label": "Weight"},"flying_weight":{"type":"string","label": "Flying Weight"},"material":{"type":"string","label": "Material"}}','additional_features' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='additional_features'); ''')
    
    
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'email_verification_admin', 'True','email_verification_admin' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='email_verification_admin'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'email_verification_user', 'True','email_verification_user' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='email_verification_user'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'normal', '5','normal' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='normal'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'medium', '10','medium' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='medium'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'version', '22.1','version' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='version'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'releasedate', '10/10/2023','releasedate' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='releasedate'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'reason_module', '[ "Drone","Item"  ]','reason_module' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='reason_module'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'releasedays', '15','releasedays' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='releasedays'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'log_file_path', 'attachments/','log_file_path' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='log_file_path'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'prefix', 'IAXEAGL2207','prefix' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='prefix'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'serial_no', '10004','serial_no' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='serial_no'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'userlimit', '5','userlimit' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='userlimit'); ''')
    cursor.execute('''INSERT INTO dms_settings (conf_key,conf_value, conf_description) SELECT 'profile_schema', '{"designation":{   "type":"string",   "input_type":"text",   "label":"Designation"},"organization":{   "type":"string",   "input_type":"text",   "label":"Organization"},"department":{   "type":"string",   "input_type":"text",   "label":"Department"}}','profile_schema' WHERE NOT EXISTS (SELECT 1 FROM dms_settings WHERE conf_key='profile_schema'); ''')
    # cursor.execute('''INSERT INTO dms_permission (name, code) SELECT 'Drone Delete', 'drone-delete' WHERE NOT EXISTS (SELECT 1 FROM dms_permission WHERE code='drone-delete'); ''')

    connection.commit()
    # print('Data inserted successfully')

except Exception as e:
    print(str(e))


# Closing the connection
cursor.close()
connection.close()
# print('Connection closed')