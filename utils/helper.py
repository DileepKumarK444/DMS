# from xhtml2pdf import pisa
from userpermissions.models import UserRoleModel
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import random
import array
from masters.models import Customer, DroneConfiguraion, DroneAllocation, CustomerUser
from re import sub
from rest_framework.authtoken.models import Token


def get_all_user_permissions(user_id):
    data = UserRoleModel.objects.raw(
        '''select distinct dms_permission.code,1 as id from dms_user_roles join dms_role_group on 
        dms_user_roles.role_id=dms_role_group.role_id join dms_group_permission on 
        dms_role_group.group_id=dms_group_permission.group_id join dms_permission on 
        dms_group_permission.permission_id=dms_permission.id where dms_user_roles.user_id=%s''', [user_id])
    permissions = []
    for dt in data:
        permissions.append(dt.code)
    return permissions

def generate_password():
     
    MAX_LEN = 12
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS = ['@', '#', '$', '*']
    
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    
    password = ""
    for x in temp_pass_list:
            password = password + x
            
    return password
# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

def get_customer_by_token(token='',msg=''):
    print(msg)
    if(token):
        try:
            token_exists = DroneConfiguraion.objects.filter(token=token).values()
            cust = DroneAllocation.objects.filter(
                drone_id=token_exists[0]['drone_id']
                ).values()
            cust = Customer.objects.filter(id=cust[0]['customer_id']).values()
            return cust[0]['account_name']+' - '+msg
        except:
            return 'Unknown Customer - '+msg
    else:
        return 'Unknown Customer - '+msg

def get_customer_details(id,msg):
    if(id):
        try:
            cust = Customer.objects.filter(id=id).values()
            return cust[0]['account_name']+' - '+msg
        except:
            return 'Unknown Customer - '+msg
    else:
        return 'Unknown Customer - '+msg
def get_customer_id(request):
    token = sub('Token ', '', request.META.get(
                    'HTTP_AUTHORIZATION', None))
    token_obj = Token.objects.get(key=token)
    user = token_obj.user
    cust = CustomerUser.objects.filter(user=user).values()
    return cust[0]['customer_id']

    