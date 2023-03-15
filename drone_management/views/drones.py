from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from userpermissions.decorators import permission_decorator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
import json
from django.core import serializers
from masters.models import DmsSetting, Company, Country, Designation, State, Product,Category, ProductType, TransactionLog, DroneAllocation, LogTemplate,DroneConfiguraion
from drone_management.models import DroneType, BatteryMaster, RCMaster, SensorMaster, CameraMaster,Drone,DroneComponent, DroneStatus, DronePurpose
import datetime
from drone_management.form import SaveDroneFrom, SaveDroneUpdateFrom, SaveConfigFrom
from django.contrib.auth.models import User
from utils import helper
import os,sys
from ast import literal_eval
from django.db.models import F
from django.conf import settings
from dms.Key_generation import random_key,pgpy_key
import secrets
import paramiko
from utils.encryption import aes
encry = aes(settings.KEY, settings.IV)
# include('drone_management.Key_generator')
# from random_key pgpy_key import Key_generator
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT
ROOT_DIR = os.path.abspath(os.curdir)

class getSchema(LoginRequiredMixin, View):
    def get(self, request):
        schema = serializers.serialize('json', DmsSetting.objects.filter(conf_key='additional_features'))
        return JsonResponse({'success': True, 'schema': schema}, status=200)

class onLoad(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST['id']
        drone_comp = list(DroneComponent.objects.filter(drone=id).values())
        drones = list(Drone.objects.filter(id=id).values())
        # schema = serializers.serialize('json', DmsSetting.objects.filter(conf_key='additional_features'))
        return JsonResponse({'success': True, 'drones': drones,'drone_comp':drone_comp}, status=200)
        
class GetConfig(LoginRequiredMixin, View):
    def get(self, request,cid):
        # print('cid',cid)
        # a = random_key(32)
        # print(a.key)

        # a = pgpy_key('')
        # print((a.prikey), (a.pubkey))
        try:
            drone_config = DroneConfiguraion.objects.get(drone=cid)
        except:
            drone_config = ''
        templates = LogTemplate.objects.all()
        # schema = serializers.serialize('json', DmsSetting.objects.filter(conf_key='additional_features'))
        return render(request, 'drones/config.html',{'templates':templates,'id':cid,'drone_config':drone_config})
class ActivateDrone(LoginRequiredMixin, View):
    def post(self, request):
        cid = request.POST['id']
        drone = Drone.objects.get(id=cid)
        drone.status = True
        drone.active =True
        drone.drone_status = None
        drone.save()
        return JsonResponse({'success': True, 'msg': 'Successfully Activated'}, status=200)
class TestConnection(LoginRequiredMixin, View):
    def post(self, request):
        try:
            host = request.POST['txt_host']
            port = request.POST['txt_port']
            username = request.POST['txt_username']
            password = request.POST['txt_password']
            folder_path = request.POST['txt_folder_path']
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.connect('odroid.actionfi.com', port='8888', username='u0_a63', password='odroid')
            ssh.connect(host, port=port, username=username, password=password)
            return JsonResponse({'success': True, 'msg': 'Test Connection Succeeded'}, status=200)
        except Exception as error_message:
            return JsonResponse({'success': False, 'msg': json.dumps(str(error_message))}, status=200)
class SaveConfig(LoginRequiredMixin, View):
    def post(self, request):
        try:
            
            form = SaveConfigFrom(request.POST)
            if form.is_valid():
                # a = random_key(32)
                # print(a.key)
                id = request.POST['hd_id']
                mac_id = request.POST['txt_mac_id']
                fc_id = request.POST['txt_fc_id']
                host = request.POST['txt_host']
                port = request.POST['txt_port']
                username = request.POST['txt_username']
                password = request.POST['txt_password']
                folder_path = request.POST['txt_folder_path']
                token =  secrets.token_hex(32)  
                a = pgpy_key('')
                
                encryptToken = str(token)
                encryptPublicKey = str(a.prikey)
                encryptPrivateKey = str(a.pubkey)

                # encryptToken = encry.encrypt(str(token))
                # encryptPublicKey = encry.encrypt(str(a.prikey))
                # encryptPrivateKey = encry.encrypt(str(a.pubkey))

                # with open('PrivateKey', 'w') as f:
                #     f.write(encryptPrivateKey)

                with open('attachments/token/Token', 'w') as f:
                    f.write(encryptToken)

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                dd = ssh.connect(host, port=port, username=username, password=password)
                sftp = ssh.open_sftp()
                
                # sftp.put('PrivateKey',folder_path+'PrivateKey')
                print(folder_path)
                sftp.put('attachments/token/Token',folder_path+'Unverified_Token.token')
                sftp.close()
                drone = Drone.objects.get(id=id)
                log_temp = LogTemplate.objects.get(id=request.POST['sb_template'])

                DroneConfiguraion.objects.update_or_create(
                    drone=id,
                    defaults={ 
                        'drone' :drone,
                        'template' : log_temp,
                        'mac_id' : mac_id,
                        'fc_id' : fc_id,
                        'host' : host,
                        'port' : port,
                        'username' : username,
                        'password' : password,
                        'path' : folder_path,
                        'public_key' : str(a.prikey),
                        'private_key' : str(a.pubkey),
                        'token' : token,
                        'created_by' : request.user
                    }
                )

                # drone_config = DroneConfiguraion.objects.get(drone=id)
                # print('drone_config',drone_config)
                # if drone_config:
                #     print('Update')
                    
                #     drone_config.drone = drone
                #     drone_config.template = log_temp
                #     drone_config.mac_id = mac_id
                #     drone_config.fc_id = fc_id
                #     drone_config.host = host
                #     drone_config.port = port
                #     drone_config.username = username
                #     drone_config.password = password
                #     drone_config.path = folder_path
                #     drone_config.public_key = encryptPublicKey
                #     drone_config.private_key = encryptPrivateKey
                #     drone_config.token = encryptToken
                #     drone_config.created_by = request.user
                #     drone_config.save()
                    
                # else:
                #     drone_config = DroneConfiguraion(
                #         drone = drone,
                #         template = log_temp,
                #         mac_id = mac_id,
                #         fc_id = fc_id,
                #         host = host,
                #         port = port,
                #         username = username,
                #         password = password,
                #         path = folder_path,
                #         public_key = encryptPublicKey,
                #         private_key = encryptPrivateKey,
                #         token = encryptToken,
                #         created_by = request.user
                #         )
                #     drone_config.save()

                # decryptPublicKey = encry.decrypt(encryptPublicKey)
                # decryptPrivateKey = encry.decrypt(encryptPrivateKey)

                # print('Public Key',decryptPublicKey)
                # print('Private Key',decryptPrivateKey)

                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as e:
            print('ERROR :'+str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)
        

class DroneList(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='drone-list'))
    def get(self, request):
        query_url = ''
        drones = Drone.objects.filter().order_by('-id')
        
        try:
            query = request.GET['search']
        except Exception as e:
            query = ''
        if query:
            dronedata = Drone.objects.filter(
                Q(model__icontains=request.GET['search']) |
                Q(model_no__icontains=request.GET["search"]) |
                Q(serial_no__icontains=request.GET["search"]) |
                Q(drone_type__name__icontains=request.GET["search"])|
                Q(uin__icontains=request.GET["search"]).order_by('-id')
                # |
                # Q(remote_control__name__icontains=request.GET["search"])
                )
        else:
            dronedata = Drone.objects.filter().order_by('-id')

        page = request.GET.get('page', 1)
        paginator = Paginator(dronedata, TABLE_ROW_LIMIT)

        try:
            drones = paginator.page(page)
        except PageNotAnInteger:
            drones = paginator.page(1)
        except EmptyPage:
            drones = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        drone_status = DroneStatus.objects.filter(type='Drone')
        return render(request, 'drones/list.html', {'drone_status':drone_status,'data': dronedata, 'drones': drones, 'query': query, 'query_url':query_url})

    @method_decorator(permission_decorator(permission='drone-delete'))
    def delete(self, request):
        try:
            print('request',request)
            
            
            # prod_check = DroneAllocation.objects.filter(drone=request.GET['id']).count()
            # if prod_check:
            #     return JsonResponse({'success': 'exist', 'msg': 'Sorry can\'t delete, Drone is already allocated.'})
            # data = Category.objects.get(id=request.GET['id'])
            # data.delete()
            del_st = DroneStatus.objects.get(id=request.GET['del'])
            DroneAllocation.objects.filter(drone=request.GET['id']).delete()
            Drone.objects.filter(id=request.GET['id']).update(status=False,allocated=False,drone_status=del_st,active=False)
            return JsonResponse({'success': True, 'url': '/drone/drone-details/'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=200)
class DroneEdit(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='drone-edit'))
    def get(self, request,cid):
        drones1 = Drone.objects.filter(id=cid).values()
        if(drones1[0]['status']):
            drones = Drone.objects.get(id=cid)
            drone_comp = DroneComponent.objects.filter(drone=cid).values()
            product = Product.objects.filter(status=True)
            batteries = product.filter(Q(id__in=(literal_eval(drone_comp[0]['battery']))) | (Q(trans_type='New') & Q(category__type__type='Battery') & Q(active=True))).values('id','category__model','serial_number','category')
            # print(drone_comp[0]['Remote Control'])
            
            
            cameras = product.filter(Q(id__in=(literal_eval(drone_comp[0]['camera']))) | (Q(trans_type='New') & Q(category__type__type='Camera') & Q(active=True))).values('id','category__model','serial_number','category')
            # batteries = Product.objects.filter(category__type__type='Battery',trans_type='New',id__in=(literal_eval(drone_comp[0]['Battery']))).values('id','category__model','serial_number','category')
            remotes = product.filter(category__type__type='Remote Control',trans_type='New', active=True).values('id','category__model','serial_number','category')
            sensors = product.filter(Q(id__in=(literal_eval(drone_comp[0]['sensors']))) | (Q(trans_type='New') & Q(category__type__type='Sensor') & Q(active=True))).values('id','category__model','serial_number','category')
            # print(sensors)
            rc = product.filter(Q(id=((drone_comp[0]['rc']))) | (Q(trans_type='New') & Q(category__type__type='Remote Control') & Q(active=True))).values('id','category__model','serial_number','category')
            print(rc)
            fc = product.filter(Q(id__in=(literal_eval(drone_comp[0]['fc']))) | (Q(trans_type='New') & Q(category__type__type='Flight Controller') & Q(active=True))).values('id','category__model','serial_number','category')
            frame = product.filter(Q(id__in=(literal_eval(drone_comp[0]['frame']))) | (Q(trans_type='New') & Q(category__type__type='Frame') & Q(active=True))).values('id','category__model','serial_number','category')
            qgc = product.filter(Q(id__in=(literal_eval(drone_comp[0]['qgc']))) | (Q(trans_type='New') & Q(category__type__type='QGC') & Q(active=True))).values('id','category__model','serial_number','category')

            schema = ''

            dronePurposes = DronePurpose.objects.all()
            print("drones[0]['drone_purpose']",drones1[0])
            dronetypes = DroneType.objects.filter(purpose=drones1[0]['drone_purpose_id'])
            return render(request, 'drones/edit.html', {'dronetypes':dronetypes,'dronePurposes':dronePurposes,'id':cid,'drone_comp':drone_comp,'drones':drones,'schema':schema,'batteries': batteries, 'remotes': remotes, 'sensors':sensors,'cameras':cameras,'rcs':rc,'fcs':fc,'qgcs':qgc,'frames':frame})
        else:
            return redirect('/drone/drone-details')

class DroneAdd(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='drone-add'))
    def get(self, request):
        # dronetypes = DroneType.objects.all()
        # batteries = BatteryMaster.objects.all()
        # remotes = RCMaster.objects.all()
        # sensors = SensorMaster.objects.all()
        # cameras = CameraMaster.objects.all()
        product = Product.objects.filter(status=True)
        cameras = product.filter(category__type__type='Camera',trans_type='New',active=True).values('id','category__model','serial_number','category')
        batteries = product.filter(category__type__type='Battery',trans_type='New',active=True).values('id','category__model','serial_number','category')
        remotes = product.filter(category__type__type='Remote Control',trans_type='New',active=True).values('id','category__model','serial_number','category')
        sensors = product.filter(category__type__type='Sensor',trans_type='New',active=True).values('id','category__model','serial_number','category')

        rc = product.filter(category__type__type='Remote Control',trans_type='New',active=True).values('id','category__model','serial_number','category')
        fc = product.filter(category__type__type='Flight Controller',trans_type='New',active=True).values('id','category__model','serial_number','category')
        frame = product.filter(category__type__type='Frame',trans_type='New',active=True).values('id','category__model','serial_number','category')
        qgc = product.filter(category__type__type='QGC',trans_type='New',active=True).values('id','category__model','serial_number','category')
        dronePurposes = DronePurpose.objects.all()
        prefix = DmsSetting.objects.filter(conf_key='prefix').values('conf_value')
        prefix = prefix[0]['conf_value']
        serial_no = DmsSetting.objects.filter(conf_key='serial_no').values('conf_value')
        serial_no = serial_no[0]['conf_value']
        schema = ''
        return render(request, 'drones/add.html', {'serial_no':serial_no,'prefix':prefix,'dronePurposes':dronePurposes,'schema':schema,'batteries': batteries, 'remotes': remotes, 'sensors':sensors,'cameras':cameras,'rcs':rc,'fcs':fc,'qgcs':qgc,'frames':frame})
    @method_decorator(permission_decorator(permission='drone-save'))
    def post(self, request):
        # print(request.POST)
        # print(request.POST.getlist('camera_cat'))
        # sensors_cat = request.POST.getlist('sensors_cat')
        # for sensor in sensors_cat:
        #     # print('Sensor',sensor)
        #     Category.objects.filter(id=sensor).update(quantity=F('quantity') - 1)

        try:
            filepath = request.FILES if request.FILES else False
            form = SaveDroneFrom(request.POST,request.FILES)
            if form.is_valid():

                # drone_check = Drone.objects.filter(serial_no=request.POST['txt_serial_no']).count()
                # if drone_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry serial number already exist.'})
                # drone_check = Drone.objects.filter(uin=request.POST['txt_uin']).count()
                # if drone_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry UIN already exist.'})
                
                image = ''
                if filepath != False:
                    image = request.FILES['file']
                    mdi_file = request.FILES['mdi_file']



                model = request.POST['txt_modal']
                model_no = request.POST['txt_modal_no']
                serial_no = request.POST['txt_serial_no']
                uin = request.POST['txt_uin']
                drone_type = DroneType.objects.get(id=request.POST['sb_drone_type'])
                purpose = DronePurpose.objects.get(id=request.POST['sb_drone_purpose'])
                # remote_control = RCMaster.objects.get(id=request.POST['sb_rc'])
                video_link = request.POST['txt_video_link']
                features = request.POST['ta_features']
                
                active = request.POST['active']
                schema_data = request.POST['schema_data']

                battery = request.POST.getlist('sb_battery')
                sensor = request.POST.getlist('sb_sensor')
                camera = request.POST.getlist('sb_camera')

                rc = request.POST['sb_rc']
                fc = request.POST.getlist('sb_fc')
                qgc = request.POST.getlist('sb_qgc')
                frame = request.POST.getlist('sb_frame')

                battery_cat = request.POST.getlist('battery_cat')
                sensors_cat = request.POST.getlist('sensors_cat')
                camera_cat = request.POST.getlist('camera_cat')
                rc_cat = request.POST.getlist('rc_cat')
                fc_cat = request.POST.getlist('fc_cat')
                qgc_cat = request.POST.getlist('qgc_cat')
                frame_cat = request.POST.getlist('frame_cat')

                img_hotspot = request.POST['img_hotspot']
                print(img_hotspot)

                if active == 'true':
                    active = True
                else:
                    active = False
                drone = Drone(
                    model = model,
                    model_no = model_no,
                    serial_no = serial_no,
                    uin = uin,
                    drone_type = drone_type,
                    purpose = drone_purpose,
                    video_link = video_link,
                    features = features,
                    image = image,
                    image1 = image,
                    image2 = mdi_file,
                    status = True,
                    active =active,
                    schema = img_hotspot,
                    additional_features = schema_data,
                    created_by = request.user
                )
                drone.save()
                drone_comp = DroneComponent(
                    drone=drone,
                    battery = json.dumps(battery),
                    sensors = json.dumps(sensor),
                    camera = json.dumps(camera),
                    rc = rc,
                    fc = json.dumps(fc),
                    qgc = json.dumps(qgc),
                    frame = json.dumps(frame),
                    created_by = request.user,
                )
                drone_comp.save()
                # Update Product 

                for b in battery:
                    Product.objects.filter(id=b).update(trans_type='Allocated')
                    br = Product.objects.filter(id=b).values()
                    Category.objects.filter(id=br[0]['category_id']).update(quantity=F('quantity') - 1)

                for s in sensor:
                    Product.objects.filter(id=s).update(trans_type='Allocated')
                    sr = Product.objects.filter(id=s).values()
                    Category.objects.filter(id=sr[0]['category_id']).update(quantity=F('quantity') - 1)
                
                for c in camera:
                    Product.objects.filter(id=c).update(trans_type='Allocated')
                    cr = Product.objects.filter(id=c).values()
                    Category.objects.filter(id=cr[0]['category_id']).update(quantity=F('quantity') - 1)

                Product.objects.filter(id=rc).update(trans_type='Allocated')
                rcr = Product.objects.filter(id=rc).values()
                Category.objects.filter(id=rcr[0]['category_id']).update(quantity=F('quantity') - 1)

                for f in fc:
                    Product.objects.filter(id=f).update(trans_type='Allocated')
                    fr = Product.objects.filter(id=f).values()
                    Category.objects.filter(id=fr[0]['category_id']).update(quantity=F('quantity') - 1)

                for q in qgc:
                    Product.objects.filter(id=q).update(trans_type='Allocated')
                    qr = Product.objects.filter(id=q).values()
                    Category.objects.filter(id=qr[0]['category_id']).update(quantity=F('quantity') - 1)

                for fr in frame:
                    Product.objects.filter(id=fr).update(trans_type='Allocated')
                    frr = Product.objects.filter(id=fr).values()
                    Category.objects.filter(id=frr[0]['category_id']).update(quantity=F('quantity') - 1)
                    
                serial_no = DmsSetting.objects.filter(conf_key='serial_no').values('conf_value')
                DmsSetting.objects.filter(conf_key='serial_no').update(conf_value=int(serial_no[0]['conf_value']) + 1)

                

                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)


class DroneUpdate(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='drone-update'))
    def post(self, request):
        
        try:
            filepath = request.FILES if request.FILES else False
            form = SaveDroneUpdateFrom(request.POST,request.FILES)
            if form.is_valid():
                

                # drone_check = Drone.objects.filter(serial_no=request.POST['txt_serial_no']).exclude(id=request.POST['id']).count()
                # if drone_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry serial number already exist.'})
                # drone_check = Drone.objects.filter(uin=request.POST['txt_uin']).exclude(id=request.POST['id']).count()
                # if drone_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry UIN already exist.'})

                image = ''
                mdi_file = ''
                if filepath != False:
                    image = request.FILES['file']
                    mdi_file = request.FILES['mdi_file']

                
                id = request.POST['id']
                model = request.POST['txt_modal']
                model_no = request.POST['txt_modal_no']
                serial_no = request.POST['txt_serial_no']
                uin = request.POST['txt_uin']
                drone_type = DroneType.objects.get(id=request.POST['sb_drone_type'])
                purpose = DronePurpose.objects.get(id=request.POST['sb_drone_purpose'])
                print('purpose',drone_type)
                video_link = request.POST['txt_video_link']
                features = request.POST['ta_features']
                
                active = request.POST['active']
                schema_data = request.POST['schema_data']

                battery = request.POST.getlist('sb_battery')
                sensor = request.POST.getlist('sb_sensor')
                camera = request.POST.getlist('sb_camera')

                rc = request.POST['sb_rc']
                fc = request.POST.getlist('sb_fc')
                qgc = request.POST.getlist('sb_qgc')
                frame = request.POST.getlist('sb_frame')

                # battery_cat = request.POST['battery_cat']
                # sensors_cat = request.POST['sensors_cat']
                # camera_cat = request.POST['camera_cat']
                # rc_cat = request.POST['rc_cat']
                # fc_cat = request.POST['fc_cat']
                # qgc_cat = request.POST['qgc_cat']
                # frame_cat = request.POST['frame_cat']

                img_hotspot = request.POST['img_hotspot']
                # print('battery_cat',camera_cat)
                
                if active == 'true':
                    active = True
                else:
                    active = False


                drone_comp = DroneComponent.objects.filter(drone=id).values()
                battery_r = drone_comp[0]['battery']
                sensors_r = drone_comp[0]['sensors']
                camera_r = drone_comp[0]['camera']
                rc_r = drone_comp[0]['rc']
                fc_r = drone_comp[0]['fc']
                qgc_r = drone_comp[0]['qgc']
                frame_r = drone_comp[0]['frame']
                
                for br in json.loads(battery_r):
                    Product.objects.filter(id=br).update(trans_type='New')
                    br_cat = Product.objects.filter(id=br).values()
                    Category.objects.filter(id=br_cat[0]['category_id']).update(quantity=F('quantity') + 1)
                    
                for sr in json.loads(sensors_r):
                    Product.objects.filter(id=sr).update(trans_type='New')
                    sr_cat = Product.objects.filter(id=sr).values()
                    Category.objects.filter(id=sr_cat[0]['category_id']).update(quantity=F('quantity') + 1)
                
                for cr in json.loads(camera_r):
                    Product.objects.filter(id=cr).update(trans_type='New')
                    cr_cat = Product.objects.filter(id=cr).values()
                    Category.objects.filter(id=cr_cat[0]['category_id']).update(quantity=F('quantity') + 1)
                
                Product.objects.filter(id=rc_r).update(trans_type='New')
                rr_cat = Product.objects.filter(id=rc_r).values()
                Category.objects.filter(id=rr_cat[0]['category_id']).update(quantity=F('quantity') + 1)
                
                for fcr in json.loads(fc_r):
                    Product.objects.filter(id=fcr).update(trans_type='New')
                    fcr_cat = Product.objects.filter(id=fcr).values()
                    Category.objects.filter(id=fcr_cat[0]['category_id']).update(quantity=F('quantity') + 1)
                
                for qr in json.loads(qgc_r):
                    Product.objects.filter(id=qr).update(trans_type='New')
                    qr_cat = Product.objects.filter(id=qr).values()
                    Category.objects.filter(id=qr_cat[0]['category_id']).update(quantity=F('quantity') + 1)
                
                for fr in json.loads(frame_r):
                    Product.objects.filter(id=fr).update(trans_type='New')
                    fr_cat = Product.objects.filter(id=fr).values()
                    Category.objects.filter(id=fr_cat[0]['category_id']).update(quantity=F('quantity') + 1)
                
                drone = Drone.objects.get(id=id)
                
                drone.model = model
                drone.model_no = model_no
                drone.serial_no = serial_no
                drone.uin = uin
                drone.drone_type = drone_type
                drone.drone_purpose = purpose
                drone.video_link = video_link
                drone.features = features
                if(image):
                    drone.image = image
                    drone.image1 = image
                if(mdi_file):
                    drone.image2 = mdi_file
                drone.status = True
                drone.active =active
                if(active):
                    drone.drone_status = None
                drone.schema = img_hotspot
                drone.additional_features = schema_data
                drone.created_by = request.user
                drone.save()

                drone = Drone.objects.get(id=id)

                drone_comp = DroneComponent.objects.get(drone=id)
                drone_comp.drone=drone
                drone_comp.battery = json.dumps(battery)
                drone_comp.sensors = json.dumps(sensor)
                drone_comp.camera = json.dumps(camera)
                drone_comp.rc = rc
                drone_comp.fc = json.dumps(fc)
                drone_comp.qgc = json.dumps(qgc)
                drone_comp.frame = json.dumps(frame)
                drone_comp.created_by = request.user
                drone_comp.save()
                
                for b in battery:
                    
                    Product.objects.filter(id=b).update(trans_type='Allocated')
                    br = Product.objects.filter(id=b).values()
                    Category.objects.filter(id=br[0]['category_id']).update(quantity=F('quantity') - 1)
                    self.save_log(br[0]['category_id'],'Battery')
                
                for s in sensor:
                    Product.objects.filter(id=s).update(trans_type='Allocated')
                    sr = Product.objects.filter(id=s).values()
                    Category.objects.filter(id=sr[0]['category_id']).update(quantity=F('quantity') - 1)
                    self.save_log(sr[0]['category_id'],'Sensor')
                
                for c in camera:
                    print('BBBBBB',c)
                    Product.objects.filter(id=c).update(trans_type='Allocated')
                    cr = Product.objects.filter(id=c).values()
                    Category.objects.filter(id=cr[0]['category_id']).update(quantity=F('quantity') - 1)
                    self.save_log(cr[0]['category_id'],'Camera')

                Product.objects.filter(id=rc).update(trans_type='Allocated')
                rcr = Product.objects.filter(id=rc).values()
                Category.objects.filter(id=rcr[0]['category_id']).update(quantity=F('quantity') - 1)
                self.save_log(rcr[0]['category_id'],'Remote Control')
                
                for f in fc:
                    Product.objects.filter(id=f).update(trans_type='Allocated')
                    fr = Product.objects.filter(id=f).values()
                    Category.objects.filter(id=fr[0]['category_id']).update(quantity=F('quantity') - 1)
                    self.save_log(fr[0]['category_id'],'Flight Controller')

                for q in qgc:
                    Product.objects.filter(id=q).update(trans_type='Allocated')
                    qr = Product.objects.filter(id=q).values()
                    Category.objects.filter(id=qr[0]['category_id']).update(quantity=F('quantity') - 1)
                    self.save_log(qr[0]['category_id'],'QGC')

                for fr in frame:
                    Product.objects.filter(id=fr).update(trans_type='Allocated')
                    frr = Product.objects.filter(id=fr).values()
                    Category.objects.filter(id=frr[0]['category_id']).update(quantity=F('quantity') - 1)
                    self.save_log(frr[0]['category_id'],'Frame')

                

                # Update Stock
                # for battery in battery_cat:
                #     Category.objects.filter(id=battery).update(quantity=F('quantity') - 1)
                #     self.save_log(battery,'Battery')

                # for sensor in sensors_cat:
                #     Category.objects.filter(id=sensors_cat).update(quantity=F('quantity') - 1)
                #     self.save_log(sensor,'Sensor')
                    
                
                # for camera in camera_cat:
                #     Category.objects.filter(id=camera_cat).update(quantity=F('quantity') - 1)
                #     self.save_log(camera,'Camera')
                # for rc in rc_cat:
                #     Category.objects.filter(id=rc_cat).update(quantity=F('quantity') - 1)
                #     self.save_log(rc,'Remote Control')

                # for fc in fc_cat:
                #     Category.objects.filter(id=fc_cat).update(quantity=F('quantity') - 1)
                #     self.save_log(fc,'Flight Controller')

                # for qgc in qgc_cat:
                #     Category.objects.filter(id=qgc_cat).update(quantity=F('quantity') - 1)
                #     self.save_log(qgc,'QGC')

                # for frame in frame_cat:
                #     Category.objects.filter(id=frame_cat).update(quantity=F('quantity') - 1)
                #     self.save_log(frame,'Frame')

                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)
    def save_log(self,id,label):
        # print(Category.objects.filter(id=id).first().type)
        cat = Category.objects.get(id=id)
        type = ProductType.objects.get(id = str(Category.objects.filter(id=id).first().type))
        description = 'Allocated one '+label+' on '+str(datetime.datetime.today().strftime('%Y-%m-%d'))+',Category Id :'+str(id)
        
        trans_log = TransactionLog(
        category=cat,
        type = type,
        quantity = 1,
        action = 'edit',
        date = datetime.datetime.today().strftime('%Y-%m-%d'),
        description = description,
        trans_type = 'Allocated',
        
        )
        trans_log.save()
        return True

# class MasterCustomersEdit(LoginRequiredMixin, View):
#     # @method_decorator(permission_decorator(permission='role-list'))
#     def get(self, request, cid):
#         company = Company.objects.all()
#         country = Country.objects.all()
#         # state = State, 
#         designation = Designation.objects.all()
#         return render(request, 'customers/edit.html', {'company': company, 'country': country, 'designation': designation})
#     def post(self, request):
#         pass
class GetDroneType(LoginRequiredMixin, View):
    # @method_decorator(permission_decorator(permission='role-list'))
    def post(self, request):
        try:
            purpose = ''
            json_data = request.body.decode("utf-8")
            
            data = json.loads(json_data)
            print('json_data',data)
            state =''
            if data['id']:
                purpose = serializers.serialize('json', DroneType.objects.filter(purpose=data['id']))
            return JsonResponse({'success': True, 'data': purpose}, status=200)
        except Exception as e:
            print('ERROR :'+str(e))
            # msg = helper.get_customer_by_token(token,str(e))
            # logger.info(msg)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)

class getFeatures(LoginRequiredMixin, View):
    def post(self, request):
        try:
            # json_data = request.body.decode("utf-8")
            # data = json.loads(json_data)
            state =''
            if request.POST['id']:
                drone_type = list(DroneType.objects.filter(id=request.POST['id']).values())
            return JsonResponse({'success': True, 'data': drone_type}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)